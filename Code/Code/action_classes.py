import tkinter as tk
import pydirectinput

from ui_action_frames.enums import MovementType, Direction

from pynput.keyboard import Key, Controller
keyboard = Controller()

from pynput.mouse import Controller, Button
mouse = Controller()

from pynput import keyboard as my_keyboard




# On crée un dictionnaire qui, pour chaque touche spéciale ainsi que le clic droit et le clic gauche,
# contient l'élément pynput correspondant. Cela permet, lorsqu'on doit simuler un appui, de simplement
# donner la clé correspondante et le dictionnaire retourne l'élément adapté pour simuler l'appui.
# --------------------------------------------------------------------------------------------------------
# We create a dictionary that, for each special key as well as the right and left mouse clicks, 
# contains the corresponding pynput element. This allows, when simulating a key press, to simply 
# provide the corresponding key, and the dictionary returns the appropriate element to simulate the press.
SP_KEY_DICT = {
                "alt":Key.alt, "ctrl":Key.ctrl, "altgr":Key.alt_gr, "cmd":Key.cmd, 
                "esc":Key.esc, "delete":Key.delete, "shift":Key.shift, "tab":Key.tab, 
                "backspace":Key.backspace, "up":Key.up, "left":Key.left, "right":Key.right, 
                "down":Key.down, "caps lock":Key.caps_lock, "enter":Key.enter, "enter":Key.enter, 
                "click r":Button.right, "click l":Button.left
}



last_m_pos = (0, 0)



def position_mouse():
    global last_m_pos
    """
    Fonction qui retourne la position de la souris de l'utilisateur.
    ----------------------------------------------------------------
    Function that returns the user's mouse position.
    """
    m_pos = mouse.position
    if m_pos == None:
        return last_m_pos
    else:
        last_m_pos = m_pos
        return m_pos




class KeyPoisiton:
    """
    Cette classe permet de capturer la position de la souris de l'utilisateur dans
    "click right", "click left", "move" lorsque l'utilisateur clique simultanément 
    sur les touches "X" et "V" (ces touches peuvent être modifiées).
    ------------------------------------------------------------------------------
    This class allows entering the position of the user's mouse in "click right", 
    "click left", and in "move" when they click on "X" and "V" simultaneously 
    (these keys can be modified).
    """

    # Cette variable permet de savoir si nous sommes en train d'observer les 
    # touches pressées ou non.
    # -----------------------------------------------------------------------
    # This variable indicates whether we are currently monitoring the pressed 
    # keys or not.
    is_listening = False

    # Touche de base pour écrire la position.
    # ---------------------------------------
    # Default key to write the position.
    pos_key_sc = ["x", "v"]


    def __init__(self, set_coordinate_click, set_coordinate_move):
        """
        On prend en paramètre "set_coordinate", qui permet d'inscrire la position 
        de la souris dans "click right", "click left", et "move". 
        --------------------------------------------------------------------
        We take "set_coordinate" as a parameter, that allows us to record the mouse 
        position in "click right", "click left", and "move".
        """

        # On met "is_listening" à "True" pour indiquer que nous sommes 
        # en train d'observer les touches pressées.
        # ------------------------------------------------------------
        # We set "is_listening" to "True" to indicate that we are 
        # observing the pressed keys.
        KeyPoisiton.is_listening = True

        # On récupère la fonction qui permet d'inscrire la position 
        # de la souris dans "click right", "click left", et "move".
        # -----------------------------------------------------------
        # We retrieve the function that allows us to record the mouse 
        # position in "click right," "click left," and "move".
        self.set_coordinate_click = set_coordinate_click
        self.set_coordinate_move = set_coordinate_move

        # On crée un set qui contiendra les touches "x" et ou "v" lorsqu'elles sont pressées.
        # -----------------------------------------------------------------------------------
        # We create a set that will contain the keys "x" and/or "v" when they are pressed.
        self.key_pos = set()

        # On décide d'observer tous les appuis et les relâchements de touches.
        # --------------------------------------------------------------------
        # We decide to observe all key presses and releases.
        self.listener = my_keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )

        # On commence à observer.
        # -----------------------
        # We start to observe.
        self.listener.start()



    def on_press(self, key):
        """
        Cette fonction est appelée lorsque une touche est pressée. On commence par vérifier 
        si la touche est une touche spéciale. Sinon, on regarde si c'est une des touches 
        permettant d'écrire la position. Si c'est le cas, on l'ajoute au set "key_pos". 
        Ensuite, si le set comporte deux éléments, cela signifie que les deux touches sont 
        pressées. Dans ce cas, on appelle "set_coordinate" et on lui donne en paramètre la position 
        de la souris.
        ---------------------------------------------------------------------------------------
        This function is called when a key is pressed. We start by checking if the key is a 
        special key. If not, we check if it's one of the keys that allows writing the position. 
        If it is, we add it to the "key_pos" set. Then, if the set contains two elements, it 
        means that both keys are pressed. In this case, we call "set_coordinate" and pass the mouse 
        position as a parameter.
        """

        try:
            key_char = key.char
        except AttributeError:
            key_char = None
        
        if key_char in KeyPoisiton.pos_key_sc:
            self.key_pos.add(key_char)


        if len(self.key_pos) == len(KeyPoisiton.pos_key_sc):
            for element in KeyPoisiton.pos_key_sc:
                self.key_pos.remove(element)
            self.set_coordinate_click(mouse.position, "xy")
            self.set_coordinate_move(mouse.position, "xy")



    def on_release(self, key):
        """"
        Cette fonction est appelée lorsque une touche est relâchée. On commence par vérifier 
        si la touche est une touche spéciale. Sinon, on vérifie si c'est une des touches 
        permettant d'écrire la position. Si c'est le cas, on la retire du set "key_pos".
        ------------------------------------------------------------------------------------
        This function is called when a key is released. We start by checking if the key is 
        a special key. If not, we check if it's one of the keys that allows writing the 
        position. If it is, we remove it from the "key_pos" set.
        """
    
        try:
            key_char = key.char

        except AttributeError:
            key_char = None
        
        if key_char in self.key_pos:
            self.key_pos.remove(key_char)





    def stop_listening(self):
        """
        Cette fonction permet d'arrêter d'observer les pressions et les 
        relâchements de touches.
        ---------------------------------------------------------------
        This function stops monitoring key presses and releases.
        """

        KeyPoisiton.is_listening = False
        self.listener.stop()





class KeyLoggerApp:
    """
    Cette classe permet de stopper l'exécution de la suite d'actions lorsque l'on appuie 
    sur les deux touches "y" et "j" (ces touches peuvent être modifiées). Elle n'est 
    utilisée que par "SameTime", "Loop" et "ActionDict".
    ------------------------------------------------------------------------------------
    This class allows stopping the execution of the action sequence when both the 
    "y" and "j" keys are pressed (these keys can be modified). It is only used by 
    "SameTime", "Loop", and "ActionDict".
    """

    # Variable permettant au conteneur ("SameTime", "Loop") ou à "start" dans "ActionDict" 
    # de ne pas exécuter de nouvelles actions alors que les touches pour arrêter 
    # l'exécution de la suite d'actions ont été pressées, car avant de commencer à 
    # exécuter une action, ils vérifient que "stop_run" vaut false.
    # ----------------------------------------------------------------------------------
    # Variable allowing the container ("SameTime", "Loop") or "start" in "ActionDict" not 
    # to execute new actions while the keys to stop the execution of the action sequence 
    # have been pressed, because before starting to execute an action, they check that 
    # "stop_run" is false.
    stop_run = False

    # Touche d'arrêt pour la suite d'actions.
    # ---------------------------------------
    # Stop key for the action sequence.
    stop_key = ["y", "j"]

    def __init__(self, cancel_task):
        """
        On prend en paramètre "cancel_task", qui permet de stopper les actions en cours 
        comme "KeyPress", "Loop", ou "SameTime". elle annule l'appel retardé de certaines 
        fonctions (celles appelées par "window.after") et réinitialise les variables 
        nécessaires à leurs valeurs initiales afin de permettre une réexécution correcte 
        de la suite d'actions.
        ---------------------------------------------------------------------------------
        We take "cancel_task" as a parameter, which allows stopping ongoing actions 
        such as "KeyPress", "Loop", or "SameTime". It cancels the delayed call of 
        certain functions (those called by "window.after") and resets the necessary 
        variables to their initial values to enable the correct re-execution of the 
        sequence of actions.
        """


        # On récupère "cancel_task", qui permet de stopper les actions en cours comme 
        # "KeyPress", "Loop", ou "SameTime". elle annule l'appel retardé de certaines 
        # fonctions (celles appelées par "window.after") et réinitialise les variables 
        # nécessaires à leurs valeurs initiales afin de permettre une réexécution correcte 
        # de la suite d'actions.
        # --------------------------------------------------------------------------------
        # We retrieve "cancel_task", which allows stopping ongoing actions like 
        # "KeyPress", "Loop", or "SameTime". It cancels the delayed call of certain 
        # functions (those called by "window.after") and resets the necessary variables 
        # to their initial values to enable the correct re-execution of the 
        # action sequence.
        self.cancel_task = cancel_task

        # On crée un set qui contiendra les touches "j" et ou "y" lorsqu'elles sont pressées.
        # -----------------------------------------------------------------------------------
        # We create a set that will contain the keys "j" and/or "y" when they are pressed.
        self.key_skip = set()

        # On décide d'observer tous les appuis et les relâchements de touches.
        # --------------------------------------------------------------------
        # We decide to observe all key presses and releases.
        self.listener = my_keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        # On commence à observer.
        # -----------------------
        # We start to observe.
        self.listener.start()



    def on_press(self, key):
        """
        Cette fonction est appelée lorsque une touche est pressée. On commence par vérifier 
        si la touche est une touche spéciale. Sinon, on regarde si c'est une des touches 
        permettant d'arrêter le programme. Si c'est le cas, on l'ajoute au set "key_skip". 
        Ensuite, si le set comporte deux éléments, cela signifie que les deux touches pour 
        stopper le programme sont pressées. Dans ce cas, on met "stop_run" à "True", on arrête 
        d'observer les appuis et les relâchements des touches, et on appelle "cancel_task".
        --------------------------------------------------------------------------------------
        This function is called when a key is pressed. We start by checking if the key is a 
        special key. If not, we check if it is one of the keys that stops the program. If it 
        is, we add it to the "key_skip" set. Then, if the set contains two elements, it means 
        that both keys to stop the program have been pressed. In this case, we set "stop_run" 
        to "True", stop monitoring key presses and releases, and call "cancel_task".
        """

        try:
            key_char = key.char
        except AttributeError:
            key_char = None
        
        if key_char in KeyLoggerApp.stop_key:
            self.key_skip.add(key_char)


        if len(self.key_skip) == len(KeyLoggerApp.stop_key):
            KeyLoggerApp.stop_run = True
            self.listener.stop()
            self.cancel_task()


    def on_release(self, key):
        """"
        Cette fonction est appelée lorsque une touche est relâchée. On commence par vérifier 
        si la touche est une touche spéciale. Sinon, on vérifie si c'est une des touches 
        permettant d'arrêter le programme. Si c'est le cas, on la retire du set "key_skip".
        ------------------------------------------------------------------------------------
        This function is called when a key is released. We start by checking if the key is 
        a special key. Otherwise, we check if it is one of the keys that allows the program 
        to stop. If so, we remove it from the "key_skip" set.
        """

        try:
            key_char = key.char
        except AttributeError:
            key_char = None
        
        
        if key_char in self.key_skip:
            self.key_skip.remove(key_char)


















def press_key(list_sp_keys, keys):
    """
    Cette fonction va actionner les touches qui lui sont données en paramètre, 
    qu'il s'agisse de touches spéciales ou non.
    --------------------------------------------------------------------------
    This function will press the keys given to it as parameters, 
    whether they are special keys or not.
    """
    for sp_key in list_sp_keys:
        if sp_key != "click r" and sp_key != "click l":
            keyboard.press(SP_KEY_DICT[sp_key])
        else:
            mouse.press(SP_KEY_DICT[sp_key])
    
    for key in keys:
        keyboard.press(key)




def release_key(list_sp_keys, keys):
    """
    Cette fonction va relâcher les touches qui lui sont données en paramètre, 
    qu'il s'agisse de touches spéciales ou non.
    -------------------------------------------------------------------------
    This function will release the keys given to it as parameters, 
    whether they are special keys or not.
    """

    for sp_key in list_sp_keys:
        if sp_key != "click r" and sp_key != "click l":
            keyboard.release(SP_KEY_DICT[sp_key])
        else:
            mouse.release(SP_KEY_DICT[sp_key])
    
    for key in keys:
        keyboard.release(key)




class KeyPress:
    """
    Cette classe permet d'actionner des touches pendant un certain temps.
    Les fonctions de cette classe sont :

    ->"__init__": prend tous les paramètres nécessaires pour actionner des touches pendant un certain temps, 
    y compris les touches, les touches spéciales, la durée, et l'unité de temps (millisecondes ou secondes).
    ->"run_act": actionne les touches choisies par l'utilisateur.
    ->"stop_press": relâche les touches qui ont été actionnées précédemment.
    ->"text": retourne une chaîne de caractères la plus courte possible pour identifier l'action.
    --------------------------------------------------------------------------------------------------------
    This class allows pressing keys for a certain period of time.
    The functions of this class are:

    ->__init__: takes all the necessary parameters to press keys for a certain period of time, 
    including the keys, special keys, duration, and the time unit (milliseconds or seconds).
    ->"run_act": presses the keys chosen by the user.
    ->"stop_press": releases the keys that were previously pressed.
    ->"text": returns the shortest possible string to identify the action.
    """

    def __init__(self, keys:str, list_sp_keys:list, time_wait:float):
        """
        Pour l'initialisation de la classe, nous prenons en paramètre: les touches, les touches spéciales, 
        la durée et l'unité de temps (millisecondes ou secondes).
        En premier, nous vérifions l'unité de mesure donnée ; si c'est en secondes, nous multiplions 
        le temps donné par 1000, car il est de base compté en millisecondes. Ensuite, nous supprimons 
        les caractères en double de la chaîne de caractères qui contient toutes les touches normales, 
        puis nous trions les noms des touches spéciales par ordre de taille pour la fonction "text".
        --------------------------------------------------------------------------------------------------
        For the initialization of the class, we take as parameters: the keys, special keys, the duration, 
        and the time unit (milliseconds or seconds).
        First, we check the given unit of measurement; if it is in seconds, we multiply the given time 
        by 1000, as it is originally counted in milliseconds. Next, we remove duplicate characters from 
        the string that contains all the normal keys, and then we sort the names of the special keys by 
        size for the "text" function.
        """
        self.time_wait_s = time_wait
        self.time_wait_ms = int(time_wait*1000)


        self.keys = "".join(list(set(keys)))
        self.list_sp_keys = sorted(list_sp_keys, key=lambda x: len(x), reverse=True)



    def run_act(self):
        """
        Cette fonction appelle "press_key" pour actionner les touches que l'utilisateur a entrées au préalable, 
        puis retourne le temps d'attente pendant lequel ces touches doivent être pressées. 
        (Ensuite, la fonction qui a appelé cette fonction se chargera, après ce temps, d'appeler "stop_press".)
        -------------------------------------------------------------------------------------------------------
        This function calls "press_key" to press the keys that the user entered previously, 
        then returns the wait time during which these keys must be pressed. (Subsequently, the function 
        that called this function will take care of calling "stop_press" after this time.)
        """

        press_key(self.list_sp_keys, self.keys)
        return self.time_wait_ms



    def stop_press(self):
        """
        Cette fonction appelle "release_key" pour relâcher les touches qui ont été précédemment actionnées.
        ---------------------------------------------------------------------------------------------------
        This function calls "release_key" to release the keys that were previously pressed.
        """

        release_key(self.list_sp_keys, self.keys)



    def text(self):
        """
        Cette fonction retourne une chaîne de caractères appropriée pour la suite d'actions avec les "Checkbutton". 
        Elle retourne une chaîne contenant le maximum d'informations tout en étant la plus courte possible, 
        donc elle abrège certaines informations pour éviter de prendre trop de place dans les menus.
        -----------------------------------------------------------------------------------------------------------
        This function returns a string that is suitable for the sequence of actions with the "Checkbutton." 
        It returns a string containing the maximum amount of information while being as short as possible, thus 
        abbreviating certain information to avoid taking up too much space in the menus.
        """

        if len(self.keys)>5:
            if len(self.list_sp_keys) > 1:
                return f"KeyPress : {self.time_wait_s} | {self.keys[:3]}.. | {self.list_sp_keys[0]}.."
            elif len(self.list_sp_keys) == 1:
                return f"KeyPress : {self.time_wait_s} | {self.keys[:3]}.. | {self.list_sp_keys[0]}"
            else:
                return f"KeyPress : {self.time_wait_s} | {self.keys[:3]}.."

        elif len(self.keys) == 0:
            if len(self.list_sp_keys) > 1:
                return f"KeyPress : {self.time_wait_s} | {self.list_sp_keys[0]}.."
            elif len(self.list_sp_keys) == 1:
                return f"KeyPress : {self.time_wait_s} | {self.list_sp_keys[0]}"

        else:
            if len(self.list_sp_keys) > 1:
                return f"KeyPress : {self.time_wait_s} | {self.keys} | {self.list_sp_keys[0]}.."
            elif len(self.list_sp_keys) == 1:
                return f"KeyPress : {self.time_wait_s} | {self.keys} | {self.list_sp_keys[0]}"
            else:
                return f"KeyPress : {self.time_wait_s} | {self.keys}"



    def type_act(self):
        """
        Cette fonction retourne le type de cette action sous forme de chaîne de caractères.
        -----------------------------------------------------------------------------------
        This function returns the type of this action as a string.
        """

        return "key press"







class ClickLeft:
    """
    Cette classe permet d'effectuer un clic gauche à un certain endroit.
    Les fonctions de cette classe sont :

    ->"__init__" : prend en paramètres la position x et y où doit se faire ce clic.
    ->"run_act" : déplace la souris à la position demandée puis effectue le clic.
    ->"text" : retourne une chaîne de caractères la plus courte possible pour identifier l'action.
    ----------------------------------------------------------------------------------------------
    This class allows a left-click at a specific location.
    The functions of this class are:

    ->"__init__": takes the x and y positions where the click should happen as parameters.
    ->"run_act": moves the mouse to the requested position and then clicks.
    ->"text": returns the shortest possible string to identify the action.
    """

    def __init__(self, pos_x:int, pos_y:int):
        """
        On prend la position à laquelle doit s'effectuer le clic.
        ---------------------------------------------------------
        We take the position where the click should occur.
        """

        self.pos_x = pos_x
        self.pos_y = pos_y



    def run_act(self):
        """
        On déplace la souris à la position choisie par l'utilisateur, puis on effectue le clic.
        ---------------------------------------------------------------------------------------
        We move the mouse to the position chosen by the user, then perform the click.
        """

        mouse.position = (self.pos_x, self.pos_y)
        mouse.press(Button.left)
        mouse.release(Button.left)



    def text(self):
        """
        On retourne la chaîne de caractères représentant l'action.
        ----------------------------------------------------------
        We return the string representing the action.
        """

        return f"ClickLeft : {self.pos_x} | {self.pos_y}"


    def type_act(self):
        """
        Cette fonction retourne le type de cette action sous forme de chaîne de caractères.
        -----------------------------------------------------------------------------------
        This function returns the type of this action as a string.
        """

        return "click l"








class ClickRight:
    """
    Cette classe permet d'effectuer un clic droit à un certain endroit.
    Les fonctions de cette classe sont :

    ->"__init__" : prend en paramètres la position x et y où doit se faire ce clic.
    ->"run_act" : déplace la souris à la position demandée puis effectue le clic.
    ->"text" : retourne une chaîne de caractères la plus courte possible pour identifier l'action.
    ----------------------------------------------------------------------------------------------
    This class allows a right-click at a specific location.
    The functions of this class are:

    ->"__init__": takes the x and y positions where the click should happen as parameters.
    ->"run_act": moves the mouse to the requested position and then clicks.
    ->"text": returns the shortest possible string to identify the action.
    """
    
    def __init__(self, pos_x:int, pos_y:int):
        """
        On prend la position à laquelle doit s'effectuer le clic.
        ---------------------------------------------------------
        We take the position where the click should occur.
        """

        self.pos_x = pos_x
        self.pos_y = pos_y



    def run_act(self):
        """
        On déplace la souris à la position choisie par l'utilisateur, puis on effectue le clic.
        ---------------------------------------------------------------------------------------
        We move the mouse to the position chosen by the user, then perform the click.
        """

        mouse.position = (self.pos_x, self.pos_y)
        mouse.press(Button.right)
        mouse.release(Button.right)



    def text(self):
        """
        On retourne la chaîne de caractères représentant l'action.
        ----------------------------------------------------------
        We return the string representing the action.
        """

        return f"ClickRight : {self.pos_x} | {self.pos_y}"

    def type_act(self):
        """
        Cette fonction retourne le type de cette action sous forme de chaîne de caractères.
        -----------------------------------------------------------------------------------
        This function returns the type of this action as a string.
        """

        return "click r"




class Move:
    """
    Cette classe permet de déplacer la souris à l'endroit choisi par l'utilisateur.
    Les fonctions de cette classe sont :

    ->"__init__" : prend en paramètres la position x et y où doit se déplacer la souris.
    ->"run_act" : déplace la souris à la position demandée.
    ->"text" : retourne une chaîne de caractères la plus courte possible pour identifier l'action.
    ----------------------------------------------------------------------------------------------
    This class allows moving the mouse to the location chosen by the user.
    The functions of this class are :

    ->"__init__": takes the x and y position as parameters where the mouse should move.
    ->"run_act": moves the mouse to the requested position.
    ->"text": returns the shortest possible string to identify the action.
    """

    def __init__(self, pos_x:int, pos_y:int, movement_type:str):
        """
        On prend la position à laquelle doit se déplacer la souris.
        -----------------------------------------------------------
        We take the position where the mouse should move.
        """
        self.movement_type = movement_type

        self.pos_x = pos_x
        self.pos_y = pos_y



    def run_act(self):
        """
        On déplace la souris à la position choisie par l'utilisateur.
        -------------------------------------------------------------
        We move the mouse to the position chosen by the user.
        """
        
        if self.movement_type is MovementType.ABSOLUTE:
            pydirectinput.moveRel(self.pos_x - mouse.position[0], self.pos_y - mouse.position[1])
        else:
            pydirectinput.moveRel(self.pos_x, self.pos_y)



    def text(self):
        """
        On retourne la chaîne de caractères représentant l'action.
        ----------------------------------------------------------
        We return the string representing the action.
        """

        
        if self.movement_type is MovementType.ABSOLUTE:
            return f"Absolute : {self.pos_x} | {self.pos_y}"
        else:
            return f"Relative : {self.pos_x} | {self.pos_y}"

    def type_act(self):
        """
        Cette fonction retourne le type de cette action sous forme de chaîne de caractères.
        -----------------------------------------------------------------------------------
        This function returns the type of this action as a string.
        """

        return "move"





class Write:
    """
    Cette classe permet de faire écrire un texte choisi par l'utilisateur.
    Les fonctions de cette classe sont :

    ->"__init__" : prend en paramètre le texte que l'utilisateur souhaite faire écrire.
    ->"run_act" : écrit le texte.
    ->"text" : retourne une chaîne de caractères la plus courte possible pour identifier l'action.
    ----------------------------------------------------------------------------------------------
    This class allows writing a text chosen by the user.
    The functions of this class are:

    ->"__init__" : takes as a parameter the text that the user wants to be written.
    ->"run_act" : writes the text.
    ->"text" : returns the shortest possible string to identify the action.
    """

    def __init__(self, text_to_write:str):
        """
        On prend en paramètre le texte que l'utilisateur souhaite faire écrire.
        -----------------------------------------------------------------------
        We take as a parameter the text that the user wants to write.
        """

        self.text_to_write = text_to_write



    def run_act(self):
        """
        On fait écrire le texte que l'utilisateur a choisi.
        ---------------------------------------------------
        We write the text that the user has chosen.
        """

        keyboard.type(self.text_to_write)



    def text(self):
        """
        On retourne une chaîne de caractères appropriée pour la suite d'actions avec les "Checkbutton". 
        Elle retourne une chaîne contenant le maximum d'informations tout en étant la plus courte possible, 
        donc elle abrège certaines informations pour éviter de prendre trop de place dans les menus.
        -----------------------------------------------------------------------------------------------------------
        We returns a string that is suitable for the sequence of actions with the "Checkbutton." 
        It returns a string containing the maximum amount of information while being as short as possible, thus 
        abbreviating certain information to avoid taking up too much space in the menus.
        """
        
        if len(self.text_to_write)>7:
            return f"Write : {self.text_to_write[:5]}.."
        else:
            return f"Write : {self.text_to_write}"



    def type_act(self):
        """
        Cette fonction retourne le type de cette action sous forme de chaîne de caractères.
        -----------------------------------------------------------------------------------
        This function returns the type of this action as a string.
        """

        return "write"
    






class Scroll:
    """
    Cette classe permet de faire défiler (scroller).
    Les fonctions de cette classe sont :

    ->"__init__" : prend en paramètre le nombre de pas que l'utilisateur souhaite scroller 
    ainsi que la direction.
    ->"run_act" : effectue le défilement.
    ->"text" : retourne une chaîne de caractères la plus courte possible pour identifier l'action.
    ----------------------------------------------------------------------------------------------
    This class allows scrolling.
    The functions of this class are:

    ->"__init__" : takes as parameters the number of steps the user wants to scroll and 
    the direction.
    ->"run_act" : performs the scrolling.
    ->"text" : returns the shortest possible string to identify the action.
    """

    def __init__(self, step:int, direction:str):
        """
        On prend en paramètre le nombre de pas que l'utilisateur souhaite scroller 
        ainsi que la direction dans laquelle il veut scroller.
        --------------------------------------------------------------------------
        We take as parameters the number of steps the user wants to scroll and 
        the direction in which they want to scroll.
        """
        self.step = step
        self.direction = direction



    def run_act(self):
        """
        On fait défiler le nombre de pas choisi par l'utilisateur dans la 
        direction qu'il a choisie.
        -----------------------------------------------------------------
        We scroll the number of steps chosen by the user in the direction 
        they have chosen.
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



    def text(self):
        """
        On retourne la chaîne de caractères représentant l'action.
        ----------------------------------------------------------
        We return the string representing the action.
        """

        return f"Scroll : {self.direction.value} | {self.step}"


    def type_act(self):
        """
        Cette fonction retourne le type de cette action sous forme de chaîne de caractères.
        -----------------------------------------------------------------------------------
        This function returns the type of this action as a string.
        """

        return "scroll"




class Wait:
    """
    Cette classe permet d'attendre entre deux actions.
    Les fonctions de cette classe sont :
    
    ->"__init__" : prend en paramètre le temps que l'utilisateur souhaite attendre et l'unité 
    de temps (millisecondes ou secondes).
    ->"run_act" : retourne le temps d'attente.
    ->"text" : retourne une chaîne de caractères la plus courte possible pour identifier l'action.
    --------------------------------------------------------------------------------------------
    This class allows waiting between two actions.
    The functions of this class are:

    ->"__init__": takes as a parameter the time the user wants to wait and the unit of time 
    (milliseconds or seconds).
    ->"run_act": returns the wait time.
    ->"text": returns the shortest possible string to identify the action.
    """
    
    def __init__(self, time_wait:float):
        """
        On prend en paramètre le temps que l'utilisateur souhaite attendre et l'unité 
        de temps (millisecondes ou secondes).
        Tout d'abord, nous vérifions l'unité de mesure donnée ; si c'est en secondes, 
        nous multiplions le temps par 1000, car il est par défaut compté en millisecondes.
        ----------------------------------------------------------------------------------
        We take as a parameter the time the user wants to wait and the time unit 
        (milliseconds or seconds).
        First, we check the given unit of measurement; if it is in seconds, we multiply 
        the time by 1000, as it is by default counted in milliseconds.
        """
        self.time_wait_ms = int(time_wait*1000)
        self.time_wait_s = time_wait




    def run_act(self):
        """
        On retourne le temps d'attente pendant lequel le programme doit suspendre l'exécution 
        de la suite d'actions avant de la reprendre.
        -------------------------------------------------------------------------------------
        We return the waiting time during which the program must suspend the execution of 
        the sequence of actions before resuming it.
        """

        return self.time_wait_ms



    def text(self):
        """
        On retourne la chaîne de caractères représentant l'action.
        ----------------------------------------------------------
        We return the string representing the action.
        """

        return f"Wait : {self.time_wait_s}s"


    def type_act(self):
        """
        Cette fonction retourne le type de cette action sous forme de chaîne de caractères.
        -----------------------------------------------------------------------------------
        This function returns the type of this action as a string.
        """

        return "wait"










class Loop:
    """
    Cette classe permet d'exécuter une suite d'actions un certain nombre de fois 
    d'affilée.
    Les fonctions de cette classe sont :

    ->"__init__" : takes as parameters the interface window to be able to call functions 
    after a certain delay, the number of executions the loop must perform with the 
    sequence of actions, as well as the name of the loop.
    ->"new_action" : permet d'ajouter une action à la suite d'actions qui sera répétée 
    le nombre de fois choisi par l'utilisateur.
    ->"cancel_task" : permet de stopper l'exécution de la suite d'actions.
    ->"run_act" : appelle "a_turn" un certain nombre de fois, jusqu'à ce que le nombre 
    de répétitions demandé soit atteint, puis appelle la fonction qui a initialement 
    appelé "run_act" pour continuer l'exécution de la suite d'actions.
    ->"a_turn" : exécute une fois chaque action de la liste.
    ->"add_tree_CNTR" : permet d'ajouter à l'arbre les actions qui se trouvent dans cette 
    boucle avec l'incrémentation correspondante.
    ->"text" : retourne une chaîne de caractères la plus courte possible pour identifier 
    l'action.
    -------------------------------------------------------------------------------------
    This class allows executing a sequence of actions a certain number of times in a row. 
    The functions of this class are:

    ->"__init__": takes as parameters the number of executions that the loop must perform 
    with the sequence of actions, as well as the name of the loop.
    ->"new_action": Allows adding an action to the sequence of actions, which will be 
    repeated the number of times chosen by the user.
    ->"cancel_task": Stops the execution of the sequence of actions.
    ->"run_act": Calls "a_turn" a certain number of times until the requested number of 
    repetitions is reached, then calls the function that initially called "run_act" to 
    continue the execution of the sequence of actions.
    ->"a_turn": Executes each action in the list once.
    ->"add_tree_CNTR": Adds the actions in this loop to the action tree with the 
    corresponding increment.
    ->"text": Returns the shortest possible string to identify the action.
    """

    def __init__(self, window, nb_turns:int, name:str):
        """ 
        On prend en paramètre la fenêtre de l'interface, le nombre d'exécutions que la boucle doit effectuer avec 
        la suite d'actions, ainsi que le nom de la boucle.
        ------------------------------------------------------------------------------
        We take as parameters the number of executions the loop must perform with the 
        sequence of actions, as well as the name of the loop.
        """

        # On prend la fenêtre de l'interface pour ensuite utiliser "window.after", 
        # qui permet d'appeler des fonctions après un certain temps,sans bloquer 
        # l'exécution du programme.
        # ------------------------------------------------------------------------
        # We take the interface window to then use "window.after", which allows 
        # functions to be called after a certain time without blocking the 
        # program's execution. We take the interface window to then use 
        # "window.after", which allows functions to be called after a certain 
        # time without blocking the program's execution.
        self.window = window

        # On récupère les valeurs données en paramètre, le nom et le nombre de tours, 
        # et on crée une variable "ctr_of_turns" qui va s'incrémenter à chaque 
        # tour de boucle jusqu'à atteindre le nombre demandé.
        # -----------------------------------------------------------------------------
        # We retrieve the values given as parameters, the name and the number of loops, 
        # and create a variable "ctr_of_turns" that increments with each loop iteration 
        # until the requested number is reached.
        self.name = name
        self.nb_turns = nb_turns
        self.ctr_of_turns = 0

        # On crée "id_after", une variable qui contiendra par la suite l'identifiant des fonctions 
        # appelées avec "window.after", afin de permettre à "cancel_task" d'annuler l'appel de ces 
        # fonctions.
        # ----------------------------------------------------------------------------------------
        # We create "id_after", a variable that will later hold the identifier of functions called 
        # with "window.after", allowing "cancel_task" to cancel the call of these functions.
        self.id_after = None


        # On crée le dictionnaire "act_dict_CNTR" qui contiendra les actions, puis on crée la 
        # variable "act_K_CNTR" qui servira de clé pour chaque action du dictionnaire, que l'on 
        # incrémentera pour chaque action. Ensuite, on crée une variable "ctr_of_act_CNTR", qui 
        # s'incrémentera après l'exécution de chaque action afin de parcourir le dictionnaire.
        # ------------------------------------------------------------------------------------------
        # We create the dictionary "act_dict_CNTR" that will contain the actions, then we create 
        # the variable "act_K_CNTR", which will serve as the key for each action in the dictionary, 
        # and we increment it for each action. Next, we create a variable "ctr_of_act_CNTR", which 
        # will increment after the execution of each action to allow traversing the dictionary.
        self.act_dict_CNTR = {}
        self.act_K_CNTR = 0
        self.ctr_of_act_CNTR = 0

        # On crée le dictionnaire qui va contenir tous les "Checkbutton", "dict_tree_CNTR", 
        # et qui aura comme clé "K_tree_CNTR", qui s'incrémentera après la création 
        # de chaque "Checkbutton".
        # -----------------------------------------------------------------------------------
        # We create the dictionary that will contain all the "Checkbutton", "dict_tree_CNTR", 
        # and which will have as the key "K_tree_CNTR", which will increment after the 
        # creation of each "Checkbutton".
        self.dict_tree_CNTR = {}
        self.K_tree_CNTR = 0



    def new_action(self, inst_act):
        """
        On prend l'instance de l'action en paramètre et on l'ajoute au dictionnaire d'actions de 
        la boucle "act_dict_CNTR" avec pour clé "act_K_CNTR", puis on incrémente "act_K_CNTR".
        ----------------------------------------------------------------------------------------
        We take the action instance as a parameter and add it to the action dictionary of the 
        loop "act_dict_CNTR" with the key "act_K_CNTR", then we increment "act_K_CNTR".
        """

        self.act_dict_CNTR[self.act_K_CNTR] = inst_act
        self.act_K_CNTR += 1



    def cancel_task(self):
        """
        Cette fonction permet de stopper l'exécution de la suite d'actions. Elle est appelée soit par 
        "ActionDict", soit par le conteneur dans lequel se trouve cette instance ("SameTime", "Loop").

        On commence par tenter d'appeler "stop_press" sur la dernière action qu'on a appelée, afin que 
        si l'action était "KeyPress", on relâche les touches pressées. Ensuite, on tente d'appeler 
        "cancel_task" sur la dernière action qu'on a appelée, afin que si cette action est un conteneur, 
        elle arrête son exécution (en faisant la même chose).

        Après cela, on regarde s'il y a une fonction qui a été appelée avec "window.after" (par exemple, 
        pour "wait", on utilise "window.after"). Si c'est le cas, on annule l'appel, puis on met 
        "ctr_of_act_CNTR" à 0 pour pouvoir par la suite réexécuter cette boucle.
        ------------------------------------------------------------------------------------------------
        This function allows stopping the execution of the sequence of actions. It is called either by 
        "ActionDict" or by the container in which this instance is located ("SameTime", "Loop").

        We start by trying to call "stop_press" on the last action we invoked, so that if the action was 
        "KeyPress", we release the pressed keys. Next, we attempt to call "cancel_task" on the last 
        action we invoked, so that if this action is a container, it stops its execution 
        (by doing the same thing).

        After that, we check if there is a function that has been called with "window.after" (for example, 
        for "wait", we use "window.after"). If so, we cancel the call, and then set "ctr_of_act_CNTR" to 0 
        to allow the subsequent re-execution of this loop.
        """

        try:
            self.act_dict_CNTR[self.ctr_of_act_CNTR-1].stop_press()
        except:
            pass
        try:
            self.act_dict_CNTR[self.ctr_of_act_CNTR-1].cancel_task()
        except:
            pass
        
        if self.id_after is not None:
            self.window.after_cancel(self.id_after)
            self.id_after = None
        self.ctr_of_act_CNTR = 0



    def run_act(self, advent_function=None, sleep_act_time=None):
        """
        Cette fonction prend en paramètre la fonction qui a appelé cette fonction, "advent_function", 
        afin qu'à la fin de l'exécution de la boucle, nous puissions l'appeler pour continuer l'exécution 
        de la suite d'actions.

        On commence par récupérer "advent_function" si elle a été donnée. Ensuite, on vérifie si nous 
        n'avons pas encore effectué tous les tours de boucle. Si c'est le cas, nous en 
        effectuons un autre en appelant "a_turn". Puis, nous incrémentons "ctr_of_turns" pour compter 
        le nombre de tours. Sinon, nous remettons "ctr_of_turns" à 0, puis nous appelons la fonction 
        qui nous a initialement appelés pour continuer la suite d'actions.
        -------------------------------------------------------------------------------------------------
        This function takes as a parameter the function that called it, "advent_function", so that at the 
        end of the loop execution, we can call it to continue the execution of the sequence of actions.

        We start by retrieving "advent_function" if it has been provided. Then, we check if we have not 
        yet completed all the loop iterations. If that is the case, we perform another iteration by 
        calling "a_turn". Next, we increment "ctr_of_turns" to count the number of iterations. Otherwise, 
        we reset "ctr_of_turns" to 0 and then call the function that initially called us to continue the 
        sequence of actions.
        """
        
        if not advent_function == None:
            self.advent_function = advent_function
            self.sleep_act_time = sleep_act_time

        if self.ctr_of_turns < self.nb_turns:
            self.window.after(0, self.a_turn)
            self.ctr_of_turns += 1

        else:
            self.ctr_of_turns = 0
            self.window.after(0, self.advent_function)



    def a_turn(self):
        """
        Cette fonction va exécuter les actions de la suite, en en exécutant une et en incrémentant 
        "ctr_of_act_CNTR", puis en se rappelant pour exécuter l'action suivante jusqu'à la fin.
        ------------------------------------------------------------------------------------------
        This function will execute the actions in the sequence, by executing one and incrementing 
        "ctr_of_act_CNTR", then calling itself again to execute the next action until the end.
        """


        # On vérifie que toutes les actions n'ont pas déjà été exécutées.
        # ---------------------------------------------------------------
        # We check that all the actions have not already been executed.
        if not self.ctr_of_act_CNTR >= self.act_K_CNTR and not KeyLoggerApp.stop_run:
            
            # On incrémente "ctr_of_act_CNTR" pour savoir lorsque toutes les actions ont 
            # été parcourues.
            # ---------------------------------------------------------------------------
            # We increment "ctr_of_act_CNTR" to know when all actions have been executed.
            self.ctr_of_act_CNTR += 1

            # On vérifie si l'utilisateur a laissé le "Checkbutton" coché. S'il l'a décoché, 
            # on n'exécute pas l'action.
            # -------------------------------------------------------------------------------
            # We check if the user has left the "Checkbutton" checked. If they have unchecked 
            # it, the action is not executed.
            if list(self.dict_tree_CNTR[self.ctr_of_act_CNTR-1])[0].get() == 1:

                # On vérifie si l'action est un conteneur (Loop, SameTime).
                # ---------------------------------------------------------
                # We check if the action is a container (Loop, SameTime).
                if isinstance(self.act_dict_CNTR[self.ctr_of_act_CNTR-1], Loop) or isinstance(self.act_dict_CNTR[self.ctr_of_act_CNTR-1], SameTime):

                    # On appelle la fonction "run_act" du conteneur en lui passant en paramètre 
                    # "self.a_turn", pour qu'après avoir exécuté ce qu'elle a à faire, elle 
                    # puisse nous rappeler afin que nous puissions continuer l'exécution des 
                    # autres actions.
                    # -------------------------------------------------------------------------
                    # We call the "run_act" function of the container, passing it the parameter 
                    # "self.a_turn", so that after executing what it has to do, it can call us 
                    # back so that we can continue the execution of the other actions.
                    self.window.after(0, lambda : self.act_dict_CNTR[self.ctr_of_act_CNTR-1].run_act(self.a_turn, self.sleep_act_time))
                
                else:
                    # On exécute l'action en faisant appel à "run_act" et en récupérant ce 
                    # qu'elle retourne, car "Wait" et "KeyPress" retournent un temps.
                    # --------------------------------------------------------------------
                    # We execute the action by calling "run_act" and retrieving what it 
                    # returns, as "Wait" and "KeyPress" return a time.
                    time = self.act_dict_CNTR[self.ctr_of_act_CNTR-1].run_act()


                    # On regarde si l'action que l'on vient d'exécuter était "KeyPress" pour pouvoir 
                    # appeler "call_stop_press" après le temps d'attente choisi par l'utilisateur.
                    # ------------------------------------------------------------------------------
                    # We check if the action we just executed was "KeyPress" in order to call 
                    # "call_stop_press" after the waiting time chosen by the user.
                    if isinstance(self.act_dict_CNTR[self.ctr_of_act_CNTR-1], KeyPress):
                        self.id_after = self.window.after(time, self.call_stop_press)

                    # On regarde si l'action que l'on vient d'exécuter était "Wait" pour pouvoir 
                    # rappeler "a_turn" après le temps d'attente choisi par l'utilisateur.
                    # --------------------------------------------------------------------------
                    # We check if the action we just executed was "Wait" in order to call 
                    # "a_turn" after the wait time chosen by the user.
                    elif isinstance(self.act_dict_CNTR[self.ctr_of_act_CNTR-1], Wait):
                        self.id_after = self.window.after(time+self.sleep_act_time, self.a_turn)
                    
                    else:
                        # L'action que nous venons d'appeler ne nécessite pas de temps d'attente, alors 
                        # nous appelons "a_turn" pour exécuter l'action suivante.
                        # -----------------------------------------------------------------------------
                        # The action we just called does not require any waiting time, so we call 
                        # "a_turn" to execute the next action.
                        self.window.after(self.sleep_act_time, self.a_turn)
            else:

                # L'utilisateur a décoché l'action pour éviter qu'elle ne s'exécute, alors nous appelons 
                # "a_turn" pour exécuter l'action suivante.
                # --------------------------------------------------------------------------------------
                # The user has unchecked the action to prevent it from executing, so we call "a_turn" to 
                # execute the next action.
                self.window.after(self.sleep_act_time, self.a_turn)
            
        else:
            # On a exécuté chaque action, alors on met "ctr_of_act_CNTR" à 0 pour refaire un tour si besoin. 
            # Puis, on appelle "run_act", qui va soit refaire un tour de boucle, soit appeler la fonction 
            # qui l'a initialement appelée.
            # ----------------------------------------------------------------------------------------------
            # We have executed each action, so we set "ctr_of_act_CNTR" to 0 to make another pass if needed. 
            # Then, we call "run_act", which will either repeat the loop or call the function that 
            # initially called it.
            self.ctr_of_act_CNTR = 0
            self.window.after(0, self.run_act)



    def call_stop_press(self):
        """
        Cette fonction appelle "stop_press" pour "KeyPress" afin de relâcher les touches précédemment 
        pressées, puis on appelle "a_turn" pour exécuter l'action d'après dans la boucle.
        ---------------------------------------------------------------------------------------------
        This function calls "stop_press" for "KeyPress" to release the previously pressed keys, then 
        we call "a_turn" to execute the next action in the loop.
        """

        self.act_dict_CNTR[self.ctr_of_act_CNTR-1].stop_press()
        self.window.after(self.sleep_act_time, self.a_turn)
        



    def add_tree_CNTR(self, text, inter_tree, spacing):
        """
        Cette fonction prend en paramètre la chaîne de caractères représentant l'action qui a été 
        ajoutée à la boucle, l'instance de la classe "IntfTree" qui nous permet d'avoir accès à la 
        frame dans laquelle nous devons ajouter le "Checkbutton" "all_actions", ainsi que la ligne 
        à laquelle nous devons afficher le "Checkbutton" "row_ChkBt". On prend aussi en paramètre 
        l'incrémentation à laquelle doit être positionné le "Checkbutton". 
        Cette fonction permet d'ajouter à l'arbre les actions qui se trouvent dans cette boucle 
        avec l'incrémentation correspondante.
        ------------------------------------------------------------------------------------------
        This function takes as parameters the string representing the action that has been added 
        to the loop, the instance of the class "IntfTree", which allows us to access the frame 
        where we need to add the "Checkbutton" called "all_actions", as well as the row where we 
        need to display the "Checkbutton" called "row_ChkBt". We also take as a parameter the 
        increment at which the "Checkbutton" should be positioned. 
        This function allows us to add to the tree the actions that are found in this loop with 
        the corresponding increment.
        """

        # On commence par créer la variable "is_checked_act" qui permettra de savoir si le "Checkbutton" 
        # est coché ou non. Ensuite, on crée le "Checkbutton" et on l'affiche dans "all_actions".
        # ------------------------------------------------------------------------------------------------
        # We start by creating the variable "is_checked_act" which will indicate whether the "Checkbutton" 
        # is checked or not. Then, we create the "Checkbutton" and display it in "all_actions".
        is_checked_act = tk.IntVar(value=1)
        ChkBt_act = tk.Checkbutton(inter_tree.all_actions.scrollable_frame, text=text, variable=is_checked_act, bg=inter_tree.w_var.color_1)
        ChkBt_act.grid(row=inter_tree.row_ChkBt+1, column=0, sticky="wn", padx=spacing)

        # On ajoute au dictionnaire qui va contenir tous les "Checkbutton", "dict_tree_CNTR", un tuple 
        # comportant en premier "is_checked_act", qui permet de savoir si le "Checkbutton" est coché ou 
        # non, et le "Checkbutton" ce tuple a pour clé "K_tree_CNTR".
        # ---------------------------------------------------------------------------------------------
        # We add to the dictionary that will contain all the "Checkbuttons", "dict_tree_CNTR", a tuple 
        # consisting first of "is_checked_act", which indicates whether the "Checkbutton" is checked or 
        # not, and the "Checkbutton" itself. This tuple has "K_tree_CNTR" as its key.
        self.dict_tree_CNTR[self.K_tree_CNTR] = [is_checked_act, ChkBt_act]

        # On incrémente "K_tree_CNTR" et "row_ChkBt".
        # -------------------------------------------
        # We increment "K_tree_CNTR" and "row_ChkBt".
        self.K_tree_CNTR += 1
        inter_tree.row_ChkBt += 1



    def text(self):
        """
        On retourne la chaîne de caractères représentant l'action.
        ----------------------------------------------------------
        We return the string representing the action.
        """

        return f"Loop : {self.nb_turns} | {self.name}"
    


    def type_act(self):
        """
        Cette fonction retourne le type de cette action sous forme de chaîne de caractères.
        -----------------------------------------------------------------------------------
        This function returns the type of this action as a string.
        """

        return "loop"
















#########################################################
#########################################################
##################  Same_Time  ##########################
#########################################################
#########################################################



class SameTime:
    """
    Cette classe permet d'exécuter une suite d'actions en même temps que une ou plusieurs touches 
    sont pressées.
    Les fonctions de cette classe sont :

    ->"__init__" : prend en paramètre la fenêtre de l'interface pour pouvoir appeler des fonctions 
    après un certain délai, les touches à actionner, les touches spéciales, ainsi que son nom.
    ->"new_action" : permet d'ajouter une action à la suite d'actions qui sera exécutée en même 
    temps que les touches choisies par l'utilisateur seront pressées.
    ->"cancel_task" : permet de stopper l'exécution de la suite d'actions.
    ->"run_act" : appelle "run" juste après avoir actionné les touches choisies par l'utilisateur.
    ->"run" : va exécuter chaque action de la liste avant de rappeler "run_act", qui va s'occuper 
    de relâcher les touches pressées et de rappeler la fonction qui l'a initialement appelée pour 
    continuer l'exécution de la suite d'actions.
    ->"add_tree_CNTR" : permet d'ajouter à l'arbre les actions qui se trouvent dans ce conteneur 
    avec l'incrémentation correspondante.
    ->"text" : retourne une chaîne de caractères la plus courte possible pour identifier l'action.
    ----------------------------------------------------------------------------------------------
    This class allows executing a series of actions at the same time as one or more keys are 
    pressed.
    The functions of this class are:

    -> __init__: takes the interface window as a parameter to be able to call functions after a 
    certain delay, the keys to be pressed, the special keys, and its name.
    -> new_action: allows adding an action to the series of actions that will be executed while 
    the keys chosen by the user are pressed.
    -> cancel_task: stops the execution of the series of actions.
    -> run_act: calls run right after pressing the keys chosen by the user.
    -> run: will execute each action in the list before recalling run_act, which will handle 
    releasing the pressed keys and calling the function that initially invoked it to continue 
    the execution of the series of actions.
    -> add_tree_CNTR: adds to the tree the actions in this container with the corresponding 
    increment.
    -> text: returns the shortest possible string to identify the action.
    """

    def __init__(self, window, keys:str, list_sp_keys:list, name:str):
        """ 
        On prend en paramètre la fenêtre de l'interface, les touches à presser, 
        puis les touches spéciales à presser pendant l'exécution de la suite d'actions, 
        ainsi que son nom.
        -------------------------------------------------------------------------------
        We take as parameters the interface window, the keys to press, then the special 
        keys to press during the execution of the sequence of actions, as well 
        as its name.
        """

        # On prend la fenêtre de l'interface pour ensuite utiliser "window.after", 
        # qui permet d'appeler des fonctions après un certain temps,sans bloquer 
        # l'exécution du programme.
        # ------------------------------------------------------------------------
        # We take the interface window to then use "window.after", which allows 
        # functions to be called after a certain time without blocking the 
        # program's execution. We take the interface window to then use 
        # "window.after", which allows functions to be called after a certain 
        # time without blocking the program's execution.
        self.window = window

        # Nous supprimons les caractères en double de la chaîne de caractères qui contient 
        # toutes les touches normales "keys", puis nous trions les noms des touches spéciales 
        # "list_sp_keys" par ordre de taille pour la fonction "text", et après on récupère son 
        # nom "name".
        # -------------------------------------------------------------------------------------
        # We remove the duplicate characters from the string that contains all the regular keys 
        # "keys" then we sort the names of the special keys "list_sp_keys" by length for the 
        # "text" function and afterward we retrieve its name "name".
        self.keys = "".join(list(set(keys)))
        self.list_sp_keys = sorted(list_sp_keys, key=lambda x: len(x), reverse=True)
        self.name = name

        # On crée le dictionnaire "act_dict_CNTR" qui contiendra les actions, puis on crée la 
        # variable "act_K_CNTR" qui servira de clé pour chaque action du dictionnaire, que l'on 
        # incrémentera pour chaque action. Ensuite, on crée une variable "ctr_of_act_CNTR", qui 
        # s'incrémentera après l'exécution de chaque action afin de parcourir le dictionnaire.
        # ------------------------------------------------------------------------------------------
        # We create the dictionary "act_dict_CNTR" that will contain the actions, then we create 
        # the variable "act_K_CNTR", which will serve as the key for each action in the dictionary, 
        # and we increment it for each action. Next, we create a variable "ctr_of_act_CNTR", which 
        # will increment after the execution of each action to allow traversing the dictionary.
        self.act_dict_CNTR = {}
        self.act_K_CNTR = 0
        self.ctr_of_act_CNTR = 0

        # On crée "id_after", une variable qui contiendra par la suite l'identifiant des fonctions 
        # appelées avec "window.after", afin de permettre à "cancel_task" d'annuler l'appel de ces 
        # fonctions.
        # ----------------------------------------------------------------------------------------
        # We create "id_after", a variable that will later hold the identifier of functions called 
        # with 'window.after,' allowing 'cancel_task' to cancel the call of these functions.
        self.id_after = None

        # On crée "finish_running", qui permet à "run_act" de savoir si la liste d'actions a déjà 
        # été exécuter.
        # ---------------------------------------------------------------------------------------
        # We create "finish_running", which allows "run_act" to know if the list of actions has 
        # already been executed.
        self.finich_running = False

        # On crée le dictionnaire qui va contenir tous les "Checkbutton", "dict_tree_CNTR", 
        # et qui aura comme clé "K_tree_CNTR", qui s'incrémentera après la création 
        # de chaque "Checkbutton".
        # -----------------------------------------------------------------------------------
        # We create the dictionary that will contain all the 'Checkbutton', 'dict_tree_CNTR', 
        # and which will have as the key 'K_tree_CNTR', which will increment after the 
        # creation of each 'Checkbutton'.
        self.dict_tree_CNTR = {}
        self.K_tree_CNTR = 0



    def new_action(self, instance):
        """
        On prend l'instance de l'action en paramètre et on l'ajoute au dictionnaire d'actions 
        "act_dict_CNTR" avec pour clé "act_K_CNTR", puis on incrémente "act_K_CNTR".
        -------------------------------------------------------------------------------------
        We take the action instance as a parameter and add it to the action dictionary 
        "act_dict_CNTR" with the key "act_K_CNTR", then increment "act_K_CNTR".
        """

        self.act_dict_CNTR[self.act_K_CNTR] = instance
        self.act_K_CNTR += 1



    def cancel_task(self):
        """
        Cette fonction permet de stopper l'exécution de la suite d'actions. Elle est appelée soit par 
        "ActionDict", soit par le conteneur dans lequel se trouve cette instance ("SameTime", "Loop").

        On commence par tenter d'appeler "stop_press" sur la dernière action qu'on a appelée, afin que 
        si l'action était "KeyPress", on relâche les touches pressées. Ensuite, on tente d'appeler 
        "cancel_task" sur la dernière action qu'on a appelée, afin que si cette action est un conteneur, 
        elle arrête son exécution (en faisant la même chose).

        Après cela, on regarde s'il y a une fonction qui a été appelée avec "window.after" (par exemple, 
        pour "wait", on utilise "window.after"). Si c'est le cas, on annule l'appel, puis on met 
        "ctr_of_act_CNTR" à 0 pour pouvoir par la suite réexécuter ce conteneur.
        ------------------------------------------------------------------------------------------------
        This function allows stopping the execution of the sequence of actions. It is called either by 
        "ActionDict" or by the container in which this instance is located ("SameTime", "Loop").

        We start by trying to call "stop_press" on the last action we invoked, so that if the action was 
        "KeyPress", we release the pressed keys. Next, we attempt to call "cancel_task" on the last 
        action we invoked, so that if this action is a container, it stops its execution 
        (by doing the same thing).

        After that, we check if there is a function that has been called with "window.after" (for example, 
        for "wait", we use "window.after"). If so, we cancel the call, and then set "ctr_of_act_CNTR" to 0 
        to allow the subsequent re-execution of this container.
        """

        try:
            self.act_dict_CNTR[self.ctr_of_act_CNTR-1].stop_press()
        except:
            pass
        try:
            self.act_dict_CNTR[self.ctr_of_act_CNTR-1].cancel_task()
        except:
            pass
        
        if self.id_after is not None:
            self.window.after_cancel(self.id_after)
            self.id_after = None
        self.ctr_of_act_CNTR = 0





    def run_act(self, advent_function=None, sleep_act_time=None):
        """
        Cette fonction prend en paramètre la fonction qui l’a appelée, "advent_function", afin qu'à la 
        fin de l'exécution de la suite d'actions, nous puissions l'appeler pour continuer la suite 
        d'action.

        On commence par récupérer "advent_function" si elle a été fournie. Ensuite, on vérifie si la 
        suite d'actions a déjà été exécutée. Si c'est le cas, nous relâchons les touches pressées avec 
        "release_key", puis nous appelons la fonction qui nous a initialement appelés pour continuer 
        la suite d'actions, et nous mettons "finish_running" à "False".
        Sinon, nous pressons les touches demandées par l'utilisateur avec "press_key", puis nous 
        appelons "run".
        -------------------------------------------------------------------------------------------------
        This function takes the function that called it, "advent_function", as a parameter so that at 
        the end of the action sequence execution, we can call it to continue the sequence of actions.
        
        We start by retrieving "advent_function" if it was provided. Next, we check if the sequence 
        of actions has already been executed. If so, we release the pressed keys using "release_key", 
        then call the function that initially called us to continue the sequence of actions, and set 
        "finish_running" to "False".
        Otherwise, we press the keys requested by the user with "press_key" and then call "run".
        """

        if not advent_function == None:
            self.advent_function = advent_function
            self.sleep_act_time = sleep_act_time

        if self.finich_running:
            release_key(self.list_sp_keys, self.keys)
            self.window.after(self.sleep_act_time, self.advent_function)
            self.finich_running = False
        else:
            press_key(self.list_sp_keys, self.keys)
            self.window.after(0, self.run)





    def run(self):
        """
        Cette fonction va exécuter les actions de la suite, en en exécutant une et en incrémentant 
        "ctr_of_act_CNTR", puis en se rappelant pour exécuter l'action suivante jusqu'à la fin.
        ------------------------------------------------------------------------------------------
        This function will execute the actions in the sequence, by executing one and incrementing 
        "ctr_of_act_CNTR", then calling itself again to execute the next action until the end.
        """

        # On vérifie que toutes les actions n'ont pas déjà été exécutées.
        # ---------------------------------------------------------------
        # We check that all the actions have not already been executed.
        if not self.ctr_of_act_CNTR >= self.act_K_CNTR and not KeyLoggerApp.stop_run:

            # On incrémente "ctr_of_act_CNTR" pour savoir lorsque toutes les actions ont 
            # été parcourues.
            # ---------------------------------------------------------------------------
            # We increment "ctr_of_act_CNTR" to know when all actions have been executed.
            self.ctr_of_act_CNTR += 1


            # On vérifie si l'utilisateur a laissé le "Checkbutton" coché. S'il l'a décoché, 
            # on n'exécute pas l'action.
            # -------------------------------------------------------------------------------
            # We check if the user has left the "Checkbutton" checked. If they have unchecked 
            # it, the action is not executed.
            if list(self.dict_tree_CNTR[self.ctr_of_act_CNTR-1])[0].get() == 1:

                # On vérifie si l'action est un conteneur (Loop, SameTime).
                # ---------------------------------------------------------
                # We check if the action is a container (Loop, SameTime).
                if isinstance(self.act_dict_CNTR[self.ctr_of_act_CNTR-1], Loop) or isinstance(self.act_dict_CNTR[self.ctr_of_act_CNTR-1], SameTime):

                    # On appelle la fonction "run_act" du conteneur en lui passant en paramètre 
                    # "self.a_turn", pour qu'après avoir exécuté ce qu'elle a à faire, elle 
                    # puisse nous rappeler afin que nous puissions continuer l'exécution des 
                    # autres actions.
                    # -------------------------------------------------------------------------
                    # We call the "run_act" function of the container, passing it the parameter 
                    # "self.a_turn", so that after executing what it has to do, it can call us 
                    # back so that we can continue the execution of the other actions.
                    self.window.after(0, lambda : self.act_dict_CNTR[self.ctr_of_act_CNTR-1].run_act(self.run, self.sleep_act_time))
                    
                else:
                    # On exécute l'action en faisant appel à "run_act" et en récupérant ce 
                    # qu'elle retourne, car "Wait" et "KeyPress" retournent un temps.
                    # --------------------------------------------------------------------
                    # We execute the action by calling "run_act" and retrieving what it 
                    # returns, as "Wait" and "KeyPress" return a time.
                    time = self.act_dict_CNTR[self.ctr_of_act_CNTR-1].run_act()


                    # On regarde si l'action que l'on vient d'exécuter était "KeyPress" pour pouvoir 
                    # appeler "call_stop_press" après le temps d'attente choisi par l'utilisateur.
                    # ------------------------------------------------------------------------------
                    # We check if the action we just executed was "KeyPress" in order to call 
                    # "call_stop_press" after the waiting time chosen by the user.
                    if isinstance(self.act_dict_CNTR[self.ctr_of_act_CNTR-1], KeyPress):
                        self.id_after = self.window.after(time, self.stop_press)

                    # On regarde si l'action que l'on vient d'exécuter était "Wait" pour pouvoir 
                    # rappeler "a_turn" après le temps d'attente choisi par l'utilisateur.
                    # --------------------------------------------------------------------------
                    # We check if the action we just executed was "Wait" in order to call 
                    # "a_turn" after the wait time chosen by the user.
                    elif isinstance(self.act_dict_CNTR[self.ctr_of_act_CNTR-1], Wait):
                        self.id_after = self.window.after(time+self.sleep_act_time, self.run)

                    else:
                        # L'action que nous venons d'appeler ne nécessite pas de temps d'attente, alors 
                        # nous appelons "a_turn" pour exécuter l'action suivante.
                        # -----------------------------------------------------------------------------
                        # The action we just called does not require any waiting time, so we call 
                        # "a_turn" to execute the next action.
                        self.window.after(self.sleep_act_time, self.run)
            else:

                # L'utilisateur a décoché l'action pour éviter qu'elle ne s'exécute, alors nous appelons 
                # "a_turn" pour exécuter l'action suivante.
                # --------------------------------------------------------------------------------------
                # The user has unchecked the action to prevent it from executing, so we call "a_turn" to 
                # execute the next action.
                self.window.after(self.sleep_act_time, self.run)
            
        else:
            # On a exécuté chaque action, alors on met "ctr_of_act_CNTR" à 0 pour réexécuter ces actions si 
            # besoin. Ensuite, on appelle "run_act", qui va relâcher les touches pressées,  puis qui vas appeler la 
            # fonction qui l'a initialement appelée et mettre "finish_running" à "False". 
            # ----------------------------------------------------------------------------------------------
            # We have executed each action, so we set "ctr_of_act_CNTR" to 0 to make another pass if needed. 
            # Then, we call "run_act", which will either repeat the loop or call the function that 
            # initially called it.
            self.ctr_of_act_CNTR = 0
            self.finich_running = True
            self.window.after(0, self.run_act)



    def stop_press(self):
        """
        Cette fonction appelle "stop_press" pour "KeyPress" afin de relâcher les touches précédemment 
        pressées, puis on appelle "a_turn" pour exécuter l'action d'après.
        ---------------------------------------------------------------------------------------------
        This function calls "stop_press" for "KeyPress" to release the previously pressed keys, then 
        we call "a_turn" to execute the next action.
        """

        self.act_dict_CNTR[self.ctr_of_act_CNTR-1].stop_press()
        self.window.after(self.sleep_act_time, self.run)



    def add_tree_CNTR(self, text, inter_tree, spacing):
        """
        Cette fonction prend en paramètre la chaîne de caractères représentant l'action qui a été 
        ajoutée au conteneur, l'instance de la classe "IntfTree" qui nous permet d'avoir accès à la 
        frame dans laquelle nous devons ajouter le "Checkbutton" "all_actions", ainsi que la ligne 
        à laquelle nous devons afficher le "Checkbutton" "row_ChkBt". On prend aussi en paramètre 
        l'incrémentation à laquelle doit être positionné le "Checkbutton". 
        Cette fonction permet d'ajouter à l'arbre les actions qui se trouvent dans ce conteneur
        avec l'incrémentation correspondante.
        -------------------------------------------------------------------------------------------
        This function takes as parameters the string representing the action that has been added 
        to the container, the instance of the class "IntfTree", which allows us to access the frame 
        where we need to add the "Checkbutton" called "all_actions", as well as the row where we 
        need to display the "Checkbutton" called "row_ChkBt". We also take as a parameter the 
        increment at which the "Checkbutton" should be positioned. 
        This function allows us to add to the tree the actions that are found in this container 
        with the corresponding increment.
        """

        # On commence par créer la variable "is_checked_act" qui permettra de savoir si le "Checkbutton" 
        # est coché ou non. Ensuite, on crée le "Checkbutton" et on l'affiche dans "all_actions".
        # ------------------------------------------------------------------------------------------------
        # We start by creating the variable "is_checked_act" which will indicate whether the "Checkbutton" 
        # is checked or not. Then, we create the "Checkbutton" and display it in "all_actions".
        is_checked_act = tk.IntVar(value=1)
        ChkBt_act = tk.Checkbutton(inter_tree.all_actions.scrollable_frame, text=text, variable=is_checked_act, bg=inter_tree.w_var.color_1)
        ChkBt_act.grid(row=inter_tree.row_ChkBt+1, column=0, sticky="wn", padx=spacing)

        # On ajoute au dictionnaire qui va contenir tous les "Checkbutton", "dict_tree_CNTR", un tuple 
        # comportant en premier "is_checked_act", qui permet de savoir si le "Checkbutton" est coché ou 
        # non, et le "Checkbutton" ce tuple a pour clé "K_tree_CNTR".
        # ---------------------------------------------------------------------------------------------
        # We add to the dictionary that will contain all the "Checkbuttons", "dict_tree_CNTR", a tuple 
        # consisting first of "is_checked_act", which indicates whether the "Checkbutton" is checked or 
        # not, and the "Checkbutton" itself. This tuple has "K_tree_CNTR" as its key.
        self.dict_tree_CNTR[self.K_tree_CNTR] = [is_checked_act, ChkBt_act]

        # On incrémente "K_tree_CNTR" et "row_ChkBt".
        # -------------------------------------------
        # We increment "K_tree_CNTR" and "row_ChkBt".
        self.K_tree_CNTR += 1
        inter_tree.row_ChkBt += 1


    def text(self):
        """
        Cette fonction retourne une chaîne de caractères appropriée pour la suite d'actions avec les "Checkbutton". 
        Elle retourne une chaîne contenant le maximum d'informations tout en étant la plus courte possible, 
        donc elle abrège certaines informations pour éviter de prendre trop de place dans les menus.
        -----------------------------------------------------------------------------------------------------------
        This function returns a string that is suitable for the sequence of actions with the "Checkbutton." 
        It returns a string containing the maximum amount of information while being as short as possible, thus 
        abbreviating certain information to avoid taking up too much space in the menus.
        """

        if len(self.keys)>5:
            if len(self.list_sp_keys) > 1:
                return f"Same time : {self.keys[:3]}.. | {self.list_sp_keys[0]}.."
            elif len(self.list_sp_keys) == 1:
                return f"Same time : {self.keys[:3]}.. | {self.list_sp_keys[0]}"
            else:
                return f"Same time : {self.keys[:3]}.."

        elif len(self.keys) == 0:
            if len(self.list_sp_keys) > 1:
                return f"Same time : {self.list_sp_keys[0]}.."
            elif len(self.list_sp_keys) == 1:
                return f"Same time : {self.list_sp_keys[0]}"

        else:
            if len(self.list_sp_keys) > 1:
                return f"Same time : {self.keys} | {self.list_sp_keys[0]}.."
            elif len(self.list_sp_keys) == 1:
                return f"Same time : {self.keys} | {self.list_sp_keys[0]}"
            else:
                return f"Same time : {self.keys}"




    def type_act(self):
        """
        Cette fonction retourne le type de cette action sous forme de chaîne de caractères.
        -----------------------------------------------------------------------------------
        This function returns the type of this action as a string.
        """

        return "same time"