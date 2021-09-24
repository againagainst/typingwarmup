from dataclasses import dataclass
from typing import Optional


@dataclass
class State:
    wrong_input: Optional[str] = None
