"""astrbot_plugin_reply_interceptor
拦截群聊中对 bot link_resolver 解析结果(视频/图片/摘要)的回复，
命中引用即 event.stop_event() 0 token 终止后续 LLM 调用，防止刷 token。
"""
import re

from astrbot.api import AstrBotConfig, logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.event.filter import EventMessageType
from astrbot.api.message_components import Image, Plain, Reply, Video
from astrbot.api.star import Context, Star, register

# 兜底特征：link_resolver 输出文本的 signature
LINK_RESOLVER_TEXT_PATTERNS = [
    r"🍠\s*小红书",
    r"🎬\s*B站",
    r"标题",
    r"作者",
    r"播放",
    r"bilibili",
    r"douyin",
    r"xiaohongshu",
    r"weibo",
    r"小红书",
    r"B站",
    r"抖音",
    r"微博",
]


@register(
    "astrbot_plugin_reply_interceptor",
    "Texas_qwq",
    "拦截群聊中对 bot 视频/图片解析消息的回复，0 token 终止后续 LLM 调用",
    "v1.0.0",
)
class ReplyInterceptor(Star):
    def __init__(self, context: Context, config: AstrBotConfig | dict | None = None):
        super().__init__(context)
        self.context = context
        self.config = config or context.get_config()
        self.enabled = bool(self.config.get("enabled", True))
        self.log_intercepted = bool(self.config.get("log_intercepted", True))

    @filter.event_message_type(EventMessageType.GROUP_MESSAGE)
    async def intercept_reply_to_resolver(self, event: AstrMessageEvent):
        # 0. 功能开关
        if not self.enabled:
            return

        # 1. bot 自己发的消息不处理，防止自我触发
        if str(event.get_sender_id()) == str(event.get_self_id()):
            return

        # 2. 只找消息链里的 Reply 组件
        message = event.get_messages() or []
        for seg in message:
            if not isinstance(seg, Reply):
                continue
            if self._is_bot_resolver_message(event, seg):
                if self.log_intercepted:
                    logger.info(
                        "[ReplyInterceptor] 拦截对 link_resolver 解析消息的回复，0 token 终止 (引用msg_id=%s)",
                        seg.id,
                    )
                event.stop_event()
                return

    def _is_bot_resolver_message(self, event: AstrMessageEvent, reply: Reply) -> bool:
        # 被引用的消息发送者必须是 bot 自己
        if str(reply.sender_id) != str(event.get_self_id()):
            return False

        # 兜底：被引用消息链里含 Video / Image，基本就是 bot 发的媒体解析结果
        chain = reply.chain or []
        for seg in chain:
            if isinstance(seg, (Image, Video)):
                return True

        # 兜底：link_resolver 输出文本特征
        msg_str = reply.message_str or ""
        if not msg_str:
            msg_str = " ".join(
                getattr(seg, "text", "") or ""
                for seg in chain
                if isinstance(seg, Plain)
            )
        for pattern in LINK_RESOLVER_TEXT_PATTERNS:
            if re.search(pattern, msg_str, re.IGNORECASE):
                return True

        return False
