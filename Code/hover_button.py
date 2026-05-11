import tkinter as tk


class HoverButton(tk.Button):
    """
    Bouton tkinter avec effet de survol (hover).
    Change de couleur de fond lorsque la souris entre ou quitte
    la zone du bouton.
    -------------------------------------------------------------
    Tkinter button with a hover effect.
    Changes the background color when the mouse enters or leaves
    the button area.
    """


    def __init__(self, master: tk.Widget, color: str, hover: str, **kwargs) -> None:
        """
        Initialise le bouton avec ses couleurs et lie les événements souris.

        :param master: Widget parent contenant ce bouton.
        :param color: Couleur de fond par défaut (ex: "#4CAF50").
        :param hover: Couleur de fond au survol de la souris (ex: "#66BB6A").
        :param **kwargs: Arguments supplémentaires passés à tk.Button.
        ----------------------------------------------------------------------
        Initializes the button with its colors and binds the mouse events.

        :param master: Parent widget containing this button.
        :param color: Default background color (e.g. "#4CAF50").
        :param hover: Background color on mouse hover (e.g. "#66BB6A").
        :param **kwargs: Additional arguments passed to tk.Button.
        """
        # Initialisation du tk.Button parent avec un style épuré :
        # sans bordure (bd=0), sans relief visuel, et curseur "main" au survol.
        # ----------------------------------------------------------------------
        # Initialize the parent tk.Button with a clean style:
        # no border (bd=0), no visual relief, and a "hand" cursor on hover.
        super().__init__(
            master,
            bg=color,
            bd=0,
            relief="flat",
            cursor="hand2",
            **kwargs,
        )
        # Mémorisation des deux états de couleur pour les réutiliser dans les callbacks.
        # -------------------------------------------------------------------------------
        # Store both color states to reuse them in the callbacks.
        self.default_bg = color
        self.hover_bg = hover

        # Liaison des événements souris aux méthodes de changement de couleur.
        # ---------------------------------------------------------------------
        # Bind mouse events to the color-change methods.
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e: tk.Event) -> None:
        """
        Applique la couleur de survol lorsque la souris entre sur le bouton.
        :param e: Événement tkinter déclenché à l'entrée du curseur.
        ---------------------------------------------------------------------
        Applies the hover color when the mouse enters the button.
        :param e: Tkinter event triggered when the cursor enters.
        """
        self.config(bg=self.hover_bg)

    def on_leave(self, e: tk.Event) -> None:
        """
        Restaure la couleur par défaut lorsque la souris quitte le bouton.
        :param e: Événement tkinter déclenché à la sortie du curseur.
        -------------------------------------------------------------------
        Restores the default color when the mouse leaves the button.
        :param e: Tkinter event triggered when the cursor leaves.
        """
        self.config(bg=self.default_bg)
