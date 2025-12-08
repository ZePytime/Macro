


from scrollbarre import ScrollableFrame

import tkinter as tk
import pickle 
from pathlib import Path
from sequence_saver import SaveActSequence

file_path = Path("Code/Data/save_act_sequence.txt")



RdBt_list = {}
file_dict = None
choice = None

file_contents = None


def update_file(all_file, error_label):
    global RdBt_list
    global file_dict
    global choice
    global file_contents


    file_contents = file_check()
    if file_contents == False:
        for RdBt in RdBt_list.values():
            RdBt.destroy()
        
        file_dict = None
        choice = None
        RdBt_list = {}
        file_contents = None


        error_label.grid(row=0, column=0)
        
        # si file_dict est rempli proposer une restoration des fichiers



    else:
        error_label.grid_remove()

        choice = tk.StringVar(value=list(file_contents.keys())[0])

        file_dict = file_contents
        for nb_key, element in enumerate(file_contents.keys()):
            
            choix_open = tk.Radiobutton(all_file, text=element, variable=choice, value=element, background="#71B0B0")
            choix_open.grid(row=nb_key, column=0)
            RdBt_list[element] = choix_open






def file_check():
    global file_contents

    try:

        with file_path.open("rb") as file:
            file_contents = pickle.load(file)
    
    except:
        return False
        

    else:
        if isinstance(file_contents, dict):
            new_file_contents = file_contents

            for key, value in file_contents.items():
                pass
                #j ai besoin de la class SaveActSequence pour le bon fonctionnement de la suite
                if isinstance(value, SaveActSequence):
                    new_file_contents[key] = value

            if new_file_contents != {}:
                return new_file_contents
            else:
                return False
        
        else:
            return False
        




def open_file(instance_dico, reset, leave_current_container, container_manager, same_time_inst):
    global file_contents
    if not instance_dico.is_running:
        if not choice == None:
            file_contents[choice.get()].recreate_act_sequence(instance_dico, reset, leave_current_container, container_manager, same_time_inst)
    


def delet_file():
    RdBt_list[choice.get()].grid_remove()
    RdBt_list[choice.get()].destroy()
    del RdBt_list[choice.get()]
    del file_contents[choice.get()]
    with file_path.open("wb") as file:
        pickle.dump(file_contents, file)






class IntfOpenFile:

    def __init__(self, window, menu_bt_frame, frame_exchanger, w_var, reset, act_dict_manager, leave_current_container, container_manager, same_time_inst):
        self.frame_exchanger = frame_exchanger
        self.instance_dico = act_dict_manager
        self.reset = reset
        self.leave_current_container = leave_current_container

        

        file_button = tk.Button(menu_bt_frame, 
                                text="file", 
                                bg=w_var.color_2, 
                                fg="black", 
                                height=1, 
                                width=5, 
                                font=w_var.font_size, 
                                command=self.frame_display
                                )
        file_button.grid(row=0, column=2)





        self.open_frame = tk.Frame(window, bg=w_var.color_1, width=320, height=450)
        self.open_frame.grid_propagate(False)


        self.all_file = ScrollableFrame(self.open_frame)
        self.all_file.grid(row=0, column=0, padx=30, pady=10)


        self.error_label = tk.Label(self.all_file, 
                    text='you have no files', 
                    bg=w_var.color_1, 
                    fg="black", 
                    height=2, 
                    width=30, 
                    font=w_var.font_size_error
                    )



        open = tk.Button(self.open_frame, 
                        text="open", 
                        bg=w_var.color_2, 
                        fg="black", 
                        height=1, 
                        width=8, 
                        font=w_var.font_size, 
                        command=lambda : open_file(self.instance_dico, self.reset, self.leave_current_container, container_manager, same_time_inst)
                        )
        open.grid(row=1, column=0)

        open = tk.Button(self.open_frame, 
                        text="delete", 
                        bg=w_var.color_2, 
                        fg="black", 
                        height=1, 
                        width=8, 
                        font=w_var.font_size, 
                        command=lambda : self.create_popup(window)
                        )
        open.grid(row=2, column=0)

    def Clear_RdBt(self):
        for RdBt in RdBt_list.values():
            RdBt.destroy()




    def frame_display(self):
        self.Clear_RdBt()
        update_file(self.all_file.scrollable_frame, self.error_label)
        self.frame_exchanger(self.open_frame)

    def create_popup(self, window):
        try :
            choice.get()
        except KeyError:
            pass
        else:
            popup = tk.Toplevel(window)
            popup.title("Popup")
            popup.geometry("200x100")

            label = tk.Label(popup, text="Are you sure you want to delete the poop file?")
            label.pack(pady=10)

            close_button = tk.Button(popup, text="yes", command=lambda : self.delet_file(popup))
            close_button.pack(pady=5)
            close_button = tk.Button(popup, text="no", command=popup.destroy)
            close_button.pack(pady=5)

    def delet_file(self, popup):
        delet_file()
        popup.destroy()
        self.frame_display()


