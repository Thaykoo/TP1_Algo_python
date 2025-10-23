# Fichier : mode_terminal.py
# Contient le menu d'exécution complet et la logique des Parties 1, 2 et 3.

import sys
import os
import time
import random
from copy import deepcopy

# --- Configuration pour les couleurs dans le terminal (Installation: pip install colorama) ---
# NOTE: Le code fonctionne sans colorama, mais sera moins esthétique.
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    VERT = Fore.GREEN
    ROUGE = Fore.RED
    BLEU = Fore.CYAN
    JAUNE = Fore.YELLOW
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL
except ImportError:
    VERT = ROUGE = BLEU = JAUNE = BOLD = RESET = ""

# Fixe le chemin pour les modules
sys.path.append(os.path.dirname(__file__))


# Importation des dépendances des Parties 1, 2, et 3
from partie_1 import (
    Document,
    trier_par_titre, 
    ajouter_document, 
    afficher_bibliotheque,
    tri_fusion,
    comparer_temps_execution,
)
from partie_1.gestionnaire import trier_par_titre as tri_insertion_func 
from partie_1.gestionnaire import rechercher_par_titre as recherche_sequentielle_func

from partie_2 import (
    BinarySearchTree,
    comparer_recherche_performance,
    supprimer_document_bst
)

from partie_3 import (
    HashTable,
    comparer_recherche_hachage
)

# Global : Déclaration des TROIS structures de données principales
bibliotheque_list = []
bst_bibliotheque = BinarySearchTree()
hash_table_bibliotheque = HashTable(size=50) 


# ----------------------------------------------------------------------
# Fonctions d'aide (Mise à jour pour l'esthétique)
# ----------------------------------------------------------------------

def afficher_documents_formatte(docs, titre_section):
    """Affiche une liste de documents de manière esthétique."""
    if not docs:
        print(f"\n{ROUGE}ℹ️ {titre_section} est actuellement vide.{RESET}")
        return
    
    print(f"\n{BOLD}{BLEU}--- {titre_section} (Total: {len(docs)} documents) ---{RESET}")
    print(f"{'-' * 70}")
    
    # En-têtes formatés
    print(f"{BOLD}{'#':<3}{'Titre':<35}{'Auteur':<30}{RESET}")
    print(f"{'-' * 70}")
    
    for i, doc in enumerate(docs):
        # Formatage pour éviter le dépassement
        titre = doc.titre[:34].ljust(34) + ('...' if len(doc.titre) > 34 else '')
        auteur = doc.auteur[:29].ljust(29) + ('...' if len(doc.auteur) > 29 else '')
        
        print(f"{VERT}{str(i+1):<3}{RESET}{BOLD}{titre}{RESET} {JAUNE}{auteur}{RESET}")
    print(f"{'-' * 70}")

def afficher_bibliotheque_list_formatte(list_struct):
    """Affiche la liste P1."""
    afficher_documents_formatte(list_struct, "LISTE PYTHON (ORDRE ACTUEL - P1)")

def afficher_bst_in_order_formatte(bst):
    """Affiche les documents triés du BST (P2)."""
    documents_tries = bst.in_order_traversal()
    afficher_documents_formatte(documents_tries, "BST (ORDRE IN-ORDER - AUTOMATIQUEMENT TRIÉ - P2)")

# ----------------------------------------------------------------------
# Fonctions de gestion (Mise à jour pour les 3 structures)
# ----------------------------------------------------------------------

def initialiser_structures():
    """Ajoute des documents initiaux aux TROIS structures pour les tests (Liste, BST, Hash)."""
    global bst_bibliotheque, bibliotheque_list, hash_table_bibliotheque
    
    docs = [
        Document("Le Petit Prince", "Antoine de Saint-Exupéry", "conte, amitié, philosophie"),
        Document("1984", "George Orwell", "dystopie, politique, surveillance"),
        Document("Zazie dans le Métro", "Raymond Queneau", "roman, humour, argot"),
        Document("Le Guide du voyageur galactique", "Douglas Adams", "science-fiction, humour"),
        Document("Le vieil homme et la mer", "Ernest Hemingway", "littérature, mer"),
        Document("Le vieil homme et la mer - Suite", "Ernest Hemingway", "littérature, mer")
    ]
    
    bibliotheque_list.extend(docs)
    for doc in docs:
        bst_bibliotheque.insert(doc)
        hash_table_bibliotheque.insert(doc)


def ajouter_document_general(list_struct, bst_struct, hash_struct, Document_Classe):
    """Saisit un nouveau document et l'ajoute aux TROIS structures."""
    print(f"\n{BOLD}{BLEU}--- Ajout d'un nouveau document ---{RESET}")
    titre = input("   Entrez le titre du document: ").strip()
    auteur = input("   Entrez l'auteur du document: ").strip()
    mots_cles_str = input("   Entrez les mots-clés (séparés par des virgules): ").strip()

    if titre and auteur:
        nouveau_doc = Document_Classe(titre, auteur, mots_cles_str)
        list_struct.append(nouveau_doc)
        bst_struct.insert(nouveau_doc)
        hash_struct.insert(nouveau_doc)
        print(f"\n{VERT}✅ Document '{titre}' ajouté aux trois structures avec succès.{RESET}")
    else:
        print(f"\n{ROUGE}❌ Le titre et l'auteur sont obligatoires. Annulation de l'ajout.{RESET}")


def rechercher_document_bst(bst):
    """Recherche un document par titre dans le BST (P2)."""
    if bst.root is None:
        print(f"\n{ROUGE}ℹ️ Le BST est vide, aucune recherche possible.{RESET}")
        return

    terme_recherche = input(f"\n{BOLD}Entrez le titre à rechercher (BST): {RESET}").strip()
    resultat = bst.search(terme_recherche)

    if resultat:
        print(f"\n{VERT}🎉 Résultat trouvé (Recherche BST O(log n)):{RESET}")
        print(f"- {resultat}")
    else:
        print(f"\n{ROUGE}😞 Aucun document trouvé avec le titre '{terme_recherche}'.{RESET}")


def rechercher_auteur_hachage(ht):
    """Recherche tous les documents par auteur via la Table de Hachage."""
    auteur_recherche = input(f"\n{BOLD}Entrez le nom de l'Auteur à rechercher (O(1)): {RESET}").strip()
    
    resultats = ht.search_by_author(auteur_recherche)
    
    if resultats:
        print(f"\n{VERT}🎉 {len(resultats)} Résultat(s) trouvé(s) pour '{auteur_recherche}' (Recherche Hachage O(1)):{RESET}")
        for doc in resultats:
            print(f"- {doc}")
    else:
        print(f"\n{ROUGE}😞 Aucun document trouvé pour l'auteur '{auteur_recherche}'.{RESET}")


# ----------------------------------------------------------------------
# Fonction de lancement du Mode Terminal (Menu Principal)
# ----------------------------------------------------------------------

def lancer_mode_terminal():
    """Contient le menu d'exécution en ligne de commande."""
    
    global bst_bibliotheque, bibliotheque_list, hash_table_bibliotheque
    initialiser_structures()
    
    while True:
        print(f"\n{BOLD}{BLEU}{'='*75}{RESET}")
        print(f"{BOLD}{BLEU}{' '*15}GESTION DE BIBLIOTHÈQUE NUMÉRIQUE - CONSOLE{RESET}")
        print(f"{BOLD}{BLEU}{'='*75}{RESET}")
        
        print(f"{BOLD}{JAUNE}--- 1. PARTIE 1 : FONDATIONS (LISTE PYTHON) ---{RESET}")
        print(" 1. Ajouter un document (Aux trois structures)")
        print(" 2. Trier la LISTE (Tri Insertion O(n²))")
        print(" 3. Rechercher un document dans la LISTE (Recherche Séquentielle O(n))")
        print(" 4. Afficher la LISTE")
        
        print(f"{BOLD}{JAUNE}--- 2. PARTIE 2 : OPTIMISATION (ARBRE BST) ---{RESET}")
        print(" 5. Rechercher un document dans le BST (Recherche BST O(log n))")
        print(" 6. Afficher les documents triés du BST (Parcours In-order)")
        print(" 7. Supprimer un document du BST")
        
        print(f"{BOLD}{JAUNE}--- 3. PARTIE 3 : INDEXATION (TABLE DE HACHAGE) ---{RESET}")
        print(" 8. Rechercher par Auteur (Hachage O(1))")
        
        print(f"{BOLD}{JAUNE}--- 4. COMPARAISONS ET SUPPLEMENTS ---{RESET}")
        print(" 9. Comparer Tri Insertion vs. Tri Fusion")
        print(" 10. Comparer Recherche Séquentielle vs. Recherche BST")
        print(" 11. Comparer Recherche Séquentielle vs. Hachage")
        
        print(f"\n{BOLD} 0. Retour au Menu de Lancement{RESET}")
        print(f"{BOLD}{BLEU}{'='*75}{RESET}")

        choix = input(f"{BOLD}Entrez votre choix (0-11): {RESET}").strip()

        if choix == '1':
            ajouter_document_general(bibliotheque_list, bst_bibliotheque, hash_table_bibliotheque, Document) 
        
        elif choix == '2':
            trier_par_titre(bibliotheque_list)
            print(f"\n{VERT}✅ Liste triée par Tri Insertion.{RESET}")
        
        elif choix == '3':
            recherche_sequentielle_func(bibliotheque_list)
        
        elif choix == '4':
            afficher_bibliotheque_list_formatte(bibliotheque_list)
            
        elif choix == '5':
            rechercher_document_bst(bst_bibliotheque)
            
        elif choix == '6':
            afficher_bst_in_order_formatte(bst_bibliotheque)
        
        elif choix == '7':
            supprimer_document_bst(bst_bibliotheque)
            
        elif choix == '8':
            rechercher_auteur_hachage(hash_table_bibliotheque)
            
        elif choix == '9':
            comparer_temps_execution(Document, tri_insertion_func, tri_fusion)
        
        elif choix == '10':
            comparer_recherche_performance(Document, list_size=20000)
        
        elif choix == '11':
            comparer_recherche_hachage(Document, list_size=50000)
        
        elif choix == '0':
            break
        
        else:
            print(f"\n{ROUGE}❌ Choix invalide. Veuillez entrer un numéro entre 0 et 11.{RESET}")