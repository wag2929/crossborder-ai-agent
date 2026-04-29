from typing import Any
from app.agents import (
    CompetitorAgent,
    CustomerServiceAgent,
    KeywordAgent,
    ListingAgent,
    LocalizationAgent,
    ProductParserAgent,
    ProductSelectionAgent,
)


class AgentOrchestrator:
    def __init__(self) -> None:
        self.parser = ProductParserAgent()
        self.listing = ListingAgent()
        self.keyword = KeywordAgent()
        self.localization = LocalizationAgent()
        self.customer_service = CustomerServiceAgent()
        self.competitor = CompetitorAgent()
        self.product_selection = ProductSelectionAgent()

    def run(self, task_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        context: dict[str, Any] = {}
        steps: list[dict[str, Any]] = []

        if task_type == "listing":
            return self._run_steps(payload, [self.parser, self.listing])
        if task_type == "keywords":
            return self._run_steps(payload, [self.parser, self.keyword])
        if task_type == "localization":
            return self._run_steps(payload, [self.parser, self.listing, self.localization])
        if task_type == "customer_service":
            return self._run_steps(payload, [self.customer_service])
        if task_type == "competitor":
            return self._run_steps(payload, [self.competitor])
        if task_type == "product_selection":
            return self._run_steps(payload, [self.product_selection])
        if task_type == "full_workflow":
            return self._run_steps(
                payload,
                [self.parser, self.listing, self.keyword, self.localization, self.competitor, self.product_selection],
            )

        raise ValueError(f"Unsupported task type: {task_type}")

    def _run_steps(self, payload: dict[str, Any], agents: list[Any]) -> dict[str, Any]:
        context: dict[str, Any] = {}
        steps: list[dict[str, Any]] = []
        for agent in agents:
            result = agent.run(payload, context)
            steps.append(result)
            context[agent.name] = result["output"]
        return {"steps": steps, "final": steps[-1]["output"] if steps else None}


orchestrator = AgentOrchestrator()
