from action_classes import ClickRight, ClickLeft, Write, KeyPress, Wait, Loop, Move, Scroll, KeyLoggerApp, SameTime
# créé un decorateur qui execute les fonction et qui recupere ce quil retourn et appelle tree_plus en lui donnant ces parametre
# les fonction retoureront plusieur chause au decorateur les info pour tree pluce ou une erreuur

#il faut toujour passer la fonction dans la quelle on est a la boucle
import tkinter as tk


class ActionDict:
    def __init__(self, window: tk.Tk, get_most_nested_container, inter_tree):
        self.window = window


        self.sleep_act_time = 0



        self.get_most_nested_container = get_most_nested_container

        self.inter_tree = inter_tree


        self.act_dict_edit_test = {}

        self.save_list = []
        self.act_dict  = {}
        self.dict_K = 0



        self.key_2 = 0
        self.is_running = False
        self.id = None



    # ===============================================
    # === SECTION : creation de la suite d'action ===
    # ===============================================

    def left_container(self):
        self.save_list.append(["left_container"])


    def add_act(self, is_in_container, action):
        if is_in_container:
            spacing, last_lp = self.get_most_nested_container(self.act_dict, self.dict_K)
            last_lp.new_action(action)
            last_lp.add_tree_CNTR(action.text(), self.inter_tree, spacing*10)
        else:
            self.act_dict[self.dict_K] = action
            self.dict_K += 1
            self.inter_tree.add_tree(action.text())




    def add_click_l(self, position_x, position_y, is_in_container):
        action = ClickLeft(position_x, position_y)
        self.save_list.append([action.type_act(), position_x, position_y])
        self.add_act(is_in_container, action)


    def add_click_r(self, position_x, position_y, is_in_container):
        action = ClickRight(position_x, position_y)
        self.save_list.append([action.type_act(), position_x, position_y])
        self.add_act(is_in_container, action)


    def add_move(self, position_x, position_y, movement_type, is_in_container):
        action = Move(position_x, position_y, movement_type)
        self.save_list.append([action.type_act(), position_x, position_y, movement_type])
        self.add_act(is_in_container, action)


    def add_write(self, text, is_in_container):
        action = Write(text)
        self.save_list.append([action.type_act(), text])
        self.add_act(is_in_container, action)


    def add_scroll(self, nb, direction, is_in_container):
        action = Scroll(nb, direction)
        self.save_list.append([action.type_act(), nb, direction])
        self.add_act(is_in_container, action)


    def add_wait(self, time, is_in_container):
        action = Wait(time)
        self.save_list.append([action.type_act(), time])
        self.add_act(is_in_container, action)


    def add_key_press(self, keys, special_keys, time, is_in_container):
        action = KeyPress(keys, special_keys, time)
        self.save_list.append([action.type_act(), keys, special_keys, time])
        self.add_act(is_in_container, action)


    def add_same_time(self, keys, list_sp_keys, name, is_in_container):
        action = SameTime(self.window, keys, list_sp_keys, name)
        self.save_list.append([action.type_act(), keys, list_sp_keys, name])
        self.add_act(is_in_container, action)


    def add_loop(self, nb_turns, loop_name, is_in_container):
        action = Loop(self.window, nb_turns, loop_name)
        self.save_list.append([action.type_act(), nb_turns, loop_name])
        self.add_act(is_in_container, action)



    # ===================================================
    # === SECTION : modification de la suite d'action ===
    # ===================================================

    #def delet_act(self):
        #

































































    # ================================================
    # === SECTION : execution de la suite d'action ===
    # ================================================

    def cancel_task(self):
        try:
            self.act_dict[self.key_2-1].stop_press()
        except:
            pass

        try:
            self.act_dict[self.key_2-1].cancel_task()
        except:
            pass

        if self.id is not None:
            self.window.after_cancel(self.id)
            self.id = None
        self.key_2 = 0
        self.is_running = False
        self.create_popup()






    def call_stop_press(self):
        self.act_dict[self.key_2-1].stop_press()
        self.id = self.window.after(self.sleep_act_time, self.start)






    def start(self, other_value=True):
        
        if not other_value and not self.is_running:
            KeyLoggerApp.stop_run = False
            app = KeyLoggerApp(self.cancel_task)


        if other_value or not self.is_running:
            self.is_running = True
            
            if not self.key_2 >= self.dict_K and not KeyLoggerApp.stop_run:
                self.key_2 += 1
                if list(self.inter_tree.dict_tree[self.key_2-1])[0].get() == 1:

                    if isinstance(self.act_dict[self.key_2-1], Loop) or isinstance(self.act_dict[self.key_2-1], SameTime):
                        self.window.after(0, lambda : self.act_dict[self.key_2-1].run_act(self.start, self.sleep_act_time))
                    
                    else:
                        time = self.act_dict[self.key_2-1].run_act()


                    
                        if isinstance(self.act_dict[self.key_2-1], KeyPress):
                            self.id = self.window.after(time, self.call_stop_press)

                        elif isinstance(self.act_dict[self.key_2-1], Wait):
                            self.id = self.window.after(time+self.sleep_act_time, self.start)
                        
                        else:
                            self.window.after(self.sleep_act_time, self.start)
                else:
                    self.window.after(self.sleep_act_time, self.start)
                
            else:
                self.key_2 = 0
                self.is_running = False
                print("finnnnnnnnnnnnnnn")
                print(self.act_dict)
                self.create_popup()




    def create_popup(self):
        popup = tk.Toplevel(self.window)
        popup.title("Popup")
        popup.geometry("200x100")

        label = tk.Label(popup, text="the program has finished running")
        label.pack(pady=10)


