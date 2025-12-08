import pickle 
from pathlib import Path

import tkinter as tk


path_file = Path("Code/Data/save_act_sequence.txt")


class SaveActSequence:
    """
    Cette classe permet l'enregistrement d'une suite d'actions. Elle prend comme paramètre 
    d'initialisation une suite d'actions dans une certaine syntaxe.
    (Cette suite d'actions doit être une liste contenant des sous-listes, où chaque sous-liste a comme 
    premier élément le type d'action, suivi des paramètres de l'action. Dans cette liste, il peut aussi y 
    avoir l'élément "left_container".)
    La classe comporte également la fonction "recreate_act_sequence", qui commence par appeler 
    "reset", permettant de repartir de zéro, comme si l'on venait de démarrer le programme. Ensuite, elle 
    parcourt la liste et, en fonction de chaque action, elle appelle les fonctions nécessaires à la création 
    de l'action.
    ---------------------------------------------------------------------------------------------------------
    This class allows the recording of a sequence of actions. It takes as an initialization parameter a 
    sequence of actions in a specific syntax.
    (This sequence of actions must be a list containing sub-lists, where each sub-list has as its first 
    element the type of action, followed by the parameters of the action. In this list, there may also be 
    the "left_container" element.)
    The class also includes the "recreate_act_sequence" function, which begins by calling "reset", 
    allowing you to start from scratch as if the program had just started. Then, it iterates through the list 
    and, depending on the action, it calls the necessary functions to create the action.
    """

    def __init__(self, list_save):
        self.list_save = list_save




    def recreate_act_sequence(self, instance_dico, reset, leave_current_container, container_manager, same_time_inst):
        """
        Cette fonction prend les paramètres suivants :

        -"instance_dico" : l'instance de "ActionDict" pour ajouter les actions à "act_dict".
        -"reset" : permet de repartir de zéro, comme si on venait de démarrer le programme.
        -"leave_current_container" : permet de sortir d'un conteneur lorsque la sous-liste contient "left_container".
        -"container_manager" : utilisé pour passer "is_in_container" aux fonctions de "instance_dico" et pour appeler 
        "indicate_container" et "add_container".

        On commence par appeler "reset", puis on parcourt la liste enregistrée. On vérifie à quelle action 
        l'élément correspond et on appelle la fonction correspondante de "instance_dico" (du type "add_...") 
        en lui passant les paramètres contenus dans la sous-liste après le type d'action, ainsi que 
        "is_in_container".

        Si l'action est un conteneur (loop, same_time), on effectue le même processus, mais après, on 
        appelle "indicate_container" pour informer l'utilisateur qu'il est dans un conteneur, ainsi que 
        "add_container", qui ajoute l'élément conteneur à "CNTR_dict". On donne comme paramètre à ces 
        fonctions le nom du conteneur.
        Parfois, la sous-liste peut contenir "left_container". Dans ce cas, on appelle "leave_current_container" pour sortir 
        du conteneur.
        -------------------------------------------------------------------------------------------------------
        This function takes the following parameters:

        -"instance_dico": the instance of "ActionDict" to add actions to "act_dict".
        -"reset": allows you to start from scratch, as if the program had just started.
        -"leave_current_container": allows you to exit a container when the sub-list contains "left_container".
        -"container_manager": used to pass "is_in_container" to the functions of "instance_dico" and to call 
        "indicate_container" and "add_container".

        We start by calling "reset", then we iterate through the recorded list. We check which action the 
        element corresponds to and call the corresponding function of "instance_dico" (of the type "add_...") 
        by passing it the parameters found in the sub-list after the type of action, as well as "is_in_container".

        If the action is a container (loop, same_time), we follow the same process, but afterwards, we call 
        "indicate_container" to inform the user that they are in a container, as well as "add_container", which 
        adds the container element to "CNTR_dict". We pass the name of the container as a parameter to 
        these functions.

        Sometimes, the sub-list may contain "left_container". In this case, we call "leave_current_container" to exit the 
        container.
        """
        print(instance_dico.act_dict)
        reset()

        print(self.list_save)
        for element in self.list_save:
            print(element)
            match element[0]:
                
                case "click r":
                    instance_dico.add_click_r(element[1], element[2], container_manager.is_in_container)

                case "click l":
                    instance_dico.add_click_l(element[1], element[2], container_manager.is_in_container)

                case "move":
                    instance_dico.add_move(element[1], element[2], element[3], container_manager.is_in_container)

                case "write":
                    instance_dico.add_write(element[1], container_manager.is_in_container)

                case "wait":
                    instance_dico.add_wait(element[1], container_manager.is_in_container)

                case "key press":
                    instance_dico.add_key_press(element[1], element[2], element[3], container_manager.is_in_container)

                case "scroll":
                    instance_dico.add_scroll(element[1], element[2], container_manager.is_in_container)

                case "loop":
                    instance_dico.add_loop(element[1], element[2], container_manager.is_in_container)
                    container_manager.loop_names.append(element[2])
                    container_manager.indicate_container(element[2])
                    container_manager.add_container(element[2])
                    

                case "same time":
                    instance_dico.add_same_time(element[1], element[2], element[3], container_manager.is_in_container)
                    container_manager.parallel_action_names.append(element[3])
                    container_manager.indicate_container(element[3])
                    container_manager.add_container(element[3])
                    
                    

                case "left_container":
                    leave_current_container()
            print(instance_dico.save_list)
            print(instance_dico.act_dict)








def give_file_content():
    """
    Cette fonction vérifie que le fichier existe et qu'il contient bien un dictionnaire avec toutes les 
    instances de "SaveActSequence" pour être sûr.
    ---------------------------------------------------------------------------------------------------------
    This function checks that the file exists and that it indeed contains a dictionary with all the instances 
    of "SaveActSequence" to be sure.
    """
    try:
        with path_file.open("rb") as file:
            file_content = pickle.load(file)

    except:
        return False
        

    else:
        if isinstance(file_content, dict):
            for element in file_content.values():
                if not isinstance(element, SaveActSequence):
                    return False
            return file_content








def save_new_dict(nom, list_save): 
    """
    Cette fonction prend "list_save" en paramètre et va créer un nouveau dictionnaire pour enregistrer la 
    suite d'actions grâce à "SaveActSequence", et on va enregistrer ce dictionnaire dans 
    "save_act_sequence.txt". Cette fonction est appelée lorsque le fichier a été modifié par 
    l'utilisateur, ce qui le rend illisible pour le programme, ou lorsque l'utilisateur n'a jamais rien 
    enregistré ou l'a supprimé ect.
    -----------------------------------------------------------------------------------------------------
    This function takes "list_save" as a parameter and will create a new dictionary to save the action 
    sequence using "SaveActSequence", and this dictionary will be saved in "save_act_sequence.txt". 
    This function is called when the file has been modified by the user, making it unreadable for the 
    program, or when the user has never saved anything or has deleted it, etc.

    """
    file_content = {str(nom): SaveActSequence(list_save)}
    with path_file.open("wb") as file:
        pickle.dump(file_content, file)








def save(name, list_save):
    """
    Cette fonction prend comme paramètres le nom du futur fichier et la liste d'actions "give_file_content". 
    Dans cette fonction, on va vérifier que le nom est correct. Si tout est correct, on enregistre la 
    suite d'actions, sinon on retourne un message d'erreur qui va être affiché, ainsi qu'un nombre 
    indiquant le nombre de lignes que fait ce message d'erreur (une ou deux lignes).
    ---------------------------------------------------------------------------------------------------
    This function takes as parameters the name of the future file and the action list "give_file_content". 
    In this function, we will check that the name is correct. If everything is correct, the action 
    sequence is saved. Otherwise, an error message is returned and displayed, along with a number 
    indicating how many lines the error message takes (one or two lines).
    """


    # On vérifie que l'utilisateur a écrit un nom, puis on vérifie qu'il n'a pas 
    # entré un nom de plus de 25 caractères, sinon on retourne un message d'erreur.
    # ----------------------------------------------------------------------------------
    # We check that the user has entered a name, then we check that they haven't 
    # entered a name longer than 25 characters. Otherwise, an error message is returned.
    if not len(name) <= 0:
        if len(name) <= 25:
            # On tente de récupérer le contenu du fichier "save_act_sequence.txt" grâce à "give_file_content", 
            # qui retourne soit le contenu du fichier, soit "false".
            # -----------------------------------------------------------------------------------------------
            # We attempt to retrieve the content of the file "save_act_sequence.txt" using "give_file_content", 
            # which returns either the file's content or "false".
            file_content = give_file_content()

            # Si "give_file_content" a retourné "false", on appelle "save_new_dict", qui va créer un nouveau 
            # dictionnaire pour enregistrer dans "save_act_sequence.txt" l'instance de "SaveActSequence" 
            # qui contient la suite d'actions, avec pour clé son nom.
            # -----------------------------------------------------------------------------------------------
            # If "give_file_content" returned "false", we call "save_new_dict", which will create a new dictionary 
            # to save the instance of "SaveActSequence" that contains the action sequence, 
            # with its name as the key.
            if file_content == False:
                save_new_dict(name, list_save)
                return True
            else:
                # On regarde si le nom choisi par l'utilisateur n'est pas déjà utilisé.
                # ---------------------------------------------------------------------
                # We check if the name chosen by the user is not already in use.
                try:
                    file_content[name]

                except KeyError:
                    # On ajoute la suite d'actions avec pour clé son nom au dictionnaire contenant 
                    # toutes les autres suites d'actions enregistrées auparavant, puis on enregistre 
                    # le dictionnaire dans le fichier "save_act_sequence.txt" et on retourne true.
                    # --------------------------------------------------------------------------------
                    # We add the action sequence with its name as the key to the dictionary containing 
                    # all the other action sequences recorded previously, then we save the dictionary 
                    # in the file "save_act_sequence.txt" and return true.
                    file_content[name] = SaveActSequence(list_save)
                    with path_file.open("wb") as file:
                        pickle.dump(file_content, file)
                    return True
                else:
                    return "this file name is already in use", 1
                
        else:
            return "you cannot enter a name \nlonger than 25 characters", 2

    else:
        return "You have not entered a name", 1







