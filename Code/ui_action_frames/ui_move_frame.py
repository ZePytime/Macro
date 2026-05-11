
from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Tuple, Union
from functools import partial

from enums import MovementType
from ui_style import W_VAR
if TYPE_CHECKING:
    from main import WindowVariable


class MouseMoveFrame:
    """
    Cette classe permet de créer l'interface qui va nous permettre de
    définir les caractéristiques d'un mouvement de souris.
    ------------------------------------------------------------------
    This class allows the creation of an interface that will enable 
    us to define the characteristics of a mouse movement.
    """

    def __init__(self, parent_frame: tk.Frame) -> None:
        """
        Initialisation de l'interface de saisie des coordonnées.

        :param parent_frame: La frame où les widgets seront placés.
        --------------------------------------------------------------------
        Initialization of the coordinate input interface.

        :param parent_frame: Parent frame in which widgets will be created.
        """

        # Type de mouvement de la souris (déplacement relatif ou 
        # position absolue).
        # ----------------------------------------------------------
        # Mouse movement type (relative move or absolute position).
        self.move_type = MovementType.RELATIVE

        # Menu de sélection du type de mouvement.
        # ----------------------------------------
        # Movement type selection menu.
        frm_move_type = tk.Frame(parent_frame, bg=W_VAR.NEUTRAL_300)
        frm_move_type.grid(row=0, column=0)

        self._btn_relative = tk.Button(
            frm_move_type, 
            text="relative", 
            height=1, 
            width=7, 
            bg=W_VAR.BUTTON_1, 
            fg=W_VAR.TEXT_COLOR, 
            relief="flat",
            bd=0,
            font=W_VAR.little_font_size,
            cursor="hand2",
            command=partial(self.set_move_type, MovementType.RELATIVE)
            )
        self._btn_relative.grid(row=0, column=0, padx=(1, 0), pady=1)

        self._btn_absolute = tk.Button(
            frm_move_type, 
            text="absolute", 
            height=1, 
            width=7, 
            bg=W_VAR.NEUTRAL_700, 
            fg=W_VAR.TEXT_COLOR, 
            relief="flat",
            bd=0,
            font=W_VAR.little_font_size,
            cursor="hand2",
            command=partial(self.set_move_type, MovementType.ABSOLUTE)
            )
        self._btn_absolute.grid(row=0, column=1, padx=(0, 1), pady=1)

        # Label informatif.
        # ------------------
        # Info label.
        info_label = tk.Label(
            parent_frame, 
            text="Enter the number of pixels \nyou want to travel:", 
            bg=W_VAR.NEUTRAL_800, 
            fg=W_VAR.TEXT_COLOR, 
            height=2, 
            width=30, 
            font=W_VAR.font_size
            )
        info_label.grid(row=1, column=0)

        # Aperçu de la position actuelle de la souris.
        # ---------------------------------------------
        # Preview of the current mouse position.
        self.mouse_position_label = tk.Label(
            parent_frame, 
            text="0 | 0", 
            bg=W_VAR.NEUTRAL_800, 
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=13, 
            font=W_VAR.font_size
            )
        self.mouse_position_label.grid(row=2, column=0)

        # Contrôles pour X.
        # ------------------
        # X controls.
        frm_scale_x = tk.Frame(parent_frame, bg=W_VAR.NEUTRAL_800)
        frm_scale_x.grid(row=3, column=0)

        self._scale_x_relative = tk.Scale(
            frm_scale_x, 
            from_=W_VAR.screen_width*-1, 
            to=W_VAR.screen_width, 
            orient='horizontal', 
            length=150, 
            bg=W_VAR.NEUTRAL_800,
            fg=W_VAR.TEXT_COLOR,
            font=W_VAR.little_font_size,
            troughcolor=W_VAR.NEUTRAL_700,
            activebackground=W_VAR.BUTTON_1,
            highlightthickness=0,
            bd=0,
            command=lambda position :self.set_coordinate(position, "x"))
        self._scale_x_relative.grid(row=0, column=1)

        self._scale_x_absolute = tk.Scale(
            frm_scale_x, 
            from_=0, 
            to=W_VAR.screen_width, 
            orient='horizontal', 
            length=150, 
            bg=W_VAR.NEUTRAL_800,
            fg=W_VAR.TEXT_COLOR,
            font=W_VAR.little_font_size,
            troughcolor=W_VAR.NEUTRAL_700,
            activebackground=W_VAR.BUTTON_1,
            highlightthickness=0,
            bd=0,
            command=lambda position :self.set_coordinate(position, "x"))

        self._x_value_var = tk.StringVar(value="0")
        self._x_input = tk.Entry(
            frm_scale_x, 
            textvariable=self._x_value_var, 
            width=6, 
            bg=W_VAR.NEUTRAL_700,
            fg=W_VAR.TEXT_COLOR, 
            font=W_VAR.font_size,
            relief="flat",
            highlightthickness=1,
            highlightbackground=W_VAR.NEUTRAL_400,
            highlightcolor=W_VAR.BUTTON_1 
            )
        self._x_input.grid(row=0, column=0, padx=(0, 5), pady=(15, 0))

        # Contrôles pour Y.
        # ------------------
        # Y controls.
        frm_scale_y = tk.Frame(parent_frame, bg=W_VAR.NEUTRAL_800)
        frm_scale_y.grid(row=4, column=0, pady=(0, 10))

        self._scale_y_relative = tk.Scale(
            frm_scale_y, 
            from_=W_VAR.screen_height*-1, 
            to=W_VAR.screen_height, 
            orient='horizontal', 
            length=150, 
            bg=W_VAR.NEUTRAL_800,
            fg=W_VAR.TEXT_COLOR,
            font=W_VAR.little_font_size,
            troughcolor=W_VAR.NEUTRAL_700,
            activebackground=W_VAR.BUTTON_1,
            highlightthickness=0,
            bd=0,
            command=lambda position :self.set_coordinate(position, "y"))
        self._scale_y_relative.grid(row=0, column=1)

        self._scale_y_absolute = tk.Scale(
            frm_scale_y, 
            from_=0, 
            to=W_VAR.screen_height, 
            orient='horizontal', 
            length=150, 
            bg=W_VAR.NEUTRAL_800,
            fg=W_VAR.TEXT_COLOR,
            font=W_VAR.little_font_size,
            troughcolor=W_VAR.NEUTRAL_700,
            activebackground=W_VAR.BUTTON_1,
            highlightthickness=0,
            bd=0,
            command=lambda position :self.set_coordinate(position, "y"))

        self._y_var = tk.StringVar(value="0")
        self._y_input = tk.Entry(
            frm_scale_y, 
            textvariable=self._y_var, 
            width=6, 
            bg=W_VAR.NEUTRAL_700,
            fg=W_VAR.TEXT_COLOR, 
            font=W_VAR.font_size,
            relief="flat",
            highlightthickness=1,
            highlightbackground=W_VAR.NEUTRAL_400,
            highlightcolor=W_VAR.BUTTON_1 
            )
        self._y_input.grid(row=0, column=0, padx=(0, 5), pady=(15, 0))

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


    def check(self) -> Union[Tuple[int, int, MovementType], bool]:
        """
        Vérifie que les valeurs saisies sont des entiers 
        et sont dans les limites de l'écran.

        :return: Un tuple (x, y, move_type) si ok, 
            sinon False et affiche un message d'erreur.
        ---------------------------------------------------------------------
        Validate that entered coordinates are integers within screen bounds.
        
        :return: (x, y, move_type) on success, 
            otherwise returns False and shows an inline error.
        """

        # On récupère la position entrée par l'utilisateur.
        # --------------------------------------------------
        # We retrieve the position entered by the user.
        x_text = self._x_value_var.get().strip()
        y_text = self._y_var.get().strip()

        try:
            x = int(x_text.replace(" ", ""))
            y = int(y_text.replace(" ", ""))
        except ValueError:
            self._show_error("The position entered is incorrect", 1)
            return False

        if self.move_type is MovementType.RELATIVE:
            if not (W_VAR.screen_width*-1 <= x <= W_VAR.screen_width and W_VAR.screen_height*-1 <= y <= W_VAR.screen_height):
                self._show_error("The requested point is \noutside the main screen", 2)
                return False
        elif not (0 <= x <= W_VAR.screen_width and 0 <= y <= W_VAR.screen_height):
            self._show_error("The requested point is \noutside the main screen", 2)
            return False

        self._hide_error()
        return x, y, self.move_type



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
            self._y_var.set(str(value))
        elif axis == "xy":
            self._x_value_var.set(str(value[0]))
            self._y_var.set(str(value[1]))


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
        self._error_label.grid(row=7, column=0)


    def _hide_error(self) -> None:
        """
        Cache le label d'erreur.
        -------------------------
        Hide the error label.
        """

        self._error_label.grid_remove()


    def set_move_type(self, move_type: MovementType) -> None:
        """
        Change le type de mouvement de la souris (relatif ou absolu)
        et met à jour l'interface en conséquence.

        :param move_type: Le type de mouvement à définir 
            (MovementType.RELATIVE ou MovementType.ABSOLUTE).
        -------------------------------------------------------------
        Change the mouse movement type (relative or absolute) 
        and update the interface accordingly.

        :param move_type: The movement type to set 
            (MovementType.RELATIVE or MovementType.ABSOLUTE).
        """

        if move_type is MovementType.RELATIVE:
            self.move_type = MovementType.RELATIVE
            self._btn_relative.config(bg=W_VAR.BUTTON_1)
            self._btn_absolute.config(bg=W_VAR.NEUTRAL_700)
            self._scale_x_relative.grid(row=0, column=1)
            self._scale_y_relative.grid(row=0, column=1)
            self._scale_x_absolute.grid_remove()
            self._scale_y_absolute.grid_remove()

        else:
            self.move_type = MovementType.ABSOLUTE
            self._btn_relative.config(bg=W_VAR.NEUTRAL_700)
            self._btn_absolute.config(bg=W_VAR.BUTTON_1)
            self._scale_x_relative.grid_remove()
            self._scale_y_relative.grid_remove()
            self._scale_x_absolute.grid(row=0, column=1)
            self._scale_y_absolute.grid(row=0, column=1)