from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, List, Tuple, Dict, Set, Any, Union, Optional, Callable, FrozenSet, Iterable, Sequence
from functools import partial

from action_classes import ClickRight, ClickLeft, Write, KeyPress, Wait, Loop, Move, Scroll, KeyLoggerApp, ParallelActions
from enums import LEFT_CONTAINER, SpecialKeys

if TYPE_CHECKING:
    from action_classes import Action
    from main import InterTree
    from enums import MovementType, Direction


class ActionManager:
    """
    Cette classe gère le dictionnaire des actions.
    Elle permet d'ajouter des actions et de lancer l'exécution de la suite d'actions.
    --------------------------------------------------------------------------------------
    This class manages the dictionary of actions.
    It allows actions to be added and the execution of the action sequence to be started.
    """
    def __init__(self, window: tk.Tk, get_most_nested_container: Callable[([dict[int, Action]], Tuple[int, Action])], ui_action_tree: InterTree) -> None:
        """
        Initialisation de la classe ActionManager. Initialisation des variables
        nécessaires à la gestion et à l'exécution des actions.
        
        :param window: Fenêtre principale de l'application.
            elle va particulièrement servir pour les fonctions after
            de tkinter, permettant d'appeler les fonctions de manière asynchrone.
        :param get_most_nested_container: Fonction permettant de récupérer le 
            conteneur le plus imbriqué. Utile pour ajouter des actions dans des 
            conteneurs imbriqués.
        :param ui_action_tree: Instance de la classe InterTree, permettant de gérer l'arborescence des actions.
        ----------------------------------------------------------------------------------------------------
        Initializes the ActionManager class. Initializes the variables
        required for managing and executing actions.
        
        :param window: Main application window.
            It is mainly used for tkinter's after functions,
            which allow functions to be called asynchronously.
        :param get_most_nested_container: Function used to retrieve the
            most deeply nested container. Useful for adding actions
            inside nested containers.
        :param ui_action_tree: Instance of the InterTree class, used to manage the action tree.
        """

        self.window = window
        self.get_most_nested_container = get_most_nested_container
        self.ui_action_tree = ui_action_tree

        # Variable définissant le temps de pause entre chaque action lors de l'exécution.
        # --------------------------------------------------------------------------------
        # Variable defining the pause time between each action during execution.
        self.pause_between_actions = 0

        # Liste servant à sauvegarder les actions pour les recharger plus tard.
        # ----------------------------------------------------------------------
        # List used to save actions in order to reload them later.
        self.save_list: List[List[Any]] = []

        # Dictionnaire contenant les actions.
        # ------------------------------------
        # Dictionary containing the actions.
        self.action_dict: Dict[int, Action] = {}

        # Clé pour le dictionnaire des actions.
        # --------------------------------------
        # Key for the action dictionary.
        self.next_action_key = 0

        # Variable servant à savoir quelle action est en cours d'exécution
        # et si la suite d'actions a fini son exécution.
        # -----------------------------------------------------------------
        # Variable used to track which action is currently being executed
        # and whether the action sequence has finished executing.
        self.current_action_index = 0

        # Variable indiquant si la suite d'actions est en cours d'exécution.
        # ----------------------------------------------------------------------
        # Variable indicating whether the action sequence is currently running.
        self.is_running = False

        # Identifiant de la tâche asynchrone en cours.
        # ---------------------------------------------
        # Identifier of the current asynchronous task.
        self.scheduled_task_id = None


    # ===============================================
    # === SECTION : création de la suite d'action ===
    # -------------------------------------------------
    # === SECTION : creation of the action sequence ===
    # =================================================


    def leave_container(self) -> None:
        """
        Ajoute à la liste de sauvegarde l'information que l'on sort d'un conteneur.
        ----------------------------------------------------------------------------------
        Adds to the save list the information indicating that we are leaving a container.
        """
        self.save_list.append([LEFT_CONTAINER])


    def add_action(self, action: Action, is_in_container: bool) -> None:
        """
        Ajoute une action à la suite d'actions. En fonction de si l'action est 
        ajoutée dans un conteneur ou non, l'action est ajoutée dans le conteneur 
        le plus imbriqué ou à la racine de la suite d'actions. 
        Puis on ajoute l'action à l'arborescence s'il est à la racine de la
        suite d'actions, sinon le conteneur va s'en charger.

        :param action: Instance de l'action à ajouter.
        :param is_in_container: Variation indiquant si l'action est ajoutée dans un conteneur.
        ---------------------------------------------------------------------------------------
        Adds an action to the action sequence. Depending on whether the action
        is added inside a container or not, the action is added to the most
        deeply nested container or to the root of the action sequence.
        Then, the action is added to the tree if it is at the root of the
        action sequence; otherwise, the container handles it.

        :param action: Instance of the action to add.
        :param is_in_container: Flag indicating whether the action is added inside a container.
        """
        # On regarde si l'action est dans un conteneur
        # -----------------------------------------------
        # Check whether the action is inside a container
        if is_in_container:
            # On récupère le conteneur le plus imbriqué en fonction du nombre d'imbrications du dernier conteneur
            # ----------------------------------------------------------------------------------------------------
            # Retrieve the most deeply nested container based on the nesting level of the last container
            nesting_level, most_nested_container = self.get_most_nested_container(self.action_dict, self.next_action_key)
            # On ajoute l'action dans le conteneur
            # -------------------------------------
            # Add the action to the container
            most_nested_container.add_action(action)
            # On donne au conteneur l'action à ajouter dans l'arborescence
            # -------------------------------------------------------------
            # Provide the container with the action to add to the tree
            most_nested_container.add_action_container_tree(action.text(), self.ui_action_tree, nesting_level*10)
        else:
            # On ajoute l'action à la racine de la suite d'actions
            # -----------------------------------------------------
            # Add the action to the root of the action sequence
            self.action_dict[self.next_action_key] = action
            self.next_action_key += 1
            # On ajoute l'action à l'arborescence
            # ------------------------------------
            # Add the action to the tree
            self.ui_action_tree.add_tree(action.text())


    def add_left_click(self, position_x: int, position_y: int, is_in_container: bool) -> None:
        """
        Ajoute une action de clic gauche à la suite d'actions.
        
        :param position_x: Position X du clic.
        :param position_y: Position Y du clic.
        :param is_in_container: Variation indiquant si l'action est ajoutée dans un conteneur.
        ----------------------------------------------------------------------------------------
        Adds a left-click action to the action sequence.
        
        :param position_x: X position of the click.
        :param position_y: Y position of the click.
        :param is_in_container: Flag indicating whether the action is added inside a container.
        """
        # Crée une instance de ClickLeft avec les positions données.
        # -----------------------------------------------------------
        # Create a ClickLeft instance with the given positions.
        action = ClickLeft(position_x, position_y)
        # Ajoute les informations de l'action à la liste de sauvegarde.
        # --------------------------------------------------------------
        # Add the action information to the save list.
        self.save_list.append([action.action_type(), position_x, position_y])
        # Ajoute l'action à la suite d'actions, et à l'arborescence.
        # -----------------------------------------------------------
        # Add the action to the action sequence and to the tree.
        self.add_action(action, is_in_container)


    def add_right_click(self, position_x: int, position_y: int, is_in_container: bool) -> None:
        """
        Ajoute une action de clic droit à la suite d'actions.
        
        :param position_x: Position X du clic.
        :param position_y: Position Y du clic.
        :param is_in_container: Variation indiquant si l'action est ajoutée dans un conteneur.
        ---------------------------------------------------------------------------------------
        Adds a right-click action to the action sequence.
        
        :param position_x: X position of the click.
        :param position_y: Y position of the click.
        :param is_in_container: Flag indicating whether the action is added inside a container.
        """
        # Crée une instance de ClickRight avec les positions données.
        # ------------------------------------------------------------
        # Create a ClickRight instance with the given positions.
        action = ClickRight(position_x, position_y)
        # Ajoute les informations de l'action à la liste de sauvegarde.
        # --------------------------------------------------------------
        # Add the action information to the save list.
        self.save_list.append([action.action_type(), position_x, position_y])
        # Ajoute l'action à la suite d'actions, et à l'arborescence.
        # -----------------------------------------------------------
        # Add the action to the action sequence and to the tree.
        self.add_action(action, is_in_container)


    def add_move(self, position_x: int, position_y: int, move_type: MovementType, is_in_container: bool) -> None:
        """
        Ajoute une action de déplacement de souris à la suite d'actions.
        
        :param position_x: Position X du déplacement de souris.
        :param position_y: Position Y du déplacement de souris.
        :param move_type: Type de mouvement (relatif ou absolu).
        :param is_in_container: Variation indiquant si l'action est ajoutée dans un conteneur.
        ----------------------------------------------------------------------------------------
        Adds a mouse movement action to the action sequence.
        
        :param position_x: X position of the mouse movement.
        :param position_y: Y position of the mouse movement.
        :param move_type: Type of movement (relative or absolute).
        :param is_in_container: Flag indicating whether the action is added inside a container.
        """
        # Crée une instance de Move avec les positions données et le type de mouvement.
        # ------------------------------------------------------------------------------
        # Create a Move instance with the given positions and movement type.
        action = Move(position_x, position_y, move_type)
        # Ajoute les informations de l'action à la liste de sauvegarde.
        # --------------------------------------------------------------
        # Add the action information to the save list.
        self.save_list.append([action.action_type(), position_x, position_y, move_type])
        # Ajoute l'action à la suite d'actions, et à l'arborescence.
        # -----------------------------------------------------------
        # Add the action to the action sequence and to the tree.
        self.add_action(action, is_in_container)


    def add_write(self, text: str, is_in_container: bool) -> None:
        """
        Ajoute une action d'écriture à la suite d'actions.
        
        :param text: Texte à écrire.
        :param is_in_container: Variation indiquant si l'action est ajoutée dans un conteneur.
        ----------------------------------------------------------------------------------------
        Adds a typing action to the action sequence.
        
        :param text: Text to type.
        :param is_in_container: Flag indicating whether the action is added inside a container.
        """
        # Crée une instance de Write avec le texte donné.
        # ------------------------------------------------
        # Create a Write instance with the given text.
        action = Write(text)
        # Ajoute les informations de l'action à la liste de sauvegarde.
        # --------------------------------------------------------------
        # Add the action information to the save list.
        self.save_list.append([action.action_type(), text])
        # Ajoute l'action à la suite d'actions, et à l'arborescence.
        # -----------------------------------------------------------
        # Add the action to the action sequence and to the tree.
        self.add_action(action, is_in_container)


    def add_scroll(self, number_of_steps: int, scroll_direction: Direction, is_in_container: bool) -> None:
        """
        Ajoute une action de déplacement de souris à la suite d'actions.
        
        :param number_of_steps: Nombre de pas de scroll.
        :param scroll_direction: Direction du scroll.
        :param is_in_container: Variation indiquant si l'action est ajoutée dans un conteneur.
        ----------------------------------------------------------------------------------------
        Adds a mouse scroll action to the action sequence.
        
        :param number_of_steps: Number of scroll steps.
        :param scroll_direction: Scroll direction.
        :param is_in_container: Flag indicating whether the action is added inside a container.
        """
        # Crée une instance de Scroll avec le nombre de pas et la direction donnés.
        # --------------------------------------------------------------------------
        # Create a Scroll instance with the given number of steps and direction.
        action = Scroll(number_of_steps, scroll_direction)
        # Ajoute les informations de l'action à la liste de sauvegarde.
        # --------------------------------------------------------------
        # Add the action information to the save list.
        self.save_list.append([action.action_type(), number_of_steps, scroll_direction])
        # Ajoute l'action à la suite d'actions, et à l'arborescence.
        # -----------------------------------------------------------
        # Add the action to the action sequence and to the tree.
        self.add_action(action, is_in_container)


    def add_wait(self, wait_time: float, is_in_container: bool) -> None:
        """
        Ajoute une action d'attente à la suite d'actions.
        
        :param wait_time: Temps d'attente.
        :param is_in_container: Variation indiquant si l'action est ajoutée dans un conteneur.
        ----------------------------------------------------------------------------------------
        Adds a wait action to the action sequence.
        
        :param wait_time: Waiting time.
        :param is_in_container: Flag indicating whether the action is added inside a container.
        """
        # Crée une instance de Wait avec le temps d'attente donné.
        # ---------------------------------------------------------
        # Create a Wait instance with the given waiting time.
        action = Wait(wait_time)
        # Ajoute les informations de l'action à la liste de sauvegarde.
        # --------------------------------------------------------------
        # Add the action information to the save list.
        self.save_list.append([action.action_type(), wait_time])
        # Ajoute l'action à la suite d'actions, et à l'arborescence.
        # -----------------------------------------------------------
        # Add the action to the action sequence and to the tree.
        self.add_action(action, is_in_container)


    def add_key_press(self, keys_to_press: str, special_keys_to_press: SpecialKeys, press_duration: float, is_in_container: bool) -> None:
        """
        Ajoute une action de pression de touche à la suite d'actions.
        
        :param keys_to_press: Touches à presser.
        :param special_keys_to_press: Touches spéciales à presser.
        :param press_duration: Temps de pression.
        :param is_in_container: Variation indiquant si l'action est ajoutée dans un conteneur.
        ----------------------------------------------------------------------------------------
        Adds a key press action to the action sequence.
        
        :param keys_to_press: Keys to press.
        :param special_keys_to_press: Special keys to press.
        :param press_duration: Press duration.
        :param is_in_container: Flag indicating whether the action is added inside a container.
        """
        # Crée une instance de KeyPress avec les touches et le temps donnés.
        # -------------------------------------------------------------------
        # Create a KeyPress instance with the given keys and duration.
        action = KeyPress(keys_to_press, special_keys_to_press, press_duration)
        # Ajoute les informations de l'action à la liste de sauvegarde.
        # --------------------------------------------------------------
        # Add the action information to the save list.
        self.save_list.append([action.action_type(), keys_to_press, special_keys_to_press, press_duration])
        # Ajoute l'action à la suite d'actions, et à l'arborescence.
        # -----------------------------------------------------------
        # Add the action to the action sequence and to the tree.
        self.add_action(action, is_in_container)


    def add_parallel_actions(self, keys_to_press: str, special_keys_to_press: SpecialKeys, container_name: str, is_in_container: bool) -> None:
        """
        Ajoute une action de pression de touche simultanément 
        à d'autres actions dans la suite d'actions.
        
        :param keys_to_press: Touches à presser.
        :param special_keys_to_press: Touches spéciales à presser.
        :param name: Nom de l'action.
        :param is_in_container: Variation indiquant si l'action est ajoutée dans un conteneur.
        ----------------------------------------------------------------------------------------
        Adds an action that presses keys simultaneously
        with other actions in the action sequence.
        
        :param keys_to_press: Keys to press.
        :param special_keys_to_press: Special keys to press.
        :param name: Action name.
        :param is_in_container: Flag indicating whether the action is added inside a container.
        """
        # Crée une instance de ParallelActions avec les touches, le temps donnés et le nom.
        # ---------------------------------------------------------------------------
        # Create a ParallelActions instance with the given keys, special keys, and name.
        action = ParallelActions(self.window, keys_to_press, special_keys_to_press, container_name)
        # Ajoute les informations de l'action à la liste de sauvegarde.
        # --------------------------------------------------------------
        # Add the action information to the save list.
        self.save_list.append([action.action_type(), keys_to_press, special_keys_to_press, container_name])
        # Ajoute l'action à la suite d'actions, et à l'arborescence.
        # -----------------------------------------------------------
        # Add the action to the action sequence and to the tree.
        self.add_action(action, is_in_container)


    def add_loop(self, number_of_iterations: int, loop_name: str, is_in_container: bool) -> None:
        """
        Ajoute une action de boucle permettant de répéter plusieurs
        fois d'autres actions dans la suite d'actions.
        
        :param number_of_iterations: Nombre de tours de boucle.
        :param loop_name: Nom de la boucle.
        :param is_in_container: Variation indiquant si l'action est ajoutée dans un conteneur.
        ----------------------------------------------------------------------------------------
        Adds a loop action that allows repeating
        other actions multiple times in the action sequence.
        
        :param number_of_iterations: Number of loop iterations.
        :param loop_name: Loop name.
        :param is_in_container: Flag indicating whether the action is added inside a container.
        """
        # Crée une instance de Loop avec le nombre de tours et le nom donnés.
        # ---------------------------------------------------------------------
        # Create a Loop instance with the given number of iterations and name.
        action = Loop(self.window, number_of_iterations, loop_name)
        # Ajoute les informations de l'action à la liste de sauvegarde.
        # --------------------------------------------------------------
        # Add the action information to the save list.
        self.save_list.append([action.action_type(), number_of_iterations, loop_name])
        # Ajoute l'action à la suite d'actions, et à l'arborescence.
        # -----------------------------------------------------------
        # Add the action to the action sequence and to the tree.
        self.add_action(action, is_in_container)


    def clean_container_tree(self, container_instance:Loop|ParallelActions) -> None:
        """
        Parcourt le dictionnaire contenant les éléments de l'arborescence des conteneurs (container_action_checkbuttons),
        et détruit les Checkbutton qu'il contient afin de les supprimer de l'arborescence.
        
        :param container_instance: Conteneur dont on veut nettoyer l'arborescence.
        ---------------------------------------------------------------------------------------------------
        Iterates over the dictionary containing the container tree elements (container_action_checkbuttons)
        and destroys the Checkbutton widgets it contains in order to remove them
        from the tree structure.
        
        :param container_instance: Container whose tree structure needs to be cleaned.
        """
        for checkbox_button in container_instance.container_action_checkbuttons.values():
            checkbox_button[1].destroy()


    def find_containers_recursively(self, container_instance:Loop|ParallelActions) -> None:
        """
        Parcourt le dictionnaire d'actions (container_actions_dict) d'un conteneur (Loop ou ParallelActions).
        Si une action est elle-même un conteneur, la fonction s'appelle récursivement sur cette 
        action et appelle clean_container_tree afin de supprimer les actions dans 
        l'arborescence du conteneur.
        
        :param container_instance: Conteneur à analyser récursivement.
        ---------------------------------------------------------------------------------------------
        Iterates over the action dictionary (container_actions_dict) of a container
        (Loop or ParallelActions).
        If an action is itself a container, the function calls itself recursively
        on that action and then calls clean_container_tree in order to remove
        the actions from the container tree structure.
            
        :param container_instance: Container to be analyzed recursively.
        """
        for current_action in container_instance.container_actions_dict.values():
            if isinstance(current_action, Loop) or isinstance(current_action, ParallelActions):
                self.find_containers_recursively(current_action)
                self.clean_container_tree(current_action)


    def reset_state(self) -> None:
        """
        Remet les variables de la classe à leur valeur initiale
        et nettoie les arborescences des conteneurs.
        --------------------------------------------------------
        Resets the class variables to their initial values
        and cleans the container tree structures.
        """
        for current_action in self.action_dict.values():
            if isinstance(current_action, Loop) or isinstance(current_action, ParallelActions):
                self.find_containers_recursively(current_action)
                self.clean_container_tree(current_action)

        self.action_dict = {}
        self.next_action_key = 0
        self.save_list = []
        self.current_action_index = 0
        self.is_running = False
        self.scheduled_task_id = None


    # ================================================
    # === SECTION : execution de la suite d'action ===
    # --------------------------------------------------
    # === SECTION : execution of the action sequence ===
    # ==================================================


    def cancel_task(self) -> None:
        """
        Cette fonction permet de stopper l'exécution de la suite d'actions en cours. 
        Elle est appelée par une instance de KeyLoggerApp.

        - Si la dernière action appelée est une instance de KeyPress,
          on relâche les touches pressées.
        - Si la dernière action appelée est un conteneur,
          on arrête son exécution via cancel_task (il appliquera la même logique).
        - Si une fonction qui a été appelée avec window.after (par exemple, 
          pour "wait", on utilise "window.after"), on annule l'appel.
        - On réinitialise les variables d'état de l'exécution.
        - On crée une popup pour indiquer à l'utilisateur que l'exécution a été arrêtée.
        ----------------------------------------------------------------------------------------
        Stops the execution of the current action sequence.
        This method is called by an instance of KeyLoggerApp.

        - If the last called action is an instance of KeyPress,
          release the pressed keys.
        - If the last called action is a container,
          stop its execution via cancel_task (it will apply the same logic).
        - If a function was scheduled using window.after (for example,
          for a Wait action), the call is canceled.
        - Execution state variables are reset.
        - A popup is displayed to inform the user that execution has stopped.
        """

        if self.current_action_index > 0:
            # Si la dernière action appelée est une instance de KeyPress,
            # on relâche les touches pressées.
            # ------------------------------------------------------------
            # If the last called action is an instance of KeyPress,
            # release the pressed keys.
            if isinstance(self.action_dict[self.current_action_index-1], KeyPress):
                self.action_dict[self.current_action_index-1].release_keys()

            # Si la dernière action appelée est un conteneur,
            # on arrête son exécution via cancel_task (il appliquera la même logique).
            # -------------------------------------------------------------------------
            # If the last called action is a container,
            # stop its execution via cancel_task (it will apply the same logic).
            elif isinstance(self.action_dict[self.current_action_index-1], ParallelActions) or isinstance(self.action_dict[self.current_action_index-1], Loop):
                self.action_dict[self.current_action_index-1].cancel_task()


        # Si une fonction qui a été appelée avec window.after (par exemple, 
        # pour "wait", on utilise "window.after"), on annule l'appel.
        # ------------------------------------------------------------------
        # If a function was scheduled using window.after, cancel it.
        if self.scheduled_task_id is not None:
            self.window.after_cancel(self.scheduled_task_id)
            self.scheduled_task_id = None
        # On réinitialise les variables d'état de l'exécution. 
        # -----------------------------------------------------
        # Reset execution state variables.
        self.current_action_index = 0
        self.is_running = False
        # On crée une popup pour indiquer à l'utilisateur que l'exécution a été arrêtée.
        # -------------------------------------------------------------------------------
        # Display a popup informing the user that execution has stopped.
        self.create_popup()


    def call_release_keys(self) -> None:
        """
        Permet d'appeler la méthode "release_keys" de l'action "KeyPress" en cours d'exécution.
        Puis de relancer l'exécution de la suite d'actions après un temps de pause défini.
        --------------------------------------------------------------------------------------
        Calls the release_keys method of the currently executing KeyPress action,
        then resumes execution of the action sequence after a defined pause time.
        """
        self.action_dict[self.current_action_index-1].release_keys()
        self.scheduled_task_id = self.window.after(self.pause_between_actions, self.start_execution)


    def start_execution(self, is_first_call: bool=True) -> None:
        """
        Lance l'exécution de la suite d'actions.
        Cette fonction s'appelle elle-même de manière asynchrone pour exécuter chaque
        action de la suite d'actions l'une après l'autre. Afin de savoir l'action en cours
        d'exécution.
        On utilise la variable current_action_index qui est incrémentée à chaque appel de cette 
        fonction.
        Lorsqu'une action est un conteneur (Loop/ParallelActions), on appelle la méthode 
        run de ce conteneur qui s'occupe de l'exécution des actions qu'il contient, 
        puis quand il aura fini, il va rappeler la fonction start_execution, et l'exécution de 
        la suite d'action à la racine reprendra là où elle s'était arrêtée.

        :param is_first_call: Cette variable permet de savoir si l'exécution commence 
            (si l'utilisateur vient d'appuyer sur un des boutons Start ou si elle a été 
            appelée dans la continuité de l'exécution de la suite d'actions). 
            Celle-ci vaut False si c'est le premier appel, sinon elle vaut True.
        -----------------------------------------------------------------------------------
        Starts execution of the action sequence.
        This function calls itself asynchronously to execute each action
        in the sequence one after another.
        The variable current_action_index is used to track the current action index
        and is incremented at each call.

        When an action is a container (Loop/ParallelActions), its run method
        is called to execute the actions it contains. Once finished,
        it calls start_execution again so that execution of the root action sequence
        resumes where it left off.

        :param is_first_call: This variable indicates whether execution is starting 
            (i.e., whether the user has just clicked one of the Start buttons or whether 
            it was called as part of the ongoing execution of the action sequence). 
            It is set to False if this is the first call, otherwise it is set to True.
        """


        # Si is_first_call est faux (premier appel / appel venant d'un des boutons Start) et que 
        # is_running est faux, on crée l'instance de KeyLoggerApp pour permettre l'arrêt de l'exécution 
        # via des touches clavier. (La vérification de is_first_call permet d'éviter des bugs à cause de 
        # KeyLoggerApp, qui met is_running à False alors que des appels de start_execution peuvent 
        # encore se produire.)
        # -------------------------------------------------------------------------------------------------
        # If is_first_call is False (first call / call coming from one of the Start buttons) and 
        # is_running is False, we create an instance of KeyLoggerApp to allow stopping execution 
        # via keyboard inputs. (Checking is_first_call helps prevent bugs caused by 
        # KeyLoggerApp setting is_running to False while start_execution calls may 
        # still occur.)
        if not is_first_call and not self.is_running:
            KeyLoggerApp.stop_run = False
            app = KeyLoggerApp(self.cancel_task)

        # Si is_first_call est faux (premier appel / appel venant d'un des boutons Start) et que 
        # is_running est faux, ou si is_first_call est vrai (n'importe quel appel de start_execution 
        # sauf venant d'un des boutons Start) et si la suite d'actions est en cours d'exécution,
        # on lance l'exécution de la suite d'actions.
        # -------------------------------------------------------------------------------
        # If is_first_call is False (first call / call coming from one of the Start buttons) and 
        # is_running is False, or if is_first_call is True (any call to start_execution except those 
        # coming from the Start buttons) and the action sequence is currently running,
        # we start executing the action sequence.
        if (not is_first_call and not self.is_running) or self.is_running and is_first_call:
            # On indique que la suite d'actions est en cours d'exécution.
            # ------------------------------------------------------------
            # Indicate that the action sequence is running.
            self.is_running = True
            
            # On regarde si on n'est pas à la fin de la suite d'actions 
            # et que l'utilisateur n'a pas demandé l'arrêt.
            # ----------------------------------------------------------
            # Check that we are not at the end of the action sequence
            # and that the user has not requested to stop execution.
            if not self.current_action_index >= self.next_action_key and not KeyLoggerApp.stop_run:
                self.current_action_index += 1
                
                # On regarde si l'action que l'on doit exécuter n'a pas été désactivée
                # par l'utilisateur dans l'arborescence.
                # ---------------------------------------------------------------------
                # Check whether the action to be executed has not been disabled
                # by the user in the tree.
                if list(self.ui_action_tree.action_checkbuttons_dict[self.current_action_index-1])[0].get() == 1:
                    # Si l'action est un conteneur on appelle sa methode d'execution.
                    # ----------------------------------------------------------------
                    # If the action is a container, call its execution method.
                    if isinstance(self.action_dict[self.current_action_index-1], Loop) or isinstance(self.action_dict[self.current_action_index-1], ParallelActions):
                        # On donne a run la fonction start_execution pour quelle puisse 
                        # rappeler la fonction start_execution une fois quelle a fini d'executer les actions 
                        # qu'elle contient et on donne aussi le temps de pause entre chaque action.
                        # --------------------------------------------------------------------------
                        # Provide the start_execution function so the container can call it again
                        # once it has finished executing its actions, along with the pause time.
                        self.window.after(0, lambda : self.action_dict[self.current_action_index-1].run(self.start_execution, self.pause_between_actions))
                    
                    else:
                        # Si l'action n'est pas un conteneur on execute l'action
                        # on recupere le temps que doit attendre avant d'appeler laction 
                        # suivante quelle retourne si elle en a un.
                        # ------------------------------------------------------------------
                        # If the action is not a container, execute the action.
                        # Retrieve the waiting time before calling the next action, if any.
                        wait_duration = self.action_dict[self.current_action_index-1].run()


                        # Garde pour éviter les accès invalides après un arrêt.
                        # Empêche les bugs causés par la remise à zéro de current_action_index,
                        # qui sert de clé pour le dictionnaire.
                        # -----------------------------------------------------
                        # Protection to prevent invalid accesses after a stop.
                        # Prevents bugs caused by resetting current_action_index,
                        # which is used as the dictionary key.
                        if self.current_action_index <= 0: 
                            return

                        # On regarde si l'action que l'on vient d'exécuter était KeyPress pour pouvoir 
                        # appeler call_release_keys après le temps d'attente choisi par l'utilisateur.
                        # -----------------------------------------------------------------------------
                        # If the executed action was a KeyPress, call call_release_keys
                        # after the user-defined wait time.
                        if isinstance(self.action_dict[self.current_action_index-1], KeyPress):
                            self.scheduled_task_id = self.window.after(wait_duration, self.call_release_keys)

                        # On regarde si l'action que l'on vient d'exécuter était Wait pour pouvoir 
                        # rappeler start_execution après le temps d'attente choisi par l'utilisateur.
                        # -------------------------------------------------------------------------
                        # If the executed action was a Wait, call start_execution again
                        # after the user-defined wait time.
                        elif isinstance(self.action_dict[self.current_action_index-1], Wait):
                            self.scheduled_task_id = self.window.after(wait_duration+self.pause_between_actions, self.start_execution)
                        
                        else:
                            # L'action que nous venons d'appeler ne nécessite pas de temps d'attente, alors 
                            # nous appelons start_execution pour exécuter l'action suivante.
                            # ------------------------------------------------------------------------------
                            # The executed action does not require waiting time,
                            # so call start_execution to execute the next action.
                            self.window.after(self.pause_between_actions, self.start_execution)
                else:
                    # On passe à l'action suivante si celle-ci est désactivée.
                    # -----------------------------------------------------------
                    # Move on to the next action if the current one is disabled.
                    self.window.after(self.pause_between_actions, self.start_execution)
                
            else:
                # On réinitialise les variables pour une prochaine exécution et
                # on indique à l'utilisateur que la suite d'actions a fini son exécution
                # -----------------------------------------------------------------------
                # Reset variables for the next execution and
                # inform the user that the action sequence has finished executing.
                self.current_action_index = 0
                self.is_running = False
                self.create_popup()


    def create_popup(self) -> None:
        """
        Crée une popup indiquant que le programme a fini de s'exécuter.
        ------------------------------------------------------------------
        Creates a popup indicating that the program has finished running.
        """
        popup = tk.Toplevel(self.window)
        popup.title("Popup")
        popup.geometry("200x100")

        label = tk.Label(popup, text="The program has finished running")
        label.pack(pady=10)
