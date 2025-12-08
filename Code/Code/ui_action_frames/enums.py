from enum import Enum

class MovementType(Enum):
    """
    Type de mouvement de la souris (relatif ou absolu).
    """
    RELATIVE = "relative"
    ABSOLUTE = "absolute"


class Direction(Enum):
    """
    Type de direction de scroll.
    """
    UP = "up"
    LEFT = "left"
    RIGHT = "right"
    DOWN = "down"

#class ActionType(Enum):
#    CLICK_LEFT = "click_l"
#    CLICK_RIGHT = "click_r"
#    MOVE = "move"
#    WRITE = "write"
#    SCROLL = "scroll"
#    WAIT = "wait"
#    KEY_PRESS = "key_press"
#    SAME_TIME = "same_time"
#    LOOP = "loop"

