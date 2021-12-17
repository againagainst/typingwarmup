from dataclasses import dataclass, field
from layout import Finger, ISO as LayoutISO


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


def key_finger_actual(m: Mistake) -> Finger:
    return m.finger_actual


def key_finger_expected(m: Mistake) -> Finger:
    return m.finger_expected
