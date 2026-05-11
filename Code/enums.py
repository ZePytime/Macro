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


class ShortCut(Enum):
    """
    Type de raccourci clavier.
    """
    STOP = "stop_key"
    CAPTURE = "capture_key"


class ActionType(Enum):
    CLICK_LEFT = "click_l"
    CLICK_RIGHT = "click_r"
    MOVE = "move"
    WRITE = "write"
    SCROLL = "scroll"
    WAIT = "wait"
    KEY_PRESS = "key_press"
    PARALLEL_ACTIONS = "parallel_actions"
    LOOP = "loop"
    LEFT_CONTAINER = "left_container"


class SpecialKeys(Enum):
    ALT = "alt"
    CTRL = "ctrl"
    ALTGR = "altgr"
    ENTRER = "enter"
    CLICK_R = "click r"
    ESC = "esc"
    DELETE = "delete"
    SHIFT = "shift"
    TAB = "tab"
    BACKSPACE = "backspace"
    CMD = "cmd"
    UP = "up"
    LEFT = "left"
    RIGHT = "right"
    DOWN = "down"
    CAPS_LOCK = "caps lock"
    CLICK_L = "click l"

# Tuple de toutes les touches spéciales disponibles 
# --------------------------------------------------
# Tuple of all available special keys
SPECIAL_KEYS_LAYOUT = (
    (SpecialKeys.ALT, SpecialKeys.CTRL, SpecialKeys.ALTGR, SpecialKeys.ENTRER, SpecialKeys.CLICK_R), 
    (SpecialKeys.ESC, SpecialKeys.DELETE, SpecialKeys.SHIFT, SpecialKeys.TAB, SpecialKeys.BACKSPACE, SpecialKeys.CMD), 
    (SpecialKeys.UP, SpecialKeys.LEFT, SpecialKeys.RIGHT, SpecialKeys.DOWN, SpecialKeys.CAPS_LOCK, SpecialKeys.CLICK_L)
    )