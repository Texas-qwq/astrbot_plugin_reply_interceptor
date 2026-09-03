# astrbot_plugin_reply_interceptor

- 这是我第一次发布，大量使用AI编写，如有不足请多包涵。
- 不知你是否遇见过给AstrBot装了视频解析插件后，群友发了诸如b站链接一类的让bot解析，视频发出来后群友下意识直接回复bot的视频消息作评论给其他人看，但此举会导致bot被@还以为是在召唤自己，从而开始调用LLM回复群友那句本应该是评论视频内容的消息，找了一番AstrBot插件仓库发现没有人做类似的插件，所以此插件就为了解决这个问题，bot在这种不该响应回复的时候它会拦截群聊中对 bot 视频/图片解析消息（link_resolver）的回复，命中引用即 **0 token** 终止后续 LLM 调用，防止浪费token。

## 功能
- 命中 `Reply` 组件引用 bot 解析消息时，调用 `event.stop_event()` 终止事件传播
- 内置兜底特征：小红书、B站、视频/图片解析文本等

## 配置
| 配置项 | 说明 | 默认 |
| --- | --- | --- |
| `enabled` | 启用拦截功能 | `true` |
| `log_intercepted` | 拦截时输出日志 | `true` |

## 安装
- 在AstrBot插件市场搜索安装。
- 下载源码放入 AstrBot 插件目录 `data/plugins/` 后生效。

