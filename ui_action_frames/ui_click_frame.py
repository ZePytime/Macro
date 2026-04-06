from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Tuple, Union
from functools import partial

if TYPE_CHECKING:
    from main import WindowVariable




class ClickFrame:
    """
    Interface permettant de définir les paramètres d'un clic (position X,Y).
    -------------------------------------------------------------------------
    Widget that gathers X/Y coordinates for a mouse click.
    """

    def __init__(self, parent_frame: tk.Frame, w_var: WindowVariable) -> None:
        """
        Initialisation de l'interface de saisie des coordonnées.

        :param parent_frame: la frame où les widgets seront placés
        :param w_var: objet contenant les paramètres d'affichage (couleurs, tailles, screen_width/height)
        --------------------------------------------------------------------------------------------------
        Initialize the coordinate entry interface.

        :param parent_frame: parent frame in which widgets will be created
        :param w_var: dataclass-like object with style attributes (colors, fonts) and screen dimensions
        """

        self._parent = parent_frame

        # Limites de l'écran utilisées pour la validation et le widget "Scale"
        # ---------------------------------------------------------------------
        # Screen bounds used for validation and Scale widgets
        self._screen_width = w_var.screen_width
        self._screen_height = w_var.screen_height

        # Label informatif
        # -----------
        # Info label
        self._info_label = tk.Label(
            parent_frame,
            text="Enter the position at which\n you want the click to occur:",
            bg=w_var.color_1,
            fg=w_var.color_3,
            height=2,
            width=36,
            font=w_var.font_size,
        )
        self._info_label.grid(row=0, column=0)

        # Aperçu de la position actuelle de la souris
        # --------------------------------------------
        # Preview of the current mouse position
        self.mouse_position_label = tk.Label( 
            parent_frame,
            text="0 | 0",
            bg=w_var.color_1,
            fg=w_var.color_3,
            height=1,
            width=13,
            font=w_var.font_size,
        )
        self.mouse_position_label.grid(row=1, column=0)

        # Contrôles de X
        # -----------
        # X controls
        self._x_value_var = tk.StringVar(value="0")
        self._x_scale = tk.Scale(
            parent_frame,
            from_=0,
            to=self._screen_width,
            orient="horizontal",
            length=200,
            command=lambda v :self.set_coordinate(int(float(v)), "x"),
        )
        self._x_scale.grid(row=2, column=0)

        self._x_input = tk.Entry(
            parent_frame,
            textvariable=self._x_value_var,
            width=6,
            bg=w_var.color_2,
            font=w_var.font_size,
        )
        self._x_input.grid(row=3, column=0)

        # Contrôles de Y
        # -----------
        # Y controls
        self._y_value_var = tk.StringVar(value="0")
        self._y_scale = tk.Scale(
            parent_frame,
            from_=0,
            to=self._screen_height,
            orient="horizontal",
            length=200,
            command=lambda v: self.set_coordinate(int(float(v)), "y"),
        )
        self._y_scale.grid(row=4, column=0)

        self._y_input = tk.Entry(
            parent_frame,
            textvariable=self._y_value_var,
            width=6,
            bg=w_var.color_2,
            font=w_var.font_size,
        )
        self._y_input.grid(row=5, column=0)

        # Label d'erreur (caché jusqu'à utilisation)
        # ----------------------------------
        # Error label (hidden until needed)
        self._error_label = tk.Label(
            parent_frame,
            text="",
            bg=w_var.color_1,
            fg=w_var.color_3,
            height=1,
            width=40,
            font=w_var.font_size_error,
        )

    def check(self) -> Union[Tuple[int, int], bool]:
        """
        Vérifie que les valeurs saisies sont des entiers et sont dans les limites de l'écran.

        :return: un tuple (x, y) si ok, sinon False et affiche un message d'erreur.
        --------------------------------------------------------------------------------------
        Validate that entered coordinates are integers within screen bounds.
        
        :return: (x, y) on success, otherwise returns False and shows an inline error.
        """
        x_text = self._x_value_var.get().strip()
        y_text = self._y_value_var.get().strip()

        try:
            x = int(x_text.replace(" ", ""))
            y = int(y_text.replace(" ", ""))
        except ValueError:
            self._show_error("The position entered is incorrect", 1)
            return False

        if not (0 <= x <= self._screen_width and 0 <= y <= self._screen_height):
            self._show_error("The requested point is \noutside the main screen", 2)
            return False

        self._hide_error()
        return x, y

    def set_coordinate(self, value: int, axis: str = "xy") -> None:
        """
        Met à jour l'un des axes (x ou y ou les deux) à partir d'un Scale 
        ou d'une autre source.

        :param value: La valeur à renseigner dans le ou les champs de saisie.
        :param axis: La dimension à renseigner ("x", "y" ou "xy").
        ----------------------------------------------------------------------
        Update one coordinate (x or y or both) from a Scale callback 
        or other source.

        :param value: The value to set in the entry field(s).
        :param axis: The dimension to set ("x", "y", or "xy").
        """
        if axis == "x":
            self._x_value_var.set(str(value))
        elif axis == "y":
            self._y_value_var.set(str(value))
        elif axis == "xy":
            self._x_value_var.set(str(value[0]))
            self._y_value_var.set(str(value[1]))


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

