from dataclasses import dataclass


@dataclass
class State:
    repaint: bool = True
    typing_error: bool = False
