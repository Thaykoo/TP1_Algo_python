# Fichier : main.py (MODIFIÉ - Pour résoudre l'ImportError)

import sys
import os
import importlib.util

# 1. Ajoute le répertoire courant pour trouver les modules (déjà présent)
# sys.path.append(os.path.dirname(__file__))

# 2. Correction : Utiliser un import dynamique pour charger mode_terminal.py
# On crée un module à partir du chemin du fichier mode_terminal.py
file_path = os.path.join(os.path.dirname(__file__), 'mode_terminal.py')
spec = importlib.util.spec_from_file_location("mode_terminal", file_path)
if spec is None:
    print("Erreur fatale: Le fichier 'mode_terminal.py' est introuvable ou illisible.")
    sys.exit(1)
mode_terminal = importlib.util.module_from_spec(spec)
sys.modules["mode_terminal"] = mode_terminal
spec.loader.exec_module(mode_terminal)

# Importer la fonction directement depuis le module chargé
try:
    lancer_mode_terminal = mode_terminal.lancer_mode_terminal 
except AttributeError:
    print("Erreur: La fonction 'lancer_mode_terminal' n'est pas définie dans mode_terminal.py.")
    sys.exit(1)


# Importation de la fonction du mode graphique (depuis partie_1/ui.py)
try:
    from interface.ui import lancer_interface_graphique, initialiser_structures_gui
except ImportError as e:
    print(f"Erreur: Impossible de charger l'interface graphique. {e}")
    sys.exit(1)


def menu_lancement():
    """Affiche le menu de sélection du mode d'exécution."""
    
    print("\n" + "#" * 50)
    print("    BIBLIOTHÈQUE NUMÉRIQUE - SÉLECTION DU MODE")
    print("#" * 50)
    print("Veuillez choisir votre mode d'exécution :")
    print("1. Mode Terminal (Console) - Toutes les options P1/P2")
    print("2. Interface Graphique (GUI) - Fonctionnalités P1 & P2")
    print("0. Quitter")
    print("#" * 50)

    choix = input("Entrez votre choix (0, 1 ou 2): ").strip()

    if choix == '1':
        print("\n🚀 Lancement du mode Terminal (Console)...")
        lancer_mode_terminal()
    elif choix == '2':
        print("\n🖼️ Lancement de l'Interface Graphique (Tkinter)...")
        structures = initialiser_structures_gui() 
        lancer_interface_graphique(structures)
    elif choix == '0':
        print("\n👋 Au revoir ! Programme terminé.")
    else:
        print("\n❌ Choix invalide. Veuillez relancer et choisir 1, 2 ou 0.")

if __name__ == "__main__":
    menu_lancement()