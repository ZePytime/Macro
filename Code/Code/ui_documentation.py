from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Tuple, Union
from functools import partial
import webbrowser

from scrollbarre import ScrollableFrame
from action_classes import KeyLoggerApp, KeyPositon
from hotkey_manager import save_shortcuts
from enums import ShortCut

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
    def __init__(self, window: tk.Tk, menu_btn_frame: tk.Frame, switch_frame: callable, w_var: WindowVariable) -> None:
        """
        Initialisation de tous les widgets permettant la modification des raccourcis
        clavier et/ou des widgets donnant des indications pour utiliser la macro.

        :param window: Fenêtre principale dans laquelle va se trouver ce menu
        :param menu_btn_frame: Menu dans lequel on ajoute le bouton
            permettant de basculer vers cette interface
        :param switch_frame: Fonction permettant de changer de frame
            afin d'afficher cette interface
        :param w_var: Objet contenant les paramètres d'affichage 
            (couleurs, tailles, screen_width/height...)
        -----------------------------------------------------------------------------
        Initializes all widgets that allow keyboard shortcut customization
        and/or provide instructions for using the macro.

        :param window: Main window in which this menu will be displayed
        :param menu_btn_frame: Menu in which the button used to switch to 
            this interface is added
        :param switch_frame: Function used to switch frames in order to 
            display this interface
        :param w_var: Object containing display parameters 
            (colors, sizes, screen_width/height...)
        """

        self.window = window

        # Création du menu
        # -----------------
        # Menu creation

        # Bouton permettant d'accéder au menu DocumentationUI.
        # -----------------------------------------------------
        # Button used to access the DocumentationUI menu.
        doc_btn = tk.Button(menu_btn_frame, 
            text="doc", 
            bg=w_var.color_2, 
            fg="black", 
            height=1, 
            width=4, 
            font=w_var.font_size, 
            command=lambda : switch_frame(self.doc_frame)
            )
        doc_btn.grid(row=0, column=3)

        # Frame principale du menu
        # -------------------------
        # Main menu frame
        self.doc_frame = tk.Frame(
            window, 
            bg=w_var.color_1, 
            width=w_var.window_width, 
            height=w_var.window_height
            )
        self.doc_frame.grid_propagate(False)

        # Frame scrollable du menu qui va contenir tous les widgets
        # ----------------------------------------------------------
        # Scrollable menu frame that contains all widgets
        self.content_scrollable = ScrollableFrame(self.doc_frame)
        self.content_scrollable.grid(row=0, column=0, padx=30, pady=10)

        # Label informatif
        # -----------------
        # Info label
        stop_keys_label = tk.Label(
            self.content_scrollable.scrollable_frame, 
            text="Edit stop keys", 
            bg=w_var.color_1, 
            fg="black", 
            height=1, 
            width=20, 
            font=w_var.font_size
            )
        stop_keys_label.grid(row=0, column=0)

        # Entry pour la première touche du raccourci
        # -------------------------------------------
        # Entry for the first shortcut key
        pre_filling_stop_key_1 = tk.StringVar(value=KeyLoggerApp.stop_key[0])
        self.stop_key_1 = tk.Entry(
            self.content_scrollable.scrollable_frame, 
            textvariable=pre_filling_stop_key_1, 
            width=6, 
            bg=w_var.color_2, 
            font=w_var.font_size
            )
        self.stop_key_1.grid(row=1, column=0)

        # Entry pour la deuxième touche du raccourci
        # -------------------------------------------
        # Entry for the second shortcut key
        pre_filling_stop_key_2 = tk.StringVar(value=KeyLoggerApp.stop_key[1])
        self.stop_key_2 = tk.Entry(
            self.content_scrollable.scrollable_frame, 
            textvariable=pre_filling_stop_key_2, 
            width=6, 
            bg=w_var.color_2, 
            font=w_var.font_size
            )
        self.stop_key_2.grid(row=2, column=0)

        # Label d'erreur (caché jusqu'à son utilisation)
        # -----------------------------------------------
        # Error label (hidden until needed)
        self.stop_keys_error_label = tk.Label(
            self.content_scrollable.scrollable_frame, 
            text="", 
            bg=w_var.color_1, 
            fg=w_var.color_3, 
            height=1, 
            width=40, 
            font=w_var.font_size_error
            )
        
        # Bouton pour valider les touches
        # ----------------------------------
        # Button to apply the selected keys
        apply_stop_keys_btn = tk.Button(
            self.content_scrollable.scrollable_frame, 
            text="Apply", 
            bg=w_var.color_2, 
            fg="black", 
            height=1, 
            width=9, 
            font=w_var.font_size, 
            command=self.apply_stop_keys
            )
        apply_stop_keys_btn.grid(row=4, column=0)

        # Label informatif
        # -----------------
        # Info label
        capture_keys_label = tk.Label(
            self.content_scrollable.scrollable_frame, 
            text="Edit position\ncapture keys", 
            bg=w_var.color_1, 
            fg="black", 
            height=2, 
            width=20, 
            font=w_var.font_size
            )
        capture_keys_label.grid(row=5, column=0)

        # Entry pour la première touche du raccourci
        # -------------------------------------------
        # Entry for the first shortcut key
        pre_filling_capture_key_1 = tk.StringVar(value=KeyPositon.pos_key_sc[0])
        self.capture_key_1 = tk.Entry(
            self.content_scrollable.scrollable_frame, 
            textvariable=pre_filling_capture_key_1, 
            width=6, 
            bg=w_var.color_2, 
            font=w_var.font_size
            )
        self.capture_key_1.grid(row=6, column=0)

        # Entry pour la deuxième touche du raccourci
        # -------------------------------------------
        # Entry for the second shortcut key
        pre_filling_capture_key_2 = tk.StringVar(value=KeyPositon.pos_key_sc[1])
        self.capture_key_2 = tk.Entry(
            self.content_scrollable.scrollable_frame, 
            textvariable=pre_filling_capture_key_2, 
            width=6, 
            bg=w_var.color_2, 
            font=w_var.font_size
            )
        self.capture_key_2.grid(row=7, column=0)

        # Label d'erreur (caché jusqu'à son utilisation)
        # -----------------------------------------------
        # Error label (hidden until needed)
        self.capture_keys_error_label = tk.Label(
            self.content_scrollable.scrollable_frame, 
            text="", 
            bg=w_var.color_1, 
            fg=w_var.color_3, 
            height=1, 
            width=40, 
            font=w_var.font_size_error
            )
        
        # Bouton pour valider les touches
        # ----------------------------------
        # Button to apply the selected keys
        apply_capture_keys_btn = tk.Button(
            self.content_scrollable.scrollable_frame, 
            text="Apply", 
            bg=w_var.color_2, 
            fg="black", 
            height=1, 
            width=9, 
            font=w_var.font_size, 
            command=self.apply_capture_keys
            )
        apply_capture_keys_btn.grid(row=9, column=0)

        # Bouton pour ouvrir le site internet de la documentation
        # --------------------------------------------------------
        # Button to open the documentation website
        open_doc_btn = tk.Button(
            self.content_scrollable.scrollable_frame, 
            text="Doc", 
            bg=w_var.color_2, 
            fg="black", 
            height=1, 
            width=9, 
            font=w_var.font_size, 
            command=self.open_documentation
            )
        open_doc_btn.grid(row=10, column=0)


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
            KeyLoggerApp.stop_key = [new_stop_key_1, new_stop_key_2]
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
            KeyPositon.pos_key_sc = [new_capture_key_1, new_capture_key_2]
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
        popup.title("Information")
        popup.geometry("200x100")

        label = tk.Label(popup, text="The keys have been saved")
        label.pack(pady=10)

        close_btn = tk.Button(popup, text="OK", command=popup.destroy)
        close_btn.pack(pady=5)