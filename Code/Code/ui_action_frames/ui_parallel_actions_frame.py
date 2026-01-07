from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Tuple, Union
from functools import partial

if TYPE_CHECKING:
    from main import WindowVariable
    from container_manager import ContainerManager


# Tuple de toutes les touches spéciales disponibles
# --------------------------------------------------
# Tuple of all available special keys
SPECIAL_KEYS_LAYOUT = (("alt", "ctrl", "altgr", "enter", "click r"), 
               ("esc", "delete", "shift", "tab", "backspace", "cmd"), 
               ("up", "left", "right", "down", "caps lock", "click l"))

MAX_NAME_LENGTH = 20

class ParallelActionsFrame:
    """
    Cette classe permet de créer l'interface qui va nous permettre de 
    définir des appuis de clavier.
    Elles seront pressées en même temps que d'autres actions.
    -----------------------------------------------------------------------
    This class creates the interface that allows us to define key presses.
    They will be pressed simultaneously with other actions.
    """

    def __init__(self, parent_frame: tk.Frame, w_var: WindowVariable, container_manager: ContainerManager) -> None:
        """
        Initialisation de l'interface de sélection des touches.

        :param parent_frame: la frame où les widgets seront placés
        :param w_var: objet contenant les paramètres d'affichage (couleurs, tailles, 
            screen_width/height)
        :param container_manager: classe permettant de gérer les conteneurs comme loop 
            et parallel_actions
        --------------------------------------------------------------------------------
        Initialization of the key selection interface.

        :param parent_frame: parent frame in which widgets will be created
        :param w_var: dataclass-like object with style attributes (colors, fonts) and 
            screen dimensions
        :param container_manager: class to manage containers like loop and 
            parallel_actions
        """

        # Classe permettant de gérer les conteneurs comme 'loop' et 'parallel_actions', 
        # elle nous sera utile pour vérifier les noms de parallel_actions déjà 
        # utilisés et lui donner les nouveaux noms
        # ---------------------------------------------------------
        # Class managing containers such as 'loop' and 'parallel_actions',
        # it will be useful for checking already used parallel_actions names
        # and giving them the new names
        self._container_manager = container_manager

        self._w_var = w_var

        # Liste des touches spéciales actuellement appuyées
        # -------------------------------------------------
        # List of special keys currently pressed
        self._selected_special_keys = set()

        # Dictionnaire des boutons des touches spéciales
        # -------------------------------------------------
        # Dictionary of special key buttons
        self._special_key_buttons: dict[str, tk.Button] = {}

        # Label informatif
        # -----------------
        # Info label
        info_label_name = tk.Label(
            parent_frame, 
            text='Enter a name:', 
            bg=w_var.color_1, 
            fg="black", 
            height=1, 
            width=30, 
            font=w_var.font_size
            )
        info_label_name.grid(row=0, column=0)

        # Entry pour le nom
        # -------------------
        # Entry for the name
        self.name_entry = tk.Entry(
            parent_frame, 
            width=16, 
            bg=w_var.color_2, 
            font=w_var.font_size
            )
        self.name_entry.grid(row=1, column=0)

        # Label informatif
        # -----------------
        # Info label
        info_label_keys = tk.Label(
            parent_frame, 
            text="Enter all the keys you wish to use\nsimultaneously with other actions :", 
            bg=w_var.color_1, 
            fg="black", 
            height=2, 
            width=30, 
            font=w_var.font_size
            )
        info_label_keys.grid(row=2, column=0)

        # Frame des boutons de touches spéciales
        # ---------------------------------------
        # Frame of special key buttons
        frm_special_keys = tk.Frame(parent_frame, bg=w_var.color_1)
        frm_special_keys.grid(row=3, column=0)

        # Création des boutons de touches spéciales en 3
        # lignes de boutons grâce à des frames imbriquées
        # -----------------------------------------------
        # Creation of special key buttons in 3
        # rows of buttons using nested frames
        for row, list_btn in enumerate(SPECIAL_KEYS_LAYOUT):

            frame_btn = tk.Frame(frm_special_keys, bg=w_var.color_1)
            frame_btn.grid(row=row, column=0)
            for column, name in enumerate(list_btn):
                btn_special_key = tk.Button(
                    frame_btn, 
                    text=name, 
                    bg=w_var.color_2, 
                    fg="black", 
                    height=1, 
                    width=len(name), 
                    command=partial(self.toggle_special_key, name)
                    )
                btn_special_key.grid(row=0, column=column)
                self._special_key_buttons[name] = btn_special_key

        # Entry pour les touches normales
        # --------------------------------
        # Entry for normal keys
        self.entry_normal_keys = tk.Entry(
            parent_frame, 
            width=15, 
            bg=w_var.color_2, 
            font=w_var.font_size
            )
        self.entry_normal_keys.grid(row=4, column=0)

        # Label d'erreur (caché jusqu'à son utilisation)
        # -----------------------------------------------
        # Error label (hidden until needed)
        self._error_label = tk.Label(
            parent_frame, 
            text="", 
            bg=w_var.color_1, 
            fg="black", 
            height=1, 
            width=40, 
            font=w_var.font_size_error
            )


    def toggle_special_key(self, name: str) -> None:
        """
        Gère le clic sur un bouton de touche spéciale en changeant la couleur
        du bouton afin que l'utilisateur sache quelles touches sont sélectionnées
        et ajoute la touche à la liste des touches spéciales sélectionnées.
        
        :param name: nom de la touche spéciale cliquée
        ----------------------------------------------------------------------------
        Handles the click on a special key button by changing the 
        button color so that the user knows which keys are selected
        and adds the key to the list of selected special keys.

        :param name: name of the clicked special key
        """
        if name in self._selected_special_keys:
            self._selected_special_keys.remove(name)
            self._special_key_buttons[name].config(bg=self._w_var.color_2)
        else:
            self._selected_special_keys.add(name)
            self._special_key_buttons[name].config(bg=self._w_var.color_4)


    def check(self) -> Union[Tuple[str, list[str], str], bool]:
        """
        On supprime aussi les doublons dans les touches normales.
        On vérifie qu'il y a au moins une touche sélectionnée.
        On vérifie que le nom est valide (non vide, pas trop long, pas déjà utilisé).

        :return: un tuple contenant les touches normales, les touches spéciales et 
            le nom si tout est valide, sinon False
        -----------------------------------------------------------------------------
        Removes duplicates in normal keys as well.
        Checks that at least one key is selected.
        Checks that the name is valid (not empty, not too long, not already used).

        :return: a tuple containing normal keys, special keys and
            the name if everything is valid, otherwise False
        """
        normal_keys_input = self.entry_normal_keys.get()
        parallel_action_name = self.name_entry.get()

        # Supprime les caractères en double dans l'Entry des touches normales
        # Conserve le premier exemplaire de chaque caractère en respectant l'ordre
        seen = set()
        deduped_chars = []
        for ch in normal_keys_input:
            if ch not in seen:
                seen.add(ch)
                deduped_chars.append(ch)
        deduped = "".join(deduped_chars)

        # Si des doublons ont été supprimés, 
        # met à jour l'Entry pour refléter la valeur nettoyée
        if deduped != normal_keys_input:
            self.entry_normal_keys.delete(0, tk.END)
            self.entry_normal_keys.insert(0, deduped)
        
        elif len(normal_keys_input) == 0 and len(self._selected_special_keys) == 0:
            self._show_error("You must enter at least one\n special key or one normal key", 2)
            return False

        if len(parallel_action_name) == 0:
            self._show_error("You haven't chosen a name", 1)
            return False
        if len(parallel_action_name) > MAX_NAME_LENGTH:
            self._show_error(f"You cannot choose a name \nlonger than {MAX_NAME_LENGTH} characters", 2)
            return False
        if parallel_action_name in self._container_manager.parallel_action_names:
            self._show_error("This name is already in use", 1)
            return False

        self._hide_error()
        self._container_manager.parallel_action_names.append(parallel_action_name)
        return normal_keys_input, list(self._selected_special_keys), parallel_action_name


    def _show_error(self, message: str, height: int) -> None:
        """
        Affiche un message d'erreur.

        :param message: Le message à afficher.
        :param height: La hauteur du label d'erreur (en lignes).
        --------------------------------------------------------
        Show an error message.

        :param message: The message to display.
        :param height: The height of the error label (in lines).
        """
        self._error_label.config(text=message, height=height)
        self._error_label.grid(row=6, column=0)


    def _hide_error(self) -> None:
        """
        Cache le label d'erreur.
        -------------------------
        Hide the error label.
        """
        self._error_label.grid_remove()