import base64
import hashlib
import hmac
import time
from typing import Any
import httpx
from app.config import get_settings


def _sign(secret: str, timestamp: str) -> str:
    string_to_sign = f"{timestamp}\n{secret}".encode("utf-8")
    digest = hmac.new(string_to_sign, b"", digestmod=hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


async def notify_feishu(title: str, content: dict[str, Any]) -> None:
    settings = get_settings()
    if not settings.feishu_webhook_url:
        return

    body: dict[str, Any] = {
        "msg_type": "text",
        "content": {"text": f"{title}\n{content}"},
    }
    if settings.feishu_secret:
        timestamp = str(int(time.time()))
        body["timestamp"] = timestamp
        body["sign"] = _sign(settings.feishu_secret, timestamp)

    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(settings.feishu_webhook_url, json=body)
