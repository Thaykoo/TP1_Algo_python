
from abc import ABC, abstractmethod
from typing import List

try:
    from ..partie_1.document import Document
except ImportError:
    from partie_1.document import Document


class HashSearchAlgorithm(ABC):
    """
    Classe abstraite de base pour les algorithmes de recherche dans la HashTable.
    Implémente le Strategy Pattern.
    """
    
    def __init__(self):
        self.complexity = "O(n)"
    
    @abstractmethod
    def search(self, hash_table, terme: str):
        """
        Méthode abstraite de recherche.
        
        Args:
            hash_table: La table de hachage
            terme: Le terme à rechercher
            
        Returns:
            Document(s) trouvé(s) ou liste vide
        """
        pass
    
    def get_complexity(self) -> str:
        """Retourne la complexité de l'algorithme."""
        return self.complexity


class SearchByAuthorHash(HashSearchAlgorithm):
    """Recherche par auteur dans la HashTable (optimisé O(1))."""
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(1)"
    
    def search(self, hash_table, auteur: str) -> List[Document]:
        """
        Recherche tous les documents d'un auteur.
        Utilise la fonction de hachage pour un accès direct.
        
        Args:
            hash_table: La HashTable
            auteur: Le nom de l'auteur
            
        Returns:
            Liste des documents trouvés
        """
        return hash_table.search_by_author(auteur)


class SearchByTitleHash(HashSearchAlgorithm):
    """Recherche par titre dans la HashTable."""
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n)"
    
    def search(self, hash_table, titre: str) -> List[Document]:
        """
        Recherche des documents par titre.
        Parcours complet nécessaire car la table est indexée par auteur.
        
        Args:
            hash_table: La HashTable
            titre: Le titre à rechercher
            
        Returns:
            Liste des documents trouvés
        """
        return hash_table.search_by_title(titre)


class SearchByKeywordsHash(HashSearchAlgorithm):
    """Recherche par mots-clés dans la HashTable."""
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n)"
    
    def search(self, hash_table, mot_cle: str) -> List[Document]:
        """
        Recherche tous les documents contenant un mot-clé.
        
        Args:
            hash_table: La HashTable
            mot_cle: Le mot-clé à rechercher
            
        Returns:
            Liste des documents trouvés
        """
        return hash_table.search_by_keywords(mot_cle)


class SearchAdvancedHash(HashSearchAlgorithm):
    """Recherche avancée dans tous les champs de la HashTable."""
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n)"
    
    def search(self, hash_table, terme: str) -> List[Document]:
        """
        Recherche dans tous les champs (titre, auteur, mots-clés).
        
        Args:
            hash_table: La HashTable
            terme: Le terme à rechercher
            
        Returns:
            Liste des documents trouvés
        """
        return hash_table.search_advanced(terme)


class SearchMultipleCriteriaHash(HashSearchAlgorithm):
    """Recherche avec plusieurs critères dans la HashTable."""
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n)"
    
    def search(self, hash_table, titre: str = "", auteur: str = "", mot_cle: str = "") -> List[Document]:
        """
        Recherche avec plusieurs critères optionnels.
        
        Args:
            hash_table: La HashTable
            titre: Titre à rechercher (optionnel)
            auteur: Auteur à rechercher (optionnel)
            mot_cle: Mot-clé à rechercher (optionnel)
            
        Returns:
            Liste des documents correspondant aux critères
        """
        resultats = []
        
        for bucket in hash_table.table:
            for document in bucket.items:
                correspondance = True
                
                if titre and titre.lower() not in document.titre.lower():
                    correspondance = False
                
                if auteur and auteur.lower() not in document.auteur.lower():
                    correspondance = False
                
                if mot_cle:
                    mot_trouve = False
                    for mc in document.mots_cles:
                        if mot_cle.lower() in mc.lower():
                            mot_trouve = True
                            break
                    if not mot_trouve:
                        correspondance = False
                
                if correspondance:
                    resultats.append(document)
        
        return resultats


def comparer_recherche_hash_vs_liste(Document_Classe, tailles: List[int] = None):
    """
    Compare les performances de recherche entre HashTable et liste.
    
    Args:
        Document_Classe: La classe Document
        tailles: Liste des tailles à tester
        
    Returns:
        Dictionnaire avec les résultats de comparaison
    """
    import time
    import random
    
    if tailles is None:
        tailles = [100, 500, 1000, 5000, 10000]
    
    resultats = []
    
    print("\n" + "=" * 80)
    print("COMPARAISON HASHTABLE vs LISTE - Recherche par auteur")
    print("=" * 80)
    
    for taille in tailles:
        auteurs = [f"Auteur-{i:03d}" for i in range(min(100, taille // 10))]
        documents = [Document_Classe(f"Titre-{i}", random.choice(auteurs), "") 
                     for i in range(taille)]
        
        from .hashing import HashTable
        ht = HashTable(size=max(50, taille // 20))
        for doc in documents:
            ht.insert(doc)
        
        auteurs_test = random.sample(auteurs, min(10, len(auteurs)))
        
        start = time.time()
        for auteur in auteurs_test:
            [doc for doc in documents if auteur.lower() in doc.auteur.lower()]
        temps_liste = time.time() - start
        
        start = time.time()
        for auteur in auteurs_test:
            ht.search_by_author(auteur)
        temps_hash = time.time() - start
        
        gain = temps_liste / temps_hash if temps_hash > 0 else 0
        
        resultat = {
            'taille': taille,
            'temps_liste': temps_liste,
            'temps_hash': temps_hash,
            'gain': gain
        }
        resultats.append(resultat)
        
        print(f"\nTaille: {taille} documents")
        print(f"  Liste (O(n)):       {temps_liste:.6f}s")
        print(f"  HashTable (O(1)):   {temps_hash:.6f}s")
        print(f"  Gain:               {gain:.2f}x plus rapide")
    
    print("\n" + "=" * 80)
    return resultats


def analyser_distribution_hash(hash_table):
    """
    Analyse et affiche la distribution des documents dans les buckets.
    
    Args:
        hash_table: La table de hachage à analyser
        
    Returns:
        Dictionnaire avec les statistiques de distribution
    """
    distribution = [len(bucket.items) for bucket in hash_table.table]
    
    buckets_vides = distribution.count(0)
    buckets_utilises = len(distribution) - buckets_vides
    total_docs = sum(distribution)
    max_docs = max(distribution) if distribution else 0
    min_docs_non_vide = min([d for d in distribution if d > 0]) if buckets_utilises > 0 else 0
    moyenne = total_docs / buckets_utilises if buckets_utilises > 0 else 0
    
    collisions = sum(1 for d in distribution if d > 1)
    
    print("\n" + "=" * 70)
    print("ANALYSE DE LA DISTRIBUTION DE LA HASHTABLE")
    print("=" * 70)
    print(f"Taille de la table:      {len(distribution)}")
    print(f"Total documents:         {total_docs}")
    print(f"Buckets utilisés:        {buckets_utilises} ({buckets_utilises/len(distribution)*100:.1f}%)")
    print(f"Buckets vides:           {buckets_vides} ({buckets_vides/len(distribution)*100:.1f}%)")
    print(f"Documents/bucket (moy):  {moyenne:.2f}")
    print(f"Documents max (bucket):  {max_docs}")
    print(f"Documents min (non-vide): {min_docs_non_vide}")
    print(f"Buckets avec collisions: {collisions}")
    print(f"Facteur de charge:       {total_docs/len(distribution):.2f}")
    print("=" * 70)
    
    return {
        'taille_table': len(distribution),
        'total_documents': total_docs,
        'buckets_utilises': buckets_utilises,
        'buckets_vides': buckets_vides,
        'moyenne_par_bucket': moyenne,
        'max_par_bucket': max_docs,
        'collisions': collisions,
        'facteur_charge': total_docs / len(distribution) if len(distribution) > 0 else 0
    }

