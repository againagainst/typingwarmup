import datetime
from dataclasses import dataclass, field
from typing import List

from dataholders.mistake import Mistake


@dataclass(order=True, frozen=True)
class DbRecord:
    excercise_name: str
    excercise_text: str
    symbols_typed: int
    score: int
    mistakes: List[Mistake]
    date: datetime.date = field(default=datetime.datetime.now())
    version: str = "2"
