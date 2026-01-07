import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(self, width=235, height=250, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Configurer la région de défilement et rebinder les enfants quand la frame change
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Bind canvas pour le cas où la souris est directement sur le canvas
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)

    def _on_frame_configure(self, event):
        # Met à jour la zone de défilement
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # (Re)lier la molette sur tous les widgets enfants (y compris les Radiobutton créés dynamiquement)
        self._bind_all_children(self.scrollable_frame)

    def _bind_all_children(self, parent):
        for child in parent.winfo_children():
            # Lie la molette sur l'enfant : appelle le handler du canvas
            try:
                child.bind("<MouseWheel>", self._on_mouse_wheel, add="+")
            except Exception:
                pass
            # récursif pour les sous-enfants
            self._bind_all_children(child)

    def _on_mouse_wheel(self, event):
        # Défilement standard Windows (delta multiples de 120)
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        return "break"  # Empêcher la propagation aux widgets enfants
