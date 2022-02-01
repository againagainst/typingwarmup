from dataclasses import dataclass, field
from typing import List
from dataholders.finger import Finger
from dataholders.layout import ISO as LayoutISO


@dataclass
class Mistake:
    actual: str
    expected: str
    finger_actual: Finger = field(init=False)
    finger_expected: Finger = field(init=False)

    def __post_init__(self):
        self.finger_actual = LayoutISO.get(self.actual, Finger.other)
        self.finger_expected = LayoutISO.get(self.expected, Finger.other)


Mistakes = List[Mistake]
