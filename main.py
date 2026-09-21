"""Skip segmented replies for Agent responses that used tools."""

from astrbot.api import AstrBotConfig, logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star, register
from astrbot.core.message.message_event_result import ResultContentType


@register(
    "astrbot_plugin_agentShutUp",
    "CMKH1337",
    "令agent运行时的工具调用消息不被断句功能断",
    "v0.1.0",
)
class AgentShutUpPlugin(Star):
    """Keep tool-using Agent replies intact while preserving normal LLM splitting."""

    _TOOL_USED_KEY = "agent_shut_up_tool_used"

    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    @filter.on_using_llm_tool()
    async def on_using_llm_tool(
        self,
        event: AstrMessageEvent,
        tool,
        tool_args: dict | None,
    ) -> None:
        """Mark this event only after the Agent actually starts a tool call."""
        if not self.config.get("enabled", True):
            return

        event.set_extra(self._TOOL_USED_KEY, True)

    @filter.on_decorating_result()
    async def on_decorating_result(self, event: AstrMessageEvent) -> None:
        """Exclude tool-using Agent output from AstrBot's segmented reply stage."""
        if not self.config.get("enabled", True):
            return

        if not event.get_extra(self._TOOL_USED_KEY, False):
            return

        result = event.get_result()
        if result is None:
            return

        if result.result_content_type == ResultContentType.LLM_RESULT:
            result.set_result_content_type(ResultContentType.GENERAL_RESULT)
            logger.debug(
                "[agent_shut_up] skipped segmented reply for tool-using Agent result"
            )
