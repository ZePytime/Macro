from sequence_saver import save
from scrollbarre import ScrollableFrame
from action_classes import ClickRight, ClickLeft, Write, KeyPress, Wait, Loop, Move, Scroll, KeyLoggerApp, SameTime, KeyPoisiton, position_mouse
import tkinter as tk

from ui_action_frames.ui_move_frame import MouseMoveFrame
from ui_action_frames.ui_click_frame import ClickFrame
from ui_action_frames.ui_wait_frame import WaitFrame
from ui_action_frames.ui_write_frame import WriteFrame
from ui_action_frames.ui_loop_frame import LoopFrame
from ui_action_frames.ui_keyhold_frame import KeyHoldFrame
from ui_action_frames.ui_scroll_frame import ScrollFrame
from ui_action_frames.ui_parallel_actions_frame import ParallelActionsFrame


class IntfTree:
        
    def __init__(self, window, menu_bt_frame, frame_exchanger, w_var, reset):
        """
        Cette classe prend en paramètre "window", la fenêtre de l'interface, "menu_bt_frame", qui est la 
        frame dans laquelle on va placer le bouton permettant d'accéder à la frame de la classe, 
        "frame_exchanger", qui permet de changer de frame et sera utilisée par le bouton dans 
        "menu_bt_frame", "w_var" la dataclass qui contient toutes les variables pour les widgets, 
        comme les couleurs. "reset" permet de réinitialiser les valeurs comme si l'on venait de démarrer 
        le programme.
        ------------------------------------------------------------------------------------------------
        This class takes the following parameters: "window", the interface window; "menu_bt_frame", 
        which is the frame where the button that allows access to the class's frame will be placed; 
        "frame_exchanger", which allows switching between frames and will be used by the button in 
        "menu_bt_frame"; "w_var", the dataclass that contains all the variables for the widgets, such 
        as colors; and "reset", which allows resetting the values as if the program had just started.
        """

        self.is_in_move_click = False

        # Je crée le dictionnaire qui va contenir tous les "Checkbutton" avec leurs variables, afin de savoir lors de l'exécution 
        # du programme s'il faut effectuer cette action ou non en fonction de si le Checkbutton est coché ou non.
        # -----------------------------------------------------------------------------------------------------------------------
        # I am creating a dictionary that will contain all the check buttons with their variables, in order to determine during 
        # the program's execution whether to perform this action or not, depending on whether the check button is checked or not.
        self.dict_tree = {}
        self.K_dict_tree = 0
        self.row_ChkBt = 0

        self.w_var = w_var
        self.reset = reset

        self.save_clicked = False

        self.in_edit = False

        self.window = window


        # La variable qui va avoir sa valeur assignée lorsqu'une instance de "IntfActSelector" sera créée contiendra cette instance de "IntfActSelector". 
        # Elle me permettra d'avoir accès au dictionnaire contenant toutes les instances des actions "act_dict", à "start" pour lancer 
        # l'exécution du programme. La liste qui permet d'enregistrer la liste d'actions "save_list"...
        # ------------------------------------------------------------------------------------------------------------------------------------------
        # The variable that will have its value assigned when an instance of "IntfActSelector" is created will contain this instance of "IntfActSelector". 
        # It will allow me to access the dictionary containing all the instances of the actions "act_dict" .
        # to "start" for launching the program execution. The list that allows saving the list of actions is save_list...
        self.ui_act_manager = None
        self.container_manager = None





        # Création de l'interface.
        # ------------------------
        # Interface creation.




        # Bouton permettant d’accéder à l'interface de "IntfTree".
        # --------------------------------------------------
        # Button to access the "IntfTree" interface.
        tree_bt = tk.Button(menu_bt_frame, 
                            text="tree", 
                            bg=w_var.color_2, 
                            fg=w_var.color_3, 
                            height=1, 
                            width=5, 
                            font=w_var.font_size, 
                            command=lambda : frame_exchanger(self.tree_main_frame)
                            )
        tree_bt.grid(row=0, column=1)



        # Frame principale de "IntfTree".
        # -------------------------
        # Main frame of "IntfTree".
        self.tree_main_frame = tk.Frame(window, bg=w_var.color_1, width=320, height=450)
        self.tree_main_frame.grid_propagate(False)



        # Frame contenant tout ce qui concerne l'arbre d'actions, sauf pour la modification où cette frame 
        # sera remplacée par une autre, "edit_tree_frame", qui permettra de modifier la suite d'actions.
        # --------------------------------------------------------------------------------------------------
        # Frame containing everything related to the action tree, except for modifications where this frame 
        # will be replaced by another one, "edit_tree_frame", which will allow modifying the sequence of actions.
        self.tree_frame = tk.Frame(self.tree_main_frame, bg=w_var.color_1, width=320, height=450)
        self.tree_frame.grid(row=0, column=0)

        self.edit_tree_frame = tk.Frame(self.tree_main_frame, bg=w_var.color_1, width=320, height=450)

        self.edit_act_frame = tk.Frame(self.tree_main_frame, bg=w_var.color_1, width=320, height=450)







        self.var_case_wait = tk.IntVar(value=0)

        self.ckbt_wait = tk.Checkbutton(self.tree_frame, text="temps datente entre chaque action", variable=self.var_case_wait, bg=self.w_var.color_1, command=self.wait_frame_look)
        self.ckbt_wait.grid(row=0, column=0)

        self.error_label_wait = tk.Label(self.tree_frame, 
                            text='error', 
                            bg=w_var.color_1, 
                            fg=w_var.color_3, 
                            height=1, 
                            width=33, 
                            font=w_var.font_size_error
                            )

        self.arranger_wait_frm = tk.Frame(self.tree_frame, bg=w_var.color_1)


        
        self.text_zone_wait = tk.Entry(self.arranger_wait_frm, 
                                    width=8, 
                                    bg=w_var.color_2, 
                                    font=w_var.font_size
                                    )
        self.text_zone_wait.grid(row=1, column=0)
        
        self.info_label = tk.Label(self.arranger_wait_frm, 
                                   text="milliseconds", 
                                   bg=w_var.color_1, 
                                   fg=w_var.color_3, 
                                   height=1, 
                                   width=9, 
                                   font=w_var.font_size
                                   )
        self.info_label.grid(row=1, column=1)

        self.start_bt = tk.Button(self.arranger_wait_frm, 
                        text="valider", 
                        bg=w_var.color_2, 
                        fg=w_var.color_3, 
                        height=1, 
                        width=6, 
                        font=w_var.font_size, 
                        command=self.check_wait_act
                        )
        self.start_bt.grid(row=1, column=2, padx=10)




        # Menu scrolable contenant toutes les action sous forme de "Checkbutton".
        # -----------------------------------------------------------------------
        # Scrollable menu containing all actions in the form of "Checkbutton".
        self.all_actions = ScrollableFrame(self.tree_frame)
        self.all_actions.grid(row=3, column=0, padx=30, pady=10)



        # Frame pour organiser les boutons, les champs de saisie, etc.
        # ------------------------------------------------------------
        # Frame to organize the buttons, entry, etc.
        self.arranger_bt_1 = tk.Frame(self.tree_frame, bg=w_var.color_1)
        self.arranger_bt_1.grid(row=4, column=0)



        # Bouton pour démarrer l'exécution des actions.
        # ---------------------------------------------
        # Button to start the execution of actions.
        self.start_bt = tk.Button(self.arranger_bt_1, 
                        text="start", 
                        bg=w_var.color_2, 
                        fg=w_var.color_3, 
                        height=1, 
                        width=6, 
                        font=w_var.font_size, 
                        command=lambda : self.ui_act_manager.act_dict_manager.start(False)
                        )
        self.start_bt.grid(row=0, column=0)



        # Bouton permettant d'appeler une fonction lorsqu'il est cliqué, 
        # afin d'afficher les widgets nécessaires à l'enregistrement de la suite d'actions.
        # ---------------------------------------------------------------------------------------------------------------
        # Button that calls a function when clicked, to display the necessary widgets for saving the sequence of actions.
        self.save_bt = tk.Button(self.arranger_bt_1, 
                        text="save", 
                        bg=w_var.color_2, 
                        fg=w_var.color_3, 
                        height=1, 
                        width=5, 
                        font=w_var.font_size, 
                        command=self.upd_save_wdgt
                        )
        self.save_bt.grid(row=0, column=1)

        # Bouton appelant "reset" pour réinitialiser les valeurs comme si l'on venait de démarrer le programme.
        # ----------------------------------------------------------------------------------------------------------
        # Button calling "reset" to reset the values as if the program had just been started.
        self.reset_bt = tk.Button(self.arranger_bt_1, 
                        text="reset", 
                        bg=w_var.color_2, 
                        fg=w_var.color_3, 
                        height=1, 
                        width=6, 
                        font=w_var.font_size, 
                        command=self.reset
                        )
        self.reset_bt.grid(row=0, column=2)



        # Frame contenant tous les widgets nécessaires à l'enregistrement de la suite d'actions : un label pour les explications, 
        # un champ de saisie pour le nom du fichier, un label pour les erreurs, 
        # et un bouton de validation qui appelle la fonction "save" pour enregistrer.
        # ------------------------------------------------------------------------------------------------------------------------
        #Frame containing all the widgets necessary for saving the sequence of actions: a label for explanations, 
        # an entry for the file name, a label for errors, and a validation button that calls the "save" function to save.
        self.save_fram = tk.Frame(self.tree_frame, bg=w_var.color_1)

        self.info_label = tk.Label(self.save_fram, 
                            text='Put your file name:', 
                            bg=w_var.color_1, 
                            fg=w_var.color_3, 
                            height=1, 
                            width=20, 
                            font=w_var.font_size
                            )
        self.info_label.grid(row=0, column=0)
        
        self.name_entry  = tk.Entry(self.save_fram, 
                                width=15, 
                                bg=w_var.color_2, 
                                font=w_var.font_size
                                )
        self.name_entry.grid(row=1, column=0)
        
        self.error_label = tk.Label(self.save_fram, 
                            text='error', 
                            bg=w_var.color_1, 
                            fg=w_var.color_3, 
                            height=2, 
                            width=35, 
                            font=w_var.font_size_error
                            )
        
        self.validate = tk.Button(self.save_fram, 
                        text="validate", 
                        bg=w_var.color_2, 
                        fg=w_var.color_3, 
                        height=1, 
                        width=8, 
                        font=w_var.font_size, 
                        command=self.call_save
                        )
        self.validate.grid(row=3, column=0)






        # Bouton appelant "edit" pour permettre la modification de la suite d'actions.
        # ---------------------------------------------------------------------------------
        # Button calling "edit" to allow modification of the sequence of actions.
        self.edit_bt = tk.Button(self.tree_frame, 
                        text="edit", 
                        bg=w_var.color_2, 
                        fg=w_var.color_3, 
                        height=1, 
                        width=5, 
                        font=w_var.font_size, 
                        command=self.preparing_edit
                        )
        self.edit_bt.grid(row=6, column=0)







        # Menu scrolable qui contiendra toutes les actions sous forme de "Radiobutton". Lorsque l'utilisateur cliquera sur "Edit", 
        # cela lui permettra de choisir une action et de la modifier ou de la supprimer.
        # ------------------------------------------------------------------------------------------------------------------------
        # Scrollable menu that will contain all actions in the form of "Radiobutton". 
        # When the user clicks on "Edit", they will be able to choose an action and modify or delete it.
        self.all_actions_edit = ScrollableFrame(self.edit_tree_frame)
        self.all_actions_edit.grid(row=0, column=0, padx=30, pady=10)

        self.arranger_bt_2 = tk.Frame(self.edit_tree_frame, bg=w_var.color_1)
        self.arranger_bt_2.grid(row=1, column=0)

        self.delet_bt = tk.Button(self.arranger_bt_2, 
                        text="delete", 
                        bg=w_var.color_2, 
                        fg=w_var.color_3, 
                        height=1, 
                        width=5, 
                        font=w_var.font_size, 
                        command=self.call_delet_act_user_choice
                        )
        self.delet_bt.grid(row=0, column=0)



        self.edit_act_bt = tk.Button(self.arranger_bt_2, 
                        text="edit", 
                        bg=w_var.color_2, 
                        fg=w_var.color_3, 
                        height=1, 
                        width=5, 
                        font=w_var.font_size, 
                        command=self.edit_act
                        )
        self.edit_act_bt.grid(row=0, column=1)




        self.quit_edit = tk.Button(self.arranger_bt_2, 
                        text="left", 
                        bg=w_var.color_2, 
                        fg=w_var.color_3, 
                        height=1, 
                        width=5, 
                        font=w_var.font_size, 
                        command=self.quit
                        )
        self.quit_edit.grid(row=0, column=2)

        self.frame_click = tk.Frame(self.edit_act_frame, bg=self.w_var.color_1)
        self.frame_move = tk.Frame(self.edit_act_frame, bg=self.w_var.color_1)
        self.frame_write = tk.Frame(self.edit_act_frame, bg=self.w_var.color_1)
        self.frame_scroll = tk.Frame(self.edit_act_frame, bg=self.w_var.color_1)
        self.frame_wait = tk.Frame(self.edit_act_frame, bg=self.w_var.color_1)
        self.frame_pressed = tk.Frame(self.edit_act_frame, bg=self.w_var.color_1)
        self.frame_same_time = tk.Frame(self.edit_act_frame, bg=self.w_var.color_1)
        self.frame_loop = tk.Frame(self.edit_act_frame, bg=self.w_var.color_1)

        self.validate_button_edit = tk.Button(self.edit_act_frame, 
                        text="validate", 
                        bg=w_var.color_2, 
                        fg=w_var.color_3, 
                        height=1, 
                        width=5, 
                        font=w_var.font_size, 
                        command=self.validate_edit
                        )


    def wait_frame_look(self):
        if self.var_case_wait.get() == 1:
            self.arranger_wait_frm.grid(row=1, column=0)
        else:
            self.ui_act_manager.act_dict_manager.sleep_act_time = 0
            self.arranger_wait_frm.grid_remove()




    def check_wait_act(self):
        time = self.text_zone_wait.get()
        try:
            time = int(time.replace(" ", ""))
            if time <= 0:
                self.error_label_wait.config(text="the time you entered is incorrect")
                self.error_label_wait.grid(row=2, column=0)
            
            elif time > 3600000:# 3600000 milliseconds = 1h
                self.error_label_wait.config(text="the time you have entered is too long")
                self.error_label_wait.grid(row=2, column=0)
            
            else: 
                self.error_label_wait.grid_remove()
                self.ui_act_manager.act_dict_manager.sleep_act_time = time
            
        except ValueError:
            self.error_label_wait.config(text="the time you entered is incorrect")
            self.error_label_wait.grid(row=2, column=0)
        





















    def frame_act(self):
        self.move_inst = MouseMoveFrame(self.frame_move, self.w_var)
        self.click_inst = ClickFrame(self.frame_click, self.w_var)
        self.write_inst = WriteFrame(self.frame_write, self.w_var)
        self.scroll_inst = ScrollFrame(self.frame_scroll, self.w_var)
        self.wait_inst = WaitFrame(self.frame_wait, self.w_var)
        self.pressed_inst = KeyHoldFrame(self.frame_pressed, self.w_var)
        self.same_time_inst = ParallelActionsFrame(self.frame_same_time, self.w_var, self.container_manager)
        self.loop_inst = LoopFrame(self.frame_loop, self.w_var, self.container_manager)


 



    def preparing_edit(self):
        # Je vérifie que la liste d'actions n'est pas vide.
        # -------------------------------------------------
        # I check that the list of actions is not empty.
        if not len(self.dict_tree) == 0:
            self.in_edit = True


            # Je cache la frame "tree_frame" et la remplace par la frame "edit_tree_frame", qui permettra d'éditer la suite d'actions.
            # -----------------------------------------------------------------------------------------------------------------------
            # I hide the "tree_frame" and replace it with the "edit_tree_frame", which will allow editing the sequence of actions.
            self.tree_frame.grid_remove()
            self.edit_tree_frame.grid(row=0, column=0)




            # Je crée les variables nécessaires à la modification de la suite d'actions, dont "dict_edit" (un dictionnaire), 
            # qui va contenir différents éléments (actions) avec pour clés leur position dans la grille ("row_RdBt"). 
            # Les éléments contenus dans le dictionnaire sont :
            #
            # -Position : Elle est déterminée en fonction du conteneur ("Loop"/"SameTime") dans lequel l'élément se trouve. Par exemple, 
            # si c'est le 2ème élément dans une boucle, la valeur sera 1.
            # -Instance : L'instance qui réalise l'action.
            # -Radiobutton : Le "Radiobutton" associé à l'action.
            # -Booléen : Un booléen indiquant si l'élément se trouve dans un conteneur ("Loop"/"SameTime") ou non (si oui, la valeur sera True).
            # -Instance du conteneur : L'instance du conteneur dans lequel l'action se trouve. Si l'action n'est pas dans un conteneur, la valeur sera None.
            # -Nombre de conteneurs ("num_containers"): Si l'action est une instance de "Loop" ou "SameTime", cette clé contiendra le nombre de conteneurs, 
            # y compris celui-ci. Sinon, la valeur est None.
            # -Niveau d'imbrication : Un nombre représentant le niveau d'imbrication des conteneurs. Par exemple, 
            # si une boucle est à l'intérieur d'une autre boucle, les éléments dans la boucle la plus imbriquée auront une valeur de 2.
            #-----------------------------------------------------------------------------------------------------------------------------------------------------
            # I create the variables necessary for modifying the sequence of actions, including "dict_edit" (a dictionary), 
            # which will contain different elements (actions) with their grid position as keys ("row_RdBt"). 
            # The elements contained in the dictionary are:
            #
            # -Position: It is determined based on the container ("Loop"/"SameTime") in which the element is located. For example, 
            # if it is the 2nd element in a loop, the value will be 1.
            # -Instance: The instance that performs the action.
            # -Radiobutton: The "Radiobutton" associated with the action.
            # -Boolean: A boolean indicating whether the element is in a container ("Loop"/"SameTime") or not (if yes, the value will be True).
            # -Container instance: The instance of the container in which the action is located. If the action is not in a container, the value will be None.
            # -Number of containers ("num_containers"): If the action is an instance of "Loop" or "SameTime", this key will contain the number of containers, 
            # including the current one. Otherwise, the value is None.
            # -Nesting level: A number representing the level of nesting of containers. For example, if a loop is inside another loop, 
            # the elements in the innermost loop will have a value of 2.
            self.dict_edit = {}
            self.row_RdBt = 0
            self.num_containers = 0
            # Variable contenant le "Radiobutton" choisi par l'utilisateur.
            # -------------------------------------------------------------
            # Variable containing the "Radiobutton" chosen by the user.
            self.choice_RdBt = tk.IntVar(value=0)

            # Je trie le dictionnaire pour être sûr qu'il n'y a pas de bugs.
            # --------------------------------------------------------------
            # I sort the dictionary to ensure there are no bugs.
            self.ui_act_manager.act_dict_manager.act_dict = {clé: self.ui_act_manager.act_dict_manager.act_dict[clé] for clé in sorted(self.ui_act_manager.act_dict_manager.act_dict)}

            for container_index, inst_act in self.ui_act_manager.act_dict_manager.act_dict.items():

                
                # Je crée le "Radiobutton" que l'utilisateur pourra sélectionner pour modifier l'action qui lui est associée ou la supprimer.
                # ---------------------------------------------------------------------------------------------------------------------------
                # I create the "Radiobutton" that the user can select to modify the associated action or delete it.
                RdBt_edit = tk.Radiobutton(self.all_actions_edit.scrollable_frame, text=inst_act.text(), variable=self.choice_RdBt, value=self.row_RdBt, background=self.w_var.color_1)
                RdBt_edit.grid(row=self.row_RdBt, column=0, sticky="nw")

                # Si l'action est un conteneur (Loop/SameTime), on ajoute toutes les caractéristiques au dictionnaire 
                # "dict_edit". On incrémente "num_loops" et "row_RdBt", puis on appelle "explore_container", 
                # qui prend le conteneur en paramètre ainsi qu'un nombre représentant l'incrémentation. 
                # Cette fonction va faire la même chose que cette boucle for, mais avec un conteneur. 
                # Sinon, on ajoute simplement toutes ses caractéristiques au dictionnaire "dict_edit" et on incrémente "row_RdBt".
                # ----------------------------------------------------------------------------------------------------------------------------
                # If the action is a container (Loop/SameTime), all its characteristics are added to the dictionary "dict_edit". 
                # We increment "num_loops" and "row_RdBt", then call "explore_container", which takes the container as a parameter 
                # along with a number representing the increment. This function will do the same thing as this for loop, but with a container. 
                # Otherwise, we simply add all its characteristics to the dictionary "dict_edit" and increment "row_RdBt".
                if isinstance(inst_act, Loop) or isinstance(inst_act, SameTime):

                    self.dict_edit[self.row_RdBt] = [container_index, inst_act, RdBt_edit, False, None, self.num_containers, 0]
                    self.row_RdBt += 1
                    self.num_containers += 1
                    self.explore_container(inst_act, 1)
                
                else:
                    self.dict_edit[self.row_RdBt] = [container_index, inst_act, RdBt_edit, False, None, None, 0]
                    self.row_RdBt += 1






    def explore_container(self, inst_container, the_padding):
        """
        Cette fonction prend une instance d'un conteneur (Loop/SameTime) et un nombre représentant le niveau d'incrémentation de l'instance. 
        Elle va parcourir act_dict_CNTR de l'instance, qui contient toutes les actions, et pour chaque action,  elle va créer un "Radiobutton" 
        et l'ajouter au dictionnaire "dict_edit" avec toutes les caractéristiques nécessaires pour la modification 
        de la suite d'actions. Si elle trouve un conteneur (Loop/SameTime) Dans l'instance donnée en paramètre, elle va s'appeler elle-même.
        ----------------------------------------------------------------------------------------------------------------------------------------
        This function takes an instance of a container (Loop/SameTime) and a number representing the increment level of the instance. 
        It will iterate through act_dict_CNTR of the instance, which contains all the actions, and for each action, it will create a 'Radiobutton' 
        and add it to the "dict_edit" dictionary with all the necessary characteristics for modifying the sequence of actions. 
        If it finds a container (Loop/SameTime) in the instance passed as a parameter, it will call itself.
        """

        # Je trie le dictionnaire pour être sûr qu'il n'y a pas de bugs.
        # --------------------------------------------------------------
        # I sort the dictionary to ensure there are no bugs.
        inst_container.act_dict_CNTR = {clé: inst_container.act_dict_CNTR[clé] for clé in sorted(inst_container.act_dict_CNTR)}

        for container_index, inst_act in inst_container.act_dict_CNTR.items():

            # Je crée le "Radiobutton" que l'utilisateur pourra sélectionner pour modifier l'action qui lui est associée ou la supprimer. 
            # Mais cette fois, je lui ajoute un "padx" pour que l'utilisateur puisse discerner qu'il est dans une boucle.
            # ---------------------------------------------------------------------------------------------------------------------------
            # I create the "Radiobutton" that the user can select to modify the associated action or delete it. But this time, 
            # I add a padx so that the user can discern that it is within a loop.
            RdBt_edit = tk.Radiobutton(self.all_actions_edit.scrollable_frame, text=inst_act.text(), variable=self.choice_RdBt, value=self.row_RdBt, background="#71B0B0")
            RdBt_edit.grid(row=self.row_RdBt, column=0, sticky="nw", padx=the_padding*10)



            # Si l'action est un conteneur (Loop/SameTime), on ajoute toutes les caractéristiques au dictionnaire 
            # "dict_edit". On incrémente "num_loops" et "row_RdBt", puis on appelle "explore_container", 
            # qui prend le conteneur en paramètre ainsi qu'un nombre représentant l'incrémentation. 
            # Cette fonction va faire la même chose que cette boucle for, mais avec un conteneur. 
            # Sinon, on ajoute simplement toutes ses caractéristiques au dictionnaire "dict_edit" et on incrémente "row_RdBt".
            # ----------------------------------------------------------------------------------------------------------------------------
            # If the action is a container (Loop/SameTime), all its characteristics are added to the dictionary "dict_edit". 
            # We increment "num_loops" and "row_RdBt", then call "explore_container", which takes the container as a parameter 
            # along with a number representing the increment. This function will do the same thing as this for loop, but with a container. 
            # Otherwise, we simply add all its characteristics to the dictionary "dict_edit" and increment "row_RdBt".
            if isinstance(inst_act, Loop) or isinstance(inst_act, SameTime):
                self.dict_edit[self.row_RdBt] = [container_index, inst_act, RdBt_edit, True, inst_container, self.num_containers, the_padding]
                self.row_RdBt += 1
                self.num_containers += 1
                self.explore_container(inst_act, the_padding+1)

            else:
                self.dict_edit[self.row_RdBt] = [container_index, inst_act, RdBt_edit, True, inst_container, None, the_padding]
                self.row_RdBt += 1






    def dict_edit_sort(self, element_K_del):
        """
        Cette fonction permet que, lorsqu'un élément de "dict_edit" est supprimé, peu importe où il se trouvait, 
        le dictionnaire soit modifié de sorte qu'on ait l'impression que cet élément n'a jamais existé. 
        Cette fonction prend la clé de l'élément supprimé et modifie "dict_edit" en ajustant les éléments qui suivent celui supprimé : 
        les clés, ainsi que le premier élément de la liste associée à la clé, si nécessaire.
        -----------------------------------------------------------------------------------------------------------------------------------
        This function ensures that when an element of "dict_edit" is deleted, regardless of its position, 
        the dictionary is modified so that it appears as if the element never existed. This function takes the key of the deleted element 
        and modifies "dict_edit" by adjusting the elements that follow the deleted one: 
        the keys, as well as the first element of the list associated with the key, if necessary.
        """

        # Je trie le dictionnaire pour être sûr qu'il n'y a pas de bugs.
        # --------------------------------------------------------------
        # I sort the dictionary to ensure there are no bugs.
        self.dict_edit = {key: self.dict_edit[key] for key in sorted(self.dict_edit)}


        # Je crée un dictionnaire "similar_dict" qui va me permettre de modifier "dict_edit".
        # Pour modifier "dict_edit", je vais le parcourir et, si l'élément se trouve avant l'élément qui a été supprimer, 
        # on ne le change pas. Sinon, on va changer sa clé, l'afficher à la bonne place et, si nécessaire, 
        # modifier sa première valeur "container_index".
        # ---------------------------------------------------------------------------------------------------------------------------------------
        # I am creating a dictionary called "similar_dict" which will allow me to modify "dict_edit".
        # To modify "dict_edit", I will iterate through it, and if the element is found before the one that was deleted, we don't change it.
        # Otherwise, we will change its key, display it in the correct position, and, if necessary, modify its first value "container_index".
        similar_dict = {}
        for row, element in self.dict_edit.items() :
            if row > element_K_del:
                element[2].grid_remove()
                element[2].config(value=row-1)
                element[2].grid(row=row-1, column=0, sticky="nw", padx=element[6]*10)

                # Si "container_index" vaut 0, on ne la modifie pas, car cette valeur ne peut pas être négative.
                # ----------------------------------------------------------------------------------------------
                # If "container_index" is 0, we don't modify it, because this value cannot be negative.
                if element[0] != 0:

                    # Si le dictionnaire est vide, on met forcément "container_index" à 0 car, dans la condition précédente, 
                    # on a vérifié qu'il ne valait pas 0. Cela signifie que si le dictionnaire est vide, l'action précédente était 
                    # la première d'une série d'actions et qu'elle a été supprimée. Donc, on met "container_index" à 0.
                    # -----------------------------------------------------------------------------------------------------------------
                    # If the dictionary is empty, we must set "container_index" to 0 because, in the previous condition, 
                    # we verified that it was not 0. This means that if the dictionary is empty, the previous action was the first in a 
                    # series of actions and it was deleted. Therefore, we set "container_index" to 0.
                    if len(similar_dict) > 0:

                        # Si l'action d'avant n'est pas dans le même conteneur que nous, cela signifie que la valeur 
                        # "container_index" de l'action précédente n'a aucun rapport avec notre "container_index". 
                        # ------------------------------------------------------------------------------------------
                        # If the previous action is not in the same container as us, it means that the 
                        # "container_index" value of the previous action has no relation to our "container_index".
                        if element[4] == list(similar_dict[row-2])[4]:

                            # On vérifie s'il y a un décalage entre notre "container_index" et celui de l'action précédente. 
                            # Si c'est le cas, on enlève 1 à notre "container_index".
                            # ----------------------------------------------------------------------------------------------
                            # We check if there is a discrepancy between our "container_index" and the previous 
                            # action's "container_index". If so, we subtract 1 from our "container_index".
                            if list(similar_dict[row-2])[0] < element[0]-1:
                                element[0] -= 1


                        else:
                            # On vérifie si l'action précédente est un conteneur. Si c'est le cas, on met "container_index" à 0, 
                            # car cela signifie que nous sommes le premier élément de ce conteneur.
                            # --------------------------------------------------------------------------------------------------
                            # We check if the previous action is a container. If so, we set "container_index" to 0, 
                            # as this means we are the first element in that container.
                            if isinstance(list(similar_dict[row-2])[1], Loop) or isinstance(list(similar_dict[row-2])[1], SameTime):
                                element[0] = 0

                            else:
                                # On va parcourir le "similar_dict" à l'envers jusqu'à trouver la dernière action qui est dans le même conteneur que 
                                # nous et qui ne doit pas être nous. Ensuite, on regarde si "container_index" a un décalage avec le "container_index" 
                                # de la dernière action dans le même conteneur que nous.
                                # Par exemple, si nous valons 5 et que l'autre "container_index" vaut 3, il y a un décalage. Dans ce cas, nous enlevons 1 à 5.
                                # ----------------------------------------------------------------------------------------------------------------------------
                                # We will iterate through the "similar_dict" in reverse until we find the last action that is in the same container as 
                                # us and is not us. Then, we check if there is a discrepancy between our "container_index" and the "container_index" 
                                # of the last action in the same container as us.For example, if our value is 5 and the other "container_index" is 3, 
                                # there is a discrepancy. In that case, we subtract 1 from 5.
                                for key, valeur in reversed(list(similar_dict.items())):
                                    if element[4] == valeur[4]:
                                        if  key < row-1:
                                            if valeur[0] == element[0]-2 :
                                                element[0] -= 1
                                            break
                    else:
                        element[0] = 0

                # On change sa clé car elle se trouve après l'élément supprimé.
                # ------------------------------------------------------------------
                # We change its key because it is located after the deleted element.
                similar_dict[row-1] = element


            else:
                # Je réaffiche pour éviter les bugs et j'ajoute l'élément à "similar_dict".
                # -------------------------------------------------------------------------
                # I re-display to avoid bugs and add the element to "similar_dict".
                element[2].grid_remove()
                element[2].grid(row=row, column=0, sticky="nw")
                similar_dict[row] = element


        self.dict_edit = dict(similar_dict)






    def index_save(self, bad_nb):
        """
        Cette fonction retourne l'index réel d'une action dans "save_list", car celle-ci comporte des éléments non présents dans "dict_edit".
        Ces éléments non présents dans "dict_edit" sont tous des "left_container", et ils permettent à la fonction d'ouverture 
        d'une suite d'actions enregistrées précédemment de savoir quand elle doit quitter un conteneur.
        Dans cette fonction, nous allons parcourir "save_list" jusqu'à l'index donné, et chaque fois qu'il y a un "left_container", 
        nous allons avancer de 1 supplémentaire jusqu'à obtenir le bon index.
        -------------------------------------------------------------------------------------------------------------------------------------
        This function returns the real index of an action in "save_list" because it contains elements not present in "dict_edit".
        These elements not present in "dict_edit" are all "left_container", and they allow the function that opens a sequence of previously 
        recorded actions to know when it should exit a container.
        In this function, we will iterate through "save_list" until the given index, and each time there is a "left_container", 
        we will advance by 1 more until we reach the correct index.
        """

        real_index_save = bad_nb
        i = 0
        while True:
            if list(self.ui_act_manager.act_dict_manager.save_list[i])[0] == "left_container":
                real_index_save+=1
            if i >= real_index_save:
                break
            i += 1
        return real_index_save






    def sort_dict(self, the_dict, element_K_del):
        """
        Cette fonction modifie le dictionnaire donné en paramètre. Ce dictionnaire doit avoir des clés numérotées 
        à partir de 0, augmentant de 1 en 1, et doit avoir eu un élément qui a été supprimé. Cette fonction va alors 
        modifier les clés du dictionnaire de sorte qu'il n'y ait pas de décalage. Pour cela, elle va parcourir ce 
        dictionnaire et, lorsque qu'un élément se trouve après l'élément supprimé (dont on connaît la clé car elle 
        a été passée en paramètre), on va soustraire 1 à cette clé et retourner ce nouveau dictionnaire.
        --------------------------------------------------------------------------------------------------------------------
        This function modifies the dictionary given as a parameter. This dictionary must have keys numbered starting from 0, 
        increasing by 1, and must have had an element that was deleted. This function will then modify the dictionary's keys 
        so that there is no gap. To achieve this, it will iterate through the dictionary and, when an element is found 
        after the deleted one (whose key is known because it was passed as a parameter), 1 will be subtracted from that key and 
        return this new dictionary.
        """

        similar_dict = {}
        for key, element in the_dict.items() :
            if key > element_K_del:
                similar_dict[key-1] = element
            else:
                similar_dict[key] = element
        return similar_dict






    def del_left_container(self, nb):
        """
        Cette fonction permet de supprimer un élément "left_container" de "save_list". Si l'élément que l'on supprime est une boucle, 
        on donne l'index du conteneur, et la fonction va parcourir tous les éléments après cette boucle et supprimer le premier 
        "left_container" qu'elle trouvera.
        -----------------------------------------------------------------------------------------------------------------------------
        This function allows the removal of a "left_container" element from "save_list". If the element being removed is a loop, 
        the container index is provided, and the function will iterate through all the elements after that loop and 
        delete the first "left_container" it finds.
        """

        the_nb = nb
        for il_nb, element in enumerate(self.ui_act_manager.act_dict_manager.save_list[the_nb:]):
            if element[0] == "left_container":
                del self.ui_act_manager.act_dict_manager.save_list[il_nb+the_nb]
                break






    def call_delet_act_user_choice(self):
        """
        Cette fonction appelle "delet_act" en lui fournissant tous les paramètres nécessaires à la suppression de 
        l'élément choisi par l'utilisateur.
        ---------------------------------------------------------------------------------------------------------
        This function calls "delet_act", providing it with all the necessary parameters for the deletion of 
        the element selected by the user.
        """
        if not len(self.dict_edit) == 0:
            user_choice = self.choice_RdBt.get()
            info_act = self.dict_edit[user_choice]

            self.delet_act(info_act[0], info_act[1], info_act[2], info_act[3], info_act[4], info_act[5], user_choice)
        else:
            self.quit()






    def call_delet_act(self, index_element):
        """
        Cette fonction appelle "delet_act" en lui fournissant tous les paramètres nécessaires à la suppression d'un élément, 
        non pas choisi par l'utilisateur, mais par une fonction. Par exemple, la fonction va appeler "call_delet_act" 
        pour supprimer les éléments d'un conteneur si l'utilisateur a voulu supprimer le conteneur.
        --------------------------------------------------------------------------------------------------------------------
        This function calls "delet_act", providing it with all the necessary parameters for the deletion of an element, 
        not chosen by the user, but by a function. For example, the function will call "call_delet_" to delete the 
        elements of a container if the user wanted to delete the container.
        """
        if not len(self.dict_edit) == 0:
            info_act = self.dict_edit[index_element]
            self.delet_act(info_act[0], info_act[1], info_act[2], info_act[3], info_act[4], info_act[5], index_element)






    def delet_act(self, container_index, element, choix_open, i_am_in_CNTR, inst_, number_container, user_choice):

        second_element = lambda the_list: the_list[1]

        if isinstance(element, Loop) or isinstance(element, SameTime):

            # Je parcours tous les éléments du conteneur dans "dict_edit" et j'appelle "call_delet_act" en passant toujours 
            # le même index, car après la suppression d'un élément, le dictionnaire est modifié afin d'éviter tout décalage. 
            # "call_delet_act" appelle ensuite "delet_act". Lorsque qu'un élément n'est pas dans notre conteneur, 
            # cela signifie forcément la fin, car il est impossible d'avoir un autre conteneur à l'intérieur du nôtre, 
            # car ils ont été supprimés.
            # --------------------------------------------------------------------------------------------------------------
            # I iterate through all the elements of the container in "dict_edit" and call "call_delet_act", 
            # always passing the same index, because after an element is removed, the dictionary is modified 
            # to prevent any misalignment. "call_delet_act" then calls "delet_act". When an element is not in our container, 
            # it necessarily means the end, as it is impossible to have another container inside ours since 
            # they have been deleted.
            for i in range(user_choice+1, len(self.dict_edit)):

                if user_choice <= len(self.dict_edit):
                    info_act = self.dict_edit[user_choice+1]

                    if info_act[4] == element:
                        self.call_delet_act(user_choice+1)

                    else:
                        break
                else:
                    break
            


            # On supprime l'élément "left_container" lié au conteneur dans "save_list".
            # -------------------------------------------------------------------------------
            # We delete the "left_container" element related to the container in "save_list".
            self.del_left_container(self.index_save(user_choice))


            # On vérifie si l'utilisateur a quitté le conteneur. S'il se trouve encore à l'intérieur, on le fait sortir.
            # ----------------------------------------------------------------------------------------------------------
            # We check if the user has left the container. If they are still inside, we remove them.
            if list(self.container_manager.container_map[number_container])[0]:
                self.container_manager.leave_current_container()


            # On enlève 1 au nombre de conteneurs car on en supprime un, puis on supprime l'élément lié au conteneur 
            # dans "container_map". Ensuite, on appelle "sort_dict" pour corriger le décalage causé par la 
            # suppression de élément lié au conteneur.
            # ------------------------------------------------------------------------------------------------------
            # We subtract 1 from the number of containers because we are deleting one, then we delete the element 
            # related to the container in "container_map". Next, we call "sort_dict" to fix the offset caused 
            # by the deletion of the element related to the container.
            del self.container_manager.container_map[number_container]
            self.container_manager.container_map = self.sort_dict(self.container_manager.container_map, number_container)

            # On supprime le nom du conteneur dans la liste du type de conteneur correspondant 
            # (liste contenant tous les noms des conteneurs du même type, permettant d'empêcher 
            # l'utilisateur de choisir deux fois le même nom).
            # ---------------------------------------------------------------------------------
            # We delete the container name from the list of the corresponding container type 
            # (a list containing all the names of containers of the same type, 
            # preventing the user from choosing the same name twice).
            try:
                self.container_manager.loop_names.remove(element.name)
            except ValueError:
                self.container_manager.parallel_action_names.remove(element.name)


        # Si l'élément est dans une boucle, on appelle "delete_inst_in_CNTR", qui supprime 
        # les éléments différemment de "delete_inst", car il se trouve dans un conteneur.
        # --------------------------------------------------------------------------------------
        # If the element is in a loop, we call "delete_inst_in_CNTR", which deletes the elements 
        # differently from "delete_inst", because it is inside a container.
        if i_am_in_CNTR:
            self.delet_inst_in_CNTR(inst_, container_index, second_element)

            
        else:
            self.delet_inst(container_index, second_element)
        
        # On supprime l'élément correspondant à l'action dans "save_list".
        # -----------------------------------------------------------------
        # We delete the element corresponding to the action in "save_list".
        del self.ui_act_manager.act_dict_manager.save_list[self.index_save(user_choice)]

        # On enlève 1 à "row_ChkBt", la valeur qui correspond aux lignes où sont affichés les "Checkbutton" des actions.
        # ------------------------------------------------------------------------------------------------------------------------
        # We subtract 1 from "row_ChkBt", the value that corresponds to the rows where the action "Checkbutton" are displayed.
        self.row_ChkBt -= 1

        # On supprime l'élément lié à l'action du dictionnaire "dict_edit", puis on détruit le "Radiobutton"
        # associé. Ensuite, la fonction "dict_edit_sort" va enlever le décalage dans "dict_edit" potentiellement 
        # causé par la suppression.
        # ------------------------------------------------------------------------------------------------------
        # We delete the element related to the action from the dictionary "dict_edit", then we destroy the 
        # associated "Radiobutton". Next, the function "dict_edit_sort" will remove the offset in "dict_edit" 
        # potentially caused by the deletion.
        del self.dict_edit[user_choice]
        choix_open.destroy()
        self.dict_edit_sort(user_choice)

        self.choice_RdBt.set(0)

##########################################################################################################################################################################
####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE##########
######FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE########
########FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE######
##########FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####FAKE####
##########################################################################################################################################################################

    def delet_inst(self, container_index, second_element):
        """
        Cette fonction va changer la valeur de "dict_K" qui permet de créer les clés de "act_dict", puis va supprimer 
        l'action de "act_dict". Ensuite, elle va, grâce à "sort_dict", corriger les décalages, puis s'occuper de l'arbre 
        des "Checkbutton". Elle enlèvera 1 à "K_dict_tree", supprimera le "Checkbutton" lié à l'action dans 
        "dict_tree" et appellera "sort_dict" pour enlever le décalage causé par la suppression.
        ----------------------------------------------------------------------------------------------------------------
        This function will change the value of "dict_K", which is used to create the keys in "act_dict", 
        then it will delete the action from "act_dict". Next, it will correct the offsets using "sort_dict", 
        then handle the "Checkbutton" tree. It will subtract 1 from "K_dict_tree", delete the "Checkbutton" related to 
        the action in "dict_tree", and call "sort_dict" to remove the offset caused by the deletion.
        """


        self.ui_act_manager.act_dict_manager.dict_K -= 1
        del self.ui_act_manager.act_dict_manager.act_dict[container_index]
        self.ui_act_manager.act_dict_manager.act_dict = self.sort_dict(self.ui_act_manager.act_dict_manager.act_dict, container_index)


        self.K_dict_tree -= 1
        second_element(self.dict_tree[container_index]).destroy()
        del self.dict_tree[container_index]
        self.sort_dict_tree(container_index)






    def delet_inst_in_CNTR(self, the_container, container_index, second_element):
        """
        Cette fonction va changer dans le conteneur la valeur de "act_K_CNTR", qui permet de créer les clés de "act_dict_CNTR", 
        puis va supprimer l'action de "act_dict_CNTR". Ensuite, elle va, grâce à "sort_dict", corriger les décalages, 
        puis s'occuper de l'arbre des "Checkbutton". Elle enlèvera 1 à "K_tree_CNTR", supprimera le "Checkbutton" 
        lié à l'action dans "dict_tree_CNTR" et appellera "sort_dict" pour enlever le décalage causé par la suppression.
        --------------------------------------------------------------------------------------------------------------------------
        This function will modify the value of "act_K_CNTR" in the container, which is used to create the keys in 
        "act_dict_CNTR", then it will delete the action from "act_dict_CNTR". Next, it will correct the offsets using "sort_dict", 
        then handle the "Checkbutton" tree. It will subtract 1 from "K_tree_CNTR", delete the "Checkbutton" related to 
        the action in "dict_tree_CNTR", and call "sort_dict" to remove the offset caused by the deletion.
        """

        the_container.act_K_CNTR -= 1
        del the_container.act_dict_CNTR[container_index]
        the_container.act_dict_CNTR = self.sort_dict(the_container.act_dict_CNTR, container_index)

        the_container.K_tree_CNTR -= 1
        second_element(the_container.dict_tree_CNTR[container_index]).destroy()
        del the_container.dict_tree_CNTR[container_index]
        the_container.dict_tree_CNTR = self.sort_dict(the_container.dict_tree_CNTR, container_index)






    def upd_save_wdgt(self):
        """
        Cette fonction permet d'afficher les widgets nécessaires ou de les effacer en fonction de "save_clicked".
        ---------------------------------------------------------------------------------------------------------
        This function allows displaying the necessary widgets or removing them based on "save_clicked".
        """
        
        if self.save_clicked:
            self.save_fram.grid_remove()
            self.save_clicked = False
        else:
            self.save_fram.grid(row=5, column=0)
            self.save_clicked = True






    def quit(self):
        """
        Cette fonction permet de quitter le menu de modification de la suite d'actions. Je commence par 
        détruire tous les "Radiobuttons", puis je cache la frame "edit_tree_frame". Ensuite, je réaffiche tous les 
        "Checkbuttons" à la bonne place et je réaffiche "tree_frame" pour remplacer "edit_tree_frame".
        ------------------------------------------------------------------------------------------------------
        This function allows you to exit the action sequence modification menu. I start by destroying all the 
        "Radiobuttons", then I hide the "edit_tree_frame". Next, I re-display all the "Checkbuttons" in the correct 
        position and I re-display "tree_frame" to replace "edit_tree_frame".
        """
        self.in_edit = False

        for edit_list in self.dict_edit.values():
            edit_list[2].destroy()
        self.edit_tree_frame.grid_remove()

        for index, ChkBt in self.dict_tree.items():
            ChkBt[1].grid_remove()
            ChkBt[1].grid(row=ChkBt[2], column=0)
        self.tree_frame.grid(row=0, column=0)





    def call_save(self):
        """
        Cette fonction permet d'enregistrer la suite d'actions. Elle va vérifier que le programme n'est pas en 
        cours d'exécution, puis appeler la fonction "save" qui vérifiera s'il n'y a pas de problèmes. Si tout est 
        en ordre, "save" va enregistrer la suite d'actions et on retirera les paramètres d'enregistrement. 
        Sinon, "save" renverra un message d'erreur, que l'on affichera.
        ---------------------------------------------------------------------------------------------------------
        This function allows saving the sequence of actions. It will check that the program is not currently 
        running, then call the "save" function, which will verify that there are no issues. If everything is in 
        order, "save" will save the sequence of actions, and we will remove the registration parameters. 
        Otherwise, "save" will return an error message, which we will display.
        """

        if not self.ui_act_manager.act_dict_manager.is_running:
            msg_error = save(self.name_entry.get(), self.ui_act_manager.act_dict_manager.save_list)
            if msg_error == True:
                self.upd_save_wdgt()
                self.error_label.grid_remove()
            else:
                self.error_label.config(text=msg_error[0], height=msg_error[1])
                self.error_label.grid(row=2, column=0)






    def add_tree(self, text):
        """
        Cette fonction permet d'ajouter une action à l'arbre des actions. On commence par créer le 
        "Checkbutton" correspondant à l'action et sa variable que l'on va ajouter au dictionnaire "dict_tree", 
        ce qui permettra de savoir, en fonction de si la case est cochée ou non, si l'action doit s'exécuter. 
        Ensuite, on incrémente "K_dict_tree" et "row_ChkBt".
        --------------------------------------------------------------------------------------------------------
        This function allows adding an action to the action tree. We start by creating the "Checkbutton" 
        corresponding to the action and its variable, which we will add to the "dict_tree" dictionary. This will 
        help determine, depending on whether the box is checked or not, if the action should execute. Then, 
        we increment "K_dict_tree" and "row_ChkBt".
        """

        var_case = tk.IntVar(value=1)
        case_a_cocher = tk.Checkbutton(self.all_actions.scrollable_frame, text=text, variable=var_case, bg=self.w_var.color_1)
        case_a_cocher.grid(row=self.row_ChkBt+1, column=0, sticky="wn")

        self.dict_tree[self.K_dict_tree] = [var_case, case_a_cocher, self.row_ChkBt+1]

        self.K_dict_tree += 1
        self.row_ChkBt += 1


























    def sort_dict_tree(self, element_K_del):
        """
        Cette fonction modifie le dictionnaire donné dict_tree
        --------------------------------------------------------------------------------------------------------------------
        Cette fonction modifie le dictionnaire donné dict_tree
        """

        similar_dict = {}
        for key, element in self.dict_tree.items() :
            if key > element_K_del:
                similar_dict[key-1] = [element[0], element[1], element[2]-1]
            else:
                similar_dict[key] = [element[0], element[1], element[2]]
        self.dict_tree = similar_dict











    def edit_act(self):
        self.validate_button_edit.grid(row=2, column=0)


        self.edit_tree_frame.grid_remove()
        self.edit_act_frame.grid(row=0, column=0)
        user_choice = self.choice_RdBt.get()

        print(self.dict_edit)
        element = list(self.dict_edit[user_choice])[1]


        
        if element.type_act() == "click l" or element.type_act() == "click r":
            self.click_inst.set_coordinate((element.pos_x, element.pos_y), "xy")
            self.frame_click.grid(row=0, column=0)####################
            
            
            self.tkt = KeyPoisiton(self.click_inst.set_coordinate, self.move_inst.set_coordinate)
            self.is_in_move_click = True
            self.update_positions()

        match element.type_act():

            case "move":
                self.move_inst.set_coordinate((element.pos_x, element.pos_y), "xy")
                self.move_inst.set_movement_type(element.movement_type)
                self.frame_move.grid(row=0, column=0)
                self.tkt = KeyPoisiton(self.click_inst.set_coordinate, self.move_inst.set_coordinate)

                self.is_in_move_click = True
                self.update_positions()


            case "write":
                self.write_inst.text_area.delete("1.0", tk.END)
                self.write_inst.text_area.insert("1.0", element.text_to_write)
                self.frame_write.grid(row=0, column=0)



            case "scroll":
                self.scroll_inst.select_direction(element.direction)
                self.scroll_inst.entry_steps.delete(0, tk.END)
                self.scroll_inst.entry_steps.insert(0, element.step)
                self.frame_scroll.grid(row=0, column=0)

            case "wait":
                self.wait_inst.entry_wait_duration.delete(0, tk.END)
                self.wait_inst.entry_wait_duration.insert(0, element.time_wait_s)

                self.frame_wait.grid(row=0, column=0)

            case "key press":
                for sp_key in list(self.pressed_inst._selected_special_keys):
                    self.pressed_inst.toggle_special_key(sp_key)

                for sp_key in element.list_sp_keys:
                    self.pressed_inst.toggle_special_key(sp_key)

                self.pressed_inst.entry_duration.delete(0, tk.END)
                self.pressed_inst.entry_duration.insert(0, element.time_wait_s)
                self.pressed_inst.entry_normal_keys.delete(0, tk.END)
                self.pressed_inst.entry_normal_keys.insert(0, element.keys)
                self.frame_pressed.grid(row=0, column=0)

            case "same time":
                for sp_key in list(self.pressed_inst._selected_special_keys):
                    self.same_time_inst.toggle_special_key(sp_key)
                
                for sp_key in element.list_sp_keys:
                    self.same_time_inst.toggle_special_key(sp_key)
                self.same_time_inst.entry_normal_keys.delete(0, tk.END)
                self.same_time_inst.entry_normal_keys.insert(0, element.keys)
                self.container_manager.parallel_action_names.remove(element.name)
                self.same_time_inst.name_entry.delete(0, tk.END)
                self.same_time_inst.name_entry.insert(0, element.name)
                self.frame_same_time.grid(row=0, column=0)

            case "loop":
                self.loop_inst.entry_nb_turns.delete(0, tk.END)
                self.loop_inst.entry_nb_turns.insert(0, element.nb_turns)
                self.container_manager.loop_names.remove(element.name)
                self.loop_inst.entry_loop_name.delete(0, tk.END)
                self.loop_inst.entry_loop_name.insert(0, element.name)
                self.frame_loop.grid(row=0, column=0)


###############################################################################################################################################################################""

    def validate_edit(self):

        user_choice = self.choice_RdBt.get()
        
        container_index, element, RdBt_edit, i_am_in_CNTR, inst_, number_container, padding = self.dict_edit[user_choice]

        index_element_in_save = self.index_save(user_choice)

        second_element = lambda the_list: the_list[1]





        if element.type_act() == "click l" or element.type_act() == "click r":
            args = self.click_inst.check()
            if args:
                element.pos_x = args[0]
                element.pos_y = args[1]
                if inst_ == None:
                    second_element(self.dict_tree[container_index]).config(text=element.text())
                else:
                    second_element(inst_.dict_tree_CNTR[container_index]).config(text=element.text())

                self.ui_act_manager.act_dict_manager.save_list[index_element_in_save] = [element.type_act(), args[0], args[1]]
                self.tkt.stop_listening()
                self.frame_click.grid_remove()
                self.is_in_move_click = False

        else:
            match element.type_act():

                case "move":
                    args = self.move_inst.check()
                    if args:
                        element.pos_x = args[0]
                        element.pos_y = args[1]
                        element.movement_type = args[2]
                        if inst_ == None:
                            second_element(self.dict_tree[container_index]).config(text=element.text())
                        else:
                            second_element(inst_.dict_tree_CNTR[container_index]).config(text=element.text())

                        self.ui_act_manager.act_dict_manager.save_list[index_element_in_save] = [element.type_act(), args[0], args[1], args[2]]
                        self.tkt.stop_listening()
                        self.frame_move.grid_remove()
                        self.is_in_move_click = False

                case "write":
                    args = self.write_inst.check()
                    if args:
                        element.text_to_write = args[0]

                        if inst_ == None:
                            second_element(self.dict_tree[container_index]).config(text=element.text())
                        else:
                            second_element(inst_.dict_tree_CNTR[container_index]).config(text=element.text())

                        self.ui_act_manager.act_dict_manager.save_list[index_element_in_save] = [element.type_act(), args[0]]

                        self.frame_write.grid_remove()



                case "scroll":
                    args = self.scroll_inst.check()
                    print(args)
                    if args:
                        element.step = args[0]
                        element.direction = args[1]
                        if inst_ == None:
                            second_element(self.dict_tree[container_index]).config(text=element.text())
                        else:
                            second_element(inst_.dict_tree_CNTR[container_index]).config(text=element.text())

                        self.ui_act_manager.act_dict_manager.save_list[index_element_in_save] = [element.type_act(), args[0], args[1]]

                        self.frame_scroll.grid_remove()


                case "wait":
                    args = self.wait_inst.check()
                    if args:
                        element.time_wait_s = args
                        element.time_wait_ms = int(args*1000)

                        
                        if inst_ == None:
                            second_element(self.dict_tree[container_index]).config(text=element.text())
                        else:
                            second_element(inst_.dict_tree_CNTR[container_index]).config(text=element.text())


                        self.ui_act_manager.act_dict_manager.save_list[index_element_in_save] = [element.type_act(), args]
                        self.frame_wait.grid_remove()






                case "key press":
                    args = self.pressed_inst.check()
                    if args:
                        element.keys = args[0]
                        element.list_sp_keys = args[1]
                        element.time_wait_ms = int(args[2]*1000)
                        element.time_wait_s = args[2]
                        
                        if inst_ == None:
                            second_element(self.dict_tree[container_index]).config(text=element.text())
                        else:
                            second_element(inst_.dict_tree_CNTR[container_index]).config(text=element.text())


                        self.ui_act_manager.act_dict_manager.save_list[index_element_in_save] = [element.type_act(), args[0], args[1], args[2]]

                        self.frame_pressed.grid_remove()





                case "same time":


                    args = self.same_time_inst.check()
                    if args:
                        
                        if list(self.container_manager.container_map[number_container])[0]:
                            self.container_manager.container_map[number_container] = [True, args[1]]
                            self.container_manager.indicate_container(args[1])
                        else:
                            self.container_manager.container_map[number_container] = [False, args[1]]

                        element.keys = args[0]
                        element.list_sp_keys = args[1]
                        element.name = args[2]
                        
                        if inst_ == None:
                            second_element(self.dict_tree[container_index]).config(text=element.text())
                        else:
                            second_element(inst_.dict_tree_CNTR[container_index]).config(text=element.text())

                        
                        self.ui_act_manager.act_dict_manager.save_list[index_element_in_save] = [element.type_act(), args[0], args[1], args[2]]
                        self.frame_same_time.grid_remove()




                case "loop":
                    args = self.loop_inst.check()
                    if args:
                        print(self.container_manager.loop_names)


                        if list(self.container_manager.container_map[number_container])[0]:
                            self.container_manager.container_map[number_container] = [True, args[1]]
                            self.container_manager.indicate_container(args[1])
                        else:
                            self.container_manager.container_map[number_container] = [False, args[1]]

                        element.nb_turns = args[0]
                        element.name = args[1]
                        
                        if inst_ == None:
                            second_element(self.dict_tree[container_index]).config(text=element.text())
                        else:
                            second_element(inst_.dict_tree_CNTR[container_index]).config(text=element.text())

                        self.ui_act_manager.act_dict_manager.save_list[index_element_in_save] = [element.type_act(), args[0], args[1]]



                        self.frame_loop.grid_remove()

        if args:
 
            RdBt_edit.config(text=element.text())
            self.validate_button_edit.grid_remove()
            self.edit_act_frame.grid_remove()
            self.edit_tree_frame.grid(row=0, column=0)





    def update_positions(self):
        self.click_inst.mouse_position_label.config(text=f"{position_mouse()[0]} | {position_mouse()[1]}")
        self.move_inst.mouse_position_label.config(text=f"{position_mouse()[0]} | {position_mouse()[1]}")
        if self.is_in_move_click:
            self.window.after(60, self.update_positions)















