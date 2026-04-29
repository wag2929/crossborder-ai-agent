from typing import Any
from app.ai import ai_client


class BaseAgent:
    name = "base_agent"
    role = "You are a helpful cross-border e-commerce AI agent."

    def run(self, payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        prompt = self.build_prompt(payload, context)
        output = ai_client.generate(self.role, prompt, payload)
        return {"agent": self.name, "output": output}

    def build_prompt(self, payload: dict[str, Any], context: dict[str, Any]) -> str:
        return str(payload)


class ProductParserAgent(BaseAgent):
    name = "product_parser"
    role = "You extract product category, target users, scenarios, selling points, and constraints."

    def build_prompt(self, payload: dict[str, Any], context: dict[str, Any]) -> str:
        return f"Analyze this product data and extract structured selling information:\n{payload}"


class ListingAgent(BaseAgent):
    name = "listing_agent"
    role = "You create high-converting product listings for cross-border e-commerce platforms."

    def build_prompt(self, payload: dict[str, Any], context: dict[str, Any]) -> str:
        return f"Create title, five bullet points, product description, and image copy suggestions. Context: {context}. Product: {payload}"


class KeywordAgent(BaseAgent):
    name = "keyword_agent"
    role = "You are an SEO and advertising keyword expert for cross-border e-commerce."

    def build_prompt(self, payload: dict[str, Any], context: dict[str, Any]) -> str:
        return f"Generate main keywords, long-tail keywords, buyer-intent keywords, and negative keywords. Context: {context}. Product: {payload}"


class LocalizationAgent(BaseAgent):
    name = "localization_agent"
    role = "You localize e-commerce copy for overseas buyers, avoiding literal translation."

    def build_prompt(self, payload: dict[str, Any], context: dict[str, Any]) -> str:
        return f"Localize the listing and keywords for the target market. Context: {context}. Product: {payload}"


class CustomerServiceAgent(BaseAgent):
    name = "customer_service_agent"
    role = "You write polite, helpful, platform-safe customer service replies."

    def build_prompt(self, payload: dict[str, Any], context: dict[str, Any]) -> str:
        return f"Write a customer service reply based on customer_message or after-sales scenario. Context: {context}. Data: {payload}"


class CompetitorAgent(BaseAgent):
    name = "competitor_agent"
    role = "You analyze competitor listings, reviews, selling points, and improvement opportunities."

    def build_prompt(self, payload: dict[str, Any], context: dict[str, Any]) -> str:
        return f"Analyze competitor copy, pain points, review risks, pricing signals, and optimization suggestions. Context: {context}. Data: {payload}"


class ProductSelectionAgent(BaseAgent):
    name = "product_selection_agent"
    role = "You evaluate product opportunities for cross-border e-commerce sellers."

    def build_prompt(self, payload: dict[str, Any], context: dict[str, Any]) -> str:
        return f"Evaluate market demand, competition, logistics difficulty, return risk, and beginner suitability. Context: {context}. Data: {payload}"
