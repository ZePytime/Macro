from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Callable
from functools import partial

from sequence_manager import load_saved_sequences, save_all_sequences
from scrollable_frame import ScrollableFrame
from hover_button import HoverButton

if TYPE_CHECKING:
    from main import WindowVariable
    from action_manager import ActionManager
    from container_manager import ContainerManager
from ui_style import W_VAR



class SavedSequencesUI:
    """
    Gère l'interface permettant à l'utilisateur l'ouverture ou
    la suppression des fichiers (suites d'actions enregistrées)
    ------------------------------------------------------------
    Manages the interface that allows the user to open 
    or delete files(saved action sequences).
    """
    def __init__(self, window: tk.Tk, main_frm: tk.Frame, menu_btn_frame: tk.Frame, switch_frame: Callable[[tk.Frame], None], reset_action_sequence: callable, action_dict_manager: ActionManager, leave_current_container: callable, container_manager: ContainerManager) -> None:
        """
        Initialise les valeurs et l'interface afin d'afficher les fichiers
            (suites d'actions enregistrées) et de permettre de les ouvrir ou de les supprimer

        :param window: Fenêtre principale de l'interface.
        :param main_frm: Cadre principal dans lequel se trouve ce menu.
        :param menu_btn_frame: Menu dans lequel on ajoute le bouton
            permettant de basculer vers cette interface
        :param switch_frame: Fonction permettant de changer de frame
            afin d'afficher ce menu
        :param reset_action_sequence: Fonction permettant de réinitialiser la suite d'action actuelle
            et les paramètres qui y sont liés
        :param action_manager: Instance de la classe gérant le dictionnaire
            de la suite d'actions
        :param leave_current_container: Fonction permettant à recreate_action_sequence
            d'indiquer quand il sort d'un conteneur comme loop
        :param container_manager: Instance permettant d'enregistrer tous les noms
            de conteneur et de savoir si l'on est actuellement dans un conteneur
        -------------------------------------------------------------------------------------------
        Initializes the values and the interface in order to display the files
        (saved action sequences) and allow them to be opened or deleted.

        :param window: Main interface window.
        :param main_frm: Main frame in which this menu is located.
        :param menu_btn_frame: Menu in which the button allowing access to this interface is added
        :param switch_frame: Function used to switch frames in order to display this menu
        :param reset_action_sequence: Function used to reset the current action sequence
            and all related parameters
        :param action_manager: Instance of the class managing the action sequence dictionary
        :param leave_current_container: Function allowing recreate_action_sequence
            to indicate when it exits a container such as a loop
        :param container_manager: Instance used to store all container names
            and to know whether the program is currently inside a container
        """

        # Fonction permettant de changer de frame afin d'afficher ce menu
        # ----------------------------------------------------------------
        # Function used to change the frame in order to display this menu
        self.switch_frame = switch_frame

        # Fonction appelée avant d'appeler recreate_action_sequence, elle permet de
        # réinitialiser la suite d'action actuelle et les paramètres qui y sont liés
        # ---------------------------------------------------------------------------
        # Function called before calling recreate_action_sequence.
        # It resets the current action sequence and all related parameters
        self.reset_action_sequence = reset_action_sequence

        # Paramètres nécessaires à la fonction recreate_action_sequence 
        # qui permet d'ouvrir une suite d'action enregistrée
        #------------------------------------------------------------
        # Parameters required by recreate_action_sequence to open 
        # a saved action sequence
        self.action_dict_manager = action_dict_manager
        self.leave_current_container = leave_current_container

        # Dictionnaire contenant tous les radio-boutons des suites d'actions enregistrées
        # --------------------------------------------------------------------------------
        # Dictionary containing all radio buttons for saved action sequences
        self.radio_btns = {}
        # Radio-bouton actuellement sélectionné par l'utilisateur
        # --------------------------------------------------------
        # Radio button currently selected by the user
        self.selected_file = None
        # Contenu du fichier permettant d'enregistrer les suites d'actions
        # -----------------------------------------------------------------
        # File content storing the saved action sequences
        self.saved_sequences = None

        
        # Bouton permettant d'accéder à ce menu
        # --------------------------------------
        # Button allowing access to this menu
        self.open_menu_btn = HoverButton(
            menu_btn_frame, 
            text="file", 
            color=W_VAR.BUTTON_4,
            hover=W_VAR.BUTTON_4_HOVER,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=5, 
            font=W_VAR.font_size, 
            command=self.show_frame
            )
        self.open_menu_btn.grid(row=0, column=2, padx=2, pady=2)

        # Frame principale de ce menu
        # ----------------------------
        # Main frame of this menu
        self.open_menu_frame = tk.Frame(main_frm, bg=W_VAR.NEUTRAL_800, width=340, height=460)
        self.open_menu_frame.columnconfigure(0, weight=1)
        self.open_menu_frame.grid_propagate(False)

        # Frame scrollable affichant tous les fichiers (suites d'actions enregistrées)
        # -----------------------------------------------------------------------------
        # Scrollable frame displaying all files (saved action sequences)
        self.files_scrollable = ScrollableFrame(self.open_menu_frame, width=260, height=310)
        self.files_scrollable.grid(row=0, column=0, padx=30, pady=(30, 20))

        # Label d'erreur (caché jusqu'à son utilisation)
        # ----------------------------------
        # Error label (hidden until needed)
        self.error_label = tk.Label(
            self.files_scrollable.scrollable_frame, 
            text='You have no files.', 
            bg=W_VAR.NEUTRAL_700, 
            fg=W_VAR.ERROR_COLOR, 
            height=2, 
            width=35, 
            font=W_VAR.font_size_error
            )

        # Bouton d'ouverture de la suite d'action enregistrée sélectionnée
        # -----------------------------------------------------------------
        # Button used to open the selected saved action sequence
        open_btn = HoverButton(
            self.open_menu_frame, 
            text="Open", 
            color=W_VAR.BUTTON_2,
            hover=W_VAR.BUTTON_2_HOVER,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=20, 
            font=W_VAR.font_size, 
            command=lambda : self.open_file(self.action_dict_manager, self.reset_action_sequence, self.leave_current_container, container_manager)
            )
        open_btn.grid(row=1, column=0, pady=5)

        # Bouton de suppression de la suite d'action enregistrée sélectionnée
        # --------------------------------------------------------------------
        # Button used to delete the selected saved action sequence
        delete_btn = HoverButton(
            self.open_menu_frame, 
            text="Delete", 
            color=W_VAR.BUTTON_1,
            hover=W_VAR.BUTTON_1_HOVER,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=20, 
            font=W_VAR.font_size, 
            command=lambda : self.confirm_delete_popup(window)
            )
        delete_btn.grid(row=2, column=0)


    def show_frame(self) -> None:
        """
        Met à jour l'affichage des fichiers dans la frame 
        scrollable puis affiche la frame de ce menu
        --------------------------------------------------
        Updates the file display in the scrollable frame
        and then displays this menu's frame.
        """
        self.refresh_file_list(self.files_scrollable, self.error_label)
        self.switch_frame(self.open_menu_frame)


    def refresh_file_list(self, files_scrollable: ScrollableFrame, error_label: tk.Label) -> None:
        """
        Met à jour la liste de fichiers et les variables liées :
        - réinitialise les fichiers affichés dans la frame
        - vérifie s'il y a des fichiers enregistrés
        - met à jour les variables si aucun fichier n'est présent
        - sinon affiche un radio-bouton pour chaque fichier et sélectionne le premier
        
        :param files_scrollable: Frame scrollable dans laquelle on ajoute tous les fichiers
        :param error_label: Label informant qu'il n'y a pas de fichier enregistré
        ------------------------------------------------------------------------------
        Updates the list of files and related variables:
        - resets the files displayed in the frame
        - checks whether saved files exist
        - updates variables if no file is present
        - otherwise, displays a radio button for each file and selects the first one

        :param files_scrollable: Scrollable frame in which all files are added
        :param error_label: Label indicating that no file is saved
        """

        # Récupère le dictionnaire contenant les suites d'actions enregistrées
        # ---------------------------------------------------------------------
        # Retrieves the dictionary containing the saved action sequences
        self.saved_sequences = load_saved_sequences()

        # Suppression de tous les radio-boutons (fichiers) affichés dans la frame
        # ------------------------------------------------------------------------
        # Removes all radio buttons (files) displayed in the frame
        for radio_btn in self.radio_btns.values():
            radio_btn.destroy()
        
        # Si aucun fichier n'est enregistré
        # ----------------------------------
        # If no file is saved
        if not self.saved_sequences:
            # On remet les variables à None / vide
            # -------------------------------------
            # Reset variables to None / empty
            self.selected_file = None
            self.radio_btns = {}

            # On affiche le label d'erreur ("You have no files.")
            # ----------------------------------------------------
            # Display the error label ("You have no files.")
            error_label.grid(row=0, column=0)

        else:
            # On cache le label d'erreur
            # ---------------------------
            # Hide the error label
            error_label.grid_remove()

            # On sélectionne le premier fichier et on crée un radio-bouton pour chaque fichier
            # ---------------------------------------------------------------------------------
            # Select the first file and create a radio button for each file
            self.selected_file = tk.StringVar(value=list(self.saved_sequences.keys())[0])

            for nb_key, element in enumerate(self.saved_sequences.keys()):
                choix_open = tk.Radiobutton(
                    files_scrollable.scrollable_frame, 
                    text=element, 
                    variable=self.selected_file, 
                    value=element, 
                    font=W_VAR.font_size,
                    bg=W_VAR.NEUTRAL_700,
                    fg=W_VAR.TEXT_COLOR,
                    activebackground=W_VAR.NEUTRAL_800,
                    activeforeground=W_VAR.TEXT_COLOR,
                    selectcolor=W_VAR.NEUTRAL_700
                    )
                choix_open.grid(row=nb_key, column=0, sticky="w", padx=10)
                self.radio_btns[element] = choix_open


    def open_file(self, action_dict_manager: ActionManager, reset_action_sequence: callable, leave_current_container: callable, container_manager: ContainerManager) -> None:
        """
        Appelle la fonction de SavedActionSequence qui va recréer la suite d'action
        après que l'on ait réinitialisé la suite actuelle

        :param action_dict_manager: instance de la classe gérant le dictionnaire
            de la suite d'action
        :param reset_action_sequence: fonction permettant de réinitialiser la suite d'action actuelle
            et les paramètres qui y sont liés
        :param leave_current_container: fonction permettant à recreate_action_sequence
            d'indiquer quand il sort d'un conteneur comme loop
        :param container_manager: instance permettant d'enregistrer tous les noms
            de conteneur et de savoir si l'on est actuellement dans un conteneur
        ------------------------------------------------------------------------------------
        Calls the SavedActionSequence function that recreates the action sequence
        after the current one has been reset.

        :param action_dict_manager: instance of the class managing the action sequence dictionary
        :param reset_action_sequence: function used to reset the current action sequence
            and all related parameters
        :param leave_current_container: function allowing recreate_action_sequence
            to indicate when it exits a container such as a loop
        :param container_manager: instance used to store all container names
            and to know whether the program is currently inside a container
        """
        # On vérifie que la suite d'action n'est pas en cours d'exécution 
        # ----------------------------------------------------------------
        # Check that the action sequence is not currently running
        if not action_dict_manager.is_running:
            # On vérifie qu'un fichier est sélectionné
            # -----------------------------------------
            # Check that a file is selected
            if not self.selected_file == None:
                # On réinitialise la suite d'action actuelle
                # -------------------------------------------
                # Reset the current action sequence
                reset_action_sequence()
                # On recrée la suite d'action enregistrée sélectionnée
                # -----------------------------------------------------
                # Recreate the selected saved action sequence
                self.saved_sequences[self.selected_file.get()].recreate_action_sequence(action_dict_manager, leave_current_container, container_manager)


    def confirm_delete_popup(self, window: tk.Tk) -> None:
        """
        Crée une popup de confirmation avant de supprimer le fichier sélectionné
        
        :param window: Fenêtre principale de la macro
        -------------------------------------------------------------------------
        Creates a confirmation popup before deleting the selected file.

        :param window: Main window of the macro
        """
        # On vérifie qu'un fichier est sélectionné
        # -----------------------------------------
        # Check that a file is selected
        if not self.selected_file == None:
            popup = tk.Toplevel(window)
            popup.title("Zecron")
            popup.geometry("200x120")
            popup.config(bg=W_VAR.NEUTRAL_800)

            label = tk.Label(
                popup, 
                text="Are you sure you want to\ndelete the file?", 
                font=W_VAR.font_size,
                bg=W_VAR.NEUTRAL_800,
                fg=W_VAR.TEXT_COLOR
                )
            label.pack(pady=10)

            # Frame pour organiser les boutons de confirmation.
            # --------------------------------------------------
            # Frame to organize the confirmation buttons.
            confirmation_frame = tk.Frame(popup, bg=W_VAR.NEUTRAL_800)
            confirmation_frame.pack()

            # Bouton de confirmation de la suppression
            # -----------------------------------------
            # Button to confirm deletion
            yes_btn = HoverButton(
                confirmation_frame, 
                text="Yes", 
                color=W_VAR.BUTTON_1,
                hover=W_VAR.BUTTON_1_HOVER,
                fg=W_VAR.TEXT_COLOR, 
                height=1, 
                width=4, 
                font=W_VAR.font_size, 
                command=lambda : self.delete_file_and_close_popup(popup)
                )
            yes_btn.grid(row=0, column=0, padx=(0, 10))

            no_btn = HoverButton(
                confirmation_frame, 
                text="No", 
                color=W_VAR.BUTTON_1,
                hover=W_VAR.BUTTON_1_HOVER,
                fg=W_VAR.TEXT_COLOR, 
                height=1, 
                width=4, 
                font=W_VAR.font_size, 
                command=popup.destroy
                )
            no_btn.grid(row=0, column=1)


    def delete_file_and_close_popup(self, popup: tk.Toplevel) -> None:
        """
        Supprime le fichier sélectionné et ferme la popup puis met à jour l'affichage
        
        :param popup: popup de confirmation de la suppression
        ------------------------------------------------------------------------------
        Deletes the selected file, closes the popup, and updates the display.

        :param popup: confirmation popup for deletion
        """
        self.delete_file()
        popup.destroy()
        self.show_frame()


    def delete_file(self) -> None:
        """
        Permet de supprimer un fichier en supprimant son widget puis en le supprimant 
        du dictionnaire le SavedActionSequence et en réenregistrant le nouveau dictionnaire
        --------------------------------------------------------------------------------
        Deletes a file by removing its widget, removing it from the
        SavedActionSequence dictionary, and saving the updated dictionary.
        """

        if not self.selected_file == None:
            self.radio_btns[self.selected_file.get()].grid_remove()
            self.radio_btns[self.selected_file.get()].destroy()
            del self.radio_btns[self.selected_file.get()]
            del self.saved_sequences[self.selected_file.get()]
            save_all_sequences(self.saved_sequences)
