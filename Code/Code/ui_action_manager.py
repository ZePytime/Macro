import tkinter as tk

from action_classes import KeyPositon, position_mouse

from ui_action_frames.ui_move_frame import MouseMoveFrame
from ui_action_frames.ui_click_frame import ClickFrame
from ui_action_frames.ui_wait_frame import WaitFrame
from ui_action_frames.ui_write_frame import WriteFrame
from ui_action_frames.ui_loop_frame import LoopFrame
from ui_action_frames.ui_keyhold_frame import KeyHoldFrame
from ui_action_frames.ui_scroll_frame import ScrollFrame
from ui_action_frames.ui_parallel_actions_frame import ParallelActionsFrame

from action_manager import ActionDict

from container_manager import ContainerManager




class IntfActSelector:

    def __init__(self, window: tk.Tk, menu_btn_frame, switch_frame, w_var, ui_action_tree):
        """
        Cette classe prend en paramètre "window", la fenêtre de l'interface, "menu_btn_frame", qui est la 
        frame dans laquelle on va placer le bouton permettant d'accéder à la frame de la classe, 
        "switch_frame", qui permet de changer de frame et sera utilisée par le bouton dans 
        "menu_btn_frame", "w_var" la dataclass qui contient toutes les variables pour les widgets, comme 
        les couleurs, "ui_action_tree" l'instance de "IntfTree" nécessaire pour pouvoir créer une instance de 
        "ActionDict".
        ------------------------------------------------------------------------------------------------
        This class takes "window", the interface window, as a parameter, "menu_btn_frame", which is the 
        frame where we will place the button to access the class frame, "switch_frame", which allows 
        changing frames and will be used by the button in "menu_btn_frame", "w_var", the dataclass that 
        contains all the variables for the widgets, like colors, and "ui_action_tree", the instance of 
        "IntfTree" needed to create an instance of "ActionDict".
        """

        self.window = window
        self.is_in_move_click = True
        self.is_in_IntfActSelector = True

        # Bouton permettant d’accéder à l'interface de "IntfActSelector".
        # --------------------------------------------------
        # Button to access the "IntfActSelector" interface.
        act_selector_button = tk.Button(menu_btn_frame, 
                                        text="selector", 
                                        bg=w_var.color_2, 
                                        fg="black", 
                                        height=1, 
                                        width=5, 
                                        font=w_var.font_size, 
                                        command=lambda : switch_frame(self.act_selector_frame)
                                        )
        act_selector_button.grid(row=0, column=0)


        # Frame principale de "IntfActSelector".
        # -------------------------
        # Main frame of "IntfActSelector".
        self.act_selector_frame = tk.Frame(window, bg=w_var.color_1, width=320, height=450)
        self.act_selector_frame.grid_propagate(False)







        # On crée toutes les frames pour chaque action.
        # ---------------------------------------------
        # We create all the frames for each action.
        frame_click = tk.Frame(self.act_selector_frame, bg=w_var.color_1)
        frame_move = tk.Frame(self.act_selector_frame, bg=w_var.color_1) 
        frame_write = tk.Frame(self.act_selector_frame, bg=w_var.color_1)
        frame_scroll = tk.Frame(self.act_selector_frame, bg=w_var.color_1)
        frame_wait = tk.Frame(self.act_selector_frame, bg=w_var.color_1)
        frame_pressed = tk.Frame(self.act_selector_frame, bg=w_var.color_1)
        frame_same_time = tk.Frame(self.act_selector_frame, bg=w_var.color_1)
        frame_loop = tk.Frame(self.act_selector_frame, bg=w_var.color_1)


        # On affiche "frame_click" car c'est la frame par défaut lorsqu'on ouvre le 
        # programme, et on attribue à "frame_now" la frame sur laquelle on se trouve.
        # ---------------------------------------------------------------------------
        # We display "frame_click" because it is the default frame when the program 
        # is opened, and we assign "frame_now" to the frame we are currently on.
        frame_click.grid(row=7, column=0)
        self.frame_now = frame_click






        # On crée la frame qui va contenir tous les "Radiobutton", qui vont nous 
        # permettre de passer d'une frame d'une action à une autre.
        # ------------------------------------------------------------------------
        # We create the frame that will contain all the "Radiobutton", which will 
        # allow us to switch from one action's frame to another.
        Rb_frame = tk.Frame(self.act_selector_frame, bg=w_var.color_1)
        Rb_frame.grid(row=1, column=0, sticky="nw")


        # On crée un dictionnaire pour faciliter la création des "Radiobutton".
        # ---------------------------------------------------------------------
        # We create a dictionary to facilitate the creation of "Radiobutton".
        element_for_Rb = {"click l":("click left", frame_click, 1, 0), "click r":("click right", frame_click, 2, 0), 
                          "move":("move", frame_move, 3, 0), "write":("write", frame_write, 1, 2), 
                          "scroll":("scroll", frame_scroll, 2, 2), "wait":("wait", frame_wait, 3, 2), 
                          "key press":("key press", frame_pressed, 1, 3), "same time":("same time", frame_same_time, 2, 3), 
                          "loop":("loop", frame_loop, 3, 3)}

        # On sélectionne le "Radiobutton" "click l" car c'est l'action affichée en premier 
        # par défaut,puis on crée le dictionnaire qui va contenir tous les "Radiobutton".
        # -----------------------------------------------------------------------------------
        # We select the "Radiobutton" "click l" because it is the action displayed first 
        # by default, then we create the dictionary that will contain all the "Radiobutton".
        self.value_Rb = tk.StringVar(value="click l")
        dict_of_Rb = {}


        # On va parcourir le dictionnaire "element_for_Rb" pour créer tous les "Radiobutton", 
        # qui contient tous les paramètres nécessaires. On crée le "Radiobutton" en fonction 
        # des paramètres dans le dictionnaire, puis on va ajouter ce "Radiobutton" au 
        # dictionnaire "dict_of_Rb" et on va afficher le "Radiobutton".
        # ------------------------------------------------------------------------------------
        # We will go through the dictionary "element_for_Rb" to create all the "Radiobuttons", 
        # which contains all the necessary parameters. We create the "Radiobutton" based on 
        # the parameters in the dictionary, then we will add this "Radiobutton" to the 
        # dictionary "dict_of_Rb" and we will display the "Radiobutton".
        for key, (text_Rb, frame, row, column) in element_for_Rb.items():

            dict_of_Rb[key] = tk.Radiobutton(Rb_frame, text=text_Rb, variable=self.value_Rb, 
                                             value=key, background=w_var.color_1, 
                                             command= lambda frame_=frame, key_=key: self.switch(frame_, key_))
            dict_of_Rb[key].grid(row=row, column=column, sticky="nw")





        self.container_manager = ContainerManager(w_var, self.act_selector_frame)



        # On crée les instances des classes permettant de créer les interfaces pour chaque action.
        # ----------------------------------------------------------------------------------------
        # We create instances of the classes that allow creating the interfaces for each action.
        self.click_inst = ClickFrame(frame_click, w_var)
        self.move_inst = MouseMoveFrame(frame_move, w_var)
        self.write_inst = WriteFrame(frame_write, w_var)
        self.scroll_inst = ScrollFrame(frame_scroll, w_var)
        self.wait_inst = WaitFrame(frame_wait, w_var)
        self.pressed_inst = KeyHoldFrame(frame_pressed, w_var)
        self.same_time_inst = ParallelActionsFrame(frame_same_time, w_var, self.container_manager)
        self.loop_inst = LoopFrame(frame_loop, w_var, self.container_manager)

        self.update_positions()

        # On crée l'instance de "ActionDict", cette classe s'occupe de gérer le 
        # dictionnaire qui contiendra toutes les actions.
        # ------------------------------------------------------------------------------
        # We create the instance of "ActionDict", this class manages the dictionary that 
        # will contain all the actions.
        self.act_dict_manager = ActionDict(window, self.container_manager.get_most_nested_container, ui_action_tree)

        # On donne la fonction "left_container" à "leave_container_callback" dans "container_manager", qui 
        # permet de mettre à jour la liste d'enregistrements lorsqu'on quitte un conteneur.
        # ---------------------------------------------------------------------------------
        # We assign the function "left_container" to "leave_container_callback" in "container_manager", 
        # which updates the recording list when a container is exited.
        self.container_manager.leave_container_callback = self.act_dict_manager.left_container

        # On crée une instance de "KeyPosition", cette classe permet d'observer les 
        # relâchements et pressions de touches pour que, si l'utilisateur presse les 
        # deux touches correspondantes, on appelle "set_coordinate", qui va entrer dans 
        # les zones de saisie correspondantes les coordonnées données en paramètre.
        # ----------------------------------------------------------------------------
        # We create an instance of "KeyPosition", this class allows observing key 
        # releases and presses so that if the user presses the two corresponding keys, 
        # "set_coordinate" is called, which will input the given coordinates into the 
        # corresponding input fields.
        self.tkt = KeyPositon(self.click_inst.set_coordinate, self.move_inst.set_coordinate)











        # On crée le bouton pour valider la création d'actions.
        # ---------------------------------------------------------
        # We create the button to validate the creation of actions.
        check_button = tk.Button(self.act_selector_frame, 
                            text="check", 
                            bg=w_var.color_2, 
                            fg="black", 
                            height=1, 
                            width=9, 
                            font=w_var.font_size, 
                            command=self.check
                            )
        check_button.grid(row=8, column=0)

        # On crée le bouton pour lancer l'exécution de la suite d'actions.
        # -------------------------------------------------------------------
        # We create the button to start the execution of the action sequence.
        start_button = tk.Button(self.act_selector_frame, 
                        text="start", 
                        bg=w_var.color_2, 
                        fg="black", 
                        height=1, 
                        width=9, 
                        font=w_var.font_size, 
                        command=lambda : self.act_dict_manager.start(False)
                        )
        start_button.grid(row=9, column=0)






    def check(self):
        """
        Cette fonction est appelée par le bouton "check_button" et elle permet de 
        récupérer les arguments entrés par l'utilisateur pour créer les actions.
        -------------------------------------------------------------------------
        This function is called by the "check_button" and allows for retrieving 
        the arguments entered by the user to create the actions.
        """

        # On vérifie que la suite d'actions n'est pas en cours d'exécution.
        # -----------------------------------------------------------------
        # We check that the sequence of actions is not currently running.
        if not self.act_dict_manager.is_running:

            # On récupère la valeur du "Radiobutton" choisie par l'utilisateur.
            # -----------------------------------------------------------------
            # We retrieve the value of the "Radiobutton" chosen by the user.
            choie = self.value_Rb.get()

            # On cherche l'instance correspondante à la valeur du "Radiobutton" choisie par l'utilisateur. 
            # Ensuite, on appelle la fonction "check" de l'instance correspondante et, si elle ne retourne 
            # pas "False", on récupère les paramètres donnés et on appelle "add_..." de "act_dict_manager", 
            # qui va créer l'action et l'ajouter au dictionnaire des actions. Pour "loop" et "same time", on 
            # appelle les fonctions "indicate_container" et "add_container" de "container_manager", car ce sont des conteneurs.
            # ----------------------------------------------------------------------------------------------------
            # We search for the instance corresponding to the value of the "Radiobutton" chosen by the user. 
            # Then, we call the "check" function of the corresponding instance, and if it does not return "False", 
            # we retrieve the given parameters and call "add_..." from "act_dict_manager", which will create the 
            # action and add it to the action dictionary. For "loop" and "same time", we call the "indicate_container" 
            # and "add_container" functions from "container_manager", as they are containers.
            match choie:
                case "click l":
                    args = self.click_inst.check()
                    if args != False:
                        self.act_dict_manager.add_click_l(args[0], args[1], self.container_manager.is_in_container)

                case "click r":
                    args = self.click_inst.check()
                    if args != False:
                        self.act_dict_manager.add_click_r(args[0], args[1], self.container_manager.is_in_container)

                case "move":
                    args = self.move_inst.check()
                    if args != False:
                        self.act_dict_manager.add_move(args[0], args[1], args[2], self.container_manager.is_in_container)

                case "write":
                    args = self.write_inst.check()
                    if args != False:
                        self.act_dict_manager.add_write(args[0], self.container_manager.is_in_container)

                case "scroll":
                    args = self.scroll_inst.check()
                    if args != False:
                        self.act_dict_manager.add_scroll(args[0], args[1], self.container_manager.is_in_container)

                case "wait":
                    args = self.wait_inst.check()
                    if args != False:
                        self.act_dict_manager.add_wait(args, self.container_manager.is_in_container)

                case "key press":
                    args = self.pressed_inst.check()
                    if args != False:
                        self.act_dict_manager.add_key_press(args[0], args[1], args[2], self.container_manager.is_in_container)

                case "same time":
                    args = self.same_time_inst.check()
                    if args != False:
                        self.act_dict_manager.add_same_time(args[0], args[1], args[2], self.container_manager.is_in_container)
                        self.container_manager.indicate_container(args[2])
                        self.container_manager.add_container(args[2])

                case "loop":
                    args = self.loop_inst.check()
                    if args != False:
                        self.act_dict_manager.add_loop(args[0], args[1], self.container_manager.is_in_container)
                        self.container_manager.indicate_container(args[1])
                        self.container_manager.add_container(args[1])


    def switch(self, frame, key): 
        """
        Cette fonction est appelée par les "Radiobuttons" lorsque l'utilisateur en 
        sélectionne un. Elle permet de passer d'une frame d'action à une autre.
        --------------------------------------------------------------------------
        Cette fonction est appelée par les "Radiobutton" lorsque l'utilisateur en 
        sélectionne un. Elle permet de passer d'une frame d'action à une autre.
        """

        # On cache l'interface sur laquelle nous nous trouvions auparavant, puis on 
        # affiche l'interface choisie par l'utilisateur. On attribue à "frame_now" 
        # la frame dans laquelle nous nous trouvons actuellement.
        # ---------------------------------------------------------------------------
        # We hide the interface we were previously in, then we display the interface 
        # chosen by the user. We assign to "frame_now" the frame we are currently in.
        self.frame_now.grid_remove()
        frame.grid(row=7, column=0)
        self.frame_now = frame




        # On regarde si l'utilisateur a choisi l'interface de mouvement ou de clic droit ou gauche. Si c'est 
        # le cas, on crée une instance de "KeyPosition" si nécessaire. Ensuite, si l'utilisateur a choisi 
        # l'interface de mouvement, on appelle la fonction "move" de "click_inst" pour changer les 
        # indications. Sinon, on appelle la fonction "click" de "click_inst" pour changer les indications.
        # --------------------------------------------------------------------------------------------------
        # We check if the user has selected the movement interface or the right or left click interface. If 
        # so, we create an instance of "KeyPosition" if necessary. Then, if the user has chosen the movement 
        # interface, we call the "move" function of "click_inst" to change the indications. Otherwise, we 
        # call the "click" function of "click_inst" to change the indications.
        if key == "move" or key == "click l" or key == "click r":
            self.is_in_move_click = True
            
            if not KeyPositon.is_listening:
                self.update_positions()
                self.tkt = KeyPositon(self.click_inst.set_coordinate, self.move_inst.set_coordinate)

        # Vu que l'interface choisie par l'utilisateur n'est ni celle de mouvement ou de 
        # clic droit ou gauchee, on appelle "stop_listening" si nécessaire.
        # ------------------------------------------------------------------------------
        # Since the interface chosen by the user is neither the movement interface nor 
        # the right or left click interface, we call "stop_listening" if necessary.
        else:
            self.is_in_move_click = False
            if KeyPositon.is_listening:
                self.tkt.stop_listening()


    def update_positions(self):
        self.click_inst.mouse_position_label.config(text=f"{position_mouse()[0]} | {position_mouse()[1]}")
        self.move_inst.mouse_position_label.config(text=f"{position_mouse()[0]} | {position_mouse()[1]}")
        if self.is_in_move_click and self.is_in_IntfActSelector:
            self.window.after(60, self.update_positions)
            
