# bsimx

The agent-based modeling tool with [deck.gl](https://deck.gl/), [networkx](https://networkx.org/) and [osmnx](https://osmnx.readthedocs.io/en/stable/)..

## Installation

```sh
pip install networkx osmnx bsimx
```

## Getting Started

```py
import osmnx as ox
from bsimx import preview, Agent, simulate


G = ox.graph_from_place("Takamatsu Hayashi", network_type="drive")


class Escaper(Agent):
    start: int

    def on_started(self):
        self.set_start_node(self.start)
        self.set_goal_node(1042117440)
        self.set_speed(1.0)


sr = simulate([Escaper(start=1042116599), Escaper(start=4111619945)], G)
preview(sr)
```
