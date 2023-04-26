from dataclasses import dataclass, field
from itertools import count
from typing import Any, Union

from padme_conductor.Plugins.DatabasePlugin import DatabasePlugin


@dataclass
class Query:
    query: Any
    plugin: DatabasePlugin
    station_name: Union[str, None] = None
    _id: int = field(default_factory=count().__next__, init=False)
    _created_via_conductor: bool = field(default=False, init=False, repr=False)

    # def __post_init__(self):
    #     _station_queries[self.station_name].append(self)