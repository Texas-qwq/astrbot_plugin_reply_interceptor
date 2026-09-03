# astrbot_plugin_reply_interceptor

这是我第一次发布，大量使用AI编写，如有不足请多包涵，此插件主要是为了解决bot在不该相应的时候调用LLM大量响应的问题，它会拦截群聊中对 bot 视频/图片解析消息（link_resolver）的回复，命中引用即 **0 token** 终止后续 LLM 调用，防止浪费token。

## 功能
- 命中 `Reply` 组件引用 bot 解析消息时，调用 `event.stop_event()` 终止事件传播
- 内置兜底特征：小红书、B站、视频/图片解析文本等

## 配置
| 配置项 | 说明 | 默认 |
| --- | --- | --- |
| `enabled` | 启用拦截功能 | `true` |
| `log_intercepted` | 拦截时输出日志 | `true` |

## 安装
下载源码放入 AstrBot 插件目录 `data/plugins/` 后生效。

