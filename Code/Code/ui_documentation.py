import tkinter as tk


from scrollbarre import ScrollableFrame

from action_classes import KeyLoggerApp, KeyPoisiton

from hotkey_manager import save_shortcuts


class IntfDoc:
        
    def __init__(self, window, menu_bt_frame, frame_exchanger, w_var):
        """
        Cette classe prend en paramètre "window", la fenêtre de l'interface, "menu_bt_frame", qui est la 
        frame dans laquelle on va placer le bouton permettant d'accéder à la frame de la classe, 
        "frame_exchanger", qui permet de changer de frame et sera utilisée par le bouton dans 
        "menu_bt_frame", "w_var" la dataclass qui contient toutes les variables pour les widgets, 
        comme les couleurs.
        ------------------------------------------------------------------------------------------------
        This class takes the following parameters: "window", the interface window; "menu_bt_frame", 
        which is the frame where the button that allows access to the class's frame will be placed; 
        "frame_exchanger", which allows switching between frames and will be used by the button in 
        "menu_bt_frame"; "w_var", the dataclass that contains all the variables for the widgets, such 
        as colors.
        """
        self.window = window
        self.w_var = w_var


        # Création de l'interface.
        # ------------------------
        # Interface creation.


        # Bouton permettant d’accéder à l'interface de "IntfDoc".
        # --------------------------------------------------
        # Button to access the "IntfDoc" interface.
        doc_bt = tk.Button(menu_bt_frame, 
                            text="doc", 
                            bg=w_var.color_2, 
                            fg="black", 
                            height=1, 
                            width=4, 
                            font=w_var.font_size, 
                            command=lambda : frame_exchanger(self.doc_frame)
                            )
        doc_bt.grid(row=0, column=3)

        self.doc_frame = tk.Frame(window, bg=w_var.color_1, width=320, height=450)
        self.doc_frame.grid_propagate(False)


        self.doc = ScrollableFrame(self.doc_frame)
        self.doc.grid(row=0, column=0, padx=30, pady=10)

        self.text = tk.Label(self.doc.scrollable_frame, 
                    text='salut', 
                    bg=w_var.color_1, 
                    fg="black", 
                    height=2, 
                    width=4, 
                    font=w_var.font_size
                    )
        self.text.grid(row=0, column=0)









        self.text = tk.Label(self.doc.scrollable_frame, 
                    text="modifier les touches d'aret", 
                    bg=w_var.color_1, 
                    fg="black", 
                    height=1, 
                    width=20, 
                    font=w_var.font_size
                    )
        self.text.grid(row=1, column=0)


        self.K_1_stop_run = tk.StringVar(value=KeyLoggerApp.stop_key[0])
        self.K_1_stop_run_entry = tk.Entry(self.doc.scrollable_frame, 
                                    textvariable=self.K_1_stop_run, 
                                    width=6, 
                                    bg=w_var.color_2, 
                                    font=w_var.font_size
                                    )
        self.K_1_stop_run_entry.grid(row=2, column=0)

        self.K_2_stop_run = tk.StringVar(value=KeyLoggerApp.stop_key[1])
        self.K_2_stop_run_entry = tk.Entry(self.doc.scrollable_frame, 
                                    textvariable=self.K_2_stop_run, 
                                    width=6, 
                                    bg=w_var.color_2, 
                                    font=w_var.font_size
                                    )
        self.K_2_stop_run_entry.grid(row=3, column=0)

        check_button = tk.Button(self.doc.scrollable_frame, 
                            text="check", 
                            bg=w_var.color_2, 
                            fg="black", 
                            height=1, 
                            width=9, 
                            font=w_var.font_size, 
                            command=self.check_stop_key
                            )
        check_button.grid(row=4, column=0)








        self.text = tk.Label(self.doc.scrollable_frame, 
                    text="modifier les touches de\n capture de position", 
                    bg=w_var.color_1, 
                    fg="black", 
                    height=2, 
                    width=20, 
                    font=w_var.font_size
                    )
        self.text.grid(row=5, column=0)


        self.K_1_capture = tk.StringVar(value=KeyPoisiton.pos_key_sc[0])
        self.K_1_capture_entry = tk.Entry(self.doc.scrollable_frame, 
                                    textvariable=self.K_1_capture, 
                                    width=6, 
                                    bg=w_var.color_2, 
                                    font=w_var.font_size
                                    )
        self.K_1_capture_entry.grid(row=6, column=0)

        self.K_2_capture = tk.StringVar(value=KeyPoisiton.pos_key_sc[1])
        self.K_2_capture_entry = tk.Entry(self.doc.scrollable_frame, 
                                    textvariable=self.K_2_capture, 
                                    width=6, 
                                    bg=w_var.color_2, 
                                    font=w_var.font_size
                                    )
        self.K_2_capture_entry.grid(row=7, column=0)

        check_button = tk.Button(self.doc.scrollable_frame, 
                            text="check", 
                            bg=w_var.color_2, 
                            fg="black", 
                            height=1, 
                            width=9, 
                            font=w_var.font_size, 
                            command=self.check_key_pos
                            )
        check_button.grid(row=8, column=0)





    def check_stop_key(self):
        futur_stop_key_1 = self.K_1_stop_run_entry.get()
        futur_stop_key_2 = self.K_2_stop_run_entry.get()

        if len(futur_stop_key_1) == 1 and len(futur_stop_key_2) == 1:
            save_shortcuts("stop_key", [futur_stop_key_1, futur_stop_key_2])
            KeyLoggerApp.stop_key = [futur_stop_key_1, futur_stop_key_2]
            self.window.focus()

    def check_key_pos(self):
        futur_capture_key_1 = self.K_1_capture.get()
        futur_capture_key_2 = self.K_2_capture.get()

        if len(futur_capture_key_1) == 1 and len(futur_capture_key_2) == 1:
            save_shortcuts("key_pos", [futur_capture_key_1, futur_capture_key_2])
            KeyPoisiton.pos_key_sc = [futur_capture_key_1, futur_capture_key_2]
            self.window.focus()


#    def create_popup(self, window):
#
#        popup = tk.Toplevel(window)
#        popup.title("Popup")
#        popup.geometry("200x100")
#
#        label = tk.Label(popup, text="Are you sure you want to delete the poop file?")
#        label.pack(pady=10)
#
#        close_button = tk.Button(popup, text="yes", command=lambda : self.delet_file(popup))
#        close_button.pack(pady=5)
#        close_button = tk.Button(popup, text="no", command=popup.destroy)
#        close_button.pack(pady=5)