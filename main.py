
"""
Point d'entrée principal de l'application
Permet de choisir entre le mode terminal et l'interface graphique
"""

import sys
import os

sys.path.append(os.path.dirname(__file__))

try:
    from interface.ui import lancer_interface_graphique, initialiser_structures_gui
except ImportError as e:
    print(f"Erreur: Impossible de charger l'interface graphique. {e}")
    sys.exit(1)


def lancer_mode_terminal():
    """Lance le mode terminal"""
    from mode_terminal import main as terminal_main
    terminal_main()


def menu_lancement():
    """Affiche le menu de sélection du mode d'exécution"""
    print("\n" + "=" * 60)
    print(f"{'BIBLIOTHÈQUE NUMÉRIQUE - SÉLECTION DU MODE':^60}")
    print("=" * 60)
    print("\nVeuillez choisir votre mode d'exécution :")
    print("\n  1. 🖥️  Mode Terminal (Console)")
    print("  2. 🖼️  Interface Graphique (Tkinter)")
    print("  0. 🚪 Quitter")
    print("\n" + "=" * 60)

    choix = input("\nEntrez votre choix (0, 1 ou 2): ").strip()

    if choix == '1':
        print("\n🚀 Lancement du mode Terminal...\n")
        lancer_mode_terminal()
    elif choix == '2':
        print("\n🚀 Lancement de l'Interface Graphique...\n")
        structures = initialiser_structures_gui()
        lancer_interface_graphique(structures)
    elif choix == '0':
        print("\n👋 Au revoir ! Programme terminé.\n")
    else:
        print("\n❌ Choix invalide. Veuillez relancer et choisir 1, 2 ou 0.\n")


if __name__ == "__main__":
    menu_lancement()