
from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Tuple, Union
from functools import partial

from enums import MovementType

if TYPE_CHECKING:
    from main import WindowVariable


class MouseMoveFrame:
    """
    Cette classe permet de créer l'interface qui va nous permettre de
    définir les caractéristiques d'un mouvement de souris
    --------------------------------------------------------------------------
    This class allows the creation of an interface that will enable us to 
    define the characteristics of a mouse movement.
    """

    def __init__(self, parent_frame: tk.Frame, w_var: WindowVariable) -> None:
        """
        Initialisation de l'interface de saisie des coordonnées.

        :param parent_frame: la frame où les widgets seront placés
        :param w_var: objet contenant les paramètres d'affichage (couleurs, tailles, screen_width/height)
        ------------------------------------------------------------------------------------
        Initialization of the coordinate input interface.

        :param parent_frame: parent frame in which widgets will be created
        :param w_var: dataclass-like object with style attributes (colors, fonts) and screen dimensions
        """

        self._w_var = w_var

        # Limites de l'écran utilisées pour la validation et pour les widgets Scale
        # ---------------------------------------------------------------------
        # Screen bounds used for validation and Scale widgets
        self._screen_width = w_var.screen_width
        self._screen_height = w_var.screen_height

        # Type de mouvement de la souris (déplacement relatif ou position absolue)
        # -------------------------------------------------------------------------
        # Mouse movement type (relative move or absolute position)
        self.movement_type = MovementType.RELATIVE

        # Menu de sélection du type de mouvement
        # ---------------------------------------
        # Movement type selection menu
        frm_movement_type = tk.Frame(parent_frame, bg=w_var.color_1)
        frm_movement_type.grid(row=0, column=0)

        self._btn_relative = tk.Button(
            frm_movement_type, 
            text="relative", 
            bg=w_var.color_4, 
            fg="black", 
            height=1, 
            width=6, 
            command=partial(self.set_movement_type, MovementType.RELATIVE)
            )
        self._btn_relative.grid(row=0, column=0)

        self._btn_absolute = tk.Button(
            frm_movement_type, 
            text="absolute", 
            bg=w_var.color_2, 
            fg="black", 
            height=1, 
            width=6, 
            command=partial(self.set_movement_type, MovementType.ABSOLUTE)
            )
        self._btn_absolute.grid(row=0, column=1)

        # Label informatif
        # -----------
        # Info label
        info_label = tk.Label(
            parent_frame, 
            text="Enter the number of pixels \nyou want to travel:", 
            bg=w_var.color_1, 
            fg="black", 
            height=2, 
            width=30, 
            font=w_var.font_size
            )
        info_label.grid(row=1, column=0)

        # Aperçu de la position actuelle de la souris
        # --------------------------------------------
        # Preview of the current mouse position
        self.mouse_position_label = tk.Label(
            parent_frame, 
            text="0 | 0", 
            bg=w_var.color_1, 
            fg="black", 
            height=1, 
            width=13, 
            font=w_var.font_size
            )
        self.mouse_position_label.grid(row=2, column=0)

        # Contrôles pour X
        # -----------
        # X controls
        self._scale_x_relative = tk.Scale(
            parent_frame, 
            from_=self._screen_width*-1, 
            to=self._screen_width, 
            orient='horizontal', 
            length=200, 
            command=lambda position :self.set_coordinate(position, "x"))
        self._scale_x_relative.grid(row=3, column=0)

        self._scale_x_absolute = tk.Scale(
            parent_frame, 
            from_=0, 
            to=self._screen_width, 
            orient='horizontal', 
            length=200, 
            command=lambda position :self.set_coordinate(position, "x"))

        self._x_value_var = tk.StringVar(value="0")
        self._x_input = tk.Entry(
            parent_frame, 
            textvariable=self._x_value_var, 
            width=6, 
            bg=w_var.color_2, 
            font=w_var.font_size
            )
        self._x_input.grid(row=4, column=0)

        # Contrôles pour Y
        # -----------
        # Y controls
        self._scale_y_relative = tk.Scale(
            parent_frame, 
            from_=self._screen_height*-1, 
            to=self._screen_height, 
            orient='horizontal', 
            length=200, 
            command=lambda position :self.set_coordinate(position, "y"))
        self._scale_y_relative.grid(row=5, column=0)

        self._scale_y_absolute = tk.Scale(
            parent_frame, 
            from_=0, 
            to=self._screen_height, 
            orient='horizontal', 
            length=200, 
            command=lambda position :self.set_coordinate(position, "y"))

        self._y_var = tk.StringVar(value="0")
        self._y_input = tk.Entry(
            parent_frame, 
            textvariable=self._y_var, 
            width=6, 
            bg=w_var.color_2, 
            font=w_var.font_size
            )
        self._y_input.grid(row=6, column=0)

        # Label d'erreur (caché jusqu'à son utilisation)
        # ----------------------------------
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


    def check(self) -> Union[Tuple[int, int, MovementType], bool]:
        """
        Vérifie que les valeurs saisies sont des entiers et sont dans les limites de l'écran.

        :return: un tuple (x, y, movement_type) si ok, sinon False et affiche un message d'erreur.
        --------------------------------------------------------------------------------------
        Validate that entered coordinates are integers within screen bounds.
        
        :return: (x, y, movement_type) on success, otherwise returns False and shows an inline error.
        """

        # On récupère la position entrée par l'utilisateur.
        # -------------------------------------------------
        # We retrieve the position entered by the user.
        x_text = self._x_value_var.get().strip()
        y_text = self._y_var.get().strip()

        try:
            x = int(x_text.replace(" ", ""))
            y = int(y_text.replace(" ", ""))
        except ValueError:
            self._show_error("The position entered is incorrect", 1)
            return False

        if self.movement_type is MovementType.RELATIVE:
            if not (self._screen_width*-1 <= x <= self._screen_width and self._screen_height*-1 <= y <= self._screen_height):
                self._show_error("The requested point is \noutside the main screen", 2)
                return False
        elif not (0 <= x <= self._screen_width and 0 <= y <= self._screen_height):
            self._show_error("The requested point is \noutside the main screen", 2)
            return False

        self._hide_error()
        return x, y, self.movement_type



    def set_coordinate(self, value: int, axis: str = "xy") -> None:
        """
        Met à jour l'un des axes (x ou y ou les deux) à partir d'un Scale ou d'une autre source.

        :param value: La valeur à renseigner dans le ou les champs de saisie.
        :param axis: La dimension à renseigner ("x", "y" ou "xy").
        -----------------------------------------------------------------------------
        Update one coordinate (x or y or both) from a Scale callback or other source.

        :param value: The value to set in the entry field(s).
        :param axis: The dimension to set ("x", "y", or "xy").
        """

        if axis == "x":
            self._x_value_var.set(str(value))
        elif axis == "y":
            self._y_var.set(str(value))
        elif axis == "xy":
            self._x_value_var.set(str(value[0]))
            self._y_var.set(str(value[1]))


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
        self._error_label.grid(row=7, column=0)


    def _hide_error(self) -> None:
        """
        Cache le label d'erreur.
        -------------------------
        Hide the error label.
        """

        self._error_label.grid_remove()


    def set_movement_type(self, movement_type: MovementType) -> None:
        """
        Change le type de mouvement de la souris (relatif ou absolu)
        et met à jour l'interface en conséquence.

        :param movement_type: Le type de mouvement à définir 
            (MovementType.RELATIVE ou MovementType.ABSOLUTE).
        -------------------------------------------------------------
        Change the mouse movement type (relative or absolute) 
        and update the interface accordingly.

        :param movement_type: The movement type to set 
            (MovementType.RELATIVE or MovementType.ABSOLUTE).
        """

        if movement_type is MovementType.RELATIVE:
            self.movement_type = MovementType.RELATIVE
            self._btn_relative.config(bg=self._w_var.color_4)
            self._btn_absolute.config(bg=self._w_var.color_2)
            self._scale_x_relative.grid(row=3, column=0)
            self._scale_y_relative.grid(row=5, column=0)
            self._scale_x_absolute.grid_remove()
            self._scale_y_absolute.grid_remove()

        else:
            self.movement_type = MovementType.ABSOLUTE
            self._btn_relative.config(bg=self._w_var.color_2)
            self._btn_absolute.config(bg=self._w_var.color_4)
            self._scale_x_relative.grid_remove()
            self._scale_y_relative.grid_remove()
            self._scale_x_absolute.grid(row=3, column=0)
            self._scale_y_absolute.grid(row=5, column=0)