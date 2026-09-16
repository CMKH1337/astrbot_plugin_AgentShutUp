# AgentShutUp

本插件会阻止实际调用过工具的 Agent 最终回复被 AstrBot 的分段回复/断句功能拆分。

普通 LLM 的直接回复不会受到影响，仍会遵循 AstrBot 原有的断句配置。

## 使用前配置

本插件不负责合并 Agent 中间消息。要让插件生效请必须在 AstrBot WebUI 中完成以下配置：

- 关闭 **流式输出**：`provider_settings.streaming_response = false`
- 开启 **合并 Agent 中间消息**：`provider_settings.buffer_intermediate_messages = true`
- 保持 **分段回复 / 断句功能**开启：普通 LLM 回复仍然会按你原来的规则断句；本插件只让调用工具后的 Agent 最终回复跳过断句。

等效的 `data/cmd_config.json` 配置如下：

```json
{
  "provider_settings": {
    "streaming_response": false,
    "buffer_intermediate_messages": true
  }
}
```

## 工作效果
开启AgentShutUp前：

<img width="325" height="693" alt="214f6ee822ca4505e0c1c680a40e5e16" src="https://github.com/user-attachments/assets/0823fae1-3b8e-4b66-99a5-8fb814f9b2d6" />

开启AgentShutUp后：

<img width="416" height="363" alt="54c97a5051ae934f44afff85d49b45e7" src="https://github.com/user-attachments/assets/ef2f1962-25ba-4bff-ba5e-802542eeb155" />


## 安装

将整个插件目录放入 AstrBot 的 `data/plugins/` 目录，然后在 AstrBot WebUI 中重载插件。

## 插件配置

| 配置项 | 默认值 | 说明 |
| --- | --- | --- |
| `enabled` | `true` | 是否启用插件。 

## 原理

插件仅在 Agent 开始调用 LLM 工具时为当前消息事件添加标记。发送最终结果前，插件将该结果从 `LLM_RESULT` 改为 `GENERAL_RESULT`，使 AstrBot 的“仅对 LLM 结果分段”规则不再匹配它。

未调用工具的普通直接回答不会带上该标记，因此不会影响原有断句行为。

## 限制

为了跳过断句，插件会在发送前将调用工具后的 Agent 最终结果从 `LLM_RESULT` 改为 `GENERAL_RESULT`。因此 AstrBot 内置 TTS 不会自动处理这条 Agent 最终文本；普通 LLM 的 TTS 行为不受影响。

## 么么
欢迎发issue指出问题，我非常乐意改进插件
