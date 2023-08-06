from typing import Callable, Optional, Any, Union
import networkx as nx
import json
from flask import Flask, render_template
import json

from .type import (
    AgentResult,
    AreaBounds,
    EdgeResult,
    NodeResult,
    Position,
    RouteResult,
    SimulationResult,
    TimeBounds,
)

AnyGraph = Union[nx.Graph, nx.MultiGraph, nx.DiGraph, nx.MultiDiGraph]


class Environment:
    G: AnyGraph
    timestamp: int
    nodes: list[Any]
    agents: list[Any]

    def __init__(self, G: AnyGraph) -> None:
        self.G = G
        self.timestamp = 0
        self.nodes = []
        self.agents = []

    def edge_distance(self, source: Any, target: Any) -> Optional[float]:
        e = self.G.get_edge_data(source, target)
        if not e:
            return None
        if isinstance(self.G, (nx.MultiGraph, nx.MultiDiGraph)):
            return min([e[k]["length"] for k in e])
        return e["length"]

    def node_position(self, id: Any) -> Position:
        n = self.G.nodes[id]
        return Position(x=n["x"], y=n["y"])


class Agent:
    env: Environment
    id: int
    __icon: str
    __speed: float
    __progress: float
    __route: list[Any]
    __logs: list[RouteResult]
    __todos: list[tuple[Callable[[], bool], Callable[[], Any]]]

    def reset(self):
        self.__icon = "https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsoutlined/directions_run/default/48px.svg"  # noqa: E501
        self.__speed = 1.0
        self.__progress = 0.0
        self.__route = []
        self.__logs = []
        self.__todos = []
        self.env = None

    def __init__(self, **kwargs):
        self.reset()
        for k in kwargs:
            setattr(self, k, kwargs[k])

    # override

    def search_path(self, source: Any, target: Any):
        """maybe override"""
        return nx.dijkstra_path(self.env.G, source, target, weight="length")

    def on_started(self):
        """for override"""

    def on_passed(self):
        """for override"""

    def on_arrived(self):
        """for override"""

    def on_everytime(self):
        """for override"""

    def is_free(self):
        len_r = len(self.__route)
        return len_r < 2 and not self.__todos

    def set_icon(self, v: str):
        self.__icon = v
        self.log()

    def set_speed(self, v: float):
        self.__speed = v
        self.log()

    def set_start_node(self, v: Any):
        len_r = len(self.__route)
        if len_r < 2:
            self.__route = [v]
            return
        self.__route = self.search_path(v, self.__route[-1])
        self.log()

    def set_goal_node(self, v: Any):
        len_r = len(self.__route)
        if len_r < 1:
            return
        self.__route = self.search_path(self.__route[0], v)
        self.log()

    def step(self):
        self.on_everytime()
        todos = []
        for todo in self.__todos:
            if todo[0]():
                todo[1]()
                continue
            todos.append(todo)
        self.__todos = todos
        len_r = len(self.__route)
        if len_r < 2:
            return
        self.__progress += self.__speed
        e = self.env
        n1 = self.__route[0]
        n2 = self.__route[1]
        n3 = self.__route[2] if len_r > 2 else None
        d = e.edge_distance(n1, n2)
        if d is None:
            raise Exception("invalid route")
        if self.__progress < d:
            return
        # passed
        self.__progress -= d
        self.__route.pop(0)
        self.log()
        e.nodes = [n2, n1, n3]
        self.on_passed()
        if n3 is not None:
            return
        # arrived
        self.on_arrived()

    def log(self):
        e = self.env
        len_r = len(self.__route)
        if len_r == 0:
            return
        n1 = self.__route[0]
        p1 = e.node_position(n1)
        if len_r == 1:
            self.__logs.append(
                RouteResult(x=p1.x, y=p1.y, timestamp=e.timestamp, icon=self.__icon)
            )
            return
        n2 = self.__route[1]
        p2 = e.node_position(n2)
        d = e.edge_distance(n1, n2)
        w2 = self.__progress / d
        w1 = 1 - w2
        self.__logs.append(
            RouteResult(
                x=p1.x * w1 + p2.x * w2,
                y=p1.y * w1 + p2.y * w2,
                timestamp=e.timestamp,
                icon=self.__icon,
            )
        )

    def task(self, wait: Any, todo: Callable[[], Any]):
        if callable(wait):
            w = wait
        else:
            t = self.env.timestamp

            def w():
                return self.env.timestamp >= t + wait

        self.__todos.append((w, todo))

    def get_logs(self):
        return self.__logs


def create_envrironment(G: AnyGraph):
    return Environment(G)


def simulate(agents: list[Agent], G: AnyGraph) -> SimulationResult:
    # starting
    e = create_envrironment(G)
    for i, a in enumerate(agents):
        a.id = i
        a.env = e
        e.agents.append(a)

    for a in agents:
        a.on_started()

    # simulating
    while [a for a in agents if not a.is_free()]:
        e.timestamp += 1
        for a in agents:
            a.step()

    # ending
    agent_results = [
        AgentResult(classname=a.__class__.__name__, routes=a.get_logs()) for a in agents
    ]
    node_results = [NodeResult(id=id, **attr) for id, attr in G.nodes(data=True)]
    edge_results = [EdgeResult(left=left, right=right) for left, right in G.edges()]
    all_routes: list[RouteResult] = sum(
        [[r for r in a.routes] for a in agent_results], []
    )
    time_bounds = TimeBounds(
        min=0,
        max=max([r.timestamp for r in all_routes]),
    )
    xs = [r.x for r in all_routes] + [n.x for n in node_results]
    ys = [r.y for r in all_routes] + [n.y for n in node_results]
    area_bounds = AreaBounds(n=max(ys), s=min(ys), e=max(xs), w=min(xs))
    simulation_result = SimulationResult(
        nodes=node_results,
        edges=edge_results,
        agents=agent_results,
        time_bounds=time_bounds,
        area_bounds=area_bounds,
    )

    for a in agents:
        a.reset()

    return simulation_result


def preview(simulation_result: SimulationResult):
    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template(
            "index.html", simulation_result=json.dumps(simulation_result.dict())
        )

    app.run()
