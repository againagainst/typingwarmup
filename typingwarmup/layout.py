from enum import Enum


class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
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


ISO = {
    "`": Finger.left_pinky,
    "~": Finger.left_pinky,
    "1": Finger.left_pinky,
    "!": Finger.left_pinky,
    "q": Finger.left_pinky,
    "a": Finger.left_pinky,
    "z": Finger.left_pinky,
    "Q": Finger.left_pinky,
    "A": Finger.left_pinky,
    "Z": Finger.left_pinky,
    "2": Finger.left_ring,
    "@": Finger.left_ring,
    "w": Finger.left_ring,
    "W": Finger.left_ring,
    "s": Finger.left_ring,
    "S": Finger.left_ring,
    "x": Finger.left_ring,
    "X": Finger.left_ring,
    "3": Finger.left_middle,
    "#": Finger.left_middle,
    "e": Finger.left_middle,
    "E": Finger.left_middle,
    "d": Finger.left_middle,
    "D": Finger.left_middle,
    "c": Finger.left_middle,
    "C": Finger.left_middle,
    "4": Finger.left_index,
    "$": Finger.left_index,
    "r": Finger.left_index,
    "R": Finger.left_index,
    "f": Finger.left_index,
    "F": Finger.left_index,
    "v": Finger.left_index,
    "V": Finger.left_index,
    "5": Finger.left_index,
    "%": Finger.left_index,
    "t": Finger.left_index,
    "T": Finger.left_index,
    "g": Finger.left_index,
    "G": Finger.left_index,
    "b": Finger.left_index,
    "B": Finger.left_index,
    "6": Finger.right_index,
    "^": Finger.right_index,
    "y": Finger.right_index,
    "Y": Finger.right_index,
    "h": Finger.right_index,
    "H": Finger.right_index,
    "n": Finger.right_index,
    "N": Finger.right_index,
    "7": Finger.right_index,
    "&": Finger.right_index,
    "u": Finger.right_index,
    "U": Finger.right_index,
    "j": Finger.right_index,
    "J": Finger.right_index,
    "m": Finger.right_index,
    "M": Finger.right_index,
    "8": Finger.right_middle,
    "*": Finger.right_middle,
    "i": Finger.right_middle,
    "I": Finger.right_middle,
    "k": Finger.right_middle,
    "K": Finger.right_middle,
    ",": Finger.right_middle,
    "<": Finger.right_middle,
    "9": Finger.right_ring,
    "(": Finger.right_ring,
    "o": Finger.right_ring,
    "O": Finger.right_ring,
    "l": Finger.right_ring,
    "L": Finger.right_ring,
    ".": Finger.right_ring,
    ">": Finger.right_ring,
    "0": Finger.right_pinky,
    ")": Finger.right_pinky,
    "p": Finger.right_pinky,
    "P": Finger.right_pinky,
    ";": Finger.right_pinky,
    ":": Finger.right_pinky,
    "/": Finger.right_pinky,
    "?": Finger.right_pinky,
    "-": Finger.right_pinky,
    "_": Finger.right_pinky,
    "=": Finger.right_pinky,
    "+": Finger.right_pinky,
    "[": Finger.right_pinky,
    "{": Finger.right_pinky,
    "]": Finger.right_pinky,
    "}": Finger.right_pinky,
    "\\": Finger.right_pinky,
    "|": Finger.right_pinky,
    "'": Finger.right_pinky,
    '"': Finger.right_pinky,
    " ": Finger.any_thumb,
    # Special keys
    "\t": Finger.left_pinky,
    "⎀": Finger.left_pinky,
    "⏎": Finger.right_pinky,
    "⌫": Finger.right_pinky,
    "\n": Finger.right_pinky,
    "\x1b": Finger.right_pinky,
    # Extra keys
    "⇧": Finger.other,
    "⇩": Finger.other,
    "⇦": Finger.other,
    "⇨": Finger.other,
    "⇤": Finger.other,
    "⇥": Finger.other,
    "⌦": Finger.other,
    "⤒": Finger.other,
    "⤓": Finger.other,
    "⎊": Finger.other,
}
