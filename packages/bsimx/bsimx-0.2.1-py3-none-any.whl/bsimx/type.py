from typing import List
from pydantic import BaseModel


class Position(BaseModel):
    x: float
    y: float


class RouteResult(BaseModel):
    icon: str
    x: float
    y: float
    timestamp: int


class AgentResult(BaseModel):
    classname: str
    routes: List[RouteResult]


class EdgeResult(BaseModel):
    left: int | str
    right: int | str


class NodeResult(BaseModel):
    id: int | str
    x: float
    y: float


class TimeBounds(BaseModel):
    min: int
    max: int


class AreaBounds(BaseModel):
    n: float
    s: float
    e: float
    w: float


class SimulationResult(BaseModel):
    nodes: List[NodeResult]
    edges: List[EdgeResult]
    agents: List[AgentResult]
    time_bounds: TimeBounds
    area_bounds: AreaBounds
