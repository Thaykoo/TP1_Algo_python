
import time
import random
from copy import deepcopy

try:
    from ..partie_1.document import Document
except ImportError:
    class Document:
        def __init__(self, titre, auteur="Inconnu", mots_cles=""):
            self.titre = titre
            self.auteur = auteur
            self.mots_cles = mots_cles
        def __str__(self):
            return f"Titre: '{self.titre}' | Auteur: {self.auteur}"


class Bucket:
    """Représente un seau (bucket) dans la table de hachage (gestion par chaînage)."""
    def __init__(self):
        self.items = []

class HashTable:
    """Table de Hachage simple indexant les Documents par Auteur."""
    def __init__(self, size=10):
        self.size = size
        self.table = [Bucket() for _ in range(self.size)]

    def _hash(self, key):
        """Fonction de hachage simple (modulo)."""
        return hash(key) % self.size

    def insert(self, document):
        """Insère un document en utilisant l'auteur comme clé."""
        key = document.auteur.lower()
        hash_index = self._hash(key)
        bucket = self.table[hash_index]
        bucket.items.append(document)

    def search_by_author(self, author_name):
        """
        Recherche tous les documents d'un auteur.
        Complexité: O(1) en moyenne.
        """
        key = author_name.lower()
        hash_index = self._hash(key)
        bucket = self.table[hash_index]
        
        resultats = []
        for doc in bucket.items:
            if key in doc.auteur.lower():
                resultats.append(doc)
        
        if not resultats:
            for bucket in self.table:
                for doc in bucket.items:
                    if key in doc.auteur.lower():
                        resultats.append(doc)
                
        return resultats

    def search_by_title(self, titre):
        """
        Recherche tous les documents par titre.
        Complexité: O(n) car on doit parcourir tous les buckets.
        """
        resultats = []
        for bucket in self.table:
            for doc in bucket.items:
                if titre.lower() in doc.titre.lower():
                    resultats.append(doc)
        return resultats

    def search_by_keywords(self, mot_cle):
        """
        Recherche tous les documents par mots-clés.
        Complexité: O(n) car on doit parcourir tous les buckets.
        """
        resultats = []
        for bucket in self.table:
            for doc in bucket.items:
                for mot in doc.mots_cles:
                    if mot_cle.lower() in mot.lower():
                        resultats.append(doc)
                        break
        return resultats

    def search_advanced(self, terme):
        """
        Recherche avancée dans tous les champs (titre, auteur, mots-clés).
        Complexité: O(n) car on doit parcourir tous les buckets.
        """
        resultats = []
        for bucket in self.table:
            for doc in bucket.items:
                if terme.lower() in doc.titre.lower():
                    resultats.append(doc)
                elif terme.lower() in doc.auteur.lower():
                    resultats.append(doc)
                else:
                    for mot_cle in doc.mots_cles:
                        if terme.lower() in mot_cle.lower():
                            resultats.append(doc)
                            break
        return resultats
        
    def populate_from_bst(self, bst):
        """Remplit la table de hachage à partir du BST (ou de la liste)."""
        if not bst.root:
            return
        
        documents = bst.in_order_traversal()
        for doc in documents:
            self.insert(doc)


def comparer_recherche_hachage(Document_Classe, list_size=10000, table_size=1000):
    """
    Compare le temps de recherche séquentielle (O(n)) vs. Hachage (O(1)).
    """
    print("\n" + "="*70)
    print("      COMPARAISON DES PERFORMANCES DE RECHERCHE O(n) vs O(1)")
    print(f"      Taille de l'échantillon : {list_size} documents")
    print("="*70)

    auteurs_uniques = [f"Auteur {i}" for i in range(100)]
    donnees = [Document_Classe(f"Titre-{i}", random.choice(auteurs_uniques), "") for i in range(list_size)]
    
    bibliotheque_list = donnees
    ht = HashTable(size=table_size)
    for doc in donnees:
        ht.insert(doc)

    auteurs_a_chercher = random.sample(auteurs_uniques, 10)
    
    start_time_seq = time.time()
    for auteur in auteurs_a_chercher:
        [doc for doc in donnees if doc.auteur.lower() == auteur.lower()]
    end_time_seq = time.time()
    temps_sequentiel = (end_time_seq - start_time_seq) / len(auteurs_a_chercher)
    
    start_time_hash = time.time()
    for auteur in auteurs_a_chercher:
        ht.search_by_author(auteur)
    end_time_hash = time.time()
    temps_hash = (end_time_hash - start_time_hash) / len(auteurs_a_chercher)
    
    print(f"| {'Algorithme':<30} | {'Complexité (Moyenne)':<25} | {'Temps Moyen par Recherche (s)':<15} |")
    print("-" * 70)
    print(f"| {'Recherche Séquentielle (Liste)':<30} | {'O(n)':<25} | {temps_sequentiel:<25.8f} |")
    print(f"| {'Recherche Hachage (HashTable)':<30} | {'O(1)':<25} | {temps_hash:<25.8f} |")
    print("-" * 70)

    gain = (temps_sequentiel / temps_hash) if temps_hash > 0 else float('inf')
    print(f"\nConclusion : La table de hachage est environ {gain:.2f} fois plus rapide pour la recherche par clé unique (Auteur).")