from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Union, Optional
from functools import partial
import pickle 
from pathlib import Path

if TYPE_CHECKING:
    from action_manager import ActionDict
    from container_manager import ContainerManager


# Fichier dans lequel sont enregistrées les suites d'actions
# -----------------------------------------------------------
# File in which action sequences are stored
SEQUENCES_FILE_PATH = Path("Code/Data/save_act_sequence.pkl")

class SavedActionSequence:
    """
    Cette classe permet l'enregistrement d'une suite d'actions. Elle prend comme paramètre
    d'initialisation une suite d'actions dans une certaine syntaxe.
    (Cette suite d'actions doit être une liste contenant des sous-listes, où chaque sous-liste a comme
    premier élément le type d'action, suivi des paramètres de l'action.)
    La classe comporte également la fonction recreate_action_sequence. Le programme doit être remis à zéro.
    Ensuite, elle parcourt la liste et, en fonction de chaque action, elle appelle les fonctions nécessaires
    à la création de l'action.
    ---------------------------------------------------------------------------------------------------------
    This class allows the saving of an action sequence. It takes as an initialization
    parameter an action sequence written using a specific syntax.
    (This action sequence must be a list containing sub-lists, where each sub-list has
    the action type as its first element, followed by the action parameters.)
    The class also contains the recreate_action_sequence function. The program must be reset to zero.
    Then, it iterates through the list and, depending on each action, calls the functions
    required to create the action.
    """

    def __init__(self, sequence_to_save: list[Union[list[str]]]) -> None:
        """
        Enregistre la liste d'actions.
        
        :param sequence_to_save: liste d'actions à enregistrer. Elle comporte des sous-listes.
            Les sous-listes commencent par un str (le type d'action) et comportent
            les paramètres de l'action.
        --------------------------------------------------------------------------------
        Saves the list of actions.
        
        :param sequence_to_save: list of actions to save. It contains sub-lists.
            Each sub-list starts with a string (the action type) and contains
            the action parameters.
        """
        self.sequence = sequence_to_save


    def recreate_action_sequence(self, action_dict_manager: ActionDict, leave_current_container: callable, container_manager: ContainerManager) -> None:
        """
        Cette fonction prend les paramètres suivants :

        :param action_dict_manager: l'instance de ActionDict pour ajouter les actions à act_dict.
        :param leave_current_container: permet de sortir d'un conteneur lorsque la sous-liste 
            contient left_container.
        :param container_manager: utilisé pour passer is_in_container aux fonctions de 
            action_dict_manager et pour appeler indicate_container et add_container.

        Cette fonction doit être exécutée seulement une fois que le programme a été remis à zéro.
        On parcourt la liste enregistrée. On vérifie à quelle action 
        l'élément correspond et on appelle la fonction correspondante de action_dict_manager (du type add_...) 
        en lui passant les paramètres contenus dans la sous-liste après le type d'action, ainsi que 
        is_in_container.

        Si l'action est un conteneur (loop, same_time), on effectue le même processus, mais après, on 
        appelle indicate_container pour informer l'utilisateur qu'il est dans un conteneur, ainsi que 
        add_container, qui ajoute l'élément conteneur à CNTR_dict. On donne comme paramètre à ces 
        fonctions le nom du conteneur.
        Parfois, la sous-liste peut contenir left_container. Dans ce cas, on appelle leave_current_container 
        pour sortir du conteneur.
        ------------------------------------------------------------------------------------------------------
        This function takes the following parameters:

        :param action_dict_manager: the instance of ActionDict used to add actions to act_dict.
        :param leave_current_container: allows exiting a container when the sub-list contains left_container.
        :param container_manager: used to pass is_in_container to the functions of action_dict_manager and to call
            indicate_container and add_container.

        This function must only be executed once the program has been reset to zero.
        The saved list is iterated through. The action corresponding to each element
        is identified, and the corresponding function of action_dict_manager (of the form add_...)
        is called, passing the parameters contained in the sub-list after the action type,
        as well as is_in_container.

        If the action is a container (loop, same_time), the same process is applied, but afterward,
        indicate_container is called to inform the user that they are inside a container, as well as
        add_container, which adds the container element to CNTR_dict. The container name is passed
        as a parameter to these functions.
        Sometimes, the sub-list may contain left_container. In this case, leave_current_container
        is called to exit the container.
        """
        for action_entry in self.sequence:
            match action_entry[0]:
                
                case "click r":
                    action_dict_manager.add_click_r(action_entry[1], action_entry[2], container_manager.is_in_container)

                case "click l":
                    action_dict_manager.add_click_l(action_entry[1], action_entry[2], container_manager.is_in_container)

                case "move":
                    action_dict_manager.add_move(action_entry[1], action_entry[2], action_entry[3], container_manager.is_in_container)

                case "write":
                    action_dict_manager.add_write(action_entry[1], container_manager.is_in_container)

                case "wait":
                    action_dict_manager.add_wait(action_entry[1], container_manager.is_in_container)

                case "key press":
                    action_dict_manager.add_key_press(action_entry[1], action_entry[2], action_entry[3], container_manager.is_in_container)

                case "scroll":
                    action_dict_manager.add_scroll(action_entry[1], action_entry[2], container_manager.is_in_container)

                case "loop":
                    action_dict_manager.add_loop(action_entry[1], action_entry[2], container_manager.is_in_container)
                    container_manager.loop_names.append(action_entry[2])
                    container_manager.indicate_container(action_entry[2])
                    container_manager.add_container(action_entry[2])

                case "same time":
                    action_dict_manager.add_same_time(action_entry[1], action_entry[2], action_entry[3], container_manager.is_in_container)
                    container_manager.parallel_action_names.append(action_entry[3])
                    container_manager.indicate_container(action_entry[3])
                    container_manager.add_container(action_entry[3])

                case "left_container":
                    leave_current_container()


def load_saved_sequences() -> Optional[dict[str, SavedActionSequence]]:
    """
    Cette fonction récupère le contenu du fichier où sont stockées les suites 
    d'actions enregistrées. Elle vérifie que le fichier n'est pas corrompu et que 
    tout est dans le bon format (nom du fichier : str, instance de SavedActionSequence).

    :return: False si le contenu du fichier est incorrect,
        retourne un dictionnaire contenant chaque suite d'actions si tout est correct.
    ------------------------------------------------------------------------------------
    This function retrieves the content of the file in which the saved action sequences
    are stored. It checks that the file is not corrupted and that everything is in the
    correct format (file name: str, instance of SavedActionSequence).

    :return: False if the file content is invalid,
        otherwise returns a dictionary containing each action sequence.
    """

    # Ouvre le fichier
    # ----------------
    # Opens the file
    try:
        with SEQUENCES_FILE_PATH.open("rb") as file:
            saved_sequences = pickle.load(file)
    except:
        return None

    # Vérifie le format du contenu du fichier
    # ----------------------------------------
    # Checks the format of the file content

    if isinstance(saved_sequences, dict):
        for key, value in saved_sequences.items():
            if not isinstance(key, str) or not isinstance(value, SavedActionSequence):
                return None
        if saved_sequences == {}:
            return None
        return saved_sequences


def save_all_sequences(sequences_dict: dict[str, SavedActionSequence]) -> None:
    """
    Cette fonction remplace l'ancien contenu en enregistrant un dictionnaire
    contenant les suites d'actions et leurs noms dans save_act_sequence.txt

    :param sequences_dict: dictionnaire contenant les suites d'actions et leurs noms
    ---------------------------------------------------------------------------
    This function replaces the old content by saving a dictionary containing
    the action sequences and their names into save_act_sequence.txt.

    :param sequences_dict: dictionary containing the action sequences and their names
    """
    with SEQUENCES_FILE_PATH.open("wb") as file:
        pickle.dump(sequences_dict, file)


def save_sequence(name: str, action_list: list[list[str]]) -> Union[bool, Tuple[str, int]]:
    """
    Cette fonction vérifie que le nom est correct. Si celui-ci est correct, on
    l'enregistre avec sa suite d'actions. Sinon, on retourne un message d'erreur
    qui va être affiché, ainsi qu'un nombre indiquant le nombre de lignes de ce
    message d'erreur (une ou deux lignes).

    :param name: nom du futur fichier
    :param action_list: liste d'actions à enregistrer
    :return: True si l'enregistrement a réussi, sinon un message d'erreur et 
        un nombre indiquant le nombre de lignes du message d'erreur.
    # ---------------------------------------------------------------------------
    This function checks whether the name is valid. If it is valid, the action
    sequence is saved using that name. Otherwise, an error message is returned,
    along with a number indicating how many lines the error message contains
    (one or two lines).

    :param name: name of the future file
    :param action_list: list of actions to save
    :return: True if the save was successful, otherwise an error message and
        a number indicating the number of lines in the error message.
    """

    # On vérifie que l'utilisateur a écrit un nom, puis on vérifie qu'il n'a pas 
    # entré un nom de plus de 25 caractères, sinon on retourne un message d'erreur.
    # -----------------------------------------------------------------------------------
    # We check that the user has entered a name, then we check that they have not
    # entered a name longer than 25 characters. Otherwise, an error message is returned.
    if len(name) <= 0:
        return "You have not entered a name", 1
    if len(name) > 25:
        return "You cannot enter a name \nlonger than 25 characters", 2

    # On tente de récupérer le contenu du fichier save_act_sequence.txt grâce à 
    # load_saved_sequences, qui retourne soit le contenu du fichier, soit None.
    # ----------------------------------------------------------------------------
    # We attempt to retrieve the content of the file save_act_sequence.txt using 
    # load_saved_sequences, which returns either the file content or None.
    file_content = load_saved_sequences()

    # Si load_saved_sequences a retourné None, on crée un nouveau dictionnaire 
    # pour enregistrer dans save_act_sequence.txt l'instance de SavedActionSequence
    # qui contient la suite d'actions, avec pour clé son nom.
    # --------------------------------------------------------------------------
    # If load_saved_sequences returned None, we create a new dictionary to save 
    # into save_act_sequence.txt the instance of SavedActionSequence that contains 
    # the action sequence, using its name as the key.
    if not file_content:
        save_all_sequences({name: SavedActionSequence(action_list)})
        return True
    
    # On regarde si le nom choisi par l'utilisateur n'est pas déjà utilisé.
    # ---------------------------------------------------------------------
    # We check whether the name chosen by the user is already in use.
    try:
        file_content[name]

    except KeyError:
        # On ajoute la suite d'actions avec pour clé son nom au dictionnaire contenant 
        # toutes les autres suites d'actions enregistrées auparavant, puis on enregistre 
        # le dictionnaire dans le fichier save_act_sequence.txt et on retourne true.
        # ----------------------------------------------------------------------------------
        # We add the action sequence using its name as the key to the dictionary containing
        # all the other previously saved action sequences, then we save the dictionary
        # to the file save_act_sequence.txt and return true.
        file_content[name] = SavedActionSequence(action_list)
        save_all_sequences(file_content)
        return True
    else:
        return "This file name is already in use", 1
