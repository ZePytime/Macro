from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Callable
from functools import partial
import webbrowser
from hover_button import HoverButton

from action_classes import KeyLoggerApp, KeyPosition
from hotkey_manager import save_shortcuts
from enums import ShortCut

from ui_style import W_VAR

if TYPE_CHECKING:
    from main import WindowVariable


DOCUMENTATION_URL = "https://github.com/ZePytime/Macro"

class DocumentationUI:
    """
    Cette classe permet de changer les raccourcis de l'utilisateur 
    et de donner des indications pour utiliser le logiciel.
    ---------------------------------------------------------------
    This class allows the user to change keyboard shortcuts
    and provides instructions on how to use the application.
    """
    def __init__(self, window: tk.Tk, main_frm: tk.Frame, menu_btn_frame: tk.Frame, switch_frame: Callable[[tk.Frame], None]) -> None:
        """
        Initialisation de tous les widgets permettant la modification des raccourcis
        clavier et/ou des widgets donnant des indications pour utiliser la macro.

        :param window: Fenêtre principale de l'interface.
        :param main_frm: Cadre principal dans lequel se trouve ce menu.
        :param menu_btn_frame: Menu dans lequel on ajoute le bouton
            permettant de basculer vers cette interface
        :param switch_frame: Fonction permettant de changer de frame
            afin d'afficher cette interface
        -----------------------------------------------------------------------------
        Initializes all widgets that allow keyboard shortcut customization
        and/or provide instructions for using the macro.

        :param window: Main interface window.
        :param main_frm: Main frame in which this menu is located.
        :param menu_btn_frame: Menu in which the button used to switch to 
            this interface is added
        :param switch_frame: Function used to switch frames in order to 
            display this interface
        """

        self.window = window

        # Création du menu
        # -----------------
        # Menu creation

        # Bouton permettant d'accéder au menu DocumentationUI.
        # -----------------------------------------------------
        # Button used to access the DocumentationUI menu.
        self.doc_btn = HoverButton(menu_btn_frame, 
            text="doc", 
            color=W_VAR.BUTTON_4,
            hover=W_VAR.BUTTON_4_HOVER,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=4, 
            font=W_VAR.font_size, 
            command=lambda : switch_frame(self.doc_frame)
            )
        self.doc_btn.grid(row=0, column=3, padx=2, pady=2)

        # Frame principale du menu
        # -------------------------
        # Main menu frame
        self.doc_frame = tk.Frame(main_frm, bg=W_VAR.NEUTRAL_800, width=340, height=460)
        self.doc_frame.columnconfigure(0, weight=1)
        self.doc_frame.grid_propagate(False)

        # Label informatif
        # -----------------
        # Info label
        stop_keys_label = tk.Label(
            self.doc_frame, 
            text="Edit stop keys :", 
            bg=W_VAR.NEUTRAL_800, 
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=20, 
            font=W_VAR.font_size
            )
        stop_keys_label.grid(row=0, column=0, pady=(30,0))

        # Frame pour organiser les Entry des touches d'arrêt
        # ---------------------------------------------------
        # Frame to organize the stop key Entry widgets
        stop_entry_frm = tk.Frame(self.doc_frame, bg=W_VAR.NEUTRAL_800)
        stop_entry_frm.grid(row=1, column=0, pady=10)

        # Entry pour la première touche du raccourci
        # -------------------------------------------
        # Entry for the first shortcut key
        pre_filling_stop_key_1 = tk.StringVar(value=KeyLoggerApp.stop_keys[0])
        self.stop_key_1 = tk.Entry(
            stop_entry_frm, 
            textvariable=pre_filling_stop_key_1, 
            width=6, 
            bg=W_VAR.NEUTRAL_700,
            fg=W_VAR.TEXT_COLOR, 
            font=W_VAR.font_size,
            relief="flat",
            highlightthickness=1,
            highlightbackground=W_VAR.NEUTRAL_400,
            highlightcolor=W_VAR.BUTTON_1 
            )
        self.stop_key_1.grid(row=0, column=0, padx=(0, 10))

        # Entry pour la deuxième touche du raccourci
        # -------------------------------------------
        # Entry for the second shortcut key
        pre_filling_stop_key_2 = tk.StringVar(value=KeyLoggerApp.stop_keys[1])
        self.stop_key_2 = tk.Entry(
            stop_entry_frm, 
            textvariable=pre_filling_stop_key_2, 
            width=6, 
            bg=W_VAR.NEUTRAL_700,
            fg=W_VAR.TEXT_COLOR, 
            font=W_VAR.font_size,
            relief="flat",
            highlightthickness=1,
            highlightbackground=W_VAR.NEUTRAL_400,
            highlightcolor=W_VAR.BUTTON_1 
            )
        self.stop_key_2.grid(row=0, column=1)

        # Label d'erreur (caché jusqu'à son utilisation)
        # -----------------------------------------------
        # Error label (hidden until needed)
        self.stop_keys_error_label = tk.Label(
            self.doc_frame, 
            text="", 
            bg=W_VAR.NEUTRAL_800, 
            fg=W_VAR.ERROR_COLOR, 
            height=1, 
            width=40, 
            font=W_VAR.font_size_error
            )
        
        # Bouton pour valider les touches
        # ----------------------------------
        # Button to apply the selected keys
        apply_stop_keys_btn = HoverButton(
            self.doc_frame, 
            text="Apply", 
            color=W_VAR.BUTTON_1,
            hover=W_VAR.BUTTON_1_HOVER,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=20, 
            font=W_VAR.font_size, 
            command=self.apply_stop_keys
            )
        apply_stop_keys_btn.grid(row=4, column=0)

        # Label informatif
        # -----------------
        # Info label
        capture_keys_label = tk.Label(
            self.doc_frame, 
            text="Edit position capture keys :", 
            bg=W_VAR.NEUTRAL_800, 
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=20, 
            font=W_VAR.font_size
            )
        capture_keys_label.grid(row=5, column=0, pady=(20,0))

        # Frame pour organiser les Entry des touches de capture de position
        # ------------------------------------------------------------------
        # Frame to organize the position capture key Entry widgets
        capture_entry_frm = tk.Frame(self.doc_frame, bg=W_VAR.NEUTRAL_800)
        capture_entry_frm.grid(row=6, column=0, pady=10)

        # Entry pour la première touche du raccourci
        # -------------------------------------------
        # Entry for the first shortcut key
        pre_filling_capture_key_1 = tk.StringVar(value=KeyPosition.position_capture_keys[0])
        self.capture_key_1 = tk.Entry(
            capture_entry_frm, 
            textvariable=pre_filling_capture_key_1, 
            width=6, 
            bg=W_VAR.NEUTRAL_700,
            fg=W_VAR.TEXT_COLOR, 
            font=W_VAR.font_size,
            relief="flat",
            highlightthickness=1,
            highlightbackground=W_VAR.NEUTRAL_400,
            highlightcolor=W_VAR.BUTTON_1 
            )
        self.capture_key_1.grid(row=0, column=0, padx=(0, 10))

        # Entry pour la deuxième touche du raccourci
        # -------------------------------------------
        # Entry for the second shortcut key
        pre_filling_capture_key_2 = tk.StringVar(value=KeyPosition.position_capture_keys[1])
        self.capture_key_2 = tk.Entry(
            capture_entry_frm, 
            textvariable=pre_filling_capture_key_2, 
            width=6, 
            bg=W_VAR.NEUTRAL_700,
            fg=W_VAR.TEXT_COLOR, 
            font=W_VAR.font_size,
            relief="flat",
            highlightthickness=1,
            highlightbackground=W_VAR.NEUTRAL_400,
            highlightcolor=W_VAR.BUTTON_1 
            )
        self.capture_key_2.grid(row=0, column=1)

        # Label d'erreur (caché jusqu'à son utilisation)
        # -----------------------------------------------
        # Error label (hidden until needed)
        self.capture_keys_error_label = tk.Label(
            self.doc_frame, 
            text="", 
            bg=W_VAR.NEUTRAL_800, 
            fg=W_VAR.ERROR_COLOR, 
            height=1, 
            width=40, 
            font=W_VAR.font_size_error
            )
        
        # Bouton pour valider les touches
        # ----------------------------------
        # Button to apply the selected keys
        apply_capture_keys_btn = HoverButton(
            self.doc_frame, 
            text="Apply", 
            color=W_VAR.BUTTON_1,
            hover=W_VAR.BUTTON_1_HOVER,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=20, 
            font=W_VAR.font_size, 
            command=self.apply_capture_keys
            )
        apply_capture_keys_btn.grid(row=9, column=0)

        # Bouton pour ouvrir le site internet de la documentation
        # --------------------------------------------------------
        # Button to open the documentation website
        open_doc_btn = HoverButton(
            self.doc_frame, 
            text="Doc", 
            color=W_VAR.BUTTON_2,
            hover=W_VAR.BUTTON_2_HOVER,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=20, 
            font=W_VAR.font_size, 
            command=self.open_documentation
            )
        open_doc_btn.grid(row=10, column=0, pady=(8,30))


    def open_documentation(self) -> None:
        """
        Ouvre le site internet de la documentation de la macro
        -------------------------------------------------------
        Opens the macro documentation website
        """
        webbrowser.open(DOCUMENTATION_URL)


    def apply_stop_keys(self) -> None:
        """
        Vérifie que l'utilisateur ait entré qu'un seul caractère par champ.
        Sinon, on affiche une erreur. Si oui, on appelle la fonction permettant
        d'enregistrer le raccourci clavier, on modifie les touches et on crée un popup.
        --------------------------------------------------------------------------------
        Checks that the user entered only one character per field.
        If not, an error message is displayed. Otherwise, the keyboard shortcut
        is saved, the keys are updated, and a popup is shown.
        """
        new_stop_key_1 = self.stop_key_1.get()
        new_stop_key_2 = self.stop_key_2.get()

        if len(new_stop_key_1) == 1 and len(new_stop_key_2) == 1:
            save_shortcuts(ShortCut.STOP, [new_stop_key_1, new_stop_key_2])
            KeyLoggerApp.stop_keys = [new_stop_key_1, new_stop_key_2]
            self.window.focus()
            self.show_confirmation_popup()
            self.stop_keys_error_label.grid_remove()
        else:
            self.stop_keys_error_label.config(
                text="You can only enter\none character per field",
                height=2
                )
            self.stop_keys_error_label.grid(row=3, column=0)


    def apply_capture_keys(self) -> None:
        """
        Vérifie que l'utilisateur ait entré qu'un seul caractère par champ.
        Sinon, on affiche une erreur. Si oui, on appelle la fonction permettant
        d'enregistrer le raccourci clavier, on modifie les touches et on crée un popup.
        --------------------------------------------------------------------------------
        Checks that the user entered only one character per field.
        If not, an error message is displayed. Otherwise, the keyboard shortcut
        is saved, the keys are updated, and a popup is shown.
        """

        new_capture_key_1 = self.capture_key_1.get()
        new_capture_key_2 = self.capture_key_2.get()

        if len(new_capture_key_1) == 1 and len(new_capture_key_2) == 1:
            save_shortcuts(ShortCut.CAPTURE, [new_capture_key_1, new_capture_key_2])
            KeyPosition.position_capture_keys = [new_capture_key_1, new_capture_key_2]
            self.window.focus()
            self.show_confirmation_popup()
            self.capture_keys_error_label.grid_remove()
        else:
            self.capture_keys_error_label.config(
                text="You can only enter\none character per field",
                height=2
                )
            self.capture_keys_error_label.grid(row=8, column=0)


    def show_confirmation_popup(self) -> None:
        """
        Crée un popup informant l'utilisateur que les 
        touches ont bien été enregistrées.
        ----------------------------------------------
        Creates a popup informing the user that the 
        keys have been successfully saved.
        """

        popup = tk.Toplevel(self.window)
        popup.title("Zecron")
        popup.geometry("200x100")
        popup.config(bg=W_VAR.NEUTRAL_800)

        label = tk.Label(
            popup, 
            text="The keys have been saved", 
            font=W_VAR.font_size,
            bg=W_VAR.NEUTRAL_800,
            fg=W_VAR.TEXT_COLOR
        )
        label.pack(pady=10)

        close_btn = HoverButton(
            popup, 
            text="OK", 
            color=W_VAR.BUTTON_1,
            hover=W_VAR.BUTTON_1_HOVER,
            fg=W_VAR.TEXT_COLOR, 
            height=1, 
            width=10, 
            font=W_VAR.font_size, 
            command=popup.destroy)
        close_btn.pack(pady=5)