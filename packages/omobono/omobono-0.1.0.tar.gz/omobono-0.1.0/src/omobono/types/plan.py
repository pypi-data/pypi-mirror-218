from src.omobono.types.fee import Fee
from src.omobono.types.plan_cost import PlanCost


class Plan:

    def __init__(
        self,
        name: str,
        cost: list[PlanCost],
        fees: list[Fee]
    ) -> None:
        self._name = name
        self._cost = cost
        self._fees = fees

    @property
    def cost(self) -> list[PlanCost]:
        return self._cost

    @property
    def fees(self) -> list[Fee]:
        return self._fees

    @property
    def name(self) -> str:
        return self._name
