# frame --> frm
# interface --> intf
# instance --> inst
# loop --> lp
# button --> btzyzy
# Checkbutton --> ChkBt
# Radiobutton --> RdBt
# action --> act
# key --> K
# update --> upd
# widgets --> wdgt
# container --> CNTR
# counter --> ctr
# position --> pos
# window --> w
# spetial_keys --> sp_keys
# choosing_key  -->  ch_key



from dataclasses import dataclass
import tkinter as tk


from ui_action_manager import IntfActSelector
from ui_action_tree import IntfTree
from ui_sequence_loader import SavedSequencesUI
from ui_documentation import DocumentationUI
from action_classes import Loop, SameTime, KeyLoggerApp, KeyPositon

from hotkey_manager import load_shortcuts
from enums import ShortCut

# Je crée la fenêtre.
# -------------------
# I create the window.
window = tk.Tk()
# Je définis les caractères de la fenêtre.
# ---------------------------------------
# I define the window characters.
window.title("hello wold")
window.geometry("320x480")
window.minsize(320, 480)
window.config(background="#71B0B0")


# Je crée un cadre pour contenir les boutons utilisés pour naviguer dans les différents menus.
# -------------------------------------------------------------------------------------------
# I create a frame to contain the buttons used to navigate the various menus.
menu_bt_frm = tk.Frame(window, bg="#FFB268")
menu_bt_frm.grid(row=0, column=0)



# Je crée une classe de données pour les valeurs très utilisées.
# -------------------------------------------------------------
# I create a dataclass for very used values.
@dataclass
class WindowVariable:
    font_size = ("Cooper Black", 11) # font for normal text
    font_size_error = ("Impact", 11) # font for error text

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_width = 320
    window_height = 480

    color_1 = "#71B0B0" # background color
    color_2 = "#FFB268" # button background color
    color_3 = "#000000" # text color
    color_4 = "#0039F5" # button alwready clicked color

w_var = WindowVariable()

all_shortcut = load_shortcuts()
KeyLoggerApp.stop_key = all_shortcut[ShortCut.STOP]
KeyPositon.pos_key_sc = all_shortcut[ShortCut.CAPTURE]


# Je crée une fonction pour passer d'un menu à l'autre.
# --------------------------------------------------------
# I create a function to switch from one menue to another.
def switch_frame(frame):
    global frm_now
    global ui_act_manager
    global ui_action_tree
    if not ui_act_manager.act_dict_manager.is_running and not ui_action_tree.in_edit:
        
        if frame == ui_act_manager.act_selector_frame:
            ui_act_manager.is_in_IntfActSelector = True
            if frm_now != ui_act_manager.act_selector_frame:
                ui_act_manager.update_positions()
        else:
            ui_act_manager.is_in_IntfActSelector = False
        frm_now.grid_remove()
        frame.grid(row=2, column=0)
        frm_now = frame




# Je crée une fonction qui prend en paramètre une instance de "Loop"/"SameTime" et parcourt son dictionnaire 
# "dict_tree_CNTR" pour detruir tout les "Checkbutton" qu'il contien pour qu'il ne sois plus dans "tree".
# ------------------------------------------------------------------------------------------------------------
# I create a function that takes an instance of "Loop"/"SameTime" as a parameter and parses its "dict_tree_CNTR" dictionary 
# to delete all the "Checkbutton" it contains so that they are no longer in "tree".
def cleaning_tree(loop_inst:Loop|SameTime):
    for ChkBt in loop_inst.dict_tree_CNTR.values():
        ChkBt[1].destroy()



# Je crée une fonction qui prend en paramètre une instance de "Loop"/"SameTime" et parcourt son dictionnaire "act_dict_CNTR". 
# Si c'est une instance de "Loop"/"SameTime", alors la fonction s'appelle elle-même en lui donnant 
# la nouvelle instance de "Loop"/"SameTime" et appelle "cleaning_tree" en lui donnant l'instance de "Loop"/"SameTime" pour détruire les "Checkbutton".
# ------------------------------------------------------------------------------------------------------------------------------
# I create a function that takes an instance of "Loop"/"SameTime" as a parameter and scans its "act_dict_CNTR" dictionary. If it's an 
# instance of "Loop"/"SameTime", then the function calls itself by giving it the new instance of "Loop"/"SameTime" and calls "cleaning_tree", 
# giving it the instance of "Loop"/"SameTime" to destroy the "Checkbutton".
def loop_finding(loop_inst):
    for element in loop_inst.act_dict_CNTR.values():
        if isinstance(element, Loop) or isinstance(element, SameTime):
            loop_finding(element)
            cleaning_tree(element)



# Je crée une fonction qui permet de remettre certaines variables à la même valeur que si on venait de démarrer le programme, 
# pour que l'utilisateur n'ait pas à fermer le programme et à le rouvrir pour recommencer.
# -----------------------------------------------------------------------------------------------------------------------------
# I create a function that resets certain variables to the same value as if the program had just been started, so that the user 
# doesn't have to close the program and reopen it to start again.
def reset():
    global ui_act_manager
    global ui_action_tree
    # Je vérifie que la suite d'actions de l'utilisateur n'est pas en train de s'exécuter.
    # --------------------------------------------------------------------------------------------------------------
    # I check that the user's action sequence is not running.
    if not ui_act_manager.act_dict_manager.is_running:
        # Je parcours le dictionnaire "act_dict" et, si je trouve une instance de "Loop"/"SameTime", j'appelle "loop_finding" et 
        # "cleaning_tree" en leur donnant l'instance de "Loop"/"SameTime" pour détruire tous les "Checkbutton".
        # --------------------------------------------------------------------------------------------------------------
        # Je parcours le dictionnaire "act_dict" et, si je trouve une instance de "Loop"/"SameTime", j'appelle "loop_finding" 
        # et "cleaning_tree" et leur donne l'instance de "Loop"/"SameTime" pour détruire tous les "Checkbutton".
        for element in ui_act_manager.act_dict_manager.act_dict.values():
            if isinstance(element, Loop) or isinstance(element, SameTime):
                loop_finding(element)
                cleaning_tree(element)



        ui_act_manager.act_dict_manager.act_dict = {}
        ui_act_manager.act_dict_manager.save_list = []
        ui_act_manager.act_dict_manager.dict_K = 0
        ui_act_manager.act_dict_manager.key_2 = 0

        ui_act_manager.container_manager.reset()


        for values in ui_action_tree.dict_tree.values():
            values[1].grid_remove()
            values[1].destroy() 
        ui_action_tree.dict_tree = {}
        ui_action_tree.K_dict_tree = 0
        ui_action_tree.row_ChkBt = 0
        ui_action_tree.save_fram.grid_remove()
        ui_action_tree.save_clicked = False








# Je crée une instance de "IntfTree" qui va créer son bouton dans 
# "menu_bt_frm" pour accéder à son propre cadre. "IntfTree" permet à 
# l'utilisateur de visualiser toutes les actions qu'il a choisies à 
# l'aide de "Checkbutton". L'utilisateur peut décocher les actions 
# qu'il ne souhaite pas exécuter. "IntfTree" lui permet également de 
# suprimer tout ce qu'il a fait, comme s'il venait de relancer le 
# programme, afin d'éviter de le redémarrer. Il peut aussi enregistrer 
# sa suite d'actions pour plus tard, ainsi que la modifier en 
# supprimant ou en modifiant des éléments.
# --------------------------------------------------------------------
# I create an instance of "IntfTree" that will create its button in 
# "menu_bt_frm" to access its own frame. "IntfTree" allows the user to 
# view all the actions they have selected using "Checkbutton".The user 
# can uncheck the actions they do not want to execute."IntfTree" also 
# allows them to delete everything they have done, as if they were 
# restarting the program, to avoid having to restart it.They can also 
# save their sequence of actions for later, as well as modify it by 
# deleting or changing elements.
ui_action_tree = IntfTree(
    window, 
    menu_bt_frm, 
    switch_frame, 
    w_var, 
    reset
    )

# Je crée une instance de "IntfActSelector" qui va créer son bouton dans 
# "menu_bt_frm" pour accéder à son propre cadre. "IntfActSelector" permet à 
# l'utilisateur de créer ses actions et de lancer l'exécution de la suite d'actions.
# ----------------------------------------------------------------------------------
# I create an instance of "IntfActSelector" which will create its button in 
# "menu_bt_frm" to access its own frame. "IntfActSelector" allows the user to create 
# their actions and start the execution of the action sequence.
ui_act_manager = IntfActSelector(
    window, 
    menu_bt_frm, 
    switch_frame, 
    w_var, 
    ui_action_tree
    )


intf_open = SavedSequencesUI(
    window, 
    menu_bt_frm, 
    switch_frame, 
    w_var, 
    reset, 
    ui_act_manager.act_dict_manager, 
    ui_act_manager.container_manager.leave_current_container, 
    ui_act_manager.container_manager
    )


ui_documentation = DocumentationUI(
    window, 
    menu_bt_frm, 
    switch_frame, 
    w_var
    )


ui_action_tree.ui_act_manager = ui_act_manager
ui_action_tree.container_manager = ui_act_manager.container_manager
ui_action_tree.frame_act()
frm_now = ui_act_manager.act_selector_frame
frm_now.grid(row=1, column=0, sticky="wen")








window.mainloop()




