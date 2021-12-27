from dataclasses import dataclass, field
from typing import List, Tuple
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


def key_actual(m: Mistake) -> str:
    return m.actual


def key_expected(m: Mistake) -> str:
    return m.expected


def key_actual_finger(m: Mistake) -> Finger:
    return m.finger_actual


def key_expected_finger(m: Mistake) -> Finger:
    return m.finger_expected


def key_actual_combined(m: Mistake) -> Tuple[Finger, str]:
    return (m.finger_actual, m.actual)


def key_expected_combined(m: Mistake) -> Tuple[Finger, str]:
    return (m.finger_expected, m.expected)


Mistakes = List[Mistake]
