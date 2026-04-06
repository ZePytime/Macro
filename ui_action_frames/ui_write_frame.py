from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Tuple, Union
from functools import partial

if TYPE_CHECKING:
    from main import WindowVariable
    from container_manager import ContainerManager


MAX_WRITE_LENGTH = 10000000

class WriteFrame:
    """
    Cette classe permet de créer l'interface qui va nous permettre de 
    créer du texte à écrire automatiquement.
    ------------------------------------------------------------------
    This class creates the interface that will allow us to
    create text to be written automatically.
    """

    def __init__(self, parent_frame: tk.Frame, w_var: WindowVariable):
        """
        Initialisation de l'interface de création du texte à écrire
        automatiquement.
        
        :param parent_frame: la frame où les widgets seront placés
        :param w_var: objet contenant les paramètres d'affichage 
            (couleurs, tailles, screen_width/height...)
        ------------------------------------------------------------
        Initialization of the interface for creating text to
        be written automatically.

        :param parent_frame: the frame where the widgets will be placed
        :param w_var: object containing display parameters 
            (colors, sizes, screen_width/height...)
        """

        # Label informatif
        # -----------------
        # Info label
        info_label = tk.Label(
            parent_frame, 
            text='Enter the text to\nbe written automatically:', 
            bg=w_var.color_1, 
            fg="black", 
            height=3, 
            width=30, 
            font=w_var.font_size
            )
        info_label.grid(row=0, column=0)

        # Zone de texte
        # --------------
        # Text zone
        self.text_area = tk.Text(
            parent_frame, 
            height=6, 
            width=26, 
            bg=w_var.color_2, 
            font=w_var.font_size
            )
        self.text_area.grid(row=1, column=0)

        # Label d'erreur (caché jusqu'à son utilisation)
        # -----------------------------------------------
        # Error label (hidden until needed)
        self._error_label = tk.Label(
            parent_frame, 
            text="", 
            bg=w_var.color_1, 
            fg=w_var.color_3, 
            height=1, 
            width=40, 
            font=w_var.font_size_error
            )


    def check(self) -> Union[bool, list[str]]:
        """
        Vérifie que le texte entré est valide.
        Il ne doit pas être vide et ne doit pas dépasser MAX_WRITE_LENGTH.

        :return: False si le texte est invalide, sinon une liste contenant le texte.
        -----------------------------------------------------------------------------
        Check that the entered text is valid.
        It must not be empty and must not exceed MAX_WRITE_LENGTH.

        :return: False if the text is invalid, otherwise a list containing the text.
        """

        content = self.text_area.get("1.0", "end-1c")

        if len(content) == 0:
            self._show_error("You must enter some text", 1)
            return False

        if len(content) > MAX_WRITE_LENGTH:
            self._show_error(f"You can't enter more\nthan {MAX_WRITE_LENGTH} characters", 2)
            return False
        self._hide_error()
        return [content]


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
        self._error_label.grid(row=2, column=0)


    def _hide_error(self) -> None:
        """
        Cache le label d'erreur.
        -------------------------
        Hide the error label.
        """
        self._error_label.grid_remove()