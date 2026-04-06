from dataclasses import dataclass
import tkinter as tk


from ui_action_manager import ActionSelectorUI
from ui_action_tree import TreeUI
from ui_sequence_loader import SavedSequencesUI
from ui_documentation import DocumentationUI
from action_classes import KeyLoggerApp, KeyPosition

from hotkey_manager import load_shortcuts
from enums import ShortCut


# On crée la fenêtre.
# ------------------------
# Create the main window.
window = tk.Tk()

# On crée une classe de données pour les valeurs fréquemment utilisées,
# principalement liées au style de la fenêtre.
# ----------------------------------------------------------------------
# Create a data class for frequently used values,
# mainly related to the window's style.
@dataclass
class WindowVariable:
    # Police d'écriture pour les textes normaux.
    # -------------------------------------------
    # Font for regular text.
    font_size = ("Cooper Black", 11)
    # Police d'écriture pour les messages d'erreur.
    # ----------------------------------------------
    # Font for error messages.
    font_size_error = ("Impact", 11)

    # Dimensions de l'écran principal de l'utilisateur.
    # --------------------------------------------------
    # User's main screen dimensions.
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Dimensions de la fenêtre.
    # --------------------------
    # Window dimensions.
    window_width = 320
    window_height = 480

    # Couleur de fond.
    # ------------------
    # Background color.
    color_1 = "#71B0B0"
    # Couleur des boutons et des champs de texte.
    # --------------------------------------------
    # Button and text field color.
    color_2 = "#FFB268"
    # Couleur du texte.
    # ------------------
    # Text color.
    color_3 = "#000000"
    # Couleur des boutons déjà cliqués.
    # -----------------------------------
    # Color for already clicked buttons.
    color_4 = "#0039F5"

# On crée une instance de WindowVariable pour pouvoir accéder à ses valeurs.
# ---------------------------------------------------------------------------
# Create an instance of WindowVariable to access its values.
w_var = WindowVariable()

# On définit les propriétés de la fenêtre.
# -----------------------------------------
# Set window properties.
window.title("hello world")
window.geometry("320x480")
window.minsize(w_var.window_width, w_var.window_height)
window.config(background=w_var.color_1)

# On crée un cadre pour contenir les boutons 
# utilisés pour naviguer dans les différents menus.
# --------------------------------------------------
# Create a frame to hold the buttons
# used to navigate between different menus.
menu_bt_frm = tk.Frame(window, bg=w_var.color_2)
menu_bt_frm.grid(row=0, column=0)

# On remplace les raccourcis clavier par défaut par ceux enregistrés par l'utilisateur.
# --------------------------------------------------------------------------------------
# Replace default keyboard shortcuts with user-defined ones.
all_shortcuts = load_shortcuts()
KeyLoggerApp.stop_keys = all_shortcuts[ShortCut.STOP]
KeyPosition.position_capture_keys = all_shortcuts[ShortCut.CAPTURE]


# On crée une fonction pour passer d'un menu à l'autre.
# ------------------------------------------------------
# Create a function to switch between menus.
def switch_frame(frame: tk.Frame) -> None:
    """
    Cette fonction permet de passer d'un menu à l'autre en affichant 
    le cadre du menu choisi et en cachant le cadre du menu précédent.
    ------------------------------------------------------------------
    This function switches between menus by displaying
    the selected menu frame and hiding the previous one.
    """
    global current_frame
    global ui_action_manager
    global ui_action_tree
    # On vérifie que la suite d'actions n'est pas en train de s'exécuter,
    # et que l'utilisateur n'est pas en train de modifier sa suite d'actions.
    # ------------------------------------------------------------------------
    # Check that the action sequence is not currently running
    # and that the user is not editing it.
    if not ui_action_manager.action_manager.is_running and not ui_action_tree.in_edit:
        # Si l'utilisateur choisit le menu de création de suite d'actions on indique 
        # que l'utilisateur est dans le menu de création de suite d'actions.
        # ---------------------------------------------------------------------------
        # If the user selects the action sequence creation menu,
        # mark that the user is in the action selector.
        if frame == ui_action_manager.selector_frame:
            ui_action_manager.in_action_selector = True
            # Et si le menu précédent n'était pas le menu de création de suite d'actions,
            # on met à jour les positions de la souris pour les afficher à l'utilisateur.
            # ----------------------------------------------------------------------------
            # If the previous menu was not the action selector,
            # update mouse positions to display them to the user.
            if current_frame != ui_action_manager.selector_frame:
                ui_action_manager.update_mouse_positions()
        else:
            # Si l'utilisateur choisit un autre menu que celui de création de suite d'actions, 
            # on indique que l'utilisateur n'est pas dans le menu de création de suite d'actions.
            # ------------------------------------------------------------------------------------
            # If the user selects another menu,
            # mark that they are not in the action selector.
            ui_action_manager.in_action_selector = False
        
        # On cache le menu précédent et on affiche le menu choisi.
        # ---------------------------------------------------------
        # Hide the previous menu and display the selected one.
        current_frame.grid_remove()
        frame.grid(row=2, column=0)
        # On met à jour le menu actuel.
        # ------------------------------------
        # Update the current frame reference.
        current_frame = frame


# On crée une fonction permettant de réinitialiser la suite d'actions,
# comme si on venait de démarrer le programme.
# ---------------------------------------------------------------------
# Create a function to reset the action sequence,
# as if the program had just started.
def reset_action_sequence() -> None:
    """
    Cette fonction permet de réinitialiser la suite d'actions, comme si on venait de démarrer le programme.
    --------------------------------------------------------------------------------------------------------------------
    This function resets the action sequence as if the program had just started.
    """
    global ui_action_manager
    global ui_action_tree
    # On vérifie que la suite d'actions de l'utilisateur n'est pas en cours d'exécution.
    # -----------------------------------------------------------------------------------
    # Check that the action sequence is not currently running.
    if not ui_action_manager.action_manager.is_running:
        # On réinitialise les différentes parties de la suite d'actions de l'utilisateur.
        # --------------------------------------------------------------------------------
        # Reset the different parts of the user's action sequence.
        ui_action_manager.action_manager.reset_state()
        ui_action_manager.container_manager.reset_state()
        ui_action_tree.reset_state()


# Instanciation des 4 différents menus. Chaque menu va créer un 
# bouton dans menu_bt_frm pour accéder à son propre cadre.
# --------------------------------------------------------------
# Instantiate the 4 different menus. Each menu creates a button 
# in menu_bt_frm to access its own frame.
ui_action_tree = TreeUI(
    window, 
    menu_bt_frm, 
    switch_frame, 
    w_var, 
    reset_action_sequence
    )
ui_action_manager = ActionSelectorUI(
    window, 
    menu_bt_frm, 
    switch_frame, 
    w_var, 
    ui_action_tree
    )
ui_saved_sequences = SavedSequencesUI(
    window, 
    menu_bt_frm, 
    switch_frame, 
    w_var, 
    reset_action_sequence, 
    ui_action_manager.action_manager, 
    ui_action_manager.container_manager.leave_current_container, 
    ui_action_manager.container_manager
    )
ui_documentation = DocumentationUI(
    window, 
    menu_bt_frm, 
    switch_frame, 
    w_var
    )

# On permet à ui_action_tree d'accéder à ui_action_manager et à ui_action_manager.container_manager,
# afin qu'il puisse modifier la suite d'actions de l'utilisateur et lancer l'exécution...
# ---------------------------------------------------------------------------------------------------
# Allow ui_action_tree to access ui_action_manager and its container_manager,
# so it can modify the user's action sequence and trigger execution...
ui_action_tree.ui_action_manager = ui_action_manager
ui_action_tree.container_manager = ui_action_manager.container_manager

# Maintenant que ui_action_tree.container_manager est assigné,
# on lance l'instanciation des frames de chaque type d'action (pour éditer des actions).
# ---------------------------------------------------------------------------------------
# Now that ui_action_tree.container_manager is assigned,
# initialize the frames for each action type (used for editing actions).
ui_action_tree.frame_act()

# On affiche le menu de création de suite d'actions par défaut.
# --------------------------------------------------------------
# Display the action sequence creation menu by default.
current_frame = ui_action_manager.selector_frame
current_frame.grid(row=1, column=0, sticky="wen")


# On lance la boucle principale de la fenêtre.
# ---------------------------------------------
# Start the main application loop.
window.mainloop()