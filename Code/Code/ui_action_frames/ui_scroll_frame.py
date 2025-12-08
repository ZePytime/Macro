from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Tuple, Union
from functools import partial


if TYPE_CHECKING:
    from main import WindowVariable


from ui_action_frames.enums import Direction



# liste des boutons de direction
# -------------------------------
# list of direction buttons
DIRECTION_ORDER = (Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN)

MAX_SCROLL_STEPS = 10000

class ScrollFrame:
    """
    Interface permettant de définir les paramètres pour une action de scroll.
    --------------------------------------------------------------------------
    Interface allowing to define the parameters for a scroll action.
    """

    def __init__(self, parent_frame: tk.Frame, w_var: WindowVariable) -> None:
        """
        Initialisation de l'interface de création d'action de scroll.
        
        :param parent_frame: la frame où les widgets seront placés
        :param w_var: objet contenant les paramètres d'affichage 
            (couleurs, tailles, screen_width/height...)
        ----------------------------------------------------------------
        Initialization of the scroll action creation interface.

        :param parent_frame: the frame where the widgets will be placed
        :param w_var: object containing display parameters 
            (colors, sizes, screen_width/height...)
        """

        self._w_var = w_var

        # Direction de scroll sélectionnée
        # ---------------------------------
        # Selected scroll direction
        self._scroll_direction = Direction.UP

        # Label informatif
        # -----------------
        # Info label
        info_label_direction = tk.Label(
            parent_frame, 
            text='Enter the direction in\nwhich you wish to scroll:', 
            bg=w_var.color_1, 
            fg="black", 
            height=2, 
            width=30, 
            font=w_var.font_size
            )
        info_label_direction.grid(row=0, column=0)

        # Dictionnaire des boutons de direction
        # --------------------------------------
        # Dictionary of direction buttons
        self._direction_buttons = {}
        
        # Frame contenant les boutons de direction
        # -----------------------------------------
        # Frame containing the direction buttons
        btn_frame = tk.Frame(parent_frame, bg=w_var.color_1)
        btn_frame.grid(row=1, column=0)

        # Création des boutons de direction
        # ----------------------------------
        # Creation of direction buttons
        for column, btn in enumerate(DIRECTION_ORDER):
            dir_btn = tk.Button(
                btn_frame, 
                text=btn.value, 
                bg=w_var.color_2, 
                fg="black", 
                height=1, 
                width=len(btn.value), 
                command=partial(self.select_direction, btn)
                )
            dir_btn.grid(row=0, column=column)
            self._direction_buttons[btn] = dir_btn
        self._direction_buttons[self._scroll_direction].config(bg=w_var.color_4)

        # Label informatif
        # -----------------
        # Info label
        info_label_steps = tk.Label(
            parent_frame, 
            text='Enter the number of steps\nyou want to scroll through:', 
            bg=w_var.color_1, 
            fg="black", 
            height=2, 
            width=30, 
            font=w_var.font_size
            )
        info_label_steps.grid(row=2, column=0)

        # Zone de texte pour entrer le nombre de pas
        # -------------------------------------------
        # Text zone to enter the number of steps
        self.entry_steps = tk.Entry(
            parent_frame, 
            width=6, 
            bg=w_var.color_2, 
            font=w_var.font_size
            )
        self.entry_steps.grid(row=3, column=0)

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


    def select_direction(self, name: str) -> None:
        """
        Change la direction de scroll sélectionnée.
        
        :param name: le nom de la nouvelle direction
        ---------------------------------------------
        Change the selected scroll direction.

        :param name: the name of the new direction
        """
        
        self._direction_buttons[self._scroll_direction].config(bg=self._w_var.color_2)
        self._scroll_direction = name
        self._direction_buttons[name].config(bg=self._w_var.color_4)


    def check(self) -> Union[Tuple[int, Direction], bool]:
        """
        Vérifie le nombre de pas entrés par l'utilisateur.
        
        :return: le nombre de pas et la direction si tout est correct, 
            False sinon
        ---------------------------------------------------------------
        Verifies the number of steps entered by the user.

        :return: the number of steps and the direction if everything 
            is correct, False otherwise
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
