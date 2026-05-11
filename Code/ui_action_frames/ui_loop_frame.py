from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Tuple, Union
from functools import partial
from ui_style import W_VAR
if TYPE_CHECKING:
    from main import WindowVariable
    from container_manager import ContainerManager


MAX_LOOP_TURNS = 604800000
MAX_LOOP_NAME_LENGTH = 20
MIN_LOOP_TURNS = 2

class LoopFrame:
    """
    Cette classe permet de créer l'interface qui va nous permettre de 
    créer des boucles.
    ------------------------------------------------------------------
    This class creates the interface that will allow us to
    create loops.
    """

    def __init__(self, parent_frame: tk.Frame, container_manager: ContainerManager) -> None:
        """
        Initialisation de l'interface de création de boucles.

        :param parent_frame: La frame où les widgets seront placés.
        :param container_manager: Classe permettant de gérer les conteneurs 
            comme loop and parallel_action.
        --------------------------------------------------------------------
        Initialization of the loop creation interface.

        :param parent_frame: Parent frame in which widgets will be created.
        :param container_manager: Class managing containers such as 
            loop and parallel_action.
        """

        # Classe permettant de gérer les conteneurs comme loop 
        # et parallel_action, elle nous sera utile pour vérifier les noms 
        # de loop déjà utilisés et lui donner les nouveaux noms.
        # ----------------------------------------------------------------
        # Class managing containers such as loop and parallel_action,
        # it will be useful for checking already used loop names
        # and giving them the new names.
        self._container_manager  = container_manager 

        # Label informatif.
        # ------------------
        # Info label.
        info_label_name = tk.Label(
            parent_frame, 
            text='Enter loop name:', 
            bg=W_VAR.NEUTRAL_800, 
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=30, 
            font=W_VAR.font_size
            )
        info_label_name.grid(row=0, column=0)

        # Entry pour le nom de la boucle.
        # --------------------------------
        # Entry for loop name.
        self.entry_loop_name = tk.Entry(
            parent_frame, 
            width=16, 
            bg=W_VAR.NEUTRAL_700,
            fg=W_VAR.TEXT_COLOR, 
            font=W_VAR.font_size,
            relief="flat",
            highlightthickness=1,
            highlightbackground=W_VAR.NEUTRAL_400,
            highlightcolor=W_VAR.BUTTON_1 
            )
        self.entry_loop_name.grid(row=1, column=0, pady=3)

        # Label informatif.
        # ------------------
        # Info label.
        info_label_turns = tk.Label(
            parent_frame, 
            text='Enter the number of turns\nthe loop will make:', 
            bg=W_VAR.NEUTRAL_800, 
            fg=W_VAR.TEXT_COLOR, 
            height=2, 
            width=30, 
            font=W_VAR.font_size
            )
        info_label_turns.grid(row=2, column=0)

        # Entry pour le nombre de tours que fera la boucle.
        # --------------------------------------------------
        # Entry for the number of turns the loop will make.
        self.entry_nb_turns  = tk.Entry(
            parent_frame, 
            width=8, 
            bg=W_VAR.NEUTRAL_700,
            fg=W_VAR.TEXT_COLOR, 
            font=W_VAR.font_size,
            relief="flat",
            highlightthickness=1,
            highlightbackground=W_VAR.NEUTRAL_400,
            highlightcolor=W_VAR.BUTTON_1 
            )
        self.entry_nb_turns .grid(row=3, column=0, pady=3)


        # Label d'erreur (caché jusqu'à son utilisation).
        # ------------------------------------------------
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


    def check(self) -> Union[Tuple[int, str], bool]:
        """
        Vérifie que le nom de la boucle et le nombre de tours sont corrects.
        Vérifie que le nombre de tours est un entier >= MIN_LOOP_TURNS
        et <= MAX_LOOP_TURNS, que le nom de la boucle n'est pas vide, 
        ne dépasse pas MAX_LOOP_NAME_LENGTH caractères et n'est pas 
        déjà utilisé.

        :return: Un tuple (turns, name) si les entrées sont valides, 
            sinon False.
        ---------------------------------------------------------------------
        Check that the loop name and number of turns are correct.
        Verifies that the number of turns is an integer >= MIN_LOOP_TURNS 
        and <= MAX_LOOP_TURNS, that the loop name is not empty, 
        does not exceed MAX_LOOP_NAME_LENGTH characters, and is not 
        already used.

        :return: A tuple (turns, name) if the inputs are valid, 
            otherwise False.
        """
        turns_text = self.entry_nb_turns.get().strip()
        loop_name = self.entry_loop_name.get().strip()

        # Validation du nom.
        # ------------------------
        # Validation of the name.
        if len(loop_name) == 0:
            self._show_error("You haven't chosen a name for the loop", 1)
            return False

        if len(loop_name) > MAX_LOOP_NAME_LENGTH:
            self._show_error(f"You cannot choose a name\nlonger than {MAX_LOOP_NAME_LENGTH} characters", 2)
            return False

        if loop_name in self._container_manager.loop_names:
            self._show_error("This name is already in use", 1)
            return False

        # Validation du nombre de tours.
        # -----------------------------------
        # Validation of the number of turns.
        try:
            num_turns = int(turns_text.replace(" ", ""))
        except ValueError:
            self._show_error("The number of turns entered is incorrect", 1)
            return False

        if num_turns < MIN_LOOP_TURNS:
            self._show_error(f"The number of turns must be at least {MIN_LOOP_TURNS}", 1)
            return False

        if num_turns > MAX_LOOP_TURNS:
            self._show_error(f"You cannot make more\nthan {MAX_LOOP_TURNS} turns", 2)
            return False

        # Tout est valide.
        # ---------------------
        # Everything is valid.
        self._hide_error()
        self._container_manager.loop_names.append(loop_name)
        return num_turns, loop_name

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
        self._error_label.grid(row=4, column=0)


    def _hide_error(self) -> None:
        """
        Cache le label d'erreur.
        -------------------------
        Hide the error label.
        """
        self._error_label.grid_remove()