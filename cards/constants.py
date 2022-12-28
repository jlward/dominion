from enum import Enum, auto


class CardTypes(Enum):
    Action = auto()
    Attack = auto()
    Curse = auto()
    Duration = auto()
    Reaction = auto()
    Treasure = auto()
    Victory = auto()
