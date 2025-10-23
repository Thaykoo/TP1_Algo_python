
from abc import ABC, abstractmethod
from typing import List, Optional

try:
    from ..partie_1.document import Document
except ImportError:
    from partie_1.document import Document


class BSTSearchAlgorithm(ABC):
    """
    Classe abstraite de base pour les algorithmes de recherche dans le BST.
    Implémente le Strategy Pattern.
    """
    
    def __init__(self):
        self.complexity = "O(n)"
    
    @abstractmethod
    def search(self, bst, terme: str):
        """
        Méthode abstraite de recherche.
        
        Args:
            bst: L'arbre binaire de recherche
            terme: Le terme à rechercher
            
        Returns:
            Document(s) trouvé(s) ou None/liste vide
        """
        pass
    
    def get_complexity(self) -> str:
        """Retourne la complexité de l'algorithme."""
        return self.complexity


class SearchByTitleBST(BSTSearchAlgorithm):
    """Recherche par titre exact dans le BST (optimisé)."""
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(log n)"
    
    def search(self, bst, titre: str) -> Optional[Document]:
        """
        Recherche un document par titre exact.
        Utilise la structure du BST pour une recherche optimisée.
        
        Args:
            bst: Le BST
            titre: Le titre exact à rechercher
            
        Returns:
            Le document trouvé ou None
        """
        return bst.search(titre)


class SearchByAuthorBST(BSTSearchAlgorithm):
    """Recherche par auteur dans le BST."""
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n)"
    
    def search(self, bst, auteur: str) -> List[Document]:
        """
        Recherche tous les documents d'un auteur.
        Parcours complet de l'arbre nécessaire.
        
        Args:
            bst: Le BST
            auteur: Le nom de l'auteur (recherche partielle)
            
        Returns:
            Liste des documents trouvés
        """
        return bst.search_by_author(auteur)


class SearchByKeywordsBST(BSTSearchAlgorithm):
    """Recherche par mots-clés dans le BST."""
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n)"
    
    def search(self, bst, mot_cle: str) -> List[Document]:
        """
        Recherche tous les documents contenant un mot-clé.
        
        Args:
            bst: Le BST
            mot_cle: Le mot-clé à rechercher
            
        Returns:
            Liste des documents trouvés
        """
        return bst.search_by_keywords(mot_cle)


class SearchAdvancedBST(BSTSearchAlgorithm):
    """Recherche avancée dans tous les champs du BST."""
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n)"
    
    def search(self, bst, terme: str) -> List[Document]:
        """
        Recherche dans tous les champs (titre, auteur, mots-clés).
        
        Args:
            bst: Le BST
            terme: Le terme à rechercher
            
        Returns:
            Liste des documents trouvés
        """
        return bst.search_advanced(terme)


class SearchMultipleCriteriaBST(BSTSearchAlgorithm):
    """Recherche avec plusieurs critères dans le BST."""
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n)"
    
    def search(self, bst, titre: str = "", auteur: str = "", mot_cle: str = "") -> List[Document]:
        """
        Recherche avec plusieurs critères optionnels.
        
        Args:
            bst: Le BST
            titre: Titre à rechercher (optionnel)
            auteur: Auteur à rechercher (optionnel)
            mot_cle: Mot-clé à rechercher (optionnel)
            
        Returns:
            Liste des documents correspondant aux critères
        """
        resultats = []
        
        def recherche_recursive(node):
            if node is None:
                return
            
            document = node.document
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
            
            recherche_recursive(node.left)
            recherche_recursive(node.right)
        
        recherche_recursive(bst.root)
        return resultats


def comparer_recherche_bst_vs_liste(Document_Classe, tailles: List[int] = None):
    """
    Compare les performances de recherche entre BST et liste.
    
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
    print("COMPARAISON BST vs LISTE - Recherche par titre")
    print("=" * 80)
    
    for taille in tailles:
        titres = [f"Titre-{i:05d}" for i in range(taille)]
        random.shuffle(titres)
        documents = [Document_Classe(titre, "Auteur", "") for titre in titres]
        
        from .bst import BinarySearchTree
        bst = BinarySearchTree()
        for doc in documents:
            bst.insert(doc)
        
        titres_test = random.sample(titres, min(100, taille))
        
        start = time.time()
        for titre in titres_test:
            for doc in documents:
                if doc.titre.lower() == titre.lower():
                    break
        temps_liste = time.time() - start
        
        start = time.time()
        for titre in titres_test:
            bst.search(titre)
        temps_bst = time.time() - start
        
        gain = temps_liste / temps_bst if temps_bst > 0 else 0
        
        resultat = {
            'taille': taille,
            'temps_liste': temps_liste,
            'temps_bst': temps_bst,
            'gain': gain
        }
        resultats.append(resultat)
        
        print(f"\nTaille: {taille} documents")
        print(f"  Liste (O(n)):    {temps_liste:.6f}s")
        print(f"  BST (O(log n)):  {temps_bst:.6f}s")
        print(f"  Gain:            {gain:.2f}x plus rapide")
    
    print("\n" + "=" * 80)
    return resultats

