import tkinter as tk
from tkinter import ttk
from ui_style import W_VAR


class ScrollableFrame(ttk.Frame):
    """
    Widget de frame défilante basé sur ttk.Frame.

    Combine un Canvas et une Scrollbar pour permettre le défilement vertical
    des widgets enfants placés dans `scrollable_frame`.
    Le défilement à la molette est activé uniquement lorsque le curseur survole
    le widget, et est lié récursivement à tous les widgets enfants.
    ------------------------------------------------------------------------------
    A scrollable frame widget built on top of ttk.Frame.

    Combines a Canvas and a Scrollbar to enable vertical scrolling
    over any child widgets placed inside `scrollable_frame`.
    Mouse wheel scrolling is activated only when the cursor hovers
    over the widget, and is recursively bound to all child widgets.
    """

    def __init__(
        self,
        container: tk.Widget,
        width: int = 260,
        height: int = 250,
        *args,
        **kwargs,
        ) -> None:
        """
        Initialise la frame défilante et configure le canvas, la scrollbar,
        la mise en page et les liaisons d'événements souris.

        :param container: Widget parent qui contiendra cette frame défilante.
        :param width: Largeur de la zone visible du canvas en pixels (défaut : 260).
        :param height: Hauteur de la zone visible du canvas en pixels (défaut : 250).
        :param *args: Arguments positionnels supplémentaires passés à ttk.Frame.
        :param **kwargs: Arguments nommés supplémentaires passés à ttk.Frame.
        ------------------------------------------------------------------------------
        Initializes the scrollable frame and sets up the canvas, scrollbar,
        layout, and mouse event bindings.

        :param container: Parent widget that will contain this scrollable frame.
        :param width: Width of the visible canvas area in pixels (default: 260).
        :param height: Height of the visible canvas area in pixels (default: 250).
        :param *args: Additional positional arguments passed to ttk.Frame.
        :param **kwargs: Additional keyword arguments passed to ttk.Frame.
        """
        super().__init__(container, *args, **kwargs)

        # Configuration du canvas: 
        # Le canvas sert de fenêtre de visualisation défilante
        # -----------------------------------------------------
        # Canvas setup: 
        # The canvas acts as the scrollable viewport
        self.canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            bg=W_VAR.NEUTRAL_700,
            highlightthickness=0,  # Remove the default focus border
        )

        # Configuration de la scrollbar: 
        # Scrollbar verticale liée à l'axe Y du canvas.4
        # ------------------------------------------------
        # Scrollbar setup: 
        # Vertical scrollbar linked to the canvas y-axis.
        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
        )

        # Configuration de la frame interne: 
        # Les widgets enfants doivent être ajoutés à cette frame, pas directement au canvas.
        # -----------------------------------------------------------------------------------
        # Inner frame setup: 
        # All child widgets should be added to this frame, not directly to the canvas.
        self.scrollable_frame = tk.Frame(self.canvas, bg=W_VAR.NEUTRAL_700)

        # Met à jour la zone de défilement du canvas à chaque redimensionnement de la frame interne.
        # -------------------------------------------------------------------------------------------
        # Update the canvas scroll region whenever the inner frame is resized.
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)

        # Intègre la frame interne dans le canvas en haut à gauche.
        # ----------------------------------------------------------------
        # Embed the inner frame inside the canvas at the top-left corner.
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Synchronise la position de la scrollbar avec la vue du canvas
        # --------------------------------------------------------------
        # Keep the scrollbar position in sync with the canvas view
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Mise en page: 
        # Le canvas occupe tout l'espace disponible ; la scrollbar est ancrée à sa droite.
        # ---------------------------------------------------------------------------------
        # Layout: 
        # Canvas takes all available space; scrollbar is anchored to its right.
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Activation de la molette: 
        # Active le défilement uniquement lorsque le curseur est dans la zone du widget.
        # --------------------------------------------------------------------------------
        # Mouse wheel activation: 
        # Enable scrolling only while the cursor is inside the widget area.
        self.canvas.bind("<Enter>", self._activate_scroll)
        self.canvas.bind("<Leave>", self._deactivate_scroll)

        # Lie aussi la frame interne pour que le survol des widgets enfants maintienne le défilement actif.
        # --------------------------------------------------------------------------------------------------
        # Also bind the inner frame so hovering over child widgets keeps scrolling active.
        self.scrollable_frame.bind("<Enter>", self._activate_scroll)
        self.scrollable_frame.bind("<Leave>", self._deactivate_scroll)

    def _on_frame_configure(self, event: tk.Event) -> None:
        """
        Met à jour la zone de défilement du canvas pour correspondre à la taille actuelle
        de la frame interne. Appelée automatiquement à chaque ajout de widget ou redimensionnement.
        Relie également les événements molette aux nouveaux widgets enfants ajoutés.

        :param event: Événement Configure déclenché par le redimensionnement de la frame interne.
        --------------------------------------------------------------------------------------------
        Updates the canvas scroll region to match the current size of the inner frame.
        Called automatically whenever a widget is added or the frame is resized.
        Also re-binds mouse wheel events to any newly added child widgets.

        :param event: Configure event triggered by a resize of the inner frame.
        """
        # Étend la zone défilable pour englober tous les widgets de la frame interne.
        # ----------------------------------------------------------------------------
        # Expand the scrollable area to encompass all widgets in the inner frame.
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Relie tous les enfants pour que les nouveaux widgets activent aussi le défilement au survol.
        # ---------------------------------------------------------------------------------------------
        # Re-bind all children so new widgets also activate scroll on hover.
        self._bind_children(self.scrollable_frame)

    def _bind_children(self, parent: tk.Widget) -> None:
        """
        Lie récursivement les événements entrée/sortie souris à tous les widgets enfants
        du parent donné, afin que le survol de n'importe quel widget imbriqué
        maintienne la molette active.

        :param parent: Le widget dont les enfants seront liés.
        ---------------------------------------------------------------------------------
        Recursively binds mouse enter/leave events to all child widgets
        of the given parent, so that hovering over any nested widget
        keeps the mouse wheel scroll active.

        :param parent: The widget whose children will be bound.
        """
        for child in parent.winfo_children():
            child.bind("<Enter>", self._activate_scroll)
            child.bind("<Leave>", self._deactivate_scroll)
            # Récursion dans les conteneurs imbriqués (frames, labelframes, etc.)
            # --------------------------------------------------------------------
            # Recurse into nested containers (frames, labelframes, etc.)
            self._bind_children(child)

    def _activate_scroll(self, event: tk.Event) -> None:
        """
        Active le défilement à la molette globalement lorsque le curseur entre dans le widget.
        Lie l'événement MouseWheel au niveau de l'application pour qu'il soit capturé
        quel que soit le widget enfant qui a le focus.

        :param event: Événement Enter déclenché quand le curseur entre dans le widget.
        ---------------------------------------------------------------------------------------
        Enables mouse wheel scrolling globally when the cursor enters the widget.
        Binds the MouseWheel event at the application level so it is captured
        regardless of which child widget currently has focus.

        :param event: Enter event triggered when the cursor moves into the widget.
        """
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _deactivate_scroll(self, event: tk.Event) -> None:
        """
        Désactive le défilement à la molette lorsque le curseur quitte le widget.
        Supprime la liaison globale MouseWheel pour éviter d'interférer avec
        d'autres widgets défilants ailleurs dans l'application.

        :param event: Événement Leave déclenché quand le curseur quitte le widget.
        -----------------------------------------------------------------------------
        Disables mouse wheel scrolling when the cursor leaves the widget.
        Unbinds the global MouseWheel event to avoid interfering with
        other scrollable widgets elsewhere in the application.

        :param event: Leave event triggered when the cursor moves out of the widget.
        """
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mouse_wheel(self, event: tk.Event) -> None:
        """
        Fait défiler le canvas verticalement en réponse à un mouvement de molette.
        Convertit la valeur delta spécifique à la plateforme en unité de défilement :
        sous Windows, le delta est un multiple de 120 (un cran = 120).

        :param event: Événement MouseWheel portant la valeur de défilement delta.
        ------------------------------------------------------------------------------
        Scrolls the canvas vertically in response to a mouse wheel movement.
        Converts the platform-specific delta value into a scroll unit:
        on Windows, delta is a multiple of 120 (one notch = 120).

        :param event: MouseWheel event carrying the scroll delta.
        """
        # Division par 120 pour normaliser le delta en unités de défilement (1 cran = 1 unité)
        # -------------------------------------------------------------------------------------
        # Divide by 120 to normalize the delta to scroll units (1 notch = 1 unit)
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")