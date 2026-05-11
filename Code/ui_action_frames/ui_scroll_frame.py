from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Tuple, Union
from functools import partial

from enums import Direction
from ui_style import W_VAR
if TYPE_CHECKING:
    from main import WindowVariable





# Liste des boutons de direction.
# --------------------------------
# List of direction buttons.
DIRECTION_ORDER = (Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN)

MAX_SCROLL_STEPS = 10000

class ScrollFrame:
    """
    Interface permettant de définir les paramètres pour une action de scroll.
    --------------------------------------------------------------------------
    Interface allowing to define the parameters for a scroll action.
    """

    def __init__(self, parent_frame: tk.Frame) -> None:
        """
        Initialisation de l'interface de création d'action de scroll.
        
        :param parent_frame: La frame où les widgets seront placés.
        -----------------------------------------------------------------
        Initialization of the scroll action creation interface.

        :param parent_frame: The frame where the widgets will be placed.
        """

        # Direction de scroll sélectionnée.
        # ----------------------------------
        # Selected scroll direction.
        self._scroll_direction = Direction.UP

        # Label informatif.
        # ------------------
        # Info label.
        info_label_direction = tk.Label(
            parent_frame, 
            text='Enter the direction in\nwhich you wish to scroll:', 
            bg=W_VAR.NEUTRAL_800, 
            fg=W_VAR.TEXT_COLOR, 
            height=2, 
            width=30, 
            font=W_VAR.font_size
            )
        info_label_direction.grid(row=0, column=0)

        # Dictionnaire des boutons de direction.
        # ---------------------------------------
        # Dictionary of direction buttons.
        self._direction_buttons = {}
        
        # Frame contenant les boutons de direction.
        # ------------------------------------------
        # Frame containing the direction buttons.
        btn_frame = tk.Frame(parent_frame, bg=W_VAR.NEUTRAL_300, padx=1, pady=1)
        btn_frame.grid(row=1, column=0)

        # Création des boutons de direction.
        # -----------------------------------
        # Creation of direction buttons.
        for column, btn in enumerate(DIRECTION_ORDER):
            dir_btn = tk.Button(
                btn_frame, 
                text=btn.value, 
                height=1, 
                width=len(btn.value), 
                bg=W_VAR.NEUTRAL_700, 
                fg=W_VAR.TEXT_COLOR, 
                relief="flat",
                bd=0,
                font=W_VAR.little_font_size,
                cursor="hand2",
                command=partial(self.select_direction, btn)
                )
            dir_btn.grid(row=0, column=column, padx=(0, 1))
            self._direction_buttons[btn] = dir_btn
        self._direction_buttons[self._scroll_direction].config(bg=W_VAR.BUTTON_1)

        # Label informatif.
        # ------------------
        # Info label.
        info_label_steps = tk.Label(
            parent_frame, 
            text='Enter the number of steps\nyou want to scroll through:', 
            bg=W_VAR.NEUTRAL_800, 
            fg=W_VAR.TEXT_COLOR, 
            height=2, 
            width=30, 
            font=W_VAR.font_size
            )
        info_label_steps.grid(row=2, column=0)

        # Zone de texte pour entrer le nombre de pas.
        # --------------------------------------------
        # Text zone to enter the number of steps.
        self.entry_steps = tk.Entry(
            parent_frame, 
            width=7, 
            bg=W_VAR.NEUTRAL_700,
            fg=W_VAR.TEXT_COLOR, 
            font=W_VAR.font_size,
            relief="flat",
            highlightthickness=1,
            highlightbackground=W_VAR.NEUTRAL_400,
            highlightcolor=W_VAR.BUTTON_1 
            )
        self.entry_steps.grid(row=3, column=0, pady=(0, 5))

        # Label d'erreur (caché jusqu'à utilisation).
        # --------------------------------------------
        # Error label (hidden until needed).
        self._error_label = tk.Label(
            parent_frame, 
            text="", 
            bg=W_VAR.NEUTRAL_800, 
            fg=W_VAR.ERROR_COLOR, 
            height=1, 
            width=40, 
            font=W_VAR.font_size_error
            )


    def select_direction(self, name: str) -> None:
        """
        Change la direction de scroll sélectionnée.
        
        :param name: Le nom de la nouvelle direction.
        ----------------------------------------------
        Change the selected scroll direction.

        :param name: The name of the new direction.
        """
        
        self._direction_buttons[self._scroll_direction].config(bg=W_VAR.NEUTRAL_700)
        self._scroll_direction = name
        self._direction_buttons[name].config(bg=W_VAR.BUTTON_1)


    def check(self) -> Union[Tuple[int, Direction], bool]:
        """
        Vérifie le nombre de pas entrés par l'utilisateur.
        
        :return: Le nombre de pas et la direction si tout est correct, 
            False sinon.
        ---------------------------------------------------------------
        Verifies the number of steps entered by the user.

        :return: The number of steps and the direction if everything 
            is correct, False otherwise.
        """

        steps = self.entry_steps.get()
        try:
            steps = int(steps.replace(" ", ""))
        except ValueError:
            self._show_error("The number you entered is incorrect", 1)
            return False
        
        if steps > MAX_SCROLL_STEPS:
            self._show_error(f"You can't set more than {MAX_SCROLL_STEPS} steps", 1)
            return False
        if steps <= 0:
            self._show_error("You cannot set 0", 1)
            return False
        self._hide_error()
        return steps, self._scroll_direction


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
        self._error_label.grid(row=5, column=0)


    def _hide_error(self) -> None:
        """
        Cache le label d'erreur.
        -------------------------
        Hide the error label.
        """

        self._error_label.grid_remove()
