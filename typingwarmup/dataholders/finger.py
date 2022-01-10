from enum import Enum


class OrderedEnum(Enum):
    def __ge__(self, other: "OrderedEnum"):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other: "OrderedEnum"):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other: "OrderedEnum"):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other: "OrderedEnum"):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class Finger(OrderedEnum):
    left_pinky = "left pinky"
    left_ring = "left ring"
    left_middle = "left middle"
    left_index = "left index"
    any_thumb = "thumb"
    right_index = "right index"
    right_middle = "right middle"
    right_ring = "right ring"
    right_pinky = "right pinky"
    other = "other"

    def __str__(self) -> str:
        return self.value
