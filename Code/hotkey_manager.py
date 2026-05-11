from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Union
from functools import partial
import pickle 
from pathlib import Path
import pickle
from typing import Dict, List
from enums import ShortCut

# Configuration et constantes
# ---------------------------
# Configuration and constants
SHORTCUTS_PATH = Path("Data/shortcuts.pkl")  # chemin du fichier de sauvegarde (binaire pickle)
DEFAULT_SHORTCUTS: Dict[str, List[str]] = {
    ShortCut.STOP: ["y", "j"],
    ShortCut.CAPTURE: ["x", "v"],
}

# Chargement / validation / sauvegarde des raccourcis
# ---------------------------------------------------
# Load / validate / save shortcuts
def load_shortcuts() -> Dict[str, List[str]]:
    """
    Charge les raccourcis depuis le fichier. Si le fichier est absent ou corrompu,
    il est recréé avec les valeurs par défaut et renvoie ces valeurs par défaut.

    :return: Dict[str, List[str]] - Un dictionnaire des raccourcis.
    ------------------------------------------------------------------------------
    Load shortcuts from disk. If the file is missing or corrupted,
    recreate it with default values and return the defaults.
    
    :return: Dict[str, List[str]] - A dictionary of shortcuts.
    """
    # Assurer que le répertoire existe
    # --------------------------------
    # Ensure the directory exists
    SHORTCUTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        with SHORTCUTS_PATH.open("rb") as f:
            data = pickle.load(f)
    except Exception:
        # Fichier manquant ou corrompu -> recréer avec les val;eurs par défaut
        # -------------------------------------------------------------------
        # Missing or corrupted file -> recreate with default values
        reset_shortcuts_to_defaults()
        return DEFAULT_SHORTCUTS.copy()

    # Validation basique de la structure attendue
    # -------------------------------------------
    # Basic validation of the expected structure
    if not isinstance(data, dict):
        reset_shortcuts_to_defaults()
        return DEFAULT_SHORTCUTS.copy()

    for key, values in data.items():
        if key != ShortCut.STOP and key != ShortCut.CAPTURE or not isinstance(values, list):
            reset_shortcuts_to_defaults()
            return DEFAULT_SHORTCUTS.copy()
        for v in values:
            if not (isinstance(v, str) and len(v) == 1):
                reset_shortcuts_to_defaults()
                return DEFAULT_SHORTCUTS.copy()

    return data


def reset_shortcuts_to_defaults() -> None:
    """
    Réinitialise le fichier de raccourcis en écrivant les valeurs par défaut.
    -------------------------------------------------------------------------
    Reset the shortcuts file by writing the default values.
    """
    SHORTCUTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SHORTCUTS_PATH.open("wb") as f:
        pickle.dump(DEFAULT_SHORTCUTS.copy(), f, protocol=pickle.HIGHEST_PROTOCOL)


def save_shortcuts(shortcut_type: str, keys: List[str]) -> None:
    """
    Enregistre une liste de touches (raccourcis) pour un raccourci donné.
    Valide le type et le format des touches avant sauvegarde.

    :param shortcut_type: str - type du raccourci
    :param keys: List[str] - liste des touches
    ----------------------------------------------------------------
    Saves a list of keys (shortcuts) for a given shortcut type.
    Validates the type and format of the keys before saving.

    :param shortcut_type: str - type of the shortcut
    :param keys: List[str] - list of keys
    """
    if shortcut_type != ShortCut.STOP and shortcut_type != ShortCut.CAPTURE:
        raise ValueError(f"Unknown shortcut type: {shortcut_type}")

    if not isinstance(keys, list) or not all(isinstance(k, str) and len(k) == 1 for k in keys):
        raise ValueError("Keys must be a list of single-character strings")

    shortcuts = load_shortcuts()
    shortcuts[shortcut_type] = keys

    SHORTCUTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SHORTCUTS_PATH.open("wb") as f:
        pickle.dump(shortcuts, f, protocol=pickle.HIGHEST_PROTOCOL)
        
