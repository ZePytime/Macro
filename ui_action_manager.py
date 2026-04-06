from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Callable, Dict, Tuple


from ui_action_frames.ui_move_frame import MouseMoveFrame
from ui_action_frames.ui_click_frame import ClickFrame
from ui_action_frames.ui_wait_frame import WaitFrame
from ui_action_frames.ui_write_frame import WriteFrame
from ui_action_frames.ui_loop_frame import LoopFrame
from ui_action_frames.ui_keyhold_frame import KeyHoldFrame
from ui_action_frames.ui_scroll_frame import ScrollFrame
from ui_action_frames.ui_parallel_actions_frame import ParallelActionsFrame
from action_manager import ActionManager
from container_manager import ContainerManager
from action_classes import KeyPosition, position_mouse
from enums import ActionType

if TYPE_CHECKING:
    from main import WindowVariable
    from ui_action_tree import TreeUI

class ActionSelectorUI:
    """
    Cette classe permet à l'utilisateur d'ajouter des actions à sa suite.
    ----------------------------------------------------------------------
    This class allows the user to add actions to their action sequence.
    """
    def __init__(self, window: tk.Tk, menu_btn_frame: tk.Frame, switch_frame: Callable[[tk.Frame], None], w_var: WindowVariable, ui_action_tree: TreeUI) -> None:
        """
        Initialisation de tous les widgets permettant l'ajout d'actions à la suite d'actions.

        :param window: Fenêtre principale dans laquelle va se trouver ce menu
        :param menu_btn_frame: Menu dans lequel on ajoute le bouton
            permettant de basculer vers cette interface
        :param switch_frame: Fonction permettant de changer de frame
            afin d'afficher cette interface
        :param w_var: Objet contenant les paramètres d'affichage 
            (couleurs, tailles, screen_width/height...)
        :param ui_action_tree: Instance de TreeUI nécessaire pour la création 
            d'une instance de ActionManager.
        --------------------------------------------------------------------------------------
        Initializes all widgets that allow adding actions to the action sequence.

        :param window: Main window in which this menu will be displayed
        :param menu_btn_frame: Menu frame in which the button allowing
            switching to this interface is added
        :param switch_frame: Function allowing the frame to be switched
            in order to display this interface
        :param w_var: Object containing display parameters
            (colors, sizes, screen_width/height...)
        :param ui_action_tree: Instance of TreeUI required to create
            an instance of ActionManager
        """

        self.window = window

        # Variable permettant de savoir si l'utilisateur est dans la partie 
        # move ou click de l'interface, et qu'il faut donc oui ou non afficher les 
        # coordonnées de la souris de l'utilisateur en temps réel.
        # --------------------------------------------------------------------------
        # Variable indicating whether the user is currently in the move
        # or click part of the interface, and therefore whether the mouse
        # coordinates should be displayed in real time.
        self.in_move_or_click = True

        # Variable permettant de savoir si l'utilisateur est dans ce menu
        # afin de déterminer s'il faut afficher les coordonnées de la souris
        # de l'utilisateur en temps réel
        # -------------------------------------------------------------------
        # Variable indicating whether the user is currently in this menu,
        # used to determine whether mouse coordinates should be displayed
        # in real time.
        self.in_action_selector = True

        # Bouton permettant d'accéder au menu ActionSelectorUI.
        # -----------------------------------------------------
        # Button allowing access to the ActionSelectorUI menu.
        self.selector_button = tk.Button(
            menu_btn_frame, 
            text="selector", 
            bg=w_var.color_2, 
            fg="black", 
            height=1, 
            width=5, 
            font=w_var.font_size, 
            command=lambda : switch_frame(self.selector_frame)
            )
        self.selector_button.grid(row=0, column=0)

        # Frame principale du menu
        # -------------------------
        # Main frame of the menu
        self.selector_frame = tk.Frame(window, bg=w_var.color_1, width=320, height=450)
        self.selector_frame.grid_propagate(False)

        # On crée toutes les frames pour chaque action.
        # ------------------------------------------------
        # Create all frames corresponding to each action.
        click_frame = tk.Frame(self.selector_frame, bg=w_var.color_1)
        move_frame = tk.Frame(self.selector_frame, bg=w_var.color_1) 
        write_frame = tk.Frame(self.selector_frame, bg=w_var.color_1)
        scroll_frame = tk.Frame(self.selector_frame, bg=w_var.color_1)
        wait_frame = tk.Frame(self.selector_frame, bg=w_var.color_1)
        pressed_frame = tk.Frame(self.selector_frame, bg=w_var.color_1)
        parallel_actions_frame = tk.Frame(self.selector_frame, bg=w_var.color_1)
        loop_frame = tk.Frame(self.selector_frame, bg=w_var.color_1)
        # On affiche frame_click car c'est la frame par défaut lorsqu'on ouvre le 
        # programme, et on attribue à current_frame la frame sur laquelle on se trouve.
        # ----------------------------------------------------------------------------
        # Display frame_click as it is the default frame when the program starts,
        # and assign it to current_frame.
        click_frame.grid(row=7, column=0)
        self.current_frame  = click_frame

        # On crée la frame qui va contenir tous les Radiobutton, qui vont nous 
        # permettre de passer d'une frame d'une action à une autre.
        # ---------------------------------------------------------------------
        # Create the frame that will contain all Radiobuttons,
        # allowing switching between different action frames.
        self.radiobuttons_frame = tk.Frame(self.selector_frame, bg=w_var.color_1)
        self.radiobuttons_frame.grid(row=1, column=0, sticky="nw")

        # On crée un dictionnaire pour faciliter la création des Radiobutton.
        # --------------------------------------------------------------------
        # Create a dictionary to simplify Radiobutton creation.
        RADIO_ELEMENTS: Dict[str, Tuple[str, tk.Frame, int, int]] = {
            ActionType.CLICK_LEFT.value:("click left", click_frame, 1, 0), ActionType.CLICK_RIGHT.value:("click right", click_frame, 2, 0), 
            ActionType.MOVE.value:("move", move_frame, 3, 0), ActionType.WRITE.value:("write", write_frame, 1, 2), 
            ActionType.SCROLL.value:("scroll", scroll_frame, 2, 2), ActionType.WAIT.value:("wait", wait_frame, 3, 2), 
            ActionType.KEY_PRESS.value:("key press", pressed_frame, 1, 3), 
            ActionType.PARALLEL_ACTIONS.value:("parallel actions", parallel_actions_frame, 2, 3), 
            ActionType.LOOP.value:("loop", loop_frame, 3, 3)
            }

        # On sélectionne le Radiobutton ActionType.CLICK_LEFT car c'est l'action affichée par défaut.
        # --------------------------------------------------------------------------------------------
        # Select the ActionType.CLICK_LEFT Radiobutton, as it is the default displayed action.
        self.selected_action_key = tk.StringVar(value=ActionType.CLICK_LEFT.value)

        # On crée le dictionnaire qui va contenir tous les Radiobutton.
        # --------------------------------------------------------------
        # Dictionary that will contain all Radiobuttons.
        radiobuttons_dict = {}

        # On parcourt le dictionnaire RADIO_ELEMENTS pour créer tous les Radiobutton
        # permettant de basculer entre les différentes actions, puis on les ajoute
        # au dictionnaire radiobuttons_dict et on les affiche.
        # ------------------------------------------------------------------------------
        # Iterate through RADIO_ELEMENTS to create all Radiobuttons
        # allowing switching between actions, then add them to radiobuttons_dict
        # and display them.
        for key, (action_label, frame, radio_row, radio_column) in RADIO_ELEMENTS.items():
            radiobuttons_dict[key] = tk.Radiobutton(
                self.radiobuttons_frame, 
                text=action_label, 
                variable=self.selected_action_key, 
                value=key, 
                background=w_var.color_1, 
                command=lambda next_frame=frame, 
                action_key=key: self.switch_to_action_frame(next_frame, action_key)
                )
            radiobuttons_dict[key].grid(row=radio_row, column=radio_column, sticky="nw")

        # On crée l'instance de ContainerManager qui gère les conteneurs 
        # (parallel actions/loop).
        # ---------------------------------------------------------------
        # Create the ContainerManager instance that manages containers
        # (parallel actions / loops).
        self.container_manager = ContainerManager(w_var, self.selector_frame)

        # On crée les instances des classes qui vont créer les interfaces 
        # pour chaque action.
        # ----------------------------------------------------------------
        # Create instances of the classes that build the interfaces
        # for each action.
        self.click_ui = ClickFrame(click_frame, w_var)
        self.move_ui = MouseMoveFrame(move_frame, w_var)
        self.write_ui = WriteFrame(write_frame, w_var)
        self.scroll_ui = ScrollFrame(scroll_frame, w_var)
        self.wait_ui = WaitFrame(wait_frame, w_var)
        self.pressed_ui = KeyHoldFrame(pressed_frame, w_var)
        self.parallel_actions_ui = ParallelActionsFrame(parallel_actions_frame, w_var, self.container_manager)
        self.loop_ui = LoopFrame(loop_frame, w_var, self.container_manager)

        # On met à jour les positions de la souris en temps réel 
        # sur l'interface de clic.
        # -------------------------------------------------------
        # Update mouse positions in real time
        # on the click interface.
        self.update_mouse_positions()

        # On crée l'instance d'ActionManager, cette classe s'occupe de gérer
        # le dictionnaire qui contiendra toutes les actions.
        # -------------------------------------------------------------------
        # Create the ActionManager instance, which manages
        # the dictionary containing all actions.
        self.action_manager = ActionManager(window, self.container_manager.get_most_nested_container, ui_action_tree)

        # On donne la fonction leave_container à leave_container_callback
        # de l'instance de ContainerManager, ce qui permet de mettre à jour
        # la liste d'enregistrement lorsqu'on quitte un conteneur.
        # ------------------------------------------------------------------
        # Assign the leave_container function to the
        # leave_container_callback of ContainerManager.
        # This allows updating the registration list
        # when leaving a container.
        self.container_manager.leave_container_callback = self.action_manager.leave_container

        # On crée une instance de KeyPosition (cette classe permet d'observer les 
        # relâchements et pressions des touches). Si l'utilisateur presse les 
        # deux touches correspondantes, on appelle "set_coordinate", qui va entrer dans 
        # les zones de saisie correspondantes les coordonnées données en paramètre.
        # ------------------------------------------------------------------------------
        # Create a KeyPosition instance (this class listens to
        # key presses and releases). If the user presses the
        # corresponding keys, "set_coordinate" is called to
        # insert the mouse coordinates into the relevant input fields.
        self.key_position_listener = KeyPosition(self.click_ui.set_coordinate, self.move_ui.set_coordinate)

        # On crée le bouton pour valider la création d'actions.
        # ------------------------------------------------------
        # Create the button used to validate action creation.
        self.check_button = tk.Button(
            self.selector_frame, 
            text="check", 
            bg=w_var.color_2, 
            fg="black", 
            height=1, 
            width=9, 
            font=w_var.font_size, 
            command=self.validate_and_add_action
            )
        self.check_button.grid(row=8, column=0)

        # On crée le bouton pour lancer l'exécution de la suite d'actions.
        # -----------------------------------------------------------------
        # Create the button used to start executing the action sequence.
        self.start_button = tk.Button(
            self.selector_frame, 
            text="start", 
            bg=w_var.color_2, 
            fg="black", 
            height=1, 
            width=9, 
            font=w_var.font_size, 
            command=lambda : self.action_manager.start_execution(False)
            )
        self.start_button.grid(row=9, column=0)


    def validate_and_add_action(self) -> None:
        """
        Cette fonction est appelée par le bouton check_button et elle permet de 
        récupérer les arguments entrés par l'utilisateur pour créer les actions.
        -------------------------------------------------------------------------
        This function is called by the check_button and allows retrieving
        the arguments entered by the user in order to create actions.
        """

        # On vérifie que la suite d'actions n'est pas en cours d'exécution.
        # ------------------------------------------------------------------
        # Check that the action sequence is not currently running.
        if not self.action_manager.is_running:

            # On récupère la valeur du Radiobutton choisie par l'utilisateur.
            # (le type d'action à créer)
            # ----------------------------------------------------------------
            # Retrieve the value of the Radiobutton selected by the user
            # (the type of action to create).
            selected_action = self.selected_action_key.get()

            # On cherche le bon type d'action. On appelle la fonction check 
            # de l'instance correspondante au type d'action.
            # - Soit elle retourne False (paramètres invalides) et on ne fait rien.
            # - Soit elle retourne les paramètres entrés par l'utilisateur, 
            #   et onappelle add_... de action_manager, qui va créer l'action 
            #   et l'ajouter au dictionnaire des actions. 
            # Pour loop et parallel actions, on appelle les fonctions indicate_container 
            # et add_container de container_manager, car ce sont des conteneurs.
            # ---------------------------------------------------------------------------
            # Find the correct action type and call the corresponding
            # instance's check method.
            # - If it returns False, parameters are invalid and nothing is done.
            # - Otherwise, the parameters are passed to the appropriate
            #   add_... method of action_manager, which creates the action
            #   and adds it to the action dictionary.
            # For loop and parallel actions, container-related methods
            # of container_manager are also called.
            match selected_action:
                case ActionType.CLICK_LEFT.value:
                    params = self.click_ui.check()
                    if params != False:
                        self.action_manager.add_left_click(params[0], params[1], self.container_manager.is_in_container)

                case ActionType.CLICK_RIGHT.value:
                    params = self.click_ui.check()
                    if params != False:
                        self.action_manager.add_right_click(params[0], params[1], self.container_manager.is_in_container)

                case ActionType.MOVE.value:
                    params = self.move_ui.check()
                    if params != False:
                        self.action_manager.add_move(params[0], params[1], params[2], self.container_manager.is_in_container)

                case ActionType.WRITE.value:
                    params = self.write_ui.check()
                    if params != False:
                        self.action_manager.add_write(params[0], self.container_manager.is_in_container)

                case ActionType.SCROLL.value:
                    params = self.scroll_ui.check()
                    if params != False:
                        self.action_manager.add_scroll(params[0], params[1], self.container_manager.is_in_container)

                case ActionType.WAIT.value:
                    params = self.wait_ui.check()
                    if params != False:
                        self.action_manager.add_wait(params, self.container_manager.is_in_container)

                case ActionType.KEY_PRESS.value:
                    params = self.pressed_ui.check()
                    if params != False:
                        self.action_manager.add_key_press(params[0], params[1], params[2], self.container_manager.is_in_container)

                case ActionType.PARALLEL_ACTIONS.value:
                    params = self.parallel_actions_ui.check()
                    if params != False:
                        self.action_manager.add_parallel_actions(params[0], params[1], params[2], self.container_manager.is_in_container)
                        self.container_manager.indicate_container(params[2])
                        self.container_manager.add_container(params[2])

                case ActionType.LOOP.value:
                    params = self.loop_ui.check()
                    if params != False:
                        self.action_manager.add_loop(params[0], params[1], self.container_manager.is_in_container)
                        self.container_manager.indicate_container(params[1])
                        self.container_manager.add_container(params[1])


    def switch_to_action_frame(self, frame: tk.Frame, key: str) -> None: 
        """
        Cette fonction est appelée par les Radiobuttons lorsque l'utilisateur en 
        sélectionne un. Elle permet de passer d'une frame d'action à une autre.

        :param frame: Frame correspondant à l'action choisie par l'utilisateur
        :param key: Clé correspondant à l'action choisie par l'utilisateur
        ------------------------------------------------------------------------
        This function is called by the Radiobuttons when the user selects one.
        It allows switching from one action frame to another.

        :param frame: Frame corresponding to the action chosen by the user
        :param key: Key corresponding to the action chosen by the user
        """

        # On cache l'interface sur laquelle nous nous trouvions auparavant. 
        # ------------------------------------------------------------------
        # Hide the interface that was previously displayed.
        self.current_frame.grid_remove()
        # On affiche l'interface choisie par l'utilisateur.
        # --------------------------------------------------
        # Display the interface chosen by the user.
        frame.grid(row=7, column=0)
        # On attribue à current_frame la frame dans laquelle nous nous trouvons actuellement.
        # --------------------------------------------------------------------------------
        # Update current_frame to the currently displayed frame.
        self.current_frame = frame

        # On regarde si l'utilisateur a choisi l'interface de mouvement ou de clic droit ou gauche. 
        # ------------------------------------------------------------------------------------------
        # Check whether the user selected the move or click interface.
        if key == ActionType.MOVE.value or key == ActionType.CLICK_LEFT.value or key == ActionType.CLICK_RIGHT.value:
            # Variable permettant de savoir qu'on est dans une interface de mouvement ou de clic
            # -----------------------------------------------------------------------------------
            # Variable indicating that the user is in a move or click interface.
            self.in_move_or_click = True

            # On regarde s'il y a déjà une instance de KeyPosition en fonctionnement.
            # ------------------------------------------------------------------------
            # Check whether a KeyPosition instance is already running.
            if not KeyPosition.is_listening:
                # On met à jour les positions de la souris en temps réel.
                # --------------------------------------------------------
                # Update mouse positions in real time.
                self.update_mouse_positions()

                # On crée une instance de KeyPosition
                # Cette instance permet de savoir si l'utilisateur appuie sur les 
                # touches correspondantes permettant de récupérer les coordonnées 
                # de la souris et de les ajouter en paramètre de l'action actuelle.
                # On donne en paramètre les fonctions set_coordinate de click_ui et move_ui
                # ------------------------------------------------------------------------------
                # Create a KeyPosition instance.
                # This instance listens for key presses that allow
                # retrieving mouse coordinates and inserting them
                # into the parameters of the current action.
                # The set_coordinate methods of click_ui and move_ui
                # are passed as parameters.
                self.key_position_listener = KeyPosition(self.click_ui.set_coordinate, self.move_ui.set_coordinate)

        # Vu que l'interface choisie par l'utilisateur n'est ni celle de mouvement,
        # ni celle de clic droit ou gauche, on appelle "stop_listening" si nécessaire.
        # -----------------------------------------------------------------------------
        # Since the selected interface is neither move nor click,
        # call stop_listening if necessary.
        else:
            self.in_move_or_click = False
            if KeyPosition.is_listening:
                self.key_position_listener.stop_listening()


    def update_mouse_positions(self) -> None:
        """
        Cette fonction met à jour en temps réel les coordonnées de la souris
        dans les interfaces de mouvement et de clic, en se rappelant toutes les 60 ms.
        -------------------------------------------------------------------------------
        This function updates the mouse coordinates in real time
        in the move and click interfaces. It is called every 60 ms.
        """
        self.click_ui.mouse_position_label.config(text=f"{position_mouse()[0]} | {position_mouse()[1]}")
        self.move_ui.mouse_position_label.config(text=f"{position_mouse()[0]} | {position_mouse()[1]}")
        # Vérifie que l'utilisateur est toujours dans une interface de mouvement ou de clic
        # ----------------------------------------------------------------------------------
        # Check that the user is still in a move or click interface.
        if self.in_move_or_click and self.in_action_selector:
            # On rappelle cette fonction toutes les 60 ms
            # --------------------------------------------
            # Call this function again after 60 ms.
            self.window.after(60, self.update_mouse_positions)
            
