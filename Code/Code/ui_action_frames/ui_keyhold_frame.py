from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Tuple, Union
from functools import partial

if TYPE_CHECKING:
    from main import WindowVariable


# Tuple de toutes les touches spéciales disponibles
# --------------------------------------------------
# Tuple of all available special keys
SPECIAL_KEYS_LAYOUT = (("alt", "ctrl", "altgr", "enter", "click r"), 
               ("esc", "delete", "shift", "tab", "backspace", "cmd"), 
               ("up", "left", "right", "down", "caps lock", "click l"))

MAX_HOLD_DURATION = 604800  # 7 days in seconds


class KeyHoldFrame:
    """
    Cette classe permet de créer l'interface qui va nous permettre de 
    définir des appuis de clavier pour une durée donnée.
    ------------------------------------------------------------------
    This class creates the interface that will allow us to
    define key holds for a given duration.
    """

    def __init__(self, parent_frame: tk.Frame, w_var: WindowVariable) -> None:
        """
        Initialisation de l'interface de sélection des touches.

        :param parent_frame: la frame où les widgets seront placés
        :param w_var: objet contenant les paramètres d'affichage (couleurs, tailles, screen_width/height)
        ------------------------------------------------------------------------------------
        Initialization of the key selection interface.

        :param parent_frame: parent frame in which widgets will be created
        :param w_var: dataclass-like object with style attributes (colors, fonts) and screen dimensions
        """

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
        info_label_keys = tk.Label(
            parent_frame, 
            text='Enter all the keys\nyou want to use:', 
            bg=w_var.color_1, 
            fg="black", 
            height=2, 
            width=30, 
            font=w_var.font_size
            )
        info_label_keys.grid(row=0, column=0)

        # Frame des boutons de touches spéciales
        # ---------------------------------------
        # Frame of special key buttons
        frm_special_keys = tk.Frame(parent_frame, bg=w_var.color_1)
        frm_special_keys.grid(row=1, column=0)

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
        self.entry_normal_keys.grid(row=2, column=0)

        # Label informatif
        # -----------------
        # Info label
        info_label_time = tk.Label(
            parent_frame, 
            text='Enter the time during which you\nwant these buttons to be pressed:', 
            bg=w_var.color_1, 
            fg="black", 
            height=2, 
            width=30, 
            font=w_var.font_size
            )
        info_label_time.grid(row=3, column=0)

        # Entry pour le temps que les touches doivent être appuyées
        # ----------------------------------------------------------
        # Entry for the time the keys must be pressed
        self.entry_duration = tk.Entry(
            parent_frame, 
            width=15, 
            bg=w_var.color_2, 
            font=w_var.font_size
            )
        self.entry_duration.grid(row=5, column=0)


        # Label d'erreur (caché jusqu'à utilisation)
        # -------------------------------------------
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


    def check(self) -> Union[Tuple[str, list[str], float], bool]:
        """
        Vérifie que le temps saisi est un nombre, n'est pas trop élevé, moins de 3 décimales, 
        et qu'il y a au moins une touche sélectionnée. On supprime aussi les doublons dans 
        les touches normales.

        :return: un tuple (str de touches normales, liste de touches spéciales, float temps) 
            si ok, sinon False et affiche un message d'erreur.
        -------------------------------------------------------------------------------------
        Checks that the entered time is a number, not too high, less than 3 decimals,
        and that there is at least one key selected. Also removes duplicates in
        normal keys.

        :return: a tuple (str of normal keys, list of special keys, float time) if ok, 
            otherwise False and displays an error message.
        """

        normal_keys_input = self.entry_normal_keys.get()
        duration_value = self.entry_duration.get()

        # Supprime les caractères en double dans l'Entry des touches normales
        # conserve le premier exemplaire de chaque caractère en respectant l'ordre
        seen = set()
        deduped_chars = []
        for ch in normal_keys_input:
            if ch not in seen:
                seen.add(ch)
                deduped_chars.append(ch)
        deduped = "".join(deduped_chars)

        # Si des doublons ont été supprimés, met à jour l'Entry pour refléter la valeur nettoyée
        if deduped != normal_keys_input:
            self.entry_normal_keys.delete(0, tk.END)
            self.entry_normal_keys.insert(0, deduped)

        try:
            duration_value = float(duration_value.replace(" ", "").replace(",", "."))
        except ValueError:
            self._show_error("The time you entered is incorrect", 1)
            return False
        
        if len(str(duration_value).split(".", 1)[1])>3:
            self._show_error("You cannot enter more than 3\n numbers after the decimal point", 2)
            return False
        elif len(normal_keys_input) == 0 and len(self._selected_special_keys) == 0:
            self._show_error("You must enter at least one\n special key or one normal key", 2)
            return False
        elif duration_value <= 0:
            self._show_error("The time you entered must\n be greater than zero", 2)
            return False
        else:
            if duration_value > MAX_HOLD_DURATION:
                self._show_error("The time you have entered is too long", 1)
                return False
            else:
                self._hide_error()
                return normal_keys_input, list(self._selected_special_keys), duration_value


    def _show_error(self, message: str, height: int) -> None:
        """
        Affiche un message d'erreur.

        :param message: Le message à afficher.
        :param height: La hauteur du label d'erreur (en lignes).
        ---------------------------------------------------------
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
