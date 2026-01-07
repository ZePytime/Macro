from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Tuple, Union
from functools import partial

if TYPE_CHECKING:
    from main import WindowVariable


MIN_WAIT_DURATION = 0.001  # 1 ms minimum (au moins une vraie attente)
MAX_WAIT_DURATION = 604800  # 7 days in seconds
MAX_DECIMAL_PLACES = 3


class WaitFrame:
    """
    Cette classe permet de créer l'interface qui va nous permettre de 
    créer des temps d'attente.
    ------------------------------------------------------------------
    This class creates the interface that will allow us to
    create wait times.
    """

    def __init__(self, parent_frame: tk.Frame, w_var: WindowVariable) -> None:
        """
        Initialisation de l'interface de création d'un temps d'attente

        :param parent_frame: la frame où les widgets seront placés
        :param w_var: objet contenant les paramètres d'affichage 
            (couleurs, tailles, screen_width/height...)
        --------------------------------------------------------------
        Initialization of the wait time creation interface

        :param parent_frame: the frame where the widgets will be placed
        :param w_var: object containing display parameters 
            (colors, sizes, screen_width/height...)
        """

        # Label informatif
        # -----------------
        # Info label
        info_label = tk.Label(
            parent_frame, 
            text='Enter the time during\nwhich you want to wait:', 
            bg=w_var.color_1, 
            fg=w_var.color_3, 
            height=2, 
            width=30, 
            font=w_var.font_size
            )
        info_label.grid(row=0, column=0)

        # Entry pour le temps à attendre
        # -------------------------------
        # Entry for the wait time
        self.entry_wait_duration = tk.Entry(
            parent_frame, 
            width=8, 
            bg=w_var.color_2, 
            font=w_var.font_size
            )
        self.entry_wait_duration.grid(row=1, column=0)

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


    def check(self) -> Union[float, bool]:
        """
        Vérifie que le temps entré est correct.
        Vérifie que c'est un nombre positif, avec au maximum 3 chiffres après la virgule,
        et qu'il n'est pas trop grand (max 1 semaine = 604800 secondes).

        :return: Le temps en secondes si correct, False sinon.
        --------------------------------------------------------
        Verifies that the entered time is correct.
        Checks that it is a positive number, with a maximum of 3 digits after the decimal point,
        and that it is not too large (max 1 week).

        :return: The time in seconds if correct, False otherwise.
        """

        duration_text = self.entry_wait_duration.get().strip()

        # Convertir en float
        # -------------------
        # Convert to float
        try:
            duration_value = float(duration_text.replace(" ", "").replace(",", "."))
        except ValueError:
            self._show_error("The time you entered is incorrect", 1)
            return False

        # Vérifier que c'est positif
        # ---------------------------
        # Check that it's positive
        if duration_value <= MIN_WAIT_DURATION:
            self._show_error("The time must be greater than 0", 1)
            return False

        # Vérifier le nombre de décimales
        # -----------------------------------
        # Check the number of decimal places
        decimal_places = len(str(duration_value).split(".", 1)[1]) if "." in str(duration_value) else 0
        if decimal_places > MAX_DECIMAL_PLACES:
            self._show_error(f"You cannot enter more than {MAX_DECIMAL_PLACES}\ndecimal places", 2)
            return False

        # Vérifier la durée maximale
        # ---------------------------
        # Check the maximum duration
        if duration_value > MAX_WAIT_DURATION:
            self._show_error(f"The time you entered is too long\n(max {MAX_WAIT_DURATION // 86400} days)", 2)
            return False

        self._hide_error()
        return duration_value



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