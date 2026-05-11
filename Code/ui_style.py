from dataclasses import dataclass

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
    #tkinter_basic_font_size = ("Segoe UI", 9)
    #little_font_size = ("Segoe UI", 10)
    #font_size = ("Segoe UI", 12)

    #font_size = ("Segoe UI", 12)
    #little_font_size = ("Segoe UI", 10)

    font_size = ("Segoe UI", 12)
    font_size_medium = ("Segoe UI", 11)
    little_font_size = ("Segoe UI", 10)
    # Police d'écriture pour les messages d'erreur.
    # ----------------------------------------------
    # Font for error messages.
    font_size_error = ("Impact", 11)


    # Dimensions de l'écran principal de l'utilisateur.
    # --------------------------------------------------
    # User's main screen dimensions.
    screen_width = None
    screen_height = None

    # Dimensions de la fenêtre.
    # --------------------------
    # Window dimensions.
    window_width = 370
    window_height = 550

    # Couleur du texte.
    # ------------------
    # Text color.
    TEXT_COLOR = "#EAEAEA"

    # Couleur des messages d'erreur.
    # -------------------------------   
    # Color for error messages.
    ERROR_COLOR = "#f87171"

    # Nuances de gris.
    # -----------------
    # Shades of gray.
    NEUTRAL_900 = "#121212"
    NEUTRAL_800 = "#1E1E1E" # Background color
    NEUTRAL_700 = "#2C2C2C"
    NEUTRAL_600 = "#383838"
    NEUTRAL_500 = "#474747"
    NEUTRAL_400 = "#5A5A5A"
    NEUTRAL_300 = "#707070"

    # Couleur de fond de la fenêtre.
    # -------------------------------
    # Window background color.
    BACKGROUND = NEUTRAL_800

    # Couleurs des boutons.
    # ----------------------
    # Button colors.
    BUTTON_1 = "#4CAF50" # Main color
    BUTTON_1_HOVER = "#66BB6A"
    BUTTON_2 = "#2E7D32"
    BUTTON_2_HOVER = "#59B65D"
    BUTTON_3 = "#2ecc71"
    BUTTON_3_HOVER = "#27ae60"
    BUTTON_4 = "#3498db"
    BUTTON_4_HOVER = "#2980b9"
    BUTTON_5 = "#3a3f44"
    BUTTON_5_HOVER = "#4b5258"


# On crée une instance de WindowVariable pour pouvoir accéder à ses valeurs.
# ---------------------------------------------------------------------------
# Create an instance of WindowVariable to access its values.
W_VAR = WindowVariable()