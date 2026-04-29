from typing import Any
from app.config import get_settings


class AIClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    def generate(self, role: str, prompt: str, payload: dict[str, Any]) -> str:
        if self.settings.ai_provider.lower() == "zhipu" and self.settings.zhipuai_api_key:
            from zhipuai import ZhipuAI
            client = ZhipuAI(api_key=self.settings.zhipuai_api_key)
            response = client.chat.completions.create(
                model=self.settings.zhipuai_model,
                messages=[
                    {"role": "system", "content": role},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content

        product_name = payload.get("product_name", "Unknown Product")
        market = payload.get("target_market", "Global")
        platform = payload.get("platform", "Amazon")
        return f"[MOCK AI] {role}\nProduct: {product_name}\nMarket: {market}\nPlatform: {platform}\n\n{prompt[:900]}"


ai_client = AIClient()
