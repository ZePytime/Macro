from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING, Tuple, Union
from functools import partial


if TYPE_CHECKING:
    from main import WindowVariable



class ContainerManager:
    """
    Gère les conteneurs d'actions (boucles, actions parallèles).
    Permet a l'utilisateur de savoir s'il est dans un conteneur, qelle est son nom,
    et de sortir du conteneur actuel. Enregitre le nom de chaque conteneurs. 
    Gère l'imbrication des conteneurs.
    ------------------------------------------------------------------------------
    Manages action containers (loops, parallel actions).
    Allows the user to know if they are in a container, what its name is,
    and to exit the current container. Records the name of each container.
    Manages the nesting of containers.
    """

    def __init__(self, w_var, act_selector_frame):
        """
        Initialise les variables nessaires pour gérer les conteneurs d'actions.
        Initialise aussi le cadre et les widgets permettant 
        à l'utilisateur de sortir d'un conteneur.
        
        :param w_var: objet contenant les paramètres d'affichage 
            (couleurs, tailles, screen_width/height)
        :param act_selector_frame: la frame où les widgets seront placés
        ------------------------------------------------------------------------
        Initializes the variables necessary to manage action containers.
        Also initializes the frame and widgets allowing
        the user to exit a container.

        :param w_var: object containing display settings
            (colors, sizes, screen_width/height)
        :param act_selector_frame: the frame where the widgets will be placed
        """

        # Liste des noms de toutes les boucles créées par l'utilisateur.
        # ---------------------------------------------------------------
        # List of names of all loops created by the user.
        self.loop_names = []
        # Liste des noms de toutes les actions parallèles créées par l'utilisateur.
        # --------------------------------------------------------------------------
        # List of names of all parallel actions created by the user.
        self.parallel_action_names = []

        self._w_var = w_var

        # Fonction qui permet d'ajouter à la liste permettant d'enregistrer 
        # la suite actions l'information qu'on sort d'un conteneur.
        # Cette variable est modifier apres l'initialisation de "ContainerManager" 
        # et c'est à ce moment que la fonction est assignée.
        # -------------------------------------------------------------------------
        # Function that adds to the list for saving the action sequence 
        # the information that we are leaving a container.
        # This variable is modified after the initialization of "ContainerManager"
        # and it is at that moment that the function is assigned.
        self.leave_container_callback = None

        # Indique si l'utilisateur est dans un conteneur ou non.
        # -------------------------------------------------------
        # Indicates whether the user is in a container or not.
        self.is_in_container = False


        # Dictionnaire des conteneurs
        # ----------------------------
        # Dictionary of containers
        self.container_map = {}
        # Clé unique pour le dictionnaire des conteneurs
        # ---------------------------------------------
        # Unique key for the container dictionary
        self._next_container_id = 0


        
        self._leave_container_frame=tk.Frame(act_selector_frame, bg=w_var.color_1)

        # Label informatif pour le nom du conteneur actuel.
        # --------------------------------------------------
        # Info label for the name of the current container.
        self._info_label = tk.Label(
            self._leave_container_frame, 
            text="you're in the container : ", 
            bg=w_var.color_1, 
            fg="black", 
            height=2, 
            width=24, 
            font=w_var.font_size
            )
        self._info_label.grid(row=0, column=0)

        # Button pour quitter le conteneur actuel.
        # -----------------------------------------
        # Button to leave the current container.
        self._btn_leave_container = tk.Button(
            self._leave_container_frame, 
            text="leave", 
            bg=w_var.color_2, 
            fg="black", 
            height=1, 
            width=6, 
            font=w_var.font_size, 
            command=self.leave_current_container
            )
        self._btn_leave_container.grid(row=0, column=1)


    def reset(self) -> None:
        """
        Réinitialise les variables de gestion des conteneurs.
        -----------------------------------------------
        Resets the container management variables.
        """
        self.loop_names = []
        self.parallel_action_names = []
        self.container_map = {}
        self._next_container_id = 0
        self.is_in_container = False
        self._leave_container_frame.grid_remove()

    def add_container(self, name: str) -> None:
        """
        Ajoute un conteneur au dictionnaire des conteneurs,
        marque ce conteneur comme actif et met à jour l'état
        
        :param name: Nom du conteneur
        -----------------------------------------------------
        Adds a container to the container dictionary,
        marks this container as active and updates the state

        :param name: Name of the container
        """
        self.container_map[self._next_container_id] = [True, name]
        self._next_container_id += 1
        self.is_in_container = True


    def leave_current_container(self):
        """
        Permet à l'utilisateur de sortir du conteneur actuel.
        Met à jour l'affichage en fonction de l'état des conteneurs.
        -------------------------------------------------------
        Allows the user to exit the current container.
        Updates the display based on the state of the containers.
        """

        # Enregistre la sortie du conteneur dans la liste de sauvegarde.
        # ---------------------------------------------------------------
        # Records the exit from the container in the save list.
        self.leave_container_callback()

        containers_count = len(self.container_map)
        next_active_container = False

        # Marque le conteneur actuel comme inactif.
        # --------------------------------------
        # Marks the current container as inactive.
        for i in range(containers_count):
            if self.container_map[(containers_count-1)-i][0]:
                self.container_map[(containers_count-1)-i][0] = False
                break

        # Vérifie s'il reste des conteneurs actifs.
        # ---------------------------------------
        # Checks if there are any active containers left.
        for element in reversed(list(self.container_map.values())):
            if element[0]:
                next_active_container = element[1]
                break

        # Met à jour l'affichage en fonction de l'état des conteneurs.
        # -----------------------------------------------
        # Updates the display based on the state of the containers.
        if isinstance(next_active_container, str):
            self.indicate_container(next_active_container)

        else:
            self._leave_container_frame.grid_remove()
            self.is_in_container = False



    def indicate_container(self, container_name):
        """
        Affiche le cadre indiquant à l'utilisateur qu'il est dans un conteneur
        et le nom de ce conteneur.
        
        :param container_name: Nom du conteneur actuel.
        -----------------------------------------------------------------------
        Displays the frame indicating to the user that they are in a container
        and the name of that container.

        :param container_name: Name of the current container.
        """
        if len(container_name)<=10:
            self._info_label.config(text=f"You're in the container : {container_name}")
        elif len(container_name)<=15:
            self._info_label.config(text=f"You're in the container : \n{container_name}")
        elif len(container_name)<=20:
            self._info_label.config(text=f"You're in the container : \n{container_name}")
        self._leave_container_frame.grid(row=0, column=0, sticky="wen")




    def get_most_nested_container(self, actions_dict: dict, current_key: int) -> Tuple[int, Union[object, int]]:

        """
        Trouve le conteneur le plus imbriqué dans lequel on se trouve actuellement.
        
        :param act_dict: Dictionnair des action 
        :param dict_K: Clé du dictionnaire la ou on se trouve actuellement.
        :returns: Tuple[int, Union[object, int]] -
            Le nombre de conteneurs imbriqués et l'instance du conteneur le plus imbriqué.
        ----------------------------------------------------------------------------
        Finds the most nested container we are currently in.

        :param act_dict: Dictionary of actions
        :param dict_K: Key of the dictionary where we are currently located.
        :returns: Tuple[int, Union[object, int]] -
            The number of nested containers and the instance of the most nested container.
        """

        # Compte le nombre de conteneurs imbriqués.
        # ------------------------------------------
        # Counts the number of nested containers.
        container_entry = 0
        for value in self.container_map.values():
            if value[0]:
                container_entry += 1

        # Retourne le conteneur le plus imbriqué.
        # ----------------------------------------
        # Returns the most nested container.
        if container_entry > 1:
            nested_container_instance = actions_dict[current_key-1]
            for i in range(container_entry-1):
                nested_container_instance = nested_container_instance.act_dict_CNTR[nested_container_instance.act_K_CNTR-1]
            return container_entry, nested_container_instance
        else:
            return container_entry, actions_dict[current_key-1]


