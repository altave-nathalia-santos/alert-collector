from attrs import define


@define
class Alert:
    id: str
    categories: dict
    tenant: str
    timestamp: int
    valuation: int