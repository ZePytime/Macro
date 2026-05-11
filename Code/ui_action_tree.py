from __future__ import annotations

from sequence_manager import save_sequence
from scrollable_frame import ScrollableFrame
from hover_button import HoverButton
from action_classes import Loop, ParallelActions, KeyPosition, position_mouse
import tkinter as tk

from ui_action_frames.ui_move_frame import MouseMoveFrame
from ui_action_frames.ui_click_frame import ClickFrame
from ui_action_frames.ui_wait_frame import WaitFrame
from ui_action_frames.ui_write_frame import WriteFrame
from ui_action_frames.ui_loop_frame import LoopFrame
from ui_action_frames.ui_keyhold_frame import KeyHoldFrame
from ui_action_frames.ui_scroll_frame import ScrollFrame
from ui_action_frames.ui_parallel_actions_frame import ParallelActionsFrame
from typing import TYPE_CHECKING, Callable, Dict, Tuple, Any, Optional
from enums import ActionType

from ui_style import W_VAR

if TYPE_CHECKING:
    from main import WindowVariable
    from action_classes import Action

class TreeUI:
    """
    Cette classe permet à l'utilisateur de visualiser les actions de sa séquence, 
    de les modifier une par une, de les supprimer, 
    d'ajouter un temps d'attente entre elles et d'en désactiver certaines. 
    Elle permet également d'enregistrer la séquence d'actions créée par l'utilisateur 
    et de la réinitialiser (comme si le programme venait d'être démarré).
    ----------------------------------------------------------------------------------
    This class allows the user to visualize the actions in their sequence,
    modify them one by one, delete them,
    add a waiting time between them, and disable some of them.
    It also allows the user to save the created action sequence
    and reset it (as if the program had just started).

    """
    def __init__(self, window: tk.Tk, main_frm: tk.Frame, menu_btn_frame: tk.Frame, switch_frame: Callable[[tk.Frame], None], reset_action_sequence: Callable[[None], None]):
        """
        Initialisation de tous les widgets nécessaires à ce menu.

        :param window: Fenêtre principale de l'interface.
        :param main_frm: Cadre principal dans lequel se trouve ce menu.
        :param menu_btn_frame: Menu dans lequel on ajoute le bouton
            permettant de basculer vers cette interface.
        :param switch_frame: Fonction permettant de changer de frame
            afin d'afficher cette interface.
        :param reset_action_sequence: Fonction permettant de réinitialiser les valeurs 
            comme si l'on venait de démarrer le programme.
        ------------------------------------------------------------------
        Initializes all the widgets required for this menu.

        :param window: Main interface window.
        :param main_frm: Main frame in which this menu is located.
        :param menu_btn_frame: Menu in which the button is added
            allowing switching to this interface
        :param switch_frame: Function allowing frame switching
            to display this interface
        :param reset_action_sequence: Function allowing values to be reset
            as if the program had just started.
        """
        self.window = window
        self.reset_action_sequence = reset_action_sequence

        # Création du dictionnaire qui contiendra tous les Checkbutton avec leurs variables.
        # Lors de l'exécution de la suite d'actions, il permettra de savoir s'il faut effectuer 
        # chaque action en fonction de l'état du Checkbutton (coché ou non).
        # --------------------------------------------------------------------------------------
        # Creation of the dictionary that will contain all Checkbuttons with their variables.
        # During execution of the action sequence, it will determine whether each action
        # should be executed depending on the Checkbutton state (checked or not).
        self.action_checkbuttons_dict = {}
        # Clé pour le dictionnaire action_checkbuttons_dict.
        # ---------------------------------------------------
        # Key for the action_checkbuttons_dict dictionary.
        self.next_tree_dict_key = 0
        # Ligne du prochain Checkbutton à ajouter.
        # -----------------------------------------
        # Row of the next Checkbutton to add.
        self.next_checkbutton_row = 0

        # Variable permettant de savoir si l'utilisateur est dans la partie 
        # move ou click de l'interface, et qu'il faut donc oui ou non afficher les 
        # coordonnées de la souris de l'utilisateur en temps réel.
        # -------------------------------------------------------------------------
        # Variable indicating whether the user is in the move
        # or click part of the interface, meaning whether
        # mouse coordinates should be displayed in real time.
        self.in_move_or_click = False

        # Variable permettant de savoir si l'utilisateur est en train de modifier
        # sa suite d'actions.
        # ------------------------------------------------------------------------
        # Variable indicating whether the user is currently editing
        # their action sequence.
        self.in_edit = False

        # Variable permettant de savoir si les widgets d'enregistrement
        # sont affichés ou non.
        # --------------------------------------------------------------
        # Variable indicating whether the save widgets
        # are displayed or not.
        self.save_clicked = False

        # Variables qui auront leurs valeurs assignées plus tard :
        # ---------------------------------------------------------
        # Variables whose values will be assigned later :

        # Aura la valeur de l'instance de ActionManagerUI créée dans main.py.
        # Elle permettra d'accéder à ActionManager 
        # (afin d'exécuter/utiliser des fonctions/variables comme start_execution, save_list...).
        # ----------------------------------------------------------------------------------------
        # Will store the instance of ActionManagerUI created in main.py.
        # It allows access to ActionManager
        # (to execute/use functions and variables such as start_execution, save_list...).
        self.ui_action_manager = None

        # Aura la valeur de l'instance de ContainerManager créée dans ui_action_manager.py.
        # ----------------------------------------------------------------------------------
        # Will store the instance of ContainerManager created in ui_action_manager.py.
        self.container_manager = None


        # ===============================
        # === Création de l'interface ===
        # -------------------------------
        # ====== Interface Creation =====
        # ===============================


        # Bouton permettant d'accéder au menu de TreeUI.
        # -----------------------------------------------
        # Button used to access the TreeUI menu.
        self.tree_button = HoverButton(
            menu_btn_frame, 
            color=W_VAR.BUTTON_4,
            hover=W_VAR.BUTTON_4_HOVER,
            text="tree", 
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=5, 
            font=W_VAR.font_size, 
            command=lambda : switch_frame(self.tree_main_frame)
            )
        self.tree_button.grid(row=0, column=1, padx=2, pady=2)

        # Frame principale du menu.
        # --------------------------
        # Main frame of the menu.
        self.tree_main_frame = tk.Frame(main_frm, bg=W_VAR.NEUTRAL_800)

        # Frame principale affichant l'arbre des actions sous forme de Checkbutton.
        # Permet d'activer/désactiver les actions, d'ajouter des temps d'attente,
        # d'enregistrer ou réinitialiser la suite d'actions, et d'accéder au mode édition.
        # Cette frame est masquée lors de la modification de la suite d'actions.
        # ---------------------------------------------------------------------------------
        # Main frame displaying the action tree as Checkbuttons.
        # Allows enabling/disabling actions, adding waiting times,
        # saving or resetting the action sequence, and accessing edit mode.
        # This frame is hidden when modifying the action sequence.
        self.tree_frame = tk.Frame(self.tree_main_frame, bg=W_VAR.NEUTRAL_800, width=340, height=460)
        self.tree_frame.columnconfigure(0, weight=1)
        self.tree_frame.grid_propagate(False)
        self.tree_frame.grid(row=0, column=0)

        # Frame d'édition de la suite d'actions affichée sous forme de Radiobutton.
        # Permet de sélectionner une action à supprimer ou modifier.
        # Elle est masquée lors de l'édition des paramètres d'une action
        # et lors du retour à l'arbre principal.
        # --------------------------------------------------------------------------
        # Editing frame of the action sequence displayed as Radiobuttons.
        # Allows selecting an action to delete or modify.
        # It is hidden when editing the parameters of an action
        # and when returning to the main tree.
        self.edit_tree_frame = tk.Frame(self.tree_main_frame, bg=W_VAR.NEUTRAL_800, width=340, height=460)
        self.edit_tree_frame.columnconfigure(0, weight=1)
        self.edit_tree_frame.grid_propagate(False)

        # Frame d'édition des paramètres d'une action.
        # Affiche l'interface spécifique (ui_..._frame) correspondant à l'action sélectionnée.
        # -------------------------------------------------------------------------------------
        # Frame for editing the parameters of an action.
        # Displays the specific interface (ui_..._frame) corresponding to the selected action.
        self.edit_act_frame = tk.Frame(self.tree_main_frame, bg=W_VAR.NEUTRAL_800, width=340, height=460)
        self.edit_act_frame.columnconfigure(0, weight=1)
        self.edit_act_frame.grid_propagate(False)

        # ===================================================
        # === Interface principale de l'arbre des actions ===
        # ---------------------------------------------------
        # ============ Main Action Tree Interface ===========
        # ===================================================

        # Variable et Checkbutton permettant de savoir si 
        # l'utilisateur veut un temps d'attente entre chaque action.
        # -----------------------------------------------------------
        # Variable and Checkbutton used to determine whether
        # the user wants a waiting time between each action.
        self.wait_checkbox_var = tk.IntVar(value=0)
        self.wait_checkbutton = tk.Checkbutton(
            self.tree_frame, 
            text="Waiting time between each action", 
            font=W_VAR.little_font_size,
            variable=self.wait_checkbox_var, 
            bg=W_VAR.NEUTRAL_800,
            fg=W_VAR.TEXT_COLOR,
            activebackground=W_VAR.NEUTRAL_800,
            activeforeground=W_VAR.TEXT_COLOR,
            selectcolor=W_VAR.NEUTRAL_700,
            command=self.update_wait_frame_visibility
        )
        self.wait_checkbutton.grid(row=0, column=0)

        # Frame contenant les widgets nécessaires pour définir le temps d'attente entre chaque action.
        # Cette frame est affichée ou masquée en fonction de l'état du Checkbutton wait_checkbutton.
        # ---------------------------------------------------------------------------------------------
        # Frame containing the widgets required to define the waiting time between each action.
        # This frame is shown or hidden depending on the state of the wait_checkbutton.
        self.wait_time_config_frame = tk.Frame(self.tree_frame, bg=W_VAR.NEUTRAL_800)

        # Frame pour organiser les widgets liés au temps d'attente entre chaque action.
        # ------------------------------------------------------------------------------------
        # Frame used to organize the widgets related to the waiting time between each action.
        self.wait_time_label_frame = tk.Frame(self.wait_time_config_frame, bg=W_VAR.NEUTRAL_800)
        self.wait_time_label_frame.grid(row=0, column=0)

        # Champs de saisie pour le temps d'attente entre chaque action.
        # --------------------------------------------------------------
        # Input field for the waiting time between each action.
        self.wait_duration_entry = tk.Entry(
            self.wait_time_label_frame, 
            width=8,
            bg=W_VAR.NEUTRAL_700,
            fg=W_VAR.TEXT_COLOR, 
            font=W_VAR.font_size,
            relief="flat",
            highlightthickness=1,
            highlightbackground=W_VAR.NEUTRAL_400,
            highlightcolor=W_VAR.BUTTON_1,
            )
        self.wait_duration_entry.grid(row=0, column=0)
        
        self.wait_duration_label = tk.Label(
            self.wait_time_label_frame, 
            text="milliseconds", 
            bg=W_VAR.NEUTRAL_800, 
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=9, 
            font=W_VAR.font_size
            )
        self.wait_duration_label.grid(row=0, column=1, padx=(5, 12))

        # Bouton pour valider le temps d'attente entre chaque action.
        # --------------------------------------------------------------
        # Button used to validate the waiting time between each action.
        self.validate_wait_button = HoverButton(
            self.wait_time_label_frame, 
            color=W_VAR.BUTTON_1,
            hover=W_VAR.BUTTON_1_HOVER,
            text="validate", 
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=7, 
            font=W_VAR.font_size, 
            command=self.validate_wait_time
            )
        self.validate_wait_button.grid(row=0, column=2)

        # Label pour afficher les erreurs liées au temps d'attente.
        # ----------------------------------------------------------
        # Label used to display errors related to the waiting time.
        self.error_label_wait = tk.Label(
            self.wait_time_config_frame, 
            text='error', 
            bg=W_VAR.NEUTRAL_800, 
            fg=W_VAR.ERROR_COLOR, 
            height=1, 
            width=33, 
            font=W_VAR.font_size_error
            )

        # Menu scrollable qui contiendra toutes les actions sous forme de Radiobutton.
        # -----------------------------------------------------------------------------
        # Scrollable menu that will contain all actions as Radiobuttons.
        self.all_actions = ScrollableFrame(self.tree_frame)
        self.all_actions.grid(row=3, column=0, pady=(5, 0))

        # Frame pour organiser les boutons, les champs de saisie, etc.
        # -------------------------------------------------------------
        # Frame used to organize buttons, input fields, etc.
        self.control_buttons_frame = tk.Frame(self.tree_frame, bg=W_VAR.NEUTRAL_800)
        self.control_buttons_frame.grid(row=4, column=0)

        # Bouton pour démarrer l'exécution des actions.
        # ----------------------------------------------
        # Button to start the execution of the actions.
        self.start_button = HoverButton(
            self.control_buttons_frame, 
            text="start", 
            color=W_VAR.BUTTON_3,
            hover=W_VAR.BUTTON_3_HOVER,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=6, 
            font=W_VAR.font_size, 
            command=lambda : self.ui_action_manager.action_manager.start_execution(False)
            )
        self.start_button.grid(row=0, column=0, padx=(0, 3), pady=(3, 0))

        # Bouton permettant d'afficher ou de cacher les widgets 
        # nécessaires à l'enregistrement de la suite d'actions.
        # ------------------------------------------------------
        # Button used to show or hide the widgets
        # required to save the action sequence.
        self.save_button = HoverButton(
            self.control_buttons_frame, 
            text="save", 
            color=W_VAR.NEUTRAL_600,
            hover=W_VAR.NEUTRAL_500,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=5, 
            font=W_VAR.font_size, 
            command=self.toggle_save_widgets
            )
        self.save_button.grid(row=0, column=1, padx=(0, 3), pady=(3, 0))

        # Bouton appelant reset_action_sequence pour réinitialiser la suite d'actions.
        # -------------------------------------------------------------
        # Button calling reset_action_sequence to reinitialize the action sequence.
        self.reset_button = HoverButton(
            self.control_buttons_frame, 
            text="reset", 
            color=W_VAR.NEUTRAL_600,
            hover=W_VAR.NEUTRAL_500,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=6, 
            font=W_VAR.font_size, 
            command=self.reset_action_sequence
            )
        self.reset_button.grid(row=0, column=2, pady=(3, 0))

        # Bouton appelant edit pour permettre la modification de la suite d'actions.
        # ---------------------------------------------------------------------------
        # Button calling edit to allow modification of the action sequence.
        self.edit_button = HoverButton(
            self.control_buttons_frame, 
            text="edit", 
            color=W_VAR.NEUTRAL_600,
            hover=W_VAR.NEUTRAL_500,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=5, 
            font=W_VAR.font_size, 
            command=self.preparing_edit
            )
        self.edit_button.grid(row=0, column=3, padx=(3, 0), pady=(3, 0))

        # Frame contenant tous les widgets nécessaires à l'enregistrement de la suite d'actions : 
        # - Un label pour les explications
        # - Un champ de saisie pour le nom du fichier
        # - Un label pour les erreurs
        # - Un bouton de validation qui appelle la fonction save pour enregistrer.
        # ----------------------------------------------------------------------------------------
        # Frame containing all widgets required to save the action sequence:
        # - A label with instructions
        # - An input field for the file name
        # - A label for errors
        # - A validation button that calls the save function.
        self.save_frame = tk.Frame(self.tree_frame, bg=W_VAR.NEUTRAL_800)

        self.save_frame_2 = tk.Frame(self.save_frame, bg=W_VAR.NEUTRAL_800)
        self.save_frame_2.grid(row=0, column=0)

        self.save_frame_3 = tk.Frame(self.save_frame_2, bg=W_VAR.NEUTRAL_800)
        self.save_frame_3.grid(row=0, column=0)

        self.save_info_label = tk.Label(
            self.save_frame_3, 
            text='Put your file name:', 
            bg=W_VAR.NEUTRAL_800, 
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=20, 
            font=W_VAR.font_size
            )
        self.save_info_label.grid(row=0, column=0)
        self.name_entry  = tk.Entry(
            self.save_frame_3, 
            width=15,
            bg=W_VAR.NEUTRAL_700,
            fg=W_VAR.TEXT_COLOR, 
            font=W_VAR.font_size,
            relief="flat",
            highlightthickness=1,
            highlightbackground=W_VAR.NEUTRAL_400,
            highlightcolor=W_VAR.BUTTON_1 
            )
        self.name_entry.grid(row=1, column=0)



        self.save_error_label = tk.Label(
            self.save_frame, 
            text='error', 
            bg=W_VAR.NEUTRAL_800, 
            fg=W_VAR.ERROR_COLOR, 
            height=1, 
            width=45, 
            font=W_VAR.font_size_error
            )
        self.save_validate_button = HoverButton(
            self.save_frame_2, 
            text="validate", 
            color=W_VAR.BUTTON_1,
            hover=W_VAR.BUTTON_1_HOVER,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=8, 
            font=W_VAR.font_size, 
            command=self.call_save
            )
        self.save_validate_button.grid(row=0, column=1, pady=(10, 0))


        # ==================================================
        # === Interface d'édition de la suite d'actions ====
        # --------------------------------------------------
        # ======== Action Sequence Editing Interface =======
        # ==================================================


        # Menu scrolable qui contiendra toutes les actions sous forme de Radiobutton. 
        # Lorsque l'utilisateur cliquera sur Edit, cela lui permettra de choisir 
        # une action pour la modifier ou la supprimer.
        # ----------------------------------------------------------------------------
        # Scrollable menu that will contain all actions as Radiobuttons.
        # When the user clicks Edit, it allows them to choose
        # an action to modify or delete.
        self.all_actions_edit = ScrollableFrame(self.edit_tree_frame, width=260, height=325)
        self.all_actions_edit.grid(row=0, column=0, padx=30, pady=(30, 5))

        # Frame pour organiser les boutons de suppression et de modification.
        # --------------------------------------------------------------------
        # Frame used to organize the delete and edit, and exit.
        self.edit_control_buttons_frame = tk.Frame(self.edit_tree_frame, bg=W_VAR.NEUTRAL_800)
        self.edit_control_buttons_frame.grid(row=1, column=0)

        self.delete_button = HoverButton(
            self.edit_control_buttons_frame, 
            text="delete", 
            color=W_VAR.BUTTON_1, 
            hover=W_VAR.BUTTON_1_HOVER,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=10, 
            font=W_VAR.font_size, 
            command=self.call_delete_action
            )
        self.delete_button.grid(row=0, column=0, padx=(0, 5))

        self.edit_action_button = HoverButton(
            self.edit_control_buttons_frame, 
            text="edit", 
            color=W_VAR.BUTTON_1, 
            hover=W_VAR.BUTTON_1_HOVER,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=10, 
            font=W_VAR.font_size, 
            command=self.edit_act
            )
        self.edit_action_button.grid(row=0, column=1)

        self.leave_edit_button = HoverButton(
            self.edit_tree_frame, 
            text="left", 
            color=W_VAR.NEUTRAL_600, 
            hover=W_VAR.NEUTRAL_500,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=18, 
            font=W_VAR.font_size, 
            command=self.quit
            )
        self.leave_edit_button.grid(row=2, column=0, pady=(4, 0))

        # ========================================
        # === Interface d'édition d'une action ===
        # ==== Single Action Editing Interface ===
        # ========================================

        # Frame contenant les widgets nécessaires à l'édition d'une action chacun.
        # -------------------------------------------------------------------------
        # Frame containing the widgets required to edit each action type.
        self.click_frame = tk.Frame(self.edit_act_frame, bg=W_VAR.NEUTRAL_800)
        self.move_frame = tk.Frame(self.edit_act_frame, bg=W_VAR.NEUTRAL_800)
        self.write_frame = tk.Frame(self.edit_act_frame, bg=W_VAR.NEUTRAL_800)
        self.scroll_frame = tk.Frame(self.edit_act_frame, bg=W_VAR.NEUTRAL_800)
        self.wait_frame = tk.Frame(self.edit_act_frame, bg=W_VAR.NEUTRAL_800)
        self.pressed_frame = tk.Frame(self.edit_act_frame, bg=W_VAR.NEUTRAL_800)
        self.parallel_actions_frame = tk.Frame(self.edit_act_frame, bg=W_VAR.NEUTRAL_800)
        self.loop_frame = tk.Frame(self.edit_act_frame, bg=W_VAR.NEUTRAL_800)

        # Bouton de validation de l'édition de chaque action.
        # ----------------------------------------------------
        # Button used to validate the editing of each action.
        self.validate_button_edit = HoverButton(
            self.edit_act_frame, 
            text="validate", 
            color=W_VAR.BUTTON_1, 
            hover=W_VAR.BUTTON_1_HOVER,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=20, 
            font=W_VAR.font_size, 
            command=self.validate_edit
            )


    def update_wait_frame_visibility(self) -> None:
        """
        Cette fonction affiche ou masque la frame contenant les widgets nécessaires 
        pour définir le temps d'attente entre chaque action en fonction de 
        l'état du Checkbutton wait_checkbutton.
        ----------------------------------------------------------------------------
        Displays or hides the frame containing the widgets required
        to define the waiting time between each action
        depending on the state of the wait_checkbutton.
        """
        if self.wait_checkbox_var.get() == 1:
            self.wait_time_config_frame.grid(row=1, column=0)
        else:
            # Si l'utilisateur décoche le Checkbutton, on remet le temps d'attente à 0.
            # --------------------------------------------------------------------------
            # If the user unchecks the Checkbutton, reset waiting time to 0.
            self.ui_action_manager.action_manager.pause_between_actions = 0
            self.wait_time_config_frame.grid_remove()



    def validate_wait_time(self) -> None:
        """
        Cette fonction vérifie que le temps d'attente entre 
        chaque action entré par l'utilisateur est correct :
        - Il doit être un nombre entier positif.
        - Il ne doit pas être supérieur à 3600000 millisecondes (1 heure).
        -------------------------------------------------------------------
        Verifies that the waiting time entered by the user
        between each action is valid:
        - It must be a positive integer.
        - It must not exceed 3,600,000 milliseconds (1 hour).
        """
        # On récupère le temps entré par l'utilisateur dans le champ de saisie.
        # ----------------------------------------------------------------------
        # Retrieve the time entered by the user.
        time = self.wait_duration_entry.get()
        try:
            # On essaye de le convertir en entier.
            # -------------------------------------
            # Try converting it to an integer.
            time = int(time.replace(" ", ""))
            
        except ValueError:
            # On affiche une erreur car la conversion a échoué.
            # --------------------------------------------------
            # Display error if conversion fails.
            self.error_label_wait.config(text="The time you entered is incorrect")
            self.error_label_wait.grid(row=1, column=0)

        else:
            # On verifie que le temps est correct.
            # -------------------------------------
            # Check if the time is valid.
            if time <= 0:
                self.error_label_wait.config(text="the time you entered is incorrect")
                self.error_label_wait.grid(row=1, column=0)
            elif time > 3600000:# 3600000 milliseconds = 1h
                self.error_label_wait.config(text="the time you have entered is too long")
                self.error_label_wait.grid(row=1, column=0)
            else: 
                # Si le temps est correct, on le met dans action_manager et 
                # on cache le message d'erreur s'il était affiché.
                # -----------------------------------------------------------------
                # If valid, store it in action_manager and hide the error message.
                self.error_label_wait.grid_remove()
                self.ui_action_manager.action_manager.pause_between_actions = time

                # Enlève le focus du champ de saisie.
                # ------------------------------------
                # Remove focus from the input field.
                self.window.focus()



    def frame_act(self) -> None:
        """
        Cette fonction instancie les frames de chaque type d'action.
        Elle doit être appelée après que self.container_manager 
        et self.ui_action_manager soient assignés.
        -------------------------------------------------------------
        Instantiates the frames for each type of action.
        Must be called after self.container_manager
        and self.ui_action_manager have been assigned.
        """

        if self.container_manager is None:
            raise ValueError("container_manager is not assigned")
        self.click_ui = ClickFrame(self.click_frame)
        self.move_ui = MouseMoveFrame(self.move_frame)
        self.write_ui = WriteFrame(self.write_frame)
        self.scroll_ui = ScrollFrame(self.scroll_frame)
        self.wait_ui = WaitFrame(self.wait_frame)
        self.pressed_ui = KeyHoldFrame(self.pressed_frame)
        self.parallel_actions_ui = ParallelActionsFrame(self.parallel_actions_frame, self.container_manager)
        self.loop_ui = LoopFrame(self.loop_frame, self.container_manager)



    def preparing_edit(self) -> None:
        """
        Cette fonction prépare l'interface pour modifier la suite d'actions 
        et crée les valeurs nécessaires à cette modification (edit_state_map, next_radiobutton_row...).
        ------------------------------------------------------------------------------------------------
        Prepares the interface for editing the action sequence
        and creates the required values for editing (edit_state_map, next_radiobutton_row...).
        """


        # On vérifie que la liste d'actions n'est pas vide.
        # --------------------------------------------------
        # We check that the action list is not empty.
        if not len(self.action_checkbuttons_dict) == 0:
            # On indique que l'utilisateur est en train de modifier sa suite d'actions.
            # --------------------------------------------------------------------------
            # We indicate that the user is currently modifying their action sequence.
            self.in_edit = True

            # On cache la frame tree_frame et la remplace par la frame edit_tree_frame, 
            # qui permettra d'éditer la suite d'actions.
            # --------------------------------------------------------------------------
            # We hide the tree_frame and replace it with the edit_tree_frame,
            # which will allow editing of the action sequence.
            self.tree_frame.grid_remove()
            self.edit_tree_frame.grid(row=0, column=0)

            # Création des variables nécessaires à la modification de la suite d'actions.
            # Dictionnaire qui va contenir chaque élément de la suite d'actions avec les 
            # éléments/informations associées, ayant pour clé leur position dans la grille (next_radiobutton_row) :
            #
            # - container_index : C'est un nombre représentant la position de l'action dans la branche ou elle se trouve. 
            #       Par exemple, si c'est la 3ème action d'une boucle, la valeur sera 2.
            # - Instance : L'instance de l'action (qui permet l'exécution de l'action). 
            #       Une instance fille de Action (ex: ClickLeft, ParallelActions...)
            # - Radiobutton : Le Radiobutton associé à l'action, représentant l'action dans l'arbre d'édition,
            #       qui permet à l'utilisateur de sélectionner l'action pour la modifier ou la supprimer.
            # - Booléen : Un booléen indiquant si l'action se trouve dans un conteneur ou non (Loop/ParallelActions).
            # - Instance du conteneur : L'instance du conteneur dans lequel l'action se trouve (Loop/ParallelActions). 
            #       Si l'action n'est pas dans un conteneur, la valeur sera None.
            # - Nombre de conteneurs : Si l'action est un conteneur, ce nombre représente le total 
            #       de conteneurs présents dans la suite d'actions depuis la première action jusqu'à celle-ci,
            #       afin de connaître combien de conteneurs se trouvent avant lui.
            # - Niveau d'imbrication : Un nombre représentant le niveau d'imbrication des conteneurs. Par exemple,
            #      si une boucle est à l'intérieur d'une autre boucle, les éléments dans la boucle la plus imbriquée 
            #       auront une valeur de 2.
            # ------------------------------------------------------------------------------------------------------------
            # Dictionary containing each action in the sequence with
            # associated information, using its grid position as the key:
            #
            # - container_index: Position of the action within its branch.
            #   For example, if it is the 3rd action in a loop, the value will be 2.
            # - Instance: The action instance (used to execute the action).
            #   A subclass of Action (e.g., ClickLeft, ParallelActions...)
            # - Radiobutton: The Radiobutton representing the action in the edit tree,
            #   allowing the user to select it for modification or deletion.
            # - Boolean: Indicates whether the action is inside a container (Loop/ParallelActions).
            # - Container instance: The container instance in which the action is located.
            #   If not in a container, the value is None.
            # - Number of containers: If the action is a container, represents the total
            #   number of containers from the first action up to this one.
            # - Nesting level: Indicates the container nesting level.
            #   For example, if a loop is inside another loop, the deepest elements will have a value of 2.
            self.edit_state_map: Dict[int, Tuple[int, Action, tk.Radiobutton, bool, Action, int, int]] = {}
            self.next_radiobutton_row = 0
            self.num_containers = 0

            # Variable contenant le Radiobutton choisi par l'utilisateur.
            # ------------------------------------------------------------
            # Variable containing the Radiobutton selected by the user.
            self.selected_action_var = tk.IntVar(value=0)

            # On trie le dictionnaire pour être sûr qu'il n'y a pas de bugs.
            # ---------------------------------------------------------------
            # We sort the dictionary to ensure there are no bugs.
            self.ui_action_manager.action_manager.action_dict = {
                cle: self.ui_action_manager.action_manager.action_dict[cle] for cle in sorted(self.ui_action_manager.action_manager.action_dict)
                }

            # On parcourt le dictionnaire qui contient toutes les actions de la suite d'actions,
            # afin de les afficher dans l'interface d'édition et de les ajouter au dictionnaire edit_state_map.
            # --------------------------------------------------------------------------------------------------
            # We iterate through the dictionary containing all actions in the action sequence,
            # in order to display them in the editing interface and add them to the edit_state_map dictionary.

            for container_index, action_instance in self.ui_action_manager.action_manager.action_dict.items():
                
                # On crée le Radiobutton que l'utilisateur pourra sélectionner afin 
                # de modifier ou de supprimer l'action qui lui est associée.
                # ------------------------------------------------------------------
                # We create the Radiobutton that the user can select
                # to modify or delete the associated action.
                action_radiobutton = tk.Radiobutton(
                    self.all_actions_edit.scrollable_frame, 
                    text=action_instance.text(), 
                    variable=self.selected_action_var, 
                    value=self.next_radiobutton_row, 
                    bg=W_VAR.NEUTRAL_700,
                    fg=W_VAR.TEXT_COLOR,
                    font=W_VAR.little_font_size,
                    activebackground=W_VAR.NEUTRAL_800,
                    activeforeground=W_VAR.TEXT_COLOR,
                    selectcolor=W_VAR.NEUTRAL_700
                    )
                action_radiobutton.grid(row=self.next_radiobutton_row, column=0, sticky="nw")

                # Si l'action est un conteneur on ajoute ces caractéristiques au dictionnaire, 
                # on incrémente num_containers et next_radiobutton_row, 
                # puis on appelle explore_container afin quelle parcour le conteneur et qu'elle ajoute tous
                # ce qu'il contient au dictionnaire edit_state_map.
                # Sinon, on ajoute simplement les caractéristiques de l'action au dictionnaire edit_state_map 
                # et on incrémente next_radiobutton_row.
                # --------------------------------------------------------------------------------------------
                # If the action is a container, we add its characteristics to the dictionary,
                # increment num_containers and next_radiobutton_row,
                # then call explore_container so that it traverses the container
                # and adds everything it contains to the edit_state_map dictionary.
                # Otherwise, we simply add the action's characteristics to the edit_state_map dictionary
                # and increment next_radiobutton_row.
                if isinstance(action_instance, Loop) or isinstance(action_instance, ParallelActions):
                    self.edit_state_map[self.next_radiobutton_row] = [
                        container_index, action_instance, action_radiobutton, 
                        False, None, self.num_containers, 0
                        ]
                    self.next_radiobutton_row += 1
                    self.num_containers += 1
                    self.explore_container(action_instance, 1)
                else:
                    self.edit_state_map[self.next_radiobutton_row] = [
                        container_index, action_instance, 
                        action_radiobutton, False, None, None, 0
                        ]
                    self.next_radiobutton_row += 1



    def explore_container(self, inst_container: Loop|ParallelActions, indentation_level: int) -> None:
        """
        Cette fonction explore un conteneur (Loop/ParallelActions) et ajoute toutes les actions 
        qu'il contient au dictionnaire edit_state_map avec les caractéristiques nécessaires pour 
        la modification de la suite d'actions.

        :param inst_container: L'instance du conteneur à explorer (Loop/ParallelActions).
        :param indentation_level: Un nombre représentant le niveau d'incrémentation de l'instance du conteneur.
        --------------------------------------------------------------------------------------------------------
        This function explores a container (Loop/ParallelActions) and adds all the actions
        it contains to the edit_state_map dictionary with the necessary characteristics
        required for editing the action sequence.

        :param inst_container: The container instance to explore (Loop/ParallelActions).
        :param indentation_level: A number representing the nesting level of the container instance.
        """

        # On trie le dictionnaire du conteneur pour être sûr qu'il n'y a pas de bugs.
        # ----------------------------------------------------------------------------
        # We sort the container dictionary to ensure there are no bugs.
        inst_container.container_actions_dict = {key: inst_container.container_actions_dict[key] for key in sorted(inst_container.container_actions_dict)}
        
        # On parcourt le dictionnaire du conteneur qui contient toutes les actions 
        # de la suite d'actions, afin de les afficher dans l'interface d'édition 
        # et de les ajouter au dictionnaire edit_state_map
        # --------------------------------------------------------------------------
        # We iterate through the container dictionary that contains all the actions
        # in the action sequence, in order to display them in the editing interface
        # and add them to the edit_state_map dictionary.
        for container_index, action_instance in inst_container.container_actions_dict.items():

            # On crée le Radiobutton que l'utilisateur pourra sélectionner 
            # afin de modifier ou de supprimer l'action qui lui est associée.
            # Mais en lui ajoutant un padx pour que l'utilisateur puisse discerner 
            # qu'il est dans une boucle.
            # ---------------------------------------------------------------------
            # We create the Radiobutton that the user can select
            # in order to modify or delete the associated action.
            # We also add horizontal padding (padx) so that the user can visually
            # recognize that the action is inside a loop.
            action_radiobutton = tk.Radiobutton(
                self.all_actions_edit.scrollable_frame, 
                text=action_instance.text(), 
                variable=self.selected_action_var, 
                value=self.next_radiobutton_row, 
                bg=W_VAR.NEUTRAL_700,
                fg=W_VAR.TEXT_COLOR,
                font=W_VAR.little_font_size,
                activebackground=W_VAR.NEUTRAL_800,
                activeforeground=W_VAR.TEXT_COLOR,
                selectcolor=W_VAR.NEUTRAL_700
                )
            action_radiobutton.grid(row=self.next_radiobutton_row, column=0, sticky="nw", padx=indentation_level*10)


            # Si l'action est un conteneur on ajoute ces caractéristiques au dictionnaire, 
            # on incrémente num_containers et next_radiobutton_row, 
            # puis on appelle explore_container afin qu'elle parcoure le conteneur 
            # et qu'elle ajoute tout ce qu'il contient au dictionnaire edit_state_map.
            # Sinon, on ajoute simplement les caractéristiques de l'action au dictionnaire 
            # edit_state_map et on incrémente next_radiobutton_row.
            # -----------------------------------------------------------------------------
            # If the action is a container, we add its characteristics to the dictionary,
            # increment num_containers and next_radiobutton_row,
            # then call explore_container so that it traverses the container
            # and adds everything it contains to the edit_state_map dictionary.
            # Otherwise, we simply add the action's characteristics to edit_state_map
            # and increment next_radiobutton_row.
            if isinstance(action_instance, Loop) or isinstance(action_instance, ParallelActions):
                self.edit_state_map[self.next_radiobutton_row] = [
                    container_index, action_instance, action_radiobutton, True, 
                    inst_container, self.num_containers, indentation_level
                    ]
                self.next_radiobutton_row += 1
                self.num_containers += 1
                self.explore_container(action_instance, indentation_level+1)
            else:
                self.edit_state_map[self.next_radiobutton_row] = [
                    container_index, action_instance, action_radiobutton, True, 
                    inst_container, None, indentation_level
                    ]
                self.next_radiobutton_row += 1



    def edit_state_map_sort(self, deleted_element_key: int) -> None:
        """
        Cette fonction permet, lorsqu'un élément de edit_state_map a été supprimé, quelle que soit sa position,
        de modifier le dictionnaire afin de donner l'impression que cet élément n'a jamais existé.

        :param deleted_element_key: Clé de l'élément supprimé (container_index) dans edit_state_map.
        --------------------------------------------------------------------------------------------------------
        This function ensures that when an element of edit_state_map has been deleted,
        regardless of its position, the dictionary is modified so that it appears
        as if the element never existed.

        :param deleted_element_key: Key of the deleted element (container_index) in edit_state_map.
        """
        # On trie le dictionnaire afin d'éviter tout comportement incohérent.
        # --------------------------------------------------------------------
        # We sort the dictionary to avoid any inconsistent behavior.
        self.edit_state_map = {key: self.edit_state_map[key] for key in sorted(self.edit_state_map)}

        # On crée un nouveau dictionnaire que l'on remplit au fur et à mesure du parcours de edit_state_map,
        # en modifiant les éléments situés après l'élément supprimé.
        # ---------------------------------------------------------------------------------------------------
        # We create a new dictionary that we populate while iterating through edit_state_map,
        # modifying the elements located after the deleted element.
        reindexed_dict = {}

        # On parcourt edit_state_map.
        # -----------------------------------
        # We iterate through edit_state_map.
        for row, action_data in self.edit_state_map.items() :

            # Si l'élément se trouve avant celui qui a été supprimé, on ne le modifie pas.
            # On le réaffiche afin d'éviter tout décalage visuel, puis on l'ajoute à reindexed_dict.
            # ---------------------------------------------------------------------------------------
            # If the element is located before the deleted one, we do not modify it.
            # We redisplay it to avoid any visual shift, then add it to reindexed_dict.
            if row <= deleted_element_key:
                action_data[2].grid_remove()
                action_data[2].grid(row=row, column=0, sticky="nw")
                reindexed_dict[row] = action_data

            else:
                # Sinon, s'il se trouve après l'élément supprimé, on l'affiche à la bonne position
                # et on modifie sa clé après avoir vérifié s'il est nécessaire d'ajuster sa valeur container_index.
                # --------------------------------------------------------------------------------------------------
                # Otherwise, if it is located after the deleted element, we display it in the correct position
                # and modify its key after verifying whether its container_index value needs adjustment.

                action_data[2].grid_remove()
                action_data[2].config(value=row-1)
                action_data[2].grid(row=row-1, column=0, sticky="nw", padx=action_data[6]*10)

                # On commence les vérifications pour savoir si container_index doit être modifié. 
                # --------------------------------------------------------------------------------
                # We start the checks to determine whether container_index must be modified.

                # Si l'action est la première de son conteneur, il ne peut pas y 
                # avoir d'action supprimée avant lui dans ce conteneur.
                # -----------------------------------------------------------------
                # If the action is the first one in its container, there cannot be
                # any deleted action before it within that container.
                if action_data[0] != 0:
                    

                    # Si reindexed_dict est vide, cela signifie qu'il s'agit du premier
                    # élément de la suite d'actions ; quoi qu'il arrive, son container_index doit valoir 0.
                    # --------------------------------------------------------------------------------------
                    # If reindexed_dict is empty, this means it is the first
                    # element of the action sequence; in any case, its container_index must be 0.

                    if len(reindexed_dict) <= 0:
                        action_data[0] = 0
                    else:

                        # Si l'action d'avant est dans le même conteneur que nous.
                        # --------------------------------------------------------------------
                        # If the previous action is in the same container as the current one.
                        if action_data[4] == list(reindexed_dict[row-2])[4]:

                            # On vérifie s'il y a un décalage supérieur à 1 entre notre container_index et 
                            # celui de l'action précédente. Si c'est le cas, on enlève 1 à notre container_index.
                            # ------------------------------------------------------------------------------------
                            # We check whether there is a gap greater than 1 between our container_index
                            # and that of the previous action. If so, we subtract 1 from our container_index.
                            if list(reindexed_dict[row-2])[0] < action_data[0]-1:
                                action_data[0] -= 1


                        else:
                            # Sinon si l'action du conteneur d'avant n'est pas dans le même conteneur que nous, 
                            # cela signifie que la valeur container_index de l'action précédente n'a aucun 
                            # rapport avec notre container_index. 
                            # (cela signifie que soit on rentre dans un conteneur, soit on en sort). 
                            # ----------------------------------------------------------------------------------
                            # Otherwise, if the previous action’s container is not the same as ours,
                            # this means that the container_index value of the previous action
                            # has no relation to our container_index.
                            # (This means either we are entering a container or leaving one.)

                            # On vérifie si l'action précédente est un conteneur. Si c'est le cas cela signifie 
                            # que l'on entre dans un conteneur. On est donc le premier élément de ce conteneur, 
                            # et on met donc container_index à 0.
                            # ----------------------------------------------------------------------------------
                            # We check whether the previous action is a container. If so, it means
                            # we are entering a container. Therefore, we are the first element
                            # of that container, and we set container_index to 0.
                            if isinstance(list(reindexed_dict[row-2])[1], Loop) or isinstance(list(reindexed_dict[row-2])[1], ParallelActions):
                                action_data[0] = 0

                            else:
                                # Sinon si l'action précédente n'est pas un conteneur, 
                                # cela signifie que l'on sort d'un conteneur.
                                # ------------------------------------------------------
                                # Otherwise, if the previous action is not a container,
                                # it means we are exiting a container.

                                # On va parcourir le reindexed_dict à l'envers.
                                # ----------------------------------------------------
                                # We iterate through reindexed_dict in reverse order.
                                for key, valeur in reversed(list(reindexed_dict.items())):
                                    # On cherche la dernière action qui est dans le même conteneur que nous 
                                    # avant nous et qui ne doit pas être nous.
                                    # ----------------------------------------------------------------------
                                    # We look for the last action that is in the same container as us
                                    # before our position and that is not ourselves.
                                    if action_data[4] == valeur[4]:

                                        # On regarde si container_index a un décalage de 2 avec le container_index 
                                        # de la dernière action dans le même conteneur que nous. 
                                        # -------------------------------------------------------------------------
                                        # We check whether container_index has a gap of 2 compared
                                        # to the container_index of the last action in the same container.

                                        if valeur[0] == action_data[0]-2 :
                                            action_data[0] -= 1

                                        # On quitte la boucle car on a trouvé la dernière
                                        # action dans le même conteneur que nous
                                        # ------------------------------------------------
                                        # We exit the loop because we have found the last
                                        # action in the same container as us.
                                        break
                # Enfin, on ajoute l'élément modifié à reindexed_dict avec sa nouvelle clé à reindexed_dict.
                # -------------------------------------------------------------------------------------------
                # Finally, we add the modified element to reindexed_dict with its new key.
                reindexed_dict[row-1] = action_data

        # Après avoir parcouru tout le dictionnaire, on remplace edit_state_map par reindexed_dict 
        # qui est le même dictionnaire mais avec les éléments après l'élément supprimé modifiés 
        # de sorte qu'il n'y ait pas de décalage.
        # ----------------------------------------------------------------------------------------------
        # After iterating through the entire dictionary, we replace edit_state_map with reindexed_dict,
        # which is the same dictionary but with elements after the deleted element modified
        # so that there is no gap.
        self.edit_state_map = dict(reindexed_dict)
                            


    def index_save(self, dict_edit_index: int) -> int:
        """
        Cette fonction retourne l'index réel d'une action dans save_list,
        car celle-ci contient des éléments LEFT_CONTAINER non présents dans edit_state_map.

        Nous parcourons save_list jusqu'à l'index donné et,
        chaque fois qu'un LEFT_CONTAINER est rencontré,
        nous avançons d'une position supplémentaire afin d'obtenir le bon index.

        :param dict_edit_index: Index de l'action dans edit_state_map à convertir en index de save_list.
        -------------------------------------------------------------------------------------------------
        This function returns the real index of an action in save_list,
        because save_list contains LEFT_CONTAINER elements that are not present in edit_state_map.

        We iterate through save_list up to the given index and,
        each time a LEFT_CONTAINER is encountered,
        we move forward by one additional position to obtain the correct index.

        :param dict_edit_index: Index of the action in edit_state_map to convert into a save_list index.
        """
        real_index_save = dict_edit_index
        element_idx = 0

        # On parcourt save_list jusqu'à l'index real_index_save et chaque fois qu'on trouve un LEFT_CONTAINER,
        # on incrémente real_index_save de 1 pour compenser l'élément LEFT_CONTAINER qui n'est pas dans edit_state_map.
        # --------------------------------------------------------------------------------------------------------------
        # We iterate through save_list up to real_index_save and each time we find a LEFT_CONTAINER,
        # we increment real_index_save by 1 to compensate for the LEFT_CONTAINER element
        # that is not present in edit_state_map.
 
        # Dès que i devient supérieur à real_index_save, cela signifie que l'on a parcouru
        # tous les éléments de save_list situés avant l'index de l'action que l'on veut trouver.
        # ---------------------------------------------------------------------------------------
        # As soon as element_idx becomes greater than real_index_save,
        # this means we have iterated through all elements of save_list
        # located before the index of the action we want to find.
        while element_idx <= real_index_save:
            if self.ui_action_manager.action_manager.save_list[element_idx][0] == ActionType.LEFT_CONTAINER.value:
                real_index_save+=1
            element_idx += 1

        return real_index_save



    def sort_dict(self, dictionary: Dict[int, Any], deleted_element_key: int) -> Dict[int, Any]:
        """
        Cette fonction modifie le dictionnaire comportant des clés numérotées à partir de 0, 
        augmentant de 1 en 1, et doit avoir eu un élément qui a été supprimé. 
        Cette fonction va alors modifier les clés du dictionnaire de sorte qu'il n'y ait pas de décalage. 
        
        Pour cela, elle va parcourir ce dictionnaire et, lorsque qu'un élément se trouve après 
        l'élément supprimé, on va soustraire 1 à cette clé et retourner ce nouveau dictionnaire.

        :param dictionary: Le dictionnaire à modifier.
        :param deleted_element_key: La clé de l'élément supprimé dans le dictionnaire.
        --------------------------------------------------------------------------------------------------
        This function modifies a dictionary whose keys are numbered starting from 0
        and incremented by 1, after one element has been deleted.
        It updates the dictionary keys so that there is no gap.

        To do this, it iterates through the dictionary and,
        when an element is located after the deleted element,
        subtracts 1 from its key and returns the new dictionary.

        :param dictionary: The dictionary to modify.
        :param deleted_element_key: The key of the deleted element in the dictionary.
        """
        # Nouveau dictionnaire que l'on va remplir au fur et à mesure du parcours de dictionary.
        # ---------------------------------------------------------------------------------------
        # New dictionary that we populate while iterating through dictionary.
        reindexed_dict = {}

        # On parcourt le dictionnaire dictionary et, lorsque qu'un élément se trouve après l'élément supprimé,
        # on va soustraire 1 à cette clé et ajouter l'élément au nouveau dictionnaire reindexed_dict. 
        # Sinon, on ajoute l'élément au nouveau dictionnaire sans modifier sa clé.
        # -----------------------------------------------------------------------------------------------------
        # We iterate through dictionary and, when an element is located after the deleted element,
        # we subtract 1 from its key and add the element to reindexed_dict.
        # Otherwise, we add the element to the new dictionary without modifying its key.
        for key, value in dictionary.items() :
            if key > deleted_element_key:
                reindexed_dict[key-1] = value
            else:
                reindexed_dict[key] = value

        return reindexed_dict



    def del_left_container(self, nb: int) -> None:
        """
        Cette fonction permet de supprimer un élément LEFT_CONTAINER de save_list. 
        
        Cette fonction ne doit pas être appelée si un autre conteneur se trouve
        à l'intérieur du conteneur supprimé, car elle ne supprimerait
        que le premier LEFT_CONTAINER qu'elle trouverait. Il faut donc au préalable supprimer 
        les conteneurs qui se trouvent à l'intérieur du conteneur que l'on veut supprimer,
        afin d'être sûr que le LEFT_CONTAINER que l'on va supprimer est bien celui lié 
        au conteneur que l'on veut supprimer.
        
        :param nb: Index du conteneur qui a été supprimé dans save_list.
        --------------------------------------------------------------------------------------
        This function removes a LEFT_CONTAINER element from save_list.

        This function must not be called if another container exists
        inside the container being deleted, because it would only remove
        the first LEFT_CONTAINER it finds. Therefore, the containers
        inside the container to be deleted must first be removed,
        to ensure that the LEFT_CONTAINER being removed is indeed
        the one associated with the container to delete.

        :param nb: Index of the container that was deleted in save_list.
        """

        the_nb = nb

        # On parcourt save_list à partir de l'index du conteneur supprimé et on 
        # supprime le premier LEFT_CONTAINER que l'on trouve, car cela signifie que c'est 
        # celui lié au conteneur que l'on a supprimé.
        # --------------------------------------------------------------------------------
        # We iterate through save_list starting from the index of the deleted container
        # and remove the first LEFT_CONTAINER found, since it corresponds
        # to the container that was deleted.
        for current_index, element in enumerate(self.ui_action_manager.action_manager.save_list[the_nb:]):
            if element[0] == ActionType.LEFT_CONTAINER.value:
                del self.ui_action_manager.action_manager.save_list[current_index+the_nb]
                break



    def call_delete_action(self, index_element=None) -> None:
        """
        Cette fonction appelle delete_action (fonction permettant de supprimer une action) 
        en lui fournissant tous les paramètres nécessaires à la suppression de 
        l'élément choisi par l'utilisateur ou d'un élément passé en paramètre.

        :param index_element: L'index de l'élément à supprimer dans edit_state_map. 
            Si aucun index n'est passé, la fonction utilisera l'index choisi par l'utilisateur.
        ----------------------------------------------------------------------------------------
        This function calls delete_action (a function that deletes an action)
        by providing all necessary parameters to delete
        the element selected by the user or passed as an argument.

        :param index_element: The index of the element to delete in edit_state_map.
            If no index is provided, the function uses the index selected by the user.
        """
        # On vérifie que le dictionnaire n'est pas vide. 
        # Si le dictionnaire est vide, on quitte l'interface d'édition.
        # --------------------------------------------------------------
        # We check that the dictionary is not empty.
        # If the dictionary is empty, we exit the editing interface.
        if len(self.edit_state_map) == 0:
            self.quit()

        else:
            # Si un index est passé en paramètre.
            # --------------------------------------
            # If an index is passed as a parameter.
            if index_element is not None:
                # On utilise l'index passé en paramètre comme index de l'élément à supprimer.
                # ------------------------------------------------------------------------------
                # We use the index passed as a parameter as the index of the element to delete.
                user_choice = index_element
            else:
                # On récupère l'index de l'action choisi par l'utilisateur.
                # ----------------------------------------------------------
                # We retrieve the index of the action selected by the user.
                user_choice = self.selected_action_var.get()

            # On récupère les informations de l'action choisie par 
            # l'utilisateur dans le dictionnaire edit_state_map
            # ---------------------------------------------------------------
            # We retrieve the information of the action selected by the user
            # from the edit_state_map dictionary.
            info_act = self.edit_state_map[user_choice]

            # On appelle delete_action en lui fournissant tous les paramètres nécessaires 
            # à la suppression de l'élément choisi par l'utilisateur.
            # ----------------------------------------------------------------------------
            # We call delete_action by providing all necessary parameters
            # to delete the element selected by the user.
            self.delete_action(info_act[0], info_act[1], info_act[2], info_act[3], info_act[4], info_act[5], user_choice)




    def update_number_containeur(self, key_cntr_del: int) -> None:
        """
        Cette fonction met à jour le nombre de conteneurs dans 
        edit_state_map après la suppression d'un conteneur.

        :param key_cntr_del: La clé du conteneur supprimé dans edit_state_map.
        ------------------------------------------------------------------------
        This function updates the number of containers in 
        dit_state_map after a container has been deleted.

        :param key_cntr_del: The key of the deleted container in edit_state_map.
        """
        # On parcourt edit_state_map à partir de la clé du conteneur supprimé.
        # ----------------------------------------------------------------------------------
        # We iterate through edit_state_map starting from the key of the deleted container.
        for key in list(self.edit_state_map.keys()):
            if key > key_cntr_del:
                # On décrémente le numéro de conteneur pour tous les éléments suivants.
                # ----------------------------------------------------------------------
                # We decrement the container number for all subsequent elements.
                self.edit_state_map[key][5] -= 1



    def delete_action(self, container_index: int, action_instance: Action, selected_radiobutton: tk.Radiobutton, is_in_container: bool, parent_container: Optional[Loop|ParallelActions], number_container: int, user_choice: int) -> None:
        """
        Cette fonction supprime une action de la suite d'actions en fonction de l'index de l'action dans edit_state_map,
            et de toutes les informations liées à cette action dans edit_state_map.
        
        :param container_index: C'est un nombre représentant la position de l'action dans la branche ou elle se trouve. 
            Par exemple, si c'est la 3ème action d'une boucle, la valeur sera 2.
        :param action_instance: L'instance de l'action (qui permet l'exécution de l'action). 
            Une instance fille de Action (ex: ClickLeft, ParallelActions...)
        :param selected_radiobutton: Le Radiobutton associé à l'action/représentant l'action dans l'arbre d'édition,
            qui permet à l'utilisateur de sélectionner l'action pour la modifier ou la supprimer.
        :param is_in_container: Un booléen indiquant si l'action se trouve dans un conteneur ou non (Loop/ParallelActions).
        :param parent_container: L'instance du conteneur dans lequel l'action se trouve (Loop/ParallelActions). 
            Si l'action n'est pas dans un conteneur, la valeur sera None.
        :param number_container: Si l'action est un conteneur, ce nombre représente le nombre de conteneurs dans 
            la suite d'actions de la première action jusqu'à cette action afin de connaitre pour chaque conteneur
            combien de conteneurs il y a avant lui. Si l'action n'est pas un conteneur, la valeur est None.
        :param user_choice: Un nombre représentant le niveau d'imbrication des conteneurs. Par exemple,
            si une boucle est à l'intérieur d'une autre boucle, les éléments dans la boucle la plus imbriquée 
            auront une valeur de 2.
        --------------------------------------------------------------------------------------------------------------------
        This function deletes an action from the action sequence based on the action index in edit_state_map,
        along with all related information stored in edit_state_map.

        :param container_index: A number representing the position of the action in the branch where it is located.
            For example, if it is the 3rd action in a loop, the value will be 2.
        :param action_instance: The instance of the action (which enables execution of the action).
            A child instance of Action (e.g., ClickLeft, ParallelActions...).
        :param selected_radiobutton: The Radiobutton associated with the action/representing the action in the editing tree,
            which allows the user to select the action to modify or delete.
        :param is_in_container: A boolean indicating whether the action is inside a container (Loop/ParallelActions).
        :param parent_container: The container instance in which the action is located (Loop/ParallelActions).
            If the action is not in a container, the value will be None.
        :param number_container: If the action is a container, this number represents the number of containers
            in the action sequence from the first action up to this action, in order to know
            how many containers exist before it. If the action is not a container, the value is None.
        :param user_choice: A number representing the nesting level of containers. For example,
            if a loop is inside another loop, the elements in the innermost loop
            will have a value of 2.
        """

        # On regarde si l'élément à supprimer est un conteneur. 
        # Si c'est le cas, il faut supprimer tous les éléments qu'il contient,
        # puis supprimer le conteneur lui-même.
        # ---------------------------------------------------------------------
        # We check whether the element to delete is a container. 
        # If so, we must delete all elements it contains,
        # then delete the container itself.
        if isinstance(action_instance, Loop) or isinstance(action_instance, ParallelActions):

            # On parcourt edit_state_map à partir de l'index de l'élément à supprimer 
            # et on supprime tous les éléments qui se trouvent dans le conteneur que l'on veut supprimer.
            # --------------------------------------------------------------------------------------------
            # We iterate through edit_state_map starting from the index of the element to delete
            # and delete all elements that are inside the container we want to remove.
            for i in range(user_choice+1, len(self.edit_state_map)):

                # Si la clé +1 (car les clées commence à 0) du conteneur que l'on veut supprimer 
                # est égale au nombre délement dans edit_state_map, cela signifie que l'on a 
                # parcouru tous les éléments de edit_state_map après le conteneur que l'on veut supprimer,
                # et que tous les éléments qui se trouvaient dans ce conteneur ont été supprimés, 
                # donc on peut quitter la boucle.
                # -----------------------------------------------------------------------------------------
                # If the key +1 (since keys start at 0) of the container we want to delete
                # equals the number of elements in edit_state_map,
                # this means we have iterated through all elements after the container,
                # and that all elements inside this container have been deleted, so we can exit the loop.
                if user_choice+1 == len(self.edit_state_map):
                    break
                else:
                    # If the element we are examining is inside the container we want to delete,
                    # we delete it by calling "call_delete_action" with its index.
                    # -----------------------------------------------------------------------------------
                    # Si l'élément que l'on regarde se trouve dans le conteneur que l'on veut supprimer, 
                    # on le supprime en appelant "call_delete_action" avec son index.
                    if self.edit_state_map[user_choice+1][4] == action_instance:
                        self.call_delete_action(user_choice+1)
                    else:
                        # Si l'elément que l'on regarde ne se trouve pas dans le conteneur que l'on veut supprimer, 
                        # cela signifie que l'on a parcouru tous les éléments de ce conteneur, car il est impossible 
                        # d'avoir un autre conteneur à l'intérieur de celui que l'on veut supprimer car il ont tous été supprimés.
                        # On peut donc quitter la boucle.
                        # ---------------------------------------------------------------------------------------------------------
                        # If the element we are examining is not inside the container we want to delete,
                        # this means we have iterated through all elements of that container, since it is impossible
                        # to have another container inside the one we want to delete because they have all been removed.
                        # We can therefore exit the loop.
                        break

            # On supprime l'élément left_container lié au conteneur dans save_list.
            # -----------------------------------------------------------------------------------
            # We remove the left_container element associated with the container from save_list.
            self.del_left_container(self.index_save(user_choice))

            # On vérifie si l'utilisateur a quitté le conteneur. S'il se trouve encore à l'intérieur, on le fait sortir.
            # -----------------------------------------------------------------------------------------------------------
            # We check whether the user is still inside the container. If so, we make them exit it.
            if list(self.container_manager.container_map[number_container])[0]:
                self.container_manager.leave_current_container()

            # On met à jour le nombre de conteneurs pour les éléments suivants dans edit_state_map, 
            # car on a supprimé un conteneur.
            # --------------------------------------------------------------------------------------
            # We update the number of containers for subsequent elements in edit_state_map,
            # since we deleted a container.
            self.update_number_containeur(user_choice)

            # On enlève le conteneur de container_map.
            # --------------------------------------------
            # We remove the container from container_map.
            del self.container_manager.container_map[number_container]
            # On corrige le décalage dans container_map causé par la suppression de l'élément lié au conteneur.
            # --------------------------------------------------------------------------------------------------
            # We fix the shift in container_map caused by deleting the container-related element.
            self.container_manager.container_map = self.sort_dict(self.container_manager.container_map, number_container)

            # On supprime le nom du conteneur dans la liste du conteneur correspondant 
            # (liste contenant tous les noms des conteneurs du même type, permettant d'empêcher 
            # l'utilisateur de choisir deux fois le même nom).
            # ----------------------------------------------------------------------------------
            # We remove the container name from the corresponding container name list
            # (the list containing all container names of the same type,
            # used to prevent the user from selecting the same name twice).
            if isinstance(action_instance, Loop):
                self.container_manager.loop_names.remove(action_instance.name)
            else:
                self.container_manager.parallel_action_names.remove(action_instance.name)


        # On supprime le Checkbutton associé à l'action de l'arbre principal 
        # et on modifie les valeurs liées. Puis on supprime l'instance de l'action,
        # le tout différemment selon que l'élément est dans un conteneur ou non.
        # ---------------------------------------------------------------------------
        # We remove the Checkbutton associated with the action from the main tree
        # and update the related values. Then we delete the action instance,
        # differently depending on whether the element is inside a container or not.
        if is_in_container:
            self.delete_action_instance_in_container(parent_container, container_index)
        else:
            self.delete_action_instance(container_index)
        
        # On enlève 1 à next_checkbutton_row, la valeur qui correspond aux 
        # lignes où sont affichés les "Checkbutton" des actions.
        # -----------------------------------------------------------------
        # We subtract 1 from next_checkbutton_row, the value corresponding
        # to the rows where action Checkbuttons are displayed.
        self.next_checkbutton_row -= 1

        # On supprime l'élément correspondant à l'action dans save_list.
        # ------------------------------------------------------------------
        # We remove the element corresponding to the action from save_list.
        del self.ui_action_manager.action_manager.save_list[self.index_save(user_choice)]

        # On supprime l'élément lié à l'action du dictionnaire edit_state_map.
        # ---------------------------------------------------------------------
        # We remove the action-related element from edit_state_map.
        del self.edit_state_map[user_choice]

        # On détruit le Radiobutton associé.
        # ---------------------------------------
        # We destroy the associated Radiobutton.
        selected_radiobutton.destroy()

        # On utilise edit_state_map_sort pour enlever le décalage dans edit_state_map 
        # potentiellement causé par la suppression.
        # ----------------------------------------------------------------------------
        # We use edit_state_map_sort to remove any shift in edit_state_map
        # potentially caused by the deletion.
        self.edit_state_map_sort(user_choice)

        # On re selectionne le premiers Radiobuttons.
        # --------------------------------------------
        # We reselect the first Radiobutton.
        self.selected_action_var.set(0)



    def delete_action_instance_in_container(self, container: Loop|ParallelActions, container_index: int) -> None:
        """
        Cette fonction permet de supprimer du conteneur dans lequel elle se trouve:
        - l'action dans le dictionnaire des actions
        - le Checkbutton de l'arbre principal représentant l'action

        :param container: instance du conteneur dans lequel ce trouve 
            l'acion qui a été supprimer
        :param container_index: Clé correspondante à la place de l'action
            dans le conteneur
        ----------------------------------------------------------------------------------
        This function deletes from the container in which it is located:
        - the action from the action dictionary
        - the Checkbutton representing the action in the main tree

        :param container: The container instance in which the deleted action was located.
        :param container_index: The key corresponding to the position of the action
            inside the container.
        """

        # Dictionnaire des action:
        # On enlève un à la clé next_container_action_index car on supprime un élément.
        # ----------------------------------------------------------------
        # Action dictionary:
        # We subtract 1 from next_container_action_index since we are deleting an element.
        container.next_container_action_index -= 1
        # On supprime dans le dictionnaire l'instance de l'action.
        # ---------------------------------------------------------
        # We delete the action instance from the dictionary.
        del container.container_actions_dict[container_index]
        # On trie le dictionnaire pour enlever le décalage causer par la suppression d'un élément.
        # -----------------------------------------------------------------------------------------
        # We sort the dictionary to remove the shift caused by deleting an element.
        container.container_actions_dict = self.sort_dict(container.container_actions_dict, container_index)

        # Dictionnaire des checkbouton:
        # On enlève un à la clé tree_container_idx car on supprime un élément.
        # -----------------------------------------------------------------
        # Checkbutton dictionary:
        # We subtract 1 from tree_container_idx since we are deleting an element.
        container.tree_container_idx -= 1
        # On détruit le checkbouton.
        # ----------------------------
        # We destroy the Checkbutton.
        container.container_action_checkbuttons[container_index][1].destroy()
        # On supprime dans le dictionnaire le checkbouton.
        # -------------------------------------------------
        # We delete the Checkbutton from the dictionary.
        del container.container_action_checkbuttons[container_index]
        # On trie le dictionnaire pour enlever le décalage causer par la suppression d'un élément.
        # -----------------------------------------------------------------------------------------
        # We sort the dictionary to remove the shift caused by deleting an element.
        container.container_action_checkbuttons = self.sort_dict(container.container_action_checkbuttons, container_index)



    def delete_action_instance(self, container_index: int) -> None:
        """
        Cette fonction permet de supprimer l'action dans le dictionnaire des action 
        et le checkbutton représentant l'action de l'arbre principale.

        :param container_index: Clé correspondante à la place de l'action
            dans son conteneur (ici son conteneur est la branche principale)
        ----------------------------------------------------------------------------
        This function deletes the action from the action dictionary
        and the Checkbutton representing the action in the main tree.

        :param container_index: The key corresponding to the position of the action
        in its container (here, its container is the main branch).
        """
        # Dictionnaire des action:
        # On enlève un à la clé next_action_key car on supprime un élément.
        # ---------------------------------------------------------------------
        # Action dictionary:
        # We subtract 1 from next_action_key since we are deleting an element.
        self.ui_action_manager.action_manager.next_action_key -= 1
        # On supprime dans le dictionnaire des actions l'action.
        # -------------------------------------------------------
        # We delete the action from the action dictionary.
        del self.ui_action_manager.action_manager.action_dict[container_index]
        # On trie le dictionnaire pour enlever le décalage causer par la suppression d'un élément.
        # -----------------------------------------------------------------------------------------
        # We sort the dictionary to remove the shift caused by deleting an element.
        self.ui_action_manager.action_manager.action_dict = self.sort_dict(self.ui_action_manager.action_manager.action_dict, container_index)

        # Dictionnaire des checkbouton:
        # On enlève un à la clé next_tree_dict_key car on supprime un élément.
        # ------------------------------------------------------------------------
        # Checkbutton dictionary:
        # We subtract 1 from next_tree_dict_key since we are deleting an element.
        self.next_tree_dict_key -= 1
        # On détruit le checkbouton.
        # ----------------------------
        # We destroy the Checkbutton.
        self.action_checkbuttons_dict[container_index][1].destroy()
        # On supprime dans le dictionnaire le checkbouton.
        # -------------------------------------------------
        # We delete the Checkbutton from the dictionary.
        del self.action_checkbuttons_dict[container_index]
        # On trie le dictionnaire pour enlever le décalage causer par la suppression d'un élément.
        # -----------------------------------------------------------------------------------------
        # We sort the dictionary to remove the shift caused by deleting an element.
        self.sort_action_checkbuttons_dict(container_index)



    def toggle_save_widgets(self) -> None:
        """
        Cette fonction permet d'afficher ou de cacher les widgets 
        nécessaires à l'enregistrement d'une suite d'actions
        en fonction de save_clicked.
        ----------------------------------------------------------
        This function shows or hides the widgets
        required to save an action sequence,
        depending on the value of save_clicked.
        """
        
        if self.save_clicked:
            self.save_frame.grid_remove()
            self.save_clicked = False
        else:
            self.save_frame.grid(row=5, column=0)
            self.save_clicked = True



    def quit(self) -> None:
        """
        Cette fonction permet de quitter le menu de modification de la suite d'actions. 
        --------------------------------------------------------------------------------
        This function exits the action sequence editing menu.
        """

        # On met in_edit à False pour indiquer que l'on n'édite plus.
        # --------------------------------------------------------------
        # We set in_edit to False to indicate that editing has stopped.
        self.in_edit = False
        
        # On détruit tous les Radiobuttons de la frame d'édition.
        # --------------------------------------------------------
        # We destroy all Radiobuttons in the editing frame.
        for action_data in self.edit_state_map.values():
            action_data[2].destroy()
        # On cache la frame d'édition.
        # -----------------------------
        # We hide the editing frame.
        self.edit_tree_frame.grid_remove()

        # On réaffiche tous les Checkbuttons de l'arbre principal à la bonne position.
        # -----------------------------------------------------------------------------
        # We redisplay all Checkbuttons of the main tree in their correct positions.
        for index, ChkBt in self.action_checkbuttons_dict.items():
            ChkBt[1].grid_remove()
            ChkBt[1].grid(row=ChkBt[2], column=0)
        # On réaffiche tree_frame pour remplacer edit_tree_frame.
        # --------------------------------------------------------
        # We redisplay tree_frame to replace edit_tree_frame.
        self.tree_frame.grid(row=0, column=0)



    def call_save(self) -> None:
        """
        Cette fonction permet d'enregistrer la suite d'actions. 
        --------------------------------------------------------
        This function saves the action sequence.
        """
        # On vérifie que la suite d'actions n'est pas en cours d'exécution.
        # ------------------------------------------------------------------
        # We check that the action sequence is not currently running.
        if not self.ui_action_manager.action_manager.is_running:
            # On utilise save_sequence pour enregistrer la suite d'actions.
            # --------------------------------------------------------------
            # We use save_sequence to save the action sequence.
            msg_error = save_sequence(self.name_entry.get(), self.ui_action_manager.action_manager.save_list)
            
            if msg_error != True:
                # Si save_sequence a retourné un message d'erreur, on l'affiche.
                # ---------------------------------------------------------------
                # If save_sequence returned an error message, we display it.
                self.save_error_label.config(text=msg_error[0], height=msg_error[1])
                self.save_error_label.grid(row=1, column=0)
            else:
                # Sinon, on cache le message d'erreur et les widgets nécessaires à l'enregistrement.
                # -----------------------------------------------------------------------------------
                # Otherwise, we hide the error message and the save widgets.
                self.save_error_label.grid_remove()
                self.toggle_save_widgets()



    def add_tree(self, text: str) -> None:
        """
        Cette fonction permet d'ajouter une action à l'arbre des actions.

        :param text: Texte à afficher dans l'arbre des actions pour représenter l'action.
        ----------------------------------------------------------------------------------
        This function adds an action to the action tree.

        :param text: The text displayed in the action tree to represent the action.
        """

        # On crée le Checkbutton correspondant à l'action.
        # -------------------------------------------------------
        # We create the Checkbutton corresponding to the action.
        check_var = tk.IntVar(value=1)
        action_checkbutton = tk.Checkbutton(
            self.all_actions.scrollable_frame, 
            text=text, 
            variable=check_var, 
            bg=W_VAR.NEUTRAL_700,
            fg=W_VAR.TEXT_COLOR,
            font=W_VAR.little_font_size,
            activebackground=W_VAR.NEUTRAL_800,
            activeforeground=W_VAR.TEXT_COLOR,
            selectcolor=W_VAR.NEUTRAL_700
            )
        action_checkbutton.grid(row=self.next_checkbutton_row+1, column=0, sticky="wn")

        # On ajoute le Checkbutton au dictionnaire comportant tous les Checkbuttons de l'arbre principal.
        # ------------------------------------------------------------------------------------------------
        # We add the Checkbutton to the dictionary containing all Checkbuttons of the main tree.
        self.action_checkbuttons_dict[self.next_tree_dict_key] = [check_var, action_checkbutton, self.next_checkbutton_row+1]

        # On incrémente la clé du dictionnaire.
        # --------------------------------------
        # We increment the dictionary key.
        self.next_tree_dict_key += 1
        # On incrémente la variable indiquant les rangées des Checkbuttons.
        # ------------------------------------------------------------------
        # We increment the variable indicating the Checkbutton rows.
        self.next_checkbutton_row += 1



    def sort_action_checkbuttons_dict(self, deleted_element_key: int) -> None:
        """
        Cette fonction modifie le dictionnaire action_checkbuttons_dict
        après qu'un de ses éléments ait été supprimé afin de supprimer le décalage dans les clés
        et les valeurs correspondant à la rangée de chaque Checkbutton.

        :param deleted_element_key: Index de l'élément ayant été supprimé dans action_checkbuttons_dict.
        -------------------------------------------------------------------------------------------------
        This function modifies the action_checkbuttons_dict dictionary
        after one of its elements has been deleted, in order to remove
        the shift in the keys and the values corresponding to the row
        of each Checkbutton.

        :param deleted_element_key: The index of the element deleted
            from action_checkbuttons_dict.
        """

        # Nouveau dictionnaire que l'on va remplir au fur et à mesure
        # avec les éléments de action_checkbuttons_dict modifiés.
        # ------------------------------------------------------------
        # New dictionary that we will populate progressively
        # with the modified elements of action_checkbuttons_dict.
        reindexed_dict = {}

        # On parcourt action_checkbuttons_dict.
        # ---------------------------------------------
        # We iterate through action_checkbuttons_dict.
        for key, value in self.action_checkbuttons_dict.items() :
            if key > deleted_element_key:
                # Si l'élément se trouve après l'élément supprimé on l'ajoute à 
                # reindexed_dict en enlevant 1 à la clée et à l'élément correspondant 
                # à la rangée du Checkbutton.
                # --------------------------------------------------------------------
                # If the element is located after the deleted element,
                # we add it to reindexed_dict while subtracting 1 from the key
                # and from the value corresponding to the Checkbutton row.
                reindexed_dict[key-1] = [value[0], value[1], value[2]-1]
            else:
                # S'il est avant l'élément supprimé on l'ajoute sans 
                # modification à reindexed_dict.
                # ---------------------------------------------------
                # If it is located before the deleted element,
                # we add it to reindexed_dict without modification.
                reindexed_dict[key] = [value[0], value[1], value[2]]

        # On remplace action_checkbuttons_dict par sa version modifiée.
        # ---------------------------------------------------------------
        # We replace action_checkbuttons_dict with its modified version.
        self.action_checkbuttons_dict = reindexed_dict



    def edit_act(self) -> None:
        """
        Cette fonction permet d'ouvrir l'interface de modification d'une action
        en re saisissant les paramètres de l'action afin que l'utilisateur puisse les modifier
        ---------------------------------------------------------------------------------------
        This function opens the action editing interface
        by re-entering the parameters of the action so that the user can modify them.
        """

        # On cache edit_tree_frame et on affiche edit_act_frame à la place.
        # ------------------------------------------------------------------
        # Hide edit_tree_frame and display edit_act_frame instead.
        self.edit_tree_frame.grid_remove()
        self.edit_act_frame.grid(row=0, column=0)

        # On affiche le bouton permettant la modification 
        # d'une action par l'utilisateur.
        # ----------------------------------------------------------
        # Display the button allowing the user to modify an action.
        self.validate_button_edit.grid(row=2, column=0, pady=(25, 0))

        # On récupère l'instance de l'action choisie par l'utilisateur.
        # --------------------------------------------------------------
        # Retrieve the instance of the action selected by the user.
        action_instance = self.edit_state_map[self.selected_action_var.get()][1]
        # On récupère le type de l'action choisie par l'utilisateur.
        # -----------------------------------------------------------
        # Retrieve the type of the action selected by the user.
        action_type = action_instance.action_type()

        # En fonction du type on prés remplis les différents paramètres
        # (enlève les paramètres déjà présent puis ajoute les nouveaux) de 
        # l'action puis on affiche la frame permettant de les modifier.
        # -----------------------------------------------------------------
        # Depending on the type, pre-fill the different parameters
        # (remove existing parameters and then add the new ones) of
        # the action and display the frame that allows them to be edited.
        match action_type:

            case ActionType.CLICK_LEFT.value:
                self.click_ui.set_coordinate((action_instance.pos_x, action_instance.pos_y), "xy")
                self.click_frame.grid(row=0, column=0)
                # Lance l'affichage de la souris en temps réel 
                # et le raccourci de remplissage des zones de texte.
                # ---------------------------------------------------
                # Toggle already selected buttons before activating 
                # only those passed as parameters.
                self.start_keyposition()

            case ActionType.CLICK_RIGHT.value:
                self.click_ui.set_coordinate((action_instance.pos_x, action_instance.pos_y), "xy")
                self.click_frame.grid(row=0, column=0)
                # Lance l'affichage de la souris en temps réel 
                # et le raccourci de remplissage des zones de texte.
                # -------------------------------------------------------------
                # Starts the real-time mouse display
                # and the shortcut used to automatically fill the text fields.
                self.start_keyposition()

            case ActionType.MOVE.value:
                self.move_ui.set_coordinate((action_instance.pos_x, action_instance.pos_y), "xy")
                self.move_ui.set_move_type(action_instance.move_type)
                self.move_frame.grid(row=0, column=0)
                # Lance l'affichage de la souris en temps réel 
                # et le raccourci de remplissage des zones de texte.
                # -------------------------------------------------------------
                # Starts the real-time mouse display
                # and the shortcut used to automatically fill the text fields.
                self.start_keyposition()

            case ActionType.WRITE.value:
                self.write_ui.text_area.delete("1.0", tk.END)
                self.write_ui.text_area.insert("1.0", action_instance.payload_text)
                self.write_frame.grid(row=0, column=0)

            case ActionType.SCROLL.value:
                self.scroll_ui.select_direction(action_instance.direction)
                self.scroll_ui.entry_steps.delete(0, tk.END)
                self.scroll_ui.entry_steps.insert(0, action_instance.step)
                self.scroll_frame.grid(row=0, column=0)

            case ActionType.WAIT.value:
                self.wait_ui.entry_wait_duration.delete(0, tk.END)
                self.wait_ui.entry_wait_duration.insert(0, action_instance.time_wait_s)
                self.wait_frame.grid(row=0, column=0)

            case ActionType.KEY_PRESS.value:
                # On fait basculer les boutons déjà cliqués avant d'activer uniquement ceux passés en paramètre.
                # -----------------------------------------------------------------------------------------------
                # Toggle already selected buttons before activating only those passed as parameters.
                for special_key in list(self.pressed_ui._selected_special_keys):
                    self.pressed_ui.toggle_special_key(special_key)
                for special_key in action_instance.special_keys:
                    self.pressed_ui.toggle_special_key(special_key)

                self.pressed_ui.entry_duration.delete(0, tk.END)
                self.pressed_ui.entry_duration.insert(0, action_instance.time_wait_s)
                self.pressed_ui.entry_normal_keys.delete(0, tk.END)
                self.pressed_ui.entry_normal_keys.insert(0, action_instance.keys)
                self.pressed_frame.grid(row=0, column=0)

            case ActionType.PARALLEL_ACTIONS.value:
                # On fait basculer les boutons déjà cliqués avant d'activer uniquement ceux passés en paramètre.
                # -----------------------------------------------------------------------------------------------
                # Toggle already selected buttons before activating only those passed as parameters.
                for special_key in list(self.parallel_actions_ui._selected_special_keys):
                    self.parallel_actions_ui.toggle_special_key(special_key)
                for special_key in action_instance.special_keys:
                    self.parallel_actions_ui.toggle_special_key(special_key)

                self.parallel_actions_ui.entry_normal_keys.delete(0, tk.END)
                self.parallel_actions_ui.entry_normal_keys.insert(0, action_instance.keys)
                self.parallel_actions_ui.name_entry.delete(0, tk.END)
                self.parallel_actions_ui.name_entry.insert(0, action_instance.name)
                self.parallel_actions_frame.grid(row=0, column=0)

                # On supprime le nom du PARALLEL_ACTIONS de la liste parallel_action_names
                # Puis il sera re ajouter modifier ou non quand l'utilisateur validera ces modification.
                # ---------------------------------------------------------------------------------------
                # Remove the PARALLEL_ACTIONS name from the parallel_action_names list.
                # It will then be re-added (modified or not) when the user validates the changes.
                self.container_manager.parallel_action_names.remove(action_instance.name)

            case ActionType.LOOP.value:
                self.loop_ui.entry_nb_turns.delete(0, tk.END)
                self.loop_ui.entry_nb_turns.insert(0, action_instance.nb_turns)
                self.loop_ui.entry_loop_name.delete(0, tk.END)
                self.loop_ui.entry_loop_name.insert(0, action_instance.name)
                self.loop_frame.grid(row=0, column=0)

                # On supprime le nom de la boucle de la liste loop_names
                # Puis il sera re ajouter modifier ou non quand l'utilisateur validera ces modification.
                # ---------------------------------------------------------------------------------------
                # Remove the PARALLEL_ACTIONS name from the parallel_action_names list.
                # It will then be re-added (modified or not) when the user validates the changes.
                self.container_manager.loop_names.remove(action_instance.name)



    def start_keyposition(self) -> None:
        """
        Cette fonction s'occupe de lancer les éléments liés aux coordonnées
        de la souris pour les actions move et click
        (affichage des coordonnées en temps réel,
        raccourci de pré-remplissage).
        --------------------------------------------------------------------
        This function starts the elements related to mouse coordinates
        for move and click actions
        (real-time coordinate display,
        shortcut for auto-filling the fields).
        """
        
        # On crée une instance de KeyPosition.
        # Elle permet de savoir si l'utilisateur appuie sur les touches correspondantes
        # afin de récupérer les coordonnées de la souris et de les ajouter aux zones de texte dans move et click.
        # --------------------------------------------------------------------------------------------------------
        # Create an instance of KeyPosition.
        # It allows detection of whether the user presses the corresponding keys
        # in order to retrieve the mouse coordinates and add them to the text fields in move and click.
        self.mouse_position_listener = KeyPosition(self.click_ui.set_coordinate, self.move_ui.set_coordinate)
        
        # On indique que l'on est dans le menu de click ou de move.
        # ----------------------------------------------------------
        # Indicate that we are currently in the click or move menu.
        self.in_move_or_click = True

        # On lance l'affichage en temps réel de la position de la souris de l'utilisateur.
        # ---------------------------------------------------------------------------------
        # Start displaying the user's mouse position in real time.
        self.update_mouse_positions()



    def validate_edit(self):
        """
        Cette fonction récupère les nouveaux paramètres d'une action.
        S'ils sont incorrects, elle ne fait rien.
        Sinon, elle met à jour les éléments nécessaires afin de modifier
        l'action avec ces nouveaux paramètres,
        puis revient à l'interface d'édition de la suite d'actions.
        -----------------------------------------------------------------
        This function retrieves the new parameters of an action.
        If they are incorrect, it does nothing.
        Otherwise, it updates the necessary elements in order to modify
        the action with these new parameters,
        then returns to the action sequence editing interface.
        """

        # On récupère la clé de l'action choisie par l'utilisateur.
        # ----------------------------------------------------------
        # Retrieve the key of the action selected by the user.
        user_choice = self.selected_action_var.get()
        
        # On récupère toutes les valeurs associées à cette action.
        # ---------------------------------------------------------
        # Retrieve all values associated with this action.
        container_index, action_instance, RdBt_edit, is_in_container, parent_container, number_container, padding = self.edit_state_map[user_choice]

        # On récupère l'index de l'action dans la liste de sauvegarde.
        # -------------------------------------------------------------
        # Retrieve the index of the action in the save list.
        index_element_in_save = self.index_save(user_choice)

        # On cherche le bon type d'action puis on :
        # Vérifie si les paramètres sont incorrects, on ne fait rien.
        # Sinon :
        # On modifie les paramètres dans l'instance de l'action
        # On modifie l'action dans la liste d'enregistrement
        # On cache l'interface de modification de l'action
        # ------------------------------------------------------------
        # Determine the correct action type and then:
        # If the parameters are incorrect, do nothing.
        # Otherwise:
        # Modify the parameters in the action instance.
        # Modify the action in the save list.
        # Hide the action editing interface.
        match action_instance.action_type():

            case ActionType.CLICK_LEFT.value:
                args = self.click_ui.check()
                if args:
                    action_instance.pos_x = args[0]
                    action_instance.pos_y = args[1]
                    self.ui_action_manager.action_manager.save_list[index_element_in_save] = [action_instance.action_type(), args[0], args[1]]
                    self.click_frame.grid_remove()
                    # On arrête le raccourci de rempliseage des zone de texte.
                    # ---------------------------------------------------------
                    # Stop the shortcut used to auto-fill the text fields.
                    self.mouse_position_listener.stop_listening()
                    # On arrête l'afficheage de la souris en temps réel.
                    # ---------------------------------------------------
                    # Stop the real-time mouse display.
                    self.in_move_or_click = False

            case ActionType.CLICK_RIGHT.value:
                args = self.click_ui.check()
                if args:
                    action_instance.pos_x = args[0]
                    action_instance.pos_y = args[1]
                    self.ui_action_manager.action_manager.save_list[index_element_in_save] = [action_instance.action_type(), args[0], args[1]]
                    self.click_frame.grid_remove()
                    # On arrête le raccourci de rempliseage des zone de texte.
                    # ---------------------------------------------------------
                    # Stop the shortcut used to auto-fill the text fields.
                    self.mouse_position_listener.stop_listening()
                    # On arrête l'afficheage de la souris en temps réel.
                    # ---------------------------------------------------
                    # Stop the real-time mouse display.
                    self.in_move_or_click = False

            case ActionType.MOVE.value:
                args = self.move_ui.check()
                if args:
                    action_instance.pos_x = args[0]
                    action_instance.pos_y = args[1]
                    action_instance.move_type = args[2]
                    self.ui_action_manager.action_manager.save_list[index_element_in_save] = [action_instance.action_type(), args[0], args[1], args[2]]
                    self.move_frame.grid_remove()
                    # On arrête le raccourci de rempliseage des zone de texte.
                    # ---------------------------------------------------------
                    # Stop the shortcut used to auto-fill the text fields.
                    self.mouse_position_listener.stop_listening()
                    # On arrête l'afficheage de la souris en temps réel.
                    # ---------------------------------------------------
                    # Stop the real-time mouse display.
                    self.in_move_or_click = False

            case ActionType.WRITE.value:
                args = self.write_ui.check()
                if args:
                    action_instance.payload_text = args[0]
                    self.ui_action_manager.action_manager.save_list[index_element_in_save] = [action_instance.action_type(), args[0]]
                    self.write_frame.grid_remove()

            case ActionType.SCROLL.value:
                args = self.scroll_ui.check()
                if args:
                    action_instance.step = args[0]
                    action_instance.direction = args[1]
                    self.ui_action_manager.action_manager.save_list[index_element_in_save] = [action_instance.action_type(), args[0], args[1]]
                    self.scroll_frame.grid_remove()

            case ActionType.WAIT.value:
                args = self.wait_ui.check()
                if args:
                    action_instance.time_wait_s = args
                    action_instance.time_wait_ms = int(args*1000)
                    self.ui_action_manager.action_manager.save_list[index_element_in_save] = [action_instance.action_type(), args]
                    self.wait_frame.grid_remove()

            case ActionType.KEY_PRESS.value:
                args = self.pressed_ui.check()
                if args:
                    action_instance.keys = args[0]
                    action_instance.special_keys = args[1]
                    action_instance.time_wait_ms = int(args[2]*1000)
                    action_instance.time_wait_s = args[2]
                    self.ui_action_manager.action_manager.save_list[index_element_in_save] = [action_instance.action_type(), args[0], args[1], args[2]]
                    self.pressed_frame.grid_remove()

            case ActionType.PARALLEL_ACTIONS.value:
                args = self.parallel_actions_ui.check()
                if args:
                    action_instance.keys = args[0]
                    action_instance.special_keys = args[1]
                    action_instance.name = args[2]
                    self.ui_action_manager.action_manager.save_list[index_element_in_save] = [action_instance.action_type(), args[0], args[1], args[2]]
                    self.parallel_actions_frame.grid_remove()

                    if self.container_manager.container_map[number_container][0]:
                        # Si l'utilisateur se trouve encore à l'interieur du conteneur
                        # On modifie le nom de l'action dans conteneur manager on met true puis
                        # on met à joure le cadre indiquant à l'utilisateur qu'il est dans un conteneur 
                        # avec le nouveau nom.
                        # ------------------------------------------------------------------------------
                        # If the user is still inside the container:
                        # Update the action name in the container manager by setting True
                        # and update the frame indicating to the user that they are inside a container
                        # with the new name.
                        self.container_manager.container_map[number_container] = [True, args[2]]
                        self.container_manager.indicate_container(args[2])
                    else:
                        # Sinon on modifie le nom de l'action dans conteneur manager on met False.
                        # ----------------------------------------------------------------------------
                        # Otherwise update the action name in the container manager by setting False.
                        self.container_manager.container_map[number_container] = [False, args[2]]

            case ActionType.LOOP.value:
                args = self.loop_ui.check()
                if args:
                    action_instance.nb_turns = args[0]
                    action_instance.name = args[1]
                    self.ui_action_manager.action_manager.save_list[index_element_in_save] = [action_instance.action_type(), args[0], args[1]]
                    self.loop_frame.grid_remove()

                    if self.container_manager.container_map[number_container][0]:
                        # Si l'utilisateur se trouve encore à l'interieur du conteneur
                        # On modifie le nom de l'action dans conteneur manager on met true puis
                        # on met à joure le cadre indiquant à l'utilisateur qu'il est dans un 
                        # conteneur avec le nouveau nom.
                        # ----------------------------------------------------------------------
                        # If the user is still inside the container:
                        # Update the action name in the container manager by setting True
                        # and update the frame indicating to the user that they are inside a
                        # container with the new name.
                        self.container_manager.container_map[number_container] = [True, args[1]]
                        self.container_manager.indicate_container(args[1])
                    else:
                        # Sinon on modifie le nom de l'action dans conteneur manager on met False.
                        # ----------------------------------------------------------------------------
                        # Otherwise update the action name in the container manager by setting False.
                        self.container_manager.container_map[number_container] = [False, args[1]]
        
        # Si les paramètres sont corrects.
        # ---------------------------------
        # If the parameters are valid.
        if args:
            # On met à jour le Checkbutton représentant l'action dans l'arbre des actions.
            # -----------------------------------------------------------------------------
            # Update the Checkbutton representing the action in the action tree.
            if parent_container == None:
                self.action_checkbuttons_dict[container_index][1].config(text=action_instance.text())
            else:
                parent_container.container_action_checkbuttons[container_index][1].config(text=action_instance.text())
            # On met à jour le Radiobutton représentant l'action dans l'interface d'édition.
            # -------------------------------------------------------------------------------
            # Update the Radiobutton representing the action in the editing interface.
            RdBt_edit.config(text=action_instance.text())
            # On cache les éléments de la frame d'édition des paramètres pour
            # réafficher la frame d'édition de la suite d'actions.
            # ----------------------------------------------------------------
            # Hide the elements of the parameter editing frame
            # to display again the action sequence editing frame.
            self.validate_button_edit.grid_remove()
            self.edit_act_frame.grid_remove()
            self.edit_tree_frame.grid(row=0, column=0)

    def reset_state(self) -> None:
        """
        Réinitialise les variables de gestion de l'arbre.
        ----------------------------------------------------
        Reset the variables used to manage the action tree.
        """

        # Destruction des Checkbuttons de l'arbre.
        # -----------------------------------------
        # Destroy all Checkbuttons in the tree.
        for checkbutton in self.action_checkbuttons_dict.values():
            checkbutton[1].grid_remove()
            checkbutton[1].destroy() 
        
        # Réinitialisation des valeurs liées à l'arbre.
        # ----------------------------------------------
        # Reset the values related to the action tree.
        self.action_checkbuttons_dict = {}
        self.next_tree_dict_key = 0
        self.next_checkbutton_row = 0
        self.save_frame.grid_remove()
        self.save_clicked = False



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
        # vérifie que l'utilisateur est toujours dans une interface de mouvement ou de clic
        # ----------------------------------------------------------------------------------
        # Check that the user is still in a move or click interface.
        if self.in_move_or_click:
            # On rappelle cette fonction toutes les 60 ms
            # --------------------------------------------
            # Call this function again after 60 ms.
            self.window.after(60, self.update_mouse_positions)