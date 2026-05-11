from __future__ import annotations
import tkinter as tk
import pydirectinput
from abc import ABC, abstractmethod
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from pynput import keyboard as my_keyboard

from ui_style import W_VAR
keyboard = KeyboardController()
mouse = MouseController()

from enums import MovementType, Direction, SpecialKeys, ActionType

from typing import TYPE_CHECKING, Tuple, Callable, Dict
if TYPE_CHECKING:
    from ui_action_tree import TreeUI

# On crée un dictionnaire qui, pour chaque touche spéciale ainsi que le 
# clic droit et le clic gauche, contient l'élément pynput correspondant. 
# Cela permet, lorsqu'on doit simuler un appui, de simplement donner la clé 
# correspondante et le dictionnaire renvoie l'élément adapté pour simuler 
# l'appui.
# --------------------------------------------------------------------------
# We create a dictionary that, for each special key as well as right-click 
# and left-click, contains the corresponding pynput element. 
# This allows us, when simulating a key press, to simply provide the 
# corresponding key and the dictionary returns the appropriate element.
SP_KEY_DICT = {
    SpecialKeys.ALT:Key.alt, SpecialKeys.CTRL:Key.ctrl, SpecialKeys.ALTGR:Key.alt_gr, SpecialKeys.CMD:Key.cmd, 
    SpecialKeys.ESC:Key.esc, SpecialKeys.DELETE:Key.delete, SpecialKeys.SHIFT:Key.shift, SpecialKeys.TAB:Key.tab, 
    SpecialKeys.BACKSPACE:Key.backspace, SpecialKeys.UP:Key.up, SpecialKeys.LEFT:Key.left, SpecialKeys.RIGHT:Key.right, 
    SpecialKeys.DOWN:Key.down, SpecialKeys.CAPS_LOCK:Key.caps_lock, SpecialKeys.ENTRER:Key.enter, 
    SpecialKeys.CLICK_R:Button.right, SpecialKeys.CLICK_L:Button.left
}

last_mouse_pos = (0, 0)



def position_mouse() -> Tuple[int, int]:
    global last_mouse_pos
    """
    Fonction qui retourne la position de la souris de l'utilisateur.
    :return: Un tuple contenant les positions x et y de la 
        souris de l'utilisateur.
    -----------------------------------------------------------------------
    Function that returns the user's mouse position.
    :return: A tuple containing the x and y positions of the user's mouse.
    """
    m_pos = mouse.position
    if m_pos is None:
        return last_mouse_pos
    else:
        last_mouse_pos = m_pos
        return m_pos




class KeyPosition:
    """
    Cette classe permet de capturer la position de la souris de 
    l'utilisateur et de l'inscrire dans les champs de texte des interfaces 
    click_ui et move_ui. La position de la souris est capturée lorsque 
    l'utilisateur appuie simultanément sur les touches "X" et "V" 
    (ces touches peuvent être modifiées).
    -----------------------------------------------------------------------
    This class allows capturing the user's mouse position and inserting it 
    into the text fields of the click_ui and move_ui interfaces.
    The mouse position is captured when the user simultaneously presses 
    the "X" and "V" keys (these keys can be modified).
    """

    # Cette variable permet de savoir si nous sommes 
    # en train d'observer les pressions de touches ou non.
    # -----------------------------------------------------
    # This variable indicates whether we are currently 
    # listening to key presses.
    is_listening = False

    # Touche de base pour capturer la position.
    # -------------------------------------------
    # Default keys used to capture the position.
    position_capture_keys = ["x", "v"]

    


    def __init__(self, set_coordinate_click: Callable[[Tuple[int, int], str], None], set_coordinate_move: Callable[[Tuple[int, int], str], None]) -> None:
        """
        On démarre l'observation des touches pressées par 
        l'utilisateur pour capturer la position de la souris.

        :param set_coordinate_click: Fonction permettant d'inscrire 
            la position de la souris dans les champs de texte de click_ui.
        :param set_coordinate_move: Fonction permettant d'inscrire 
            la position de la souris dans les champs de texte de move_ui.
        --------------------------------------------------------------------
        Starts listening to user key presses to capture the mouse position.

        :param set_coordinate_click: Function used to insert 
            the mouse position into click_ui text fields.
        :param set_coordinate_move: Function used to insert 
            the mouse position into move_ui text fields.
        """

        # On met is_listening à True pour indiquer que nous 
        # sommes en train d'observer les touches pressées.
        # --------------------------------------------------
        # Set is_listening to True to indicate that we are 
        # listening to key presses.
        KeyPosition.is_listening = True

        # On récupère les fonctions qui permettent d'inscrire la position 
        # de la souris dans click_ui et move_ui.
        # ----------------------------------------------------------------
        # We retrieve the functions used to insert the mouse position 
        # into click_ui and move_ui.
        self.set_coordinate_click = set_coordinate_click
        self.set_coordinate_move = set_coordinate_move

        # On crée un set qui contiendra les touches 
        # de captures lorsqu'elles sont pressées.
        # ---------------------------------------------------
        # Create a set that will store pressed capture keys.
        self.pressed_position_keys = set()

        # On choisit d'observer tous les appuis et les 
        # relâchements de touches.
        # -------------------------------------------------
        # Listen to both key press and key release events.
        self.listener = my_keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )

        # On commence à observer.
        # ------------------------
        # Start listening.
        self.listener.start()


    def on_press(self, key) -> None:
        """
        Cette fonction est appelée lorsqu'une touche est pressée.
        Elle permet de vérifier si les touches pour capturer la position 
        de la souris sont pressées simultanément.

        :param key: La touche qui a été pressée.
        -----------------------------------------------------------------
        This function is called when a key is pressed.
        It checks whether the keys used to capture the mouse position 
        are pressed simultaneously.

        :param key: The key that was pressed.
        """
        # On vérifie si la touche est une touche spéciale.
        # -------------------------------------------------
        # Check if the key is a special key.
        try:
            key_char = key.char
        except AttributeError:
            key_char = None
        
        # On regarde si c'est une des touches permettant d'écrire la position. 
        # Si c'est le cas, on l'ajoute au set pressed_position_keys.
        # ---------------------------------------------------------------------
        # Check if it is one of the keys used to capture the position.
        # If so, add it to the pressed_position_keys set.
        if key_char in KeyPosition.position_capture_keys:
            self.pressed_position_keys.add(key_char)

        # On vérifie si les deux touches pour capturer la position 
        # de la souris sont pressées simultanément.
        # ---------------------------------------------------------
        # Check if both capture keys are pressed simultaneously.
        if len(self.pressed_position_keys) == len(KeyPosition.position_capture_keys):
            # Si c'est le cas, on vide le set, on appelle set_coordinate 
            # et on lui donne en paramètre la position de la souris.
            # -----------------------------------------------------------
            # If so, clear the set and call the coordinate functions.
            self.pressed_position_keys.clear()
            self.set_coordinate_click(mouse.position, "xy")
            self.set_coordinate_move(mouse.position, "xy")


    def on_release(self, key) -> None:
        """
        Cette fonction est appelée lorsqu'une touche est relâchée. 
        Elle permet de retirer les touches servant à capturer la position 
        de la souris lorsqu'elles sont relâchées de pressed_position_keys.

        :param key: La touche qui a été relâchée.
        -------------------------------------------------------------------
        This function is called when a key is released. 
        It removes the keys used to capture the mouse position 
        from pressed_position_keys when they are released.

        :param key: The key that was released.
        """

        # On vérifie si la touche est une touche spéciale.
        # -------------------------------------------------
        # Check if the key is a special key.
        try:
            key_char = key.char
        except AttributeError:
            key_char = None
        
        # On vérifie si c'est une des touches permettant de capturer 
        # la position.
        # -------------------------------------------------------------
        # Check if it is one of the keys used to capture the position.
        if key_char in self.pressed_position_keys:
            # Si c'est le cas, on l'enlève du set pressed_position_keys.
            # -----------------------------------------------------------
            # If so, remove it from the pressed_position_keys set.
            self.pressed_position_keys.remove(key_char)


    def stop_listening(self) -> None:
        """
        Cette fonction permet d'arrêter d'observer les pressions et les 
        relâchements de touches.
        ----------------------------------------------------------------
        This function stops listening to key press and release events.
        """

        KeyPosition.is_listening = False
        self.listener.stop()



class KeyLoggerApp:
    """
    Cette classe permet de stopper l'exécution de la suite d'actions 
    lorsque l'on appuie sur les deux touches "y" et "j" 
    (ces touches peuvent être modifiées). Elle n'est utilisée que par 
    ParallelActions, Loop et ActionManager.
    ------------------------------------------------------------------------
    This class allows stopping the execution of the action sequence when 
    the "y" and "j" keys are pressed simultaneously 
    (these keys can be modified). It is only used by ParallelActions, Loop,
    and ActionManager.
    """

    # Variable permettant de vérifier si les touches pour arrêter l'exécution 
    # de la suite d'actions ont été pressées. Elle permet au conteneur 
    # (ParallelActions, Loop) ou à start_execution dans ActionManager 
    # de ne pas exécuter de nouvelles actions lorsque les touches d'arrêt 
    # ont été pressées.
    # ------------------------------------------------------------------------
    # Variable used to check whether the keys to stop the execution 
    # of the action sequence have been pressed. It allows the container 
    # (ParallelActions, Loop) or start_execution in ActionManager to avoid 
    # executing new actions when the stop keys have been pressed.
    stop_run = False

    # Touche d'arrêt pour la suite d'actions.
    # ----------------------------------------
    # Stop keys for the action sequence.
    stop_keys = ["y", "j"]


    def __init__(self, cancel_task: Callable[[], None]) -> None:
        """
        Cette fonction permet d'initialiser les variables pour 
        le fonctionnement de la classe KeyLoggerApp, et démarre 
        l'observation des touches pressées par l'utilisateur pour 
        stopper l'exécution de la suite d'actions.

        :param cancel_task: Fonction permettant de stopper les 
            actions en cours.
        ---------------------------------------------------------------
        This function initializes the variables required for the 
        KeyLoggerApp class, and starts listening to user key presses 
        to stop the execution of the action sequence.

        :param cancel_task: Function used to stop the current actions.
        """

        # On récupère cancel_task pour l'appeler lorsque les 
        # touches d'arrêt sont pressées simultanément.
        # ---------------------------------------------------
        # Store cancel_task to call it when the stop keys 
        # are pressed simultaneously.
        self.cancel_task = cancel_task

        # On crée un set qui contiendra les touches d'arrêt 
        # lorsqu'elles sont pressées.
        # --------------------------------------------------
        # Create a set that will contain the stop keys 
        # when they are pressed.
        self.pressed_stop_keys = set()

        # On choisit d'observer tous les appuis et les 
        # relâchements de touches.
        # -------------------------------------------------
        # Listen to both key press and key release events.
        self.listener = my_keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        # On commence à observer.
        # ------------------------
        # Start listening.
        self.listener.start()


    def on_press(self, key) -> None:
        """
        Cette fonction est appelée lorsqu'une touche est pressée.
        Elle permet de vérifier si les touches d'arrêt de l'exécution 
        de la suite d'actions sont pressées simultanément. 
        Si oui, on appelle cancel_task pour stopper les actions en cours.

        :param key: La touche qui a été pressée.
        ------------------------------------------------------------------
        This function is called when a key is pressed.
        It checks whether the stop keys for the action sequence 
        are pressed simultaneously. 
        If so, cancel_task is called to stop the current actions.

        :param key: The key that was pressed.
        """

        # On vérifie si la touche est une touche spéciale.
        # -------------------------------------------------
        # Check if the key is a special key.
        try:
            key_char = key.char
        except AttributeError:
            key_char = None
        
        # On regarde si c'est une des touches d'arrêt qui a été pressée.
        # Si c'est le cas, on l'ajoute au set pressed_stop_keys.
        # ---------------------------------------------------------------
        # Check if it is one of the stop keys.
        # If so, add it to the pressed_stop_keys set.
        if key_char in KeyLoggerApp.stop_keys:
            self.pressed_stop_keys.add(key_char)

        # On vérifie si les deux touches pour arrêter l'exécution de 
        # la suite d'actions sont pressées simultanément.
        # -----------------------------------------------------------
        # Check if both stop keys are pressed simultaneously.
        if len(self.pressed_stop_keys) == len(KeyLoggerApp.stop_keys):
            # Si c'est le cas, on met stop_run à True pour 
            # indiquer que les touches d'arrêt ont été pressées.
            # ---------------------------------------------------
            # If so, set stop_run to True to indicate that 
            # stop keys were pressed.
            KeyLoggerApp.stop_run = True
            # On arrête d'observer les touches pressées.
            # -------------------------------------------
            # Stop listening to key presses.
            self.listener.stop()
            # On appelle cancel_task pour stopper les actions en cours.
            # ----------------------------------------------------------
            # Call cancel_task to stop current actions.
            self.cancel_task()


    def on_release(self, key) -> None:
        """
        Cette fonction est appelée lorsqu'une touche est relâchée. 
        Elle permet de retirer les touches d'arrêt lorsqu'elles 
        sont relâchées de pressed_stop_keys.

        :param key: La touche qui a été relâchée.
        -----------------------------------------------------------
        This function is called when a key is released. 
        It removes the stop keys from pressed_stop_keys 
        when they are released.

        :param key: The key that was released.
        """
        # On vérifie si la touche est une touche spéciale.
        # -------------------------------------------------
        # Check if the key is a special key.
        try:
            key_char = key.char
        except AttributeError:
            key_char = None
        
        # On vérifie si c'est une des touches permettant 
        # l'arrêt de l'exécution de la suite d'actions.
        # -----------------------------------------------
        # Check if it is one of the stop keys.
        if key_char in self.pressed_stop_keys:
            # Si c'est le cas, on l'enlève du set pressed_stop_keys.
            # -------------------------------------------------------
            # If so, remove it from the pressed_stop_keys set.
            self.pressed_stop_keys.remove(key_char)



def press_keys(special_keys: list, keys: str) -> None:
    """
    Cette fonction va actionner les touches qui lui sont données 
    en paramètre, qu'il s'agisse de touches spéciales ou non.

    :param special_keys: Une liste de touches spéciales à actionner.
    :param keys: Une chaîne de caractères contenant les touches 
        normales à actionner.
    -----------------------------------------------------------------
    This function presses the keys provided as parameters, 
    whether they are special keys or regular ones.

    :param special_keys: A list of special keys to press.
    :param keys: A string containing the regular keys to press.
    """
    
    # On parcourt les touches spéciales pour les actionner.
    # ------------------------------------------------------
    # Iterate through special keys and press them.
    for sp_key in special_keys:
        if sp_key != SpecialKeys.CLICK_R and sp_key != SpecialKeys.CLICK_L:
            keyboard.press(SP_KEY_DICT[sp_key])
        else:
            mouse.press(SP_KEY_DICT[sp_key])
    
    # On parcourt les touches normales pour les actionner.
    # -----------------------------------------------------
    # Iterate through regular keys and press them.
    for key in keys:
        keyboard.press(key)



def release_keys(special_keys: list, keys: str) -> None:
    """
    Cette fonction va relâcher les touches qui lui sont données 
    en paramètre, qu'il s'agisse de touches spéciales ou non.

    :param special_keys: Une liste de touches spéciales à relâcher.
    :param keys: Une chaîne de caractères contenant les touches 
        normales à relâcher.
    ----------------------------------------------------------------
    This function releases the keys provided as parameters, 
    whether they are special keys or regular ones.

    :param special_keys: A list of special keys to release.
    :param keys: A string containing the regular keys to release.
    """

    # On parcourt les touches spéciales pour les relâcher.
    # -----------------------------------------------------
    # Iterate through special keys and release them.
    for sp_key in special_keys:
        if sp_key != SpecialKeys.CLICK_R and sp_key != SpecialKeys.CLICK_L:
            keyboard.release(SP_KEY_DICT[sp_key])
        else:
            mouse.release(SP_KEY_DICT[sp_key])
    
    # On parcourt les touches normales pour les relâcher.
    # ----------------------------------------------------
    # Iterate through regular keys and release them.
    for key in keys:
        keyboard.release(key)



class Action(ABC):
    """
    Classe de base abstraite pour toutes les actions.
    Définit les méthodes communes que chaque action doit implémenter.
    --------------------------------------------------------------------
    Abstract base class for all actions.
    Defines the common methods that must be implemented by each action.
    """
    
    @abstractmethod
    def run(self):
        """
        Exécute l'action. Peut retourner une durée d'attente si nécessaire.
        --------------------------------------------------------------------
        Executes the action. May return a wait duration if needed.
        """
        pass
    
    @abstractmethod
    def text(self) -> str:
        """
        Retourne une chaîne descriptive de l'action.
        ---------------------------------------------
        Returns a descriptive string of the action.
        """
        pass
    
    @abstractmethod
    def action_type(self) -> str:
        """
        Retourne le type de l'action sous forme de chaîne.
        ---------------------------------------------------
        Returns the type of the action as a string.
        """
        pass




class KeyPress(Action):
    """
    Cette classe permet d'actionner des touches pendant un certain temps.
    ----------------------------------------------------------------------
    This class allows pressing keys for a specified duration.
    """

    def __init__(self, keys:str, special_keys:list, time_wait:float) -> None:
        """
        Initialisation des paramètres nécessaires à la 
        pression de touches pendant un certain temps.
        
        :param keys: Une chaîne de caractères contenant 
            les touches normales à presser.
        :param special_keys: Une liste de touches spéciales à presser.
        :param time_wait: La durée pendant laquelle les touches 
            doivent être pressées.
        ---------------------------------------------------------------------
        Initializes the parameters required to press keys 
        for a given duration.
        
        :param keys: A string containing the regular keys to press.
        :param special_keys: A list of special keys to press.
        :param time_wait: The duration for which the keys should be pressed.
        """

        # On stocke le temps d'attente en secondes pour pouvoir 
        # l'afficher dans text.
        # ------------------------------------------------------
        # Store wait time in seconds to display it in text.
        self.time_wait_s = time_wait
        # On multiplie le temps d'attente par 1000 car 
        # il est de base compté en millisecondes.
        # ---------------------------------------------
        # Convert wait time to milliseconds.
        self.time_wait_ms = int(time_wait*1000)

        # On supprime les caractères en double de la chaîne 
        # de caractères qui contient toutes les touches normales.
        # --------------------------------------------------------
        # Remove duplicate characters from the string containing 
        # all regular keys.
        self.keys = "".join(list(set(keys)))
        
        self.special_keys = special_keys

        # On crée une liste de chaînes de caractères contenant les noms 
        # des touches spéciales à partir de la liste de touches spéciales 
        # donnée en paramètre, pour pouvoir les afficher dans text.
        # ------------------------------------------------------------------
        # Create a list of strings containing the names of the special keys 
        # from the provided list, to display them in text.
        special_key_labels = []
        for sp_key in self.special_keys:
            special_key_labels.append(sp_key.value)
        # On trie les noms des touches spéciales par ordre de 
        # taille pour la fonction text.
        # --------------------------------------------------------
        # Sort special key names by length for the text function.
        self.special_key_labels = sorted(special_key_labels, key=lambda x: len(x), reverse=False)


    def run(self) -> int:
        """
        Cette fonction appelle press_keys pour actionner les touches que 
        l'utilisateur a entrées au préalable, puis retourne le temps 
        d'attente pendant lequel ces touches doivent être pressées. 
        (Ensuite, la fonction qui a appelé cette fonction se chargera, 
        après ce temps, d'appeler release_keys.)
        ----------------------------------------------------------------------
        This function calls press_keys to press the keys defined by the user, 
        then returns the duration for which these keys should remain pressed. 
        (The caller will later call release_keys after this duration.)
        """
        press_keys(self.special_keys, self.keys)
        return self.time_wait_ms


    def release_keys(self) -> None:
        """
        Cette fonction appelle release_keys pour relâcher les touches 
        qui ont été précédemment actionnées.
        ---------------------------------------------------------------
        This function calls release_keys to release the keys that were 
        previously pressed.
        """
        release_keys(self.special_keys, self.keys)


    def text(self) -> str:
        """
        Cette fonction retourne une chaîne de caractères pour représenter 
        l'action dans l'arbre des actions. Elle retourne une chaîne 
        contenant le maximum d'informations tout en étant la plus courte 
        possible, donc elle abrège certaines informations pour éviter de 
        prendre trop de place dans les menus.
        -------------------------------------------------------------------
        Returns a string representing the action in the action tree. 
        It contains as much information as possible while remaining short, 
        abbreviating some parts to avoid taking too much space.
        """
        if len(self.keys)>5:
            if len(self.special_key_labels) > 1:
                return f"KeyPress : {self.time_wait_s} | {self.keys[:3]}.. | {self.special_key_labels[0]}.."
            elif len(self.special_key_labels) == 1:
                return f"KeyPress : {self.time_wait_s} | {self.keys[:3]}.. | {self.special_key_labels[0]}"
            else:
                return f"KeyPress : {self.time_wait_s} | {self.keys[:3]}.."

        elif len(self.keys) == 0:
            if len(self.special_key_labels) > 1:
                return f"KeyPress : {self.time_wait_s} | {self.special_key_labels[0]}.."
            elif len(self.special_key_labels) == 1:
                return f"KeyPress : {self.time_wait_s} | {self.special_key_labels[0]}"

        else:
            if len(self.special_key_labels) > 1:
                return f"KeyPress : {self.time_wait_s} | {self.keys} | {self.special_key_labels[0]}.."
            elif len(self.special_key_labels) == 1:
                return f"KeyPress : {self.time_wait_s} | {self.keys} | {self.special_key_labels[0]}"
            else:
                return f"KeyPress : {self.time_wait_s} | {self.keys}"


    def action_type(self) -> str:
        """
        Cette fonction retourne le type de cette action 
        sous forme de chaîne de caractères.
        ------------------------------------------------
        Returns the type of this action as a string.
        """
        return ActionType.KEY_PRESS.value



class ClickLeft(Action):
    """
    Cette classe permet d'effectuer un clic gauche à un certain endroit.
    ---------------------------------------------------------------------
    This class performs a left click at a given position.
    """

    def __init__(self, pos_x:int, pos_y:int) -> None:
        """
        On prend la position à laquelle doit s'effectuer le clic.

        :param pos_x: La position x à laquelle doit s'effectuer le clic.
        :param pos_y: La position y à laquelle doit s'effectuer le clic.
        -----------------------------------------------------------------
        Initializes the click position.

        :param pos_x: x position where the click should occur.
        :param pos_y: y position where the click should occur.
        """
        self.pos_x = pos_x
        self.pos_y = pos_y


    def run(self) -> None:
        """
        On déplace la souris à la position choisie par l'utilisateur, 
        puis on effectue le clic.
        -----------------------------------------------------------------
        Moves the mouse to the chosen position, then performs the click.
        """
        mouse.position = (self.pos_x, self.pos_y)
        mouse.press(Button.left)
        mouse.release(Button.left)


    def text(self) -> str:
        """
        On retourne la chaîne de caractères représentant l'action.
        -----------------------------------------------------------
        Returns the string representing the action.
        """
        return f"ClickLeft : {self.pos_x} | {self.pos_y}"


    def action_type(self) -> str:
        """
        Cette fonction retourne le type de cette action 
        sous forme de chaîne de caractères.
        ------------------------------------------------
        Returns the type of this action as a string.
        """
        return ActionType.CLICK_LEFT.value





class ClickRight(Action):
    """
    Cette classe permet d'effectuer un clic droit à un certain endroit.
    --------------------------------------------------------------------
    This class performs a right click at a given position.
    """
    
    def __init__(self, pos_x:int, pos_y:int) -> None:
        """
        On prend la position à laquelle doit s'effectuer le clic.

        :param pos_x: La position x à laquelle doit s'effectuer le clic.
        :param pos_y: La position y à laquelle doit s'effectuer le clic.
        -----------------------------------------------------------------
        Initializes the click position.

        :param pos_x: x position where the click should occur.
        :param pos_y: y position where the click should occur.
        """
        self.pos_x = pos_x
        self.pos_y = pos_y


    def run(self) -> None:
        """
        On déplace la souris à la position choisie par l'utilisateur, 
        puis on effectue le clic.
        -----------------------------------------------------------------
        Moves the mouse to the chosen position, then performs the click.
        """
        mouse.position = (self.pos_x, self.pos_y)
        mouse.press(Button.right)
        mouse.release(Button.right)


    def text(self) -> str:
        """
        On retourne la chaîne de caractères représentant l'action.
        -----------------------------------------------------------
        Returns the string representing the action.
        """
        return f"ClickRight : {self.pos_x} | {self.pos_y}"


    def action_type(self) -> str:
        """
        Cette fonction retourne le type de cette action 
        sous forme de chaîne de caractères.
        ------------------------------------------------
        Returns the type of this action as a string.
        """
        return ActionType.CLICK_RIGHT.value



class Move(Action):
    """
    Cette classe permet de déplacer la souris à l'endroit choisi par 
    l'utilisateur ou de la déplacer d'une certaine distance dans une 
    direction choisie par l'utilisateur.
    ---------------------------------------------------------------------------
    This class moves the mouse to a chosen position or by a relative distance.
    """

    def __init__(self, pos_x:int, pos_y:int, move_type:str):
        """
        On prend la position à laquelle doit se déplacer la souris et le 
        type de déplacement.

        :param pos_x: La position x à laquelle doit se déplacer la souris 
            ou la distance à laquelle doit se déplacer la souris en x.
        :param pos_y: La position y à laquelle doit se déplacer la souris 
            ou la distance à laquelle doit se déplacer la souris en y.
        :param move_type: Le type de déplacement, soit absolute pour 
            déplacer la souris à une position précise, soit relative pour 
            déplacer la souris d'une certaine distance de sa position 
            initiale en x y.
        -------------------------------------------------------------------
        Initializes movement parameters.

        :param pos_x: x position or relative movement.
        :param pos_y: y position or relative movement.
        :param move_type: absolute or relative.
        """
        self.move_type = move_type
        self.pos_x = pos_x
        self.pos_y = pos_y


    def run(self):
        """
        On déplace la souris comme choisie par l'utilisateur.
        ------------------------------------------------------
        Moves the mouse as specified by the user.
        """
        if self.move_type is MovementType.ABSOLUTE:
            pydirectinput.moveRel(self.pos_x - mouse.position[0], self.pos_y - mouse.position[1])
        else:
            pydirectinput.moveRel(self.pos_x, self.pos_y)


    def text(self):
        """
        On retourne la chaîne de caractères représentant l'action.
        -----------------------------------------------------------
        Returns the string representing the action.
        """
        if self.move_type is MovementType.ABSOLUTE:
            return f"Absolute : {self.pos_x} | {self.pos_y}"
        else:
            return f"Relative : {self.pos_x} | {self.pos_y}"

    def action_type(self):
        """
        Cette fonction retourne le type de cette action 
        sous forme de chaîne de caractères.
        ------------------------------------------------
        Returns the type of this action as a string.
        """
        return ActionType.MOVE.value



class Write(Action):
    """
    Cette classe permet de faire écrire un 
    texte choisi par l'utilisateur.
    ---------------------------------------
    This class types a user-defined text.
    """

    def __init__(self, payload_text:str) -> None:
        """
        On prend en paramètre le texte que l'utilisateur 
        souhaite faire écrire.

        :param payload_text: le texte que l'utilisateur 
            souhaite faire écrire.
        -------------------------------------------------
        Initializes the text to write.

        :param payload_text: The text to type.
        """
        self.payload_text = payload_text


    def run(self) -> None:
        """
        On fait écrire le texte que l'utilisateur a choisi.
        ----------------------------------------------------
        Types the chosen text.
        """
        keyboard.type(self.payload_text)


    def text(self) -> str:
        """
        On retourne la chaîne de caractères représentant l'action.
        -----------------------------------------------------------
        Returns the string representing the action.
        """
        if len(self.payload_text)>7:
            return f"Write : {self.payload_text[:5]}.."
        else:
            return f"Write : {self.payload_text}"


    def action_type(self) -> str:
        """
        Cette fonction retourne le type de cette 
        action sous forme de chaîne de caractères.
        ---------------------------------------------
        Returns the type of this action as a string.
        """
        return ActionType.WRITE.value



class Scroll(Action):
    """
    Cette classe permet de faire défiler (scroller).
    -------------------------------------------------
    This class performs scrolling.
    """

    def __init__(self, step:int, direction:str) -> None:
        """
        Initialisation des paramètres nécessaires au scroll de la souris.
        
        :param step: Le nombre de pas que l'utilisateur souhaite scroller.
        :param direction: La direction dans laquelle l'utilisateur 
            souhaite scroller.
        -------------------------------------------------------------------
        Initializes scrolling parameters.

        :param step: Number of scroll steps.
        :param direction: Scroll direction.
        """
        self.step = step
        self.direction = direction


    def run(self) -> None:
        """
        On fait défiler le nombre de pas choisi par l'utilisateur dans la 
        direction qu'il a choisie.
        -------------------------------------------------------------------
        Scrolls in the chosen direction for the specified number of steps.
        """

        match self.direction:
            case Direction.UP:
                mouse.scroll(0, self.step)
            case Direction.LEFT:
                mouse.scroll(self.step*-1, 0)
            case Direction.RIGHT:
                mouse.scroll(1, self.step)
            case Direction.DOWN:
                mouse.scroll(0, self.step*-1)


    def text(self) -> str:
        """
        On retourne la chaîne de caractères représentant l'action.
        -----------------------------------------------------------
        Returns the string representing the action.
        """
        return f"Scroll : {self.direction.value} | {self.step}"


    def action_type(self) -> str:
        """
        Cette fonction retourne le type de cette 
        action sous forme de chaîne de caractères.
        ---------------------------------------------
        Returns the type of this action as a string.
        """
        return ActionType.SCROLL.value



class Wait(Action):
    """
    Cette classe permet d'attendre entre deux actions.
    ---------------------------------------------------
    This class introduces a delay between actions.
    """
    
    def __init__(self, time_wait:float) -> None:
        """
        Initialisation des paramètres nécessaires 
        à la création d'un temps d'attente.

        :param time_wait: Le temps que l'utilisateur souhaite 
            attendre entre deux actions, en secondes.
        ------------------------------------------------------
        Initializes wait duration.

        :param time_wait: Wait time in seconds.
        """
        # On multiplie le temps d'attente par 1000 
        # car il est de base compté en millisecondes.
        # --------------------------------------------
        # Multiply the wait time by 1000 because 
        # it is internally handled in milliseconds.
        self.time_wait_ms = int(time_wait*1000)
        # On stocke aussi le temps d'attente en secondes 
        # pour pouvoir l'afficher dans text().
        # -----------------------------------------------
        # Also store the wait time in seconds so it can 
        # be displayed in text().
        self.time_wait_s = time_wait


    def run(self) -> int:
        """
        On retourne le temps d'attente pendant lequel le programme doit 
        suspendre l'exécution de la suite d'actions avant de la reprendre.
        -------------------------------------------------------------------
        Returns the wait duration during which execution should be paused.
        """
        return self.time_wait_ms


    def text(self) -> str:
        """
        On retourne la chaîne de caractères représentant l'action.
        -----------------------------------------------------------
        Returns the string representing the action.
        """
        return f"Wait : {self.time_wait_s}s"


    def action_type(self) -> str:
        """
        Cette fonction retourne le type de cette action 
        sous forme de chaîne de caractères.
        ------------------------------------------------
        Returns the type of this action as a string.
        """
        return ActionType.WAIT.value



class Loop(Action):
    """
    Cette classe permet d'exécuter une suite 
    d'actions un certain nombre de fois d'affilée.
    -----------------------------------------------
    This class allows executing a sequence of 
    actions a specified number of times in a row.
    """

    def __init__(self, window: tk.Tk, nb_turns:int, name:str) -> None:
        """ 
        Initialisation des paramètres nécessaires au fonctionnement 
        de la boucle.

        :param window: La fenêtre de l'interface, nécessaire pour 
            pouvoir appeler des fonctions après un certain temps 
            sans bloquer l'exécution du programme.
        :param nb_turns: Le nombre d'exécutions que la boucle doit 
            effectuer avec la suite d'actions.
        :param name: Le nom de la boucle.
        ---------------------------------------------------------------
        Initializes the parameters required for the loop to function.

        :param window: The UI window, required to call functions after 
            a delay without blocking program execution.
        :param nb_turns: The number of times the loop should execute 
            the action sequence.
        :param name: The name of the loop.
        """

        # On stocke la fenêtre principale.
        # ---------------------------------
        # Store the main window.
        self.window = window

        # On stocke le nom de la boucle pour pouvoir l'afficher dans text.
        # -----------------------------------------------------------------
        # Store the loop name to display it in text.
        self.name = name
        # Le nombre de tours.
        # ----------------------
        # Number of iterations.
        self.nb_turns = nb_turns
        # On crée une variable turn_counter qui va s'incrémenter à 
        # chaque tour de boucle jusqu'à atteindre le nombre demandé.
        # -----------------------------------------------------------
        # Counter that increments on each loop iteration until 
        # reaching the target.
        self.turn_counter = 0

        # Identifiant de la tâche asynchrone en cours.
        # ---------------------------------------------
        # Identifier of the current asynchronous task.
        self.scheduled_task_id = None

        # Dictionnaire qui va contenir les actions.
        # ------------------------------------------
        # Dictionary that will contain the actions.
        self.container_actions_dict: Dict[int, Action] = {}
        # Clé pour le dictionnaire des actions.
        # --------------------------------------
        # Key for the action dictionary.
        self.next_container_action_index = 0
        # Variable servant à savoir quelle action est en cours d'exécution
        # et si la boucle a fini son exécution.
        # -----------------------------------------------------------------
        # Variable used to track which action is currently executing
        # and whether the loop has finished execution.
        self.current_container_action_index  = 0

        # Dictionnaire qui va contenir tous les Checkbutton des actions 
        # contenues dans cette boucle dans l'arbre des actions.
        # --------------------------------------------------------------
        # Dictionary that will contain all Checkbuttons for actions 
        # in this loop within the action tree.
        self.container_action_checkbuttons = {}
        # Clé pour le dictionnaire container_action_checkbuttons.
        # --------------------------------------------------------
        # Key for container_action_checkbuttons.
        self.tree_container_idx = 0


    def add_action(self, inst_act: Action) -> None:
        """
        On prend l'instance de l'action en paramètre et on l'ajoute au 
        dictionnaire d'actions de la boucle container_actions_dict avec 
        pour clé next_container_action_index, puis on incrémente 
        next_container_action_index.

        :param inst_act: l'instance de L'action à ajouter à la suite 
            d'actions de la boucle.
        ----------------------------------------------------------------
        Takes an action instance as parameter and adds it to the loop 
        action dictionary container_actions_dict with key 
        next_container_action_index, then increments 
        next_container_action_index.

        :param inst_act: The action instance to add to the loop 
            action sequence.
        """

        self.container_actions_dict[self.next_container_action_index] = inst_act
        self.next_container_action_index += 1


    def add_action_container_tree(self, text: str, ui_action_tree: TreeUI, spacing: int) -> None:
        """
        Cette fonction permet d'ajouter à l'arbre les actions qui se 
        trouvent dans cette boucle avec l'incrémentation correspondante.

        :param text: La chaîne de caractères représentant l'action qui a 
            été ajoutée à la boucle.
        :param ui_action_tree: L'instance de la classe TreeUI qui nous 
            permet d'avoir accès à la frame (all_actions) dans laquelle 
            nous devons ajouter le Checkbutton.
        :param spacing: L'incrémentation à laquelle doit être positionné 
            le Checkbutton.
        ---------------------------------------------------------------------
        Adds the actions contained in this loop to the tree 
        with the appropriate indentation.

        :param text: The string representing the action added to the loop.
        :param ui_action_tree: Instance of TreeUI giving access to the frame 
            (all_actions) where the Checkbutton must be added.
        :param spacing: The indentation level for the Checkbutton.
        """

        # On crée la variable is_checked_act qui permettra de savoir 
        # si le Checkbutton est coché ou non.
        # -----------------------------------------------------------
        # Variable used to track whether the Checkbutton is checked.
        is_checked_act = tk.IntVar(value=1)
        # On crée le Checkbutton et on l'affiche dans all_actions avec 
        # l'incrémentation.
        # --------------------------------------------------------------------
        # Create and display the Checkbutton in all_actions with indentation.
        ChkBt_act = tk.Checkbutton(
            ui_action_tree.all_actions.scrollable_frame, 
            text=text, 
            variable=is_checked_act, 
            bg=W_VAR.NEUTRAL_700,
            fg=W_VAR.TEXT_COLOR,
            font=W_VAR.little_font_size,
            activebackground=W_VAR.NEUTRAL_800,
            activeforeground=W_VAR.TEXT_COLOR,
            selectcolor=W_VAR.NEUTRAL_700
            )
        ChkBt_act.grid(row=ui_action_tree.next_checkbutton_row+1, column=0, sticky="wn", padx=spacing)

        # On ajoute au dictionnaire qui va contenir tous les Checkbutton 
        # de la boucle (container_action_checkbuttons), une liste comportant 
        # en premier is_checked_act, puis le Checkbutton. 
        # Cette liste a pour clé tree_container_idx.
        # -------------------------------------------------------------------
        # Add to the dictionary that will store all Checkbuttons 
        # of the loop (container_action_checkbuttons), a list containing 
        # first is_checked_act, then the Checkbutton.
        # This list uses tree_container_idx as its key.
        self.container_action_checkbuttons[self.tree_container_idx] = [is_checked_act, ChkBt_act]

        # On incrémente la clé tree_container_idx.
        # -----------------------------------------
        # Increment the key tree_container_idx.
        self.tree_container_idx += 1
        # On incrémente la ligne où se trouvera la prochaine action 
        # (next_checkbutton_row).
        # -----------------------------------------------------------
        # Increment the row where the next action will be placed 
        # (next_checkbutton_row).
        ui_action_tree.next_checkbutton_row += 1


    def cancel_task(self) -> None:
        """
        Cette fonction permet de stopper l'exécution de la suite d'actions 
        en cours. Elle est appelée soit par une instance de KeyLoggerApp, 
        soit par le conteneur dans lequel elle se trouve soit par 
        ActionManager.

        - Si la dernière action appelée est une instance de KeyPress,
          on relâche les touches pressées.
        - Si la dernière action appelée est un conteneur, on arrête 
          son exécution via cancel_task (il appliquera la même logique).
        - Si une fonction qui a été appelée avec window.after (par exemple, 
          pour "wait", on utilise "window.after"), on annule l'appel.
        - On réinitialise les variables d'état de l'exécution.
        ----------------------------------------------------------------------
        This function stops the execution of the current sequence of actions.
        It can be called either by a KeyLoggerApp instance, by the container
        in which it is located, or by ActionManager.

        - If the last executed action is a KeyPress instance,
        the pressed keys are released.
        - If the last executed action is a container, its execution 
          is stopped via cancel_task (it will apply the same logic).
        - If a function was scheduled with window.after (for example,
        "wait" uses window.after), the call is canceled.
        - Execution state variables are reset.
        """

        if self.current_container_action_index > 0:
            # Si la dernière action appelée est une instance de KeyPress,
            # on relâche les touches pressées.
            # ------------------------------------------------------------
            # If the last executed action is a KeyPress instance,
            # release the pressed keys.
            if isinstance(self.container_actions_dict[self.current_container_action_index-1], KeyPress):
                self.container_actions_dict[self.current_container_action_index-1].release_keys()

            # Si la dernière action appelée est un conteneur, on arrête 
            # son exécution via cancel_task (il appliquera la même logique).
            # ---------------------------------------------------------------
            # If the last executed action is a container,
            # stop its execution via cancel_task (same logic applies).
            elif isinstance(self.container_actions_dict[self.current_container_action_index-1], ParallelActions) or isinstance(self.container_actions_dict[self.current_container_action_index-1], Loop):
                self.container_actions_dict[self.current_container_action_index-1].cancel_task()


        # Si une fonction qui a été appelée avec window.after (par exemple, 
        # pour wait, on utilise window.after), on annule l'appel.
        # ------------------------------------------------------------------
        # If a function was scheduled with window.after (e.g. for wait),
        # cancel the scheduled call.
        if self.scheduled_task_id is not None:
            self.window.after_cancel(self.scheduled_task_id)
            self.scheduled_task_id = None

        # On réinitialise les variables d'état de l'exécution.
        # -----------------------------------------------------
        # Reset execution state variables.
        self.current_container_action_index = 0


    def run(self, advent_function: Callable[[None], None]=None, pause_between_actions: int=None) -> None:
        """
        Cette fonction, à chaque fois qu'elle est appelée, exécute un 
        tour de boucle. Si le nombre de tours requis a été atteint, 
        elle appelle advent_function afin de continuer l'exécution de 
        la suite d'actions.

        :param advent_function: La fonction qui a appelé cette fonction, 
            pour pouvoir l'appeler à la fin de l'exécution de la boucle et 
            continuer le reste de l'exécution de la suite d'actions après 
            cette boucle.
        :param pause_between_actions: Le temps d'attente entre chaque 
            action choisi par l'utilisateur.
        -------------------------------------------------------------------
        This function executes one loop iteration each time it is called.
        If the required number of iterations has been reached, it calls
        advent_function to continue executing the action sequence.

        :param advent_function: The function that called this one,
            used to resume execution after the loop ends.
        :param pause_between_actions: The delay between each action defined 
            by the user.
        """
        
        # Si advent_function n'est pas None, cela signifie que c'est la 
        # première fois que run est appelée, alors on stocke advent_function 
        # pour pouvoir l'utiliser à la fin et pause_between_actions pour 
        # mettre une pause entre chaque action de la boucle.
        # --------------------------------------------------------------------
        # If advent_function is not None, this is the first call,
        # so we store it along with pause_between_actions.
        if not advent_function is None:
            self.advent_function = advent_function
            self.pause_between_actions = pause_between_actions

        # On vérifie si le nombre de tours requis n'a pas encore été atteint. 
        # Si c'est le cas, on appelle run_one_iteration pour exécuter un tour 
        # de boucle, et on incrémente turn_counter.
        # ---------------------------------------------------------------------
        # Check if the required number of iterations has not been reached yet.
        # If so, execute one loop iteration and increment turn_counter.
        if self.turn_counter < self.nb_turns:
            self.window.after(0, self.run_one_iteration)
            self.turn_counter += 1

        else:
            # Sinon, on a atteint le nombre de tours requis, alors 
            # on réinitialise turn_counter pour pouvoir reexecuter la 
            # boucle si besoin, et on appelle advent_function pour continuer 
            # l'exécution de la suite d'actions après la boucle.
            # ---------------------------------------------------------------
            # Otherwise, reset turn_counter and call advent_function
            # to continue execution after the loop.
            self.turn_counter = 0
            self.window.after(0, self.advent_function)


    def run_one_iteration(self):
        """
        Lance l'exécution d'un tour de boucle.
        Cette fonction s'appelle elle-même de manière asynchrone 
        pour exécuter chaque action de la boucle l'une après l'autre. 
        Afin de savoir l'action en cours d'exécution.
        On utilise la variable current_container_action_index qui est 
        incrémentée à chaque appel de cette fonction.
        Lorsqu'une action est un conteneur (Loop/ParallelActions), 
        on appelle la méthode run de ce conteneur qui s'occupe de
        l'exécution des actions qu'il contient, puis quand il aura fini, 
        il va rappeler la fonction start_execution, et l'exécution de 
        la boucle reprendra là où elle s'était arrêtée.
        -------------------------------------------------------------------
        Starts execution of one loop iteration.
        This function calls itself asynchronously to execute each action
        in sequence.
        The current action is tracked using current_container_action_index,
        which is incremented at each call.
        If an action is a container (Loop/ParallelActions),
        its run method is called. Once finished, it calls back
        the execution function, and the loop resumes where it stopped.
        """

        # On vérifie que toutes les actions n'ont pas déjà été exécutées
        # et que les touches d'arrêt n'ont pas été pressées pour 
        # arrêter l'exécution de la suite d'actions.
        # ---------------------------------------------------------------
        # Check that not all actions have already been executed
        # and that stop keys have not been pressed.
        if self.current_container_action_index >= self.next_container_action_index or KeyLoggerApp.stop_run:
            # On a exécuté chaque action ou l'exécution a été arrêtée, 
            # alors on met current_container_action_index à 0 pour refaire 
            # un tour si besoin. Puis, on appelle "run", qui va soit refaire 
            # un tour de boucle, soit appeler la fonction qui l'a 
            # initialement appelée.
            # ---------------------------------------------------------------
            # All actions executed or execution stopped → reset counter
            # and trigger next loop iteration or continuation.
            self.current_container_action_index = 0
            self.window.after(0, self.run)
        else:
            # On incrémente current_container_action_index 
            # car on va exécuter l'action suivante.
            # -------------------------------------------------
            # We increment current_container_action_index
            # because we are going to execute the next action.
            self.current_container_action_index += 1

            # On regarde si l'action que l'on doit exécuter n'a 
            # pas été désactivéepar l'utilisateur dans l'arborescence.
            # ---------------------------------------------------------
            # Check if the current action is disabled by the user.
            if list(self.container_action_checkbuttons[self.current_container_action_index-1])[0].get() == 0:
                # On passe à l'action suivante car celle-ci a été désactivée.
                # ------------------------------------------------------------
                # Skip disabled action.
                self.window.after(self.pause_between_actions, self.run_one_iteration)

            else:
                # Si l'action est un conteneur, on appelle sa méthode 
                # d'exécution.
                # ------------------------------------------------------------
                # If the action is a container, we call its execution method.
                if isinstance(self.container_actions_dict[self.current_container_action_index-1], Loop) or isinstance(self.container_actions_dict[self.current_container_action_index-1], ParallelActions):
                    # On donne à run la fonction run_one_iteration pour 
                    # qu'elle puisse rappeler la fonction run_one_iteration 
                    # une fois qu'elle a fini d'exécuter les actions qu'elle 
                    # contient et on donne aussi le temps de pause entre 
                    # chaque action.
                    # -------------------------------------------------------
                    # We pass the run_one_iteration function to run so that 
                    # it can call the run_one_iteration function again once 
                    # it has finished executing the actionsit contains, and 
                    # we also pass the pause time between each action.
                    self.window.after(0, lambda : self.container_actions_dict[self.current_container_action_index-1].run(self.run_one_iteration, self.pause_between_actions))
                
                else:
                    # Si l'action n'est pas un conteneur, on exécute l'action.
                    # On récupère le temps à attendre avant d'appeler l'action 
                    # suivante qu'elle retourne si elle en a un.
                    # ---------------------------------------------------------
                    # If the action is not a container, we execute the action.
                    # We retrieve the time to wait before calling the 
                    # next action that it returns if it has one.
                    time = self.container_actions_dict[self.current_container_action_index-1].run()

                    # Garde pour éviter les accès invalides après un arrêt.
                    # Empêche les bugs causés par la remise à zéro de 
                    # current_container_action_index, qui sert de clé pour 
                    # le dictionnaire.
                    # -------------------------------------------------------
                    # Guard to prevent invalid accesses after a stop.
                    # Prevents bugs caused by resetting 
                    # current_container_action_index, which is used as a key 
                    # for the dictionary.
                    if self.current_container_action_index <= 0: 
                        return
                    
                    # On regarde si l'action que l'on vient d'exécuter était 
                    # KeyPress pour pouvoir appeler call_release_keys après 
                    # le temps d'attente choisi par l'utilisateur.
                    # -------------------------------------------------------
                    # We check if the action that has just been executed was 
                    # a KeyPress in order to call call_release_keys after 
                    # the waiting time chosen by the user.
                    if isinstance(self.container_actions_dict[self.current_container_action_index-1], KeyPress):
                        self.scheduled_task_id = self.window.after(time, self.call_release_keys)

                    # On regarde si l'action que l'on vient d'exécuter était 
                    # Wait pour pouvoir rappeler run_one_iteration après le 
                    # temps d'attente choisi par l'utilisateur.
                    # -------------------------------------------------------
                    # We check if the action that has just been executed was 
                    # a Wait in order to call run_one_iteration again after 
                    # the waiting time chosen by the user.
                    elif isinstance(self.container_actions_dict[self.current_container_action_index-1], Wait):
                        self.scheduled_task_id = self.window.after(time+self.pause_between_actions, self.run_one_iteration)
                    
                    else:
                        # L'action que nous venons d'appeler ne nécessite 
                        # pas de temps d'attente, alors nous appelons 
                        # run_one_iteration pour exécuter l'action suivante.
                        # ---------------------------------------------------
                        # The action that we have just called does not 
                        # require any waiting time, so we call 
                        # run_one_iteration to execute the next action.
                        self.window.after(self.pause_between_actions, self.run_one_iteration)


    def call_release_keys(self) -> None:
        """
        Cette fonction appelle release_keys pour KeyPress afin de relâcher 
        les touches précédemment pressées, puis on appelle run_one_iteration 
        pour exécuter l'action d'après dans la boucle.
        ----------------------------------------------------------------------
        This function calls release_keys for KeyPress in order to release 
        the keys that were previously pressed, then calls run_one_iteration 
        to execute the next action in the loop.
        """
        self.container_actions_dict[self.current_container_action_index-1].release_keys()
        self.window.after(self.pause_between_actions, self.run_one_iteration)


    def text(self) -> str:
        """
        On retourne la chaîne de caractères représentant l'action.
        -----------------------------------------------------------
        Returns the string representing the action.
        """
        return f"Loop : {self.nb_turns} | {self.name}"


    def action_type(self) -> str:
        """
        Cette fonction retourne le type de cette action 
        sous forme de chaîne de caractères.
        ------------------------------------------------
        Returns the type of this action as a string.
        """
        return ActionType.LOOP.value






class ParallelActions(Action):
    """
    Cette classe permet d'exécuter une suite d'actions en 
    même temps qu'une ou plusieurs touches sont pressées.
    ------------------------------------------------------
    This class allows executing a sequence of actions 
    while one or more keys are pressed simultaneously.
    """

    def __init__(self, window: tk.Tk, keys:str, special_keys:list, name:str) -> None:
        """
        Initialisation des paramètres nécessaires au 
        fonctionnement des actions simultanées.

        :param window: La fenêtre de l'interface, nécessaire pour pouvoir 
            appeler des fonctions après un certain temps sans bloquer 
            l'exécution du programme.
        :param keys: Une chaîne de caractères contenant les touches 
            normales à presser pendant l'exécution de la suite d'actions.
        :param special_keys: Une liste de touches spéciales à presser 
            pendant l'exécution de la suite d'actions.
        :param name: Le nom de la suite d'actions simultanées.
        ----------------------------------------------------------------------
        Initializes the parameters required for running simultaneous actions.

        :param window: The interface window, required to call functions
            after a certain delay without blocking program execution.
        :param keys: A string containing the normal keys to press during 
            the execution of the action sequence.
        :param special_keys: A list of special keys to press during the 
            execution of the action sequence.
        :param name: The name of the simultaneous action sequence.
        """

        # On stocke la fenêtre principale.
        # ---------------------------------
        # Store the main window.
        self.window = window

        # On supprime les caractères en double de la chaîne de 
        # caractères qui contient toutes les touches normales (keys).
        # ------------------------------------------------------------
        # Remove duplicate characters from the string containing
        # all normal keys (keys).
        self.keys = "".join(list(set(keys)))

        # On stocke les touches spéciales.
        # ---------------------------------
        # Store the special keys.
        self.special_keys = special_keys

        # On crée une liste de chaînes de caractères contenant les noms 
        # des touches spéciales à partir de la liste de touches spéciales 
        # donnée en paramètre, pour pouvoir les afficher dans text.
        # ------------------------------------------------------------------
        # Create a list of strings containing the names of the special keys
        # from the list of special keys passed as a parameter, so they 
        # can be displayed in text.
        special_key_labels = []
        for sp_key in self.special_keys:
            special_key_labels.append(sp_key.value)
        # On trie les noms des touches spéciales par ordre de taille 
        # pour la fonction text.
        # ------------------------------------------------------------
        # Sort the special key names by length for the text function.
        self.special_key_labels = sorted(special_key_labels, key=lambda x: len(x), reverse=False)

        # On stocke le nom de la suite d'actions simultanées pour 
        # pouvoir l'afficher dans text.
        # ---------------------------------------------------------
        # Store the name of the simultaneous action sequence so it 
        # can be displayed in text.
        self.name = name

        # Dictionnaire qui va contenir les actions.
        # ------------------------------------------
        # Dictionary that will contain the actions.
        self.container_actions_dict: Dict[int, Action] = {}
        # Clé pour le dictionnaire des actions.
        # --------------------------------------
        # Key for the actions dictionary.
        self.next_container_action_index = 0
        # Variable servant à savoir quelle action est en cours 
        # d'exécution et si la suite d'actions des actions 
        # simultanées a fini son exécution.
        # -----------------------------------------------------
        # Variable used to track which action is currently 
        # being executed and whether the sequence of actions 
        # has finished executing.
        self.current_container_action_index = 0

        # Identifiant de la tâche asynchrone en cours.
        # ---------------------------------------------
        # Identifier of the current asynchronous task.
        self.scheduled_task_id = None

        # On crée finished_running, qui va permettre à run de 
        # savoir si la liste d'actions a déjà été exécutée.
        # ----------------------------------------------------
        # Create finished_running, which allows run to know 
        # if the action list has already been executed.
        self.finished_running = False

        # Dictionnaire qui va contenir tous les Checkbutton des action 
        # contenues dans ce conteneur dans l'arbre des actions.
        # -------------------------------------------------------------
        # Dictionary that will contain all Checkbuttons of the actions
        # within this container in the action tree.
        self.container_action_checkbuttons = {}
        # Clé pour le dictionnaire container_action_checkbuttons.
        # --------------------------------------------------------
        # Key for the container_action_checkbuttons dictionary.
        self.tree_container_idx = 0


    def add_action(self, instance: Action) -> None:
        """
        On prend l'instance de l'action en paramètre et on l'ajoute 
        au dictionnaire d'actions des actions paraleles 
        container_actions_dict avec pour clé next_container_action_index, 
        puis on incrémente next_container_action_index.

        :param inst_act: L'instance de l'action à ajouter à la 
            suite d'actions.
        --------------------------------------------------------------------
        Takes an action instance as a parameter and adds it to 
        the dictionary of parallel actions (container_actions_dict) 
        using next_container_action_index as the key,
        then increments next_container_action_index.

        :param inst_act: The action instance to add to the action sequence.
        """

        self.container_actions_dict[self.next_container_action_index] = instance
        self.next_container_action_index += 1



    def add_action_container_tree(self, text: str, ui_action_tree: TreeUI, spacing: int) -> None:
        """
        Cette fonction permet d'ajouter à l'arbre les actions qui se 
        trouvent dans ce conteneur avec l'incrémentation correspondante.

        :param text: La chaîne de caractères représentant l'action qui 
            a été ajoutée à ce conteneur.
        :param ui_action_tree: L'instance de la classe TreeUI qui nous 
            permet d'avoir accès à la frame (all_actions) dans laquelle 
            nous devons ajouter le Checkbutton.
        :param spacing: L'incrémentation à laquelle doit être positionné 
            le Checkbutton.
        --------------------------------------------------------------------
        This function adds the actions contained in this container
        to the tree with the corresponding indentation.

        :param text: The string representing the action added 
            to this container.
        :param ui_action_tree: The TreeUI instance that gives access to the
            frame (all_actions) where the Checkbutton must be added.
        :param spacing: The indentation level where the Checkbutton 
            should be placed.
        """

        # On crée la variable is_checked_act qui permettra 
        # de savoir si le Checkbutton est coché ou non. 
        # -------------------------------------------------
        # Create the is_checked_act variable to determine 
        # whether the Checkbutton is checked or not.
        is_checked_act = tk.IntVar(value=1)
        # On crée le Checkbutton et on l'affiche dans 
        # all_actions avec l'incrémentation.
        # --------------------------------------------
        # Create the Checkbutton and display it in 
        # all_actions with indentation.
        ChkBt_act = tk.Checkbutton(
            ui_action_tree.all_actions.scrollable_frame, 
            text=text, 
            variable=is_checked_act, 
            bg=W_VAR.NEUTRAL_700,
            fg=W_VAR.TEXT_COLOR,
            font=W_VAR.little_font_size,
            activebackground=W_VAR.NEUTRAL_800,
            activeforeground=W_VAR.TEXT_COLOR,
            selectcolor=W_VAR.NEUTRAL_700
            )
        ChkBt_act.grid(row=ui_action_tree.next_checkbutton_row+1, column=0, sticky="wn", padx=spacing)

        # On ajoute au dictionnaire qui va contenir tous les Checkbutton 
        # des actions paraleles (container_action_checkbuttons), 
        # une liste comportant en premier is_checked_act, et le Checkbutton 
        # cette liste a pour clé tree_container_idx.
        # ------------------------------------------------------------------
        # Add to the dictionary containing all Checkbuttons of parallel 
        # actions (container_action_checkbuttons), a list where the first 
        # element is is_checked_act and the second is the Checkbutton.
        # This list is stored with tree_container_idx as the key.
        self.container_action_checkbuttons[self.tree_container_idx] = [is_checked_act, ChkBt_act]

        # On incrémente la clé tree_container_idx.
        # -----------------------------------------
        # Increment the key tree_container_idx.
        self.tree_container_idx += 1
        # On incrémente la ligne où se trouvera la 
        # prochaine action (next_checkbutton_row).
        # -----------------------------------------
        # Increment the row where the next action 
        # will be placed (next_checkbutton_row).
        ui_action_tree.next_checkbutton_row += 1



    def cancel_task(self) -> None:
        """
        Cette fonction permet de stopper l'exécution de la suite 
        d'actions en cours. Elle est appelée soit par une instance 
        de KeyLoggerApp, soit par le conteneur dans lequel elle se 
        trouve soit par ActionManager.

        - Si la dernière action appelée est une instance de KeyPress,
          on relâche les touches pressées.
        - Si la dernière action appelée est un conteneur,
          on arrête son exécution via cancel_task 
          (il appliquera la même logique).
        - Si une fonction qui a été appelée avec window.after (par exemple, 
          pour "wait", on utilise "window.after"), on annule l'appel.
        - On réinitialise les variables d'état de l'exécution.
        ---------------------------------------------------------------------
        Stops the execution of the current action sequence.
        It can be called by a KeyLoggerApp instance, the parent container,
        or the ActionManager.

        - If the last executed action is a KeyPress instance,
          release the pressed keys.
        - If the last executed action is a container,
          stop its execution via cancel_task (it will apply the same logic).
        - If a function was scheduled using window.after (e.g., for "wait"),
          cancel that call.
        - Reset the execution state variables.
        """

        if self.current_container_action_index > 0:
            # Si la dernière action appelée est une instance de KeyPress,
            # on relâche les touches pressées.
            # ------------------------------------------------------------
            # If the last executed action is a KeyPress instance,
            # release the pressed keys.
            if isinstance(self.container_actions_dict[self.current_container_action_index-1], KeyPress):
                self.container_actions_dict[self.current_container_action_index-1].release_keys()

            # Si la dernière action appelée est un conteneur,
            # on arrête son exécution via cancel_task (il appliquera la même logique).
            # -------------------------------------------------------------------------
            # If the last executed action is a container,
            # stop its execution via cancel_task (it will apply the same logic).
            elif isinstance(self.container_actions_dict[self.current_container_action_index-1], ParallelActions) or isinstance(self.container_actions_dict[self.current_container_action_index-1], Loop):
                self.container_actions_dict[self.current_container_action_index-1].cancel_task()


        # Si une fonction qui a été appelée avec window.after (par exemple, 
        # pour "wait", on utilise "window.after"), on annule l'appel.
        # ------------------------------------------------------------------
        # If a function was scheduled with window.after (e.g., for "wait"),
        # cancel the call.
        if self.scheduled_task_id is not None:
            self.window.after_cancel(self.scheduled_task_id)
            self.scheduled_task_id = None

        # On réinitialise les variables d'état de l'exécution. 
        # -----------------------------------------------------
        # Reset execution state variables.
        self.current_container_action_index = 0




    def run(self, advent_function=None, pause_between_actions=None) -> None:
        """
        Cette fonction va lancer l'appui des touches choisies par 
        l'utilisateur, puis exécuter les actions de la suite, puis à la 
        fin de la suite d'actions, elle va relâcher les touches et appeler 
        la fonction qui l'a initialement appelée pour continuer l'exécution 
        de la suite d'actions après les actions simultanées.

        :param advent_function: La fonction qui a appelé cette fonction, 
            pour pouvoir l'appeler à la fin de l'exécution de la suite 
            d'actions, et continuer l'exécution de la suite d'actions 
            après les actions simultanées.
        :param pause_between_actions: Le temps d'attente entre chaque 
            action choisi par l'utilisateur.
        --------------------------------------------------------------------
        This function presses the selected keys,
        executes the sequence of actions, then at the end,
        releases the keys and calls the function that originally invoked it
        to continue execution after the parallel actions.

        :param advent_function: The function that called this one, 
            so it can becalled again after the sequence finishes.
        :param pause_between_actions: The delay between each action 
            chosen by the user.
        """

        # Si advent_function n'est pas None, cela signifie 
        # que c'est la première fois que run est appelée.
        # -------------------------------------------------
        # If advent_function is not None, it means this 
        # is the first call to run.
        if not advent_function is None:
            # On stocke advent_function pour pouvoir l'utiliser à la fin 
            # et pause_between_actions pour mettre une pause entre chaque 
            # action de la suite d'actions simultanées.
            # ---------------------------------------------------------------
            # Store advent_function and pause_between_actions for later use.
            self.advent_function = advent_function
            self.pause_between_actions = pause_between_actions

        # On vérifie si la suite d'actions a déjà été exécutée.
        # --------------------------------------------------------
        # Check if the action sequence has already been executed.
        if self.finished_running:
            # On relâche les touches appuyées.
            # ---------------------------------
            # Release pressed keys.
            release_keys(self.special_keys, self.keys)
            # On appelle advent_function pour continuer l'exécution 
            # de la suite d'actions après les actions simultanées.
            # ------------------------------------------------------
            # Call advent_function to continue execution.
            self.window.after(self.pause_between_actions, self.advent_function)
            # On remet finished_running à False pour la 
            # prochaine fois que run sera appelée.
            # ------------------------------------------
            # Reset finished_running for the next call.
            self.finished_running = False
        else:
            print("sfijgiuorfojgvojfnvoj")
            # Sinon, on appuie sur les touches choisies par l'utilisateur, 
            # et on appelle run_action pour exécuter la suite d'actions.
            # -------------------------------------------------------------
            # Otherwise, press keys and start executing actions.
            press_keys(self.special_keys, self.keys)
            self.window.after(0, self.run_action)



    def run_action(self):
        """
        Lance l'exécution des actions du conteneur.
        Cette fonction s'appelle elle-même de manière asynchrone pour 
        exécuter chaqueaction de la suite l'une après l'autre. 
        Afin de savoir l'action en cours d'exécution, on utilise la variable 
        current_container_action_index qui est incrémentée à chaque appel 
        de cette fonction.
        Lorsqu'une action est un conteneur (Loop/ParallelActions), 
        on appelle la méthode run de ce conteneur qui s'occupe de 
        l'exécution des actions qu'il contient, puis quand il aura fini, 
        il va rappeler la fonction start_execution, et l'exécution de 
        ParallelActions reprendra là où elle s'était arrêtée.
        ----------------------------------------------------------------------
        Starts the execution of the container's actions.
        This function calls itself asynchronously in order to execute each
        action in the sequence one after the other. To keep track of the 
        action currently being executed, the variable 
        current_container_action_index is used and is incremented at each 
        call of this function.
        When an action is a container (Loop/ParallelActions), the method
        run of this container is called, which handles the execution of the 
        actions it contains, then when it has finished, it will call back the 
        start_execution function, and the execution of ParallelActions will 
        resume where it had stopped.
        """

        # On vérifie que toutes les actions n'ont pas déjà été exécutées
        # et que les touches d'arrêt n'ont pas été pressées pour 
        # arrêter l'exécution de la suite d'actions.
        # ---------------------------------------------------------------
        # Check that all actions have not already been executed
        # and that the stop keys have not been pressed to
        # stop the execution of the action sequence.
        if self.current_container_action_index >= self.next_container_action_index or KeyLoggerApp.stop_run:
            # On a exécuté chaque action ou l'exécution a été arrêtée, 
            # alors on met current_container_action_index à 0 
            # pour réexécuter ces actions si besoin. 
            # --------------------------------------------------------------
            # All actions have been executed or execution has been stopped,
            # so current_container_action_index is reset to 0 in order to 
            # execute them again if needed.
            self.current_container_action_index = 0
            # On met finished_running à True pour que run sache 
            # que la suite d'actions a déjà été exécutée.
            # ----------------------------------------------------
            # Set finished_running to True so that run knows 
            # that the action sequence has already been executed.
            self.finished_running = True
            # On appelle run, qui va appeler la 
            # fonction qui l'a initialement appelée.
            # ---------------------------------------
            # Call run, which will call the 
            # function that originally invoked it.
            self.window.after(0, self.run)
        else:
            # On incrémente current_container_action_index 
            # car on va exécuter l'action suivante.
            # -------------------------------------------------
            # Increment current_container_action_index 
            # because the next action is going to be executed.
            self.current_container_action_index += 1

            # On regarde si l'action que l'on doit exécuter n'a pas 
            # été désactivée par l'utilisateur dans l'arborescence.
            # ------------------------------------------------------
            # Check whether the action that is about to be executed 
            # has been disabled by the user in the tree structure.
            if list(self.container_action_checkbuttons[self.current_container_action_index-1])[0].get() == 0:
                # On passe à l'action suivante car celle-ci a été désactivée.
                # ------------------------------------------------------------
                # Skip to the next action because this one has been disabled.
                self.window.after(self.pause_between_actions, self.run_action)
            else:

                # Si l'action est un conteneur on 
                # appelle sa méthode d'exécution.
                # --------------------------------
                # If the action is a container, 
                # call its execution method.
                if isinstance(self.container_actions_dict[self.current_container_action_index-1], Loop) or isinstance(self.container_actions_dict[self.current_container_action_index-1], ParallelActions):
                    # On donne a run la fonction run_action pour quelle puisse 
                    # rappeler la fonction run_action une fois quelle a fini 
                    # d'executer les actions qu'elle contient et on donne 
                    # aussi le temps de pause entre chaque action.
                    # ---------------------------------------------------------
                    # Pass the run function to run_action so that it can
                    # call run_action again once it has finished executing 
                    # the actions it contains, and also pass the pause time 
                    # between each action.
                    self.window.after(0, lambda : self.container_actions_dict[self.current_container_action_index-1].run(self.run_action, self.pause_between_actions))
                    
                else:

                    # Si l'action n'est pas un conteneur on execute l'action
                    # On récupère le temps d'attente avant d'appeler l'action 
                    # suivante, qu'elle retourne si elle en a un.
                    # --------------------------------------------------------
                    # If the action is not a container, execute the action
                    # Retrieve the waiting time before calling the next 
                    # action, if it returns one.
                    time = self.container_actions_dict[self.current_container_action_index-1].run()

                    # Garde pour éviter les accès invalides après un arrêt.
                    # Empêche les bugs causés par la remise à zéro de 
                    # current_container_action_index, qui sert de clé 
                    # pour le dictionnaire.
                    # -------------------------------------------------------
                    # Guard to prevent invalid access after a stop.
                    # Prevents bugs caused by resetting 
                    # current_container_action_index, which is used as a key 
                    # for the dictionary.
                    if self.current_container_action_index <= 0: 
                        return

                    # On regarde si l'action que l'on vient d'exécuter 
                    # était KeyPress pour pouvoir appeler call_release_keys 
                    # après le temps d'attente choisi par l'utilisateur.
                    # ------------------------------------------------------
                    # Check whether the action that has just been executed
                    # was KeyPress in order to call call_release_keys after 
                    # the waiting time chosen by the user.
                    if isinstance(self.container_actions_dict[self.current_container_action_index-1], KeyPress):
                        self.scheduled_task_id = self.window.after(time, self.call_release_keys)

                    # On regarde si l'action que l'on vient d'exécuter 
                    # était Wait pour pouvoir rappeler run_action après 
                    # le temps d'attente choisi par l'utilisateur.
                    # -----------------------------------------------------
                    # Check whether the action that has just been executed 
                    # was Wait in order to call run_action again after the 
                    # waiting time chosen by the user.
                    elif isinstance(self.container_actions_dict[self.current_container_action_index-1], Wait):
                        self.scheduled_task_id = self.window.after(time+self.pause_between_actions, self.run_action)

                    else:
                        # L'action que nous venons d'appeler ne nécessite 
                        # pas de temps d'attente, alors nous appelons 
                        # run_action pour exécuter l'action suivante.
                        # -------------------------------------------------
                        # The action that has just been called does not 
                        # require any waiting time, so call run_action to 
                        # execute the next action.
                        self.window.after(self.pause_between_actions, self.run_action)


    def call_release_keys(self) -> None:
        """
        Cette fonction appelle release_keys pour KeyPress afin de relâcher 
        les touches précédemment pressées, puis on appelle run_action pour 
        exécuter l'action d'après.
        -------------------------------------------------------------------
        This function calls release_keys for KeyPress in order to release 
        the keys that were previously pressed, then calls run_action to 
        execute the next action.
        """
        self.container_actions_dict[self.current_container_action_index-1].release_keys()
        self.window.after(self.pause_between_actions, self.run_action)



    def text(self) -> str:
        """
        On retourne la chaîne de caractères représentant l'action.
        -----------------------------------------------------------
        Returns the string representing the action.
        """

        if len(self.keys)>5:
            if len(self.special_key_labels) > 1:
                return f"Parallel actions : {self.keys[:3]}.. | {self.special_key_labels[0]}.."
            elif len(self.special_key_labels) == 1:
                return f"Parallel actions : {self.keys[:3]}.. | {self.special_key_labels[0]}"
            else:
                return f"Parallel actions : {self.keys[:3]}.."

        elif len(self.keys) == 0:
            if len(self.special_key_labels) > 1:
                return f"Parallel actions : {self.special_key_labels[0]}.."
            elif len(self.special_key_labels) == 1:
                return f"Parallel actions : {self.special_key_labels[0]}"

        else:
            if len(self.special_key_labels) > 1:
                return f"Parallel actions : {self.keys} | {self.special_key_labels[0]}.."
            elif len(self.special_key_labels) == 1:
                return f"Parallel actions : {self.keys} | {self.special_key_labels[0]}"
            else:
                return f"Parallel actions : {self.keys}"


    def action_type(self) -> str:
        """
        Cette fonction retourne le type de cette 
        action sous forme de chaîne de caractères.
        ---------------------------------------------
        Returns the type of this action as a string.
        """
        return ActionType.PARALLEL_ACTIONS.value