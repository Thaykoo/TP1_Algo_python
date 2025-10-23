# Fichier : partie_2/bst.py
# Implémentation de l'Arbre Binaire de Recherche (Binary Search Tree - BST)

import time
import random
from copy import deepcopy

# --- Dépendance de la Partie 1 pour la structure ---
# Nous supposons que la classe Document est accessible via l'import relatif
try:
    from ..partie_1.document import Document
except ImportError:
    # Fallback pour le test si la structure de dossier est plate
    class Document:
        def __init__(self, titre, auteur="Inconnu", mots_cles=""):
            self.titre = titre
            self.auteur = auteur
            self.mots_cles = mots_cles
        def __str__(self):
            return f"Titre: '{self.titre}' | Auteur: {self.auteur}"

# ==============================================================================
# 1. Classes Node et BinarySearchTree
# ==============================================================================

class Node:
    """Représente un nœud dans l'Arbre Binaire de Recherche."""
    def __init__(self, document):
        self.document = document  # Stocke l'objet Document
        self.left = None          # Fils gauche
        self.right = None         # Fils droit

class BinarySearchTree:
    """Implémentation du BST pour stocker des documents triés par titre."""
    def __init__(self):
        self.root = None
        self.size = 0

    # ----------------------------------------------------------------------
    # 2. Insertion de Documents
    # ----------------------------------------------------------------------

    def insert(self, document):
        """Insère un nouveau document dans l'arbre."""
        if self.root is None:
            self.root = Node(document)
            self.size += 1
        else:
            self.root = self._insert_recursif(self.root, document)

    def _insert_recursif(self, current_node, document):
        # La clé de tri est le titre, normalisé en minuscules pour la comparaison
        titre_cle = document.titre.lower()
        current_cle = current_node.document.titre.lower()

        if titre_cle < current_cle:
            if current_node.left is None:
                current_node.left = Node(document)
                self.size += 1
            else:
                self._insert_recursif(current_node.left, document)
        elif titre_cle >= current_cle: # Gère les titres identiques en les mettant à droite
            if current_node.right is None:
                current_node.right = Node(document)
                self.size += 1
            else:
                self._insert_recursif(current_node.right, document)
        
        return current_node # Retourne le nœud courant (inutile pour Python mais bonne pratique)
            
    # ----------------------------------------------------------------------
    # 3. Recherche de Documents
    # ----------------------------------------------------------------------

    def search(self, titre):
        """Recherche un document par titre dans le BST."""
        titre_cle = titre.lower()
        return self._search_recursif(self.root, titre_cle)

    def _search_recursif(self, current_node, titre_cle):
        """Méthode de recherche récursive. Complexité : O(log n) en moyenne."""
        if current_node is None:
            return None # Document non trouvé

        current_cle = current_node.document.titre.lower()

        if titre_cle == current_cle:
            return current_node.document
        elif titre_cle < current_cle:
            return self._search_recursif(current_node.left, titre_cle)
        else: # titre_cle > current_cle
            return self._search_recursif(current_node.right, titre_cle)

    # ----------------------------------------------------------------------
    # 4. Parcours In-order
    # ----------------------------------------------------------------------

    def in_order_traversal(self):
        """Effectue un parcours in-order et retourne la liste des documents triés."""
        resultats = []
        self._in_order_recursif(self.root, resultats)
        return resultats

    def _in_order_recursif(self, node, resultats):
        """Méthode de parcours récursive : Gauche -> Racine -> Droite."""
        if node:
            self._in_order_recursif(node.left, resultats)
            resultats.append(node.document)
            self._in_order_recursif(node.right, resultats)
            
    # ----------------------------------------------------------------------
    # 5. Suppression de Documents (Ajout demandé)
    # ----------------------------------------------------------------------

    def delete(self, titre):
        """Supprime un document par titre de l'arbre."""
        titre_cle = titre.lower()
        original_size = self.size
        
        self.root = self._delete_recursif(self.root, titre_cle)
        
        if self.size < original_size:
            return True # Suppression réussie
        return False # Document non trouvé

    def _delete_recursif(self, node, titre_cle):
        if node is None:
            return node

        current_cle = node.document.titre.lower()

        # 1. Parcourir pour trouver le nœud
        if titre_cle < current_cle:
            node.left = self._delete_recursif(node.left, titre_cle)
        elif titre_cle > current_cle:
            node.right = self._delete_recursif(node.right, titre_cle)
        else:
            # 2. Le nœud à supprimer est trouvé
            
            # Cas 1 : Nœud avec au plus un enfant
            if node.left is None:
                self.size -= 1
                return node.right
            elif node.right is None:
                self.size -= 1
                return node.left

            # Cas 2 : Nœud avec deux enfants
            # Trouver le successeur immédiat (le plus petit dans le sous-arbre droit)
            temp = self._trouver_min_node(node.right)
            
            # Remplacer le contenu du nœud courant par celui du successeur
            node.document = temp.document
            
            # Supprimer le successeur (le size est décrémenté dans l'appel récursif)
            node.right = self._delete_recursif(node.right, temp.document.titre.lower())
            
        return node

    def _trouver_min_node(self, node):
        """Trouve le nœud ayant la clé la plus petite dans un sous-arbre."""
        current = node
        while current.left is not None:
            current = current.left
        return current
        
# ==============================================================================
# 6. Comparaison des Performances de Recherche (Reste inchangé)
# ==============================================================================

def recherche_sequentielle(bibliotheque_list, titre_cle):
    """
    Algorithme de Recherche Séquentielle (O(n)) pour la comparaison.
    (Simule la fonction de la Partie 1)
    """
    titre_cle = titre_cle.lower()
    for document in bibliotheque_list:
        if document.titre.lower() == titre_cle:
            return document
    return None

def comparer_recherche_performance(Document_Classe, list_size=10000):
    """
    Compare le temps de recherche séquentielle (list) vs. BST.
    """
    print("\n" + "="*70)
    print("        COMPARAISON DES PERFORMANCES DE RECHERCHE")
    print(f"        Taille de l'échantillon : {list_size} documents")
    print("="*70)

    # --- Préparation des Données ---
    titres_uniques = [f"Titre-{i}" for i in range(list_size)]
    random.shuffle(titres_uniques)
    donnees = [Document_Classe(titre, "Auteur", "") for titre in titres_uniques]

    # Construction des structures
    bibliotheque_list = donnees # La liste
    bst = BinarySearchTree()
    for doc in donnees:
        bst.insert(doc)

    # Titres à rechercher (pour un test équitable)
    # On choisit 100 titres aléatoires parmi les existants
    titres_a_chercher = random.sample(titres_uniques, 100) 
    
    # --- Mesure de la Recherche Séquentielle (O(n)) ---
    start_time_seq = time.time()
    for titre in titres_a_chercher:
        recherche_sequentielle(bibliotheque_list, titre)
    end_time_seq = time.time()
    temps_sequentiel = (end_time_seq - start_time_seq) / len(titres_a_chercher)
    
    # --- Mesure de la Recherche BST (O(log n)) ---
    start_time_bst = time.time()
    for titre in titres_a_chercher:
        bst.search(titre)
    end_time_bst = time.time()
    temps_bst = (end_time_bst - start_time_bst) / len(titres_a_chercher)
    
    print(f"| {'Algorithme':<30} | {'Complexité (Moyenne)':<25} | {'Temps Moyen par Recherche (s)':<15} |")
    print("-" * 70)
    print(f"| {'Recherche Séquentielle (Partie 1)':<30} | {'O(n)':<25} | {temps_sequentiel:<25.8f} |")
    print(f"| {'Recherche BST (Partie 2)':<30} | {'O(log n)':<25} | {temps_bst:<25.8f} |")
    print("-" * 70)

    gain = (temps_sequentiel / temps_bst) if temps_bst > 0 else float('inf')
    print(f"\nConclusion : Le BST est environ {gain:.2f} fois plus rapide que la recherche séquentielle.")