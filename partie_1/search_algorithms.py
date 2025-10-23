
from abc import ABC, abstractmethod
from typing import List


class SearchAlgorithm(ABC):
    """Classe abstraite pour les algorithmes de recherche."""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.complexity = "O(?)"
    
    @abstractmethod
    def search(self, documents: List, terme: str) -> List:
        """
        Recherche des documents selon un critère.
        
        Args:
            documents: Liste de documents à rechercher
            terme: Terme de recherche
            
        Returns:
            Liste des documents correspondants
        """
        pass
    
    def __str__(self) -> str:
        return f"{self.name} ({self.complexity})"


class SearchByTitle(SearchAlgorithm):
    """
    Recherche séquentielle par titre exact.
    Complexité : O(n).
    """
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n)"
    
    def search(self, documents: List, terme: str) -> List:
        """Recherche par titre exact (insensible à la casse)."""
        terme_lower = terme.lower()
        return [doc for doc in documents if doc.titre.lower() == terme_lower]


class SearchByTitlePartial(SearchAlgorithm):
    """
    Recherche séquentielle par titre partiel.
    Complexité : O(n).
    """
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n)"
    
    def search(self, documents: List, terme: str) -> List:
        """Recherche par titre partiel (insensible à la casse)."""
        terme_lower = terme.lower()
        return [doc for doc in documents if terme_lower in doc.titre.lower()]


class SearchByAuthor(SearchAlgorithm):
    """
    Recherche séquentielle par auteur.
    Complexité : O(n).
    """
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n)"
    
    def search(self, documents: List, terme: str) -> List:
        """Recherche par auteur (insensible à la casse)."""
        terme_lower = terme.lower()
        return [doc for doc in documents if terme_lower in doc.auteur.lower()]


class SearchByKeywords(SearchAlgorithm):
    """
    Recherche séquentielle par mots-clés.
    Complexité : O(n).
    """
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n)"
    
    def search(self, documents: List, terme: str) -> List:
        """Recherche par mots-clés (insensible à la casse)."""
        terme_lower = terme.lower()
        resultats = []
        
        for doc in documents:
            for mot_cle in doc.mots_cles:
                if terme_lower in mot_cle.lower():
                    resultats.append(doc)
                    break
        
        return resultats


class SearchAdvanced(SearchAlgorithm):
    """
    Recherche avancée dans tous les champs (titre, auteur, mots-clés).
    Complexité : O(n).
    """
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n)"
    
    def search(self, documents: List, terme: str) -> List:
        """Recherche dans tous les champs."""
        terme_lower = terme.lower()
        resultats = []
        
        for doc in documents:
            if terme_lower in doc.titre.lower():
                resultats.append(doc)
                continue
            
            if terme_lower in doc.auteur.lower():
                resultats.append(doc)
                continue
            
            for mot_cle in doc.mots_cles:
                if terme_lower in mot_cle.lower():
                    resultats.append(doc)
                    break
        
        return resultats


class SearchMultiCriteria(SearchAlgorithm):
    """
    Recherche multi-critères avec filtres personnalisés.
    Complexité : O(n).
    """
    
    def __init__(self, search_title: bool = False, 
                 search_author: bool = False, 
                 search_keywords: bool = False):
        """
        Initialise la recherche multi-critères.
        
        Args:
            search_title: Rechercher dans les titres
            search_author: Rechercher dans les auteurs
            search_keywords: Rechercher dans les mots-clés
        """
        super().__init__()
        self.complexity = "O(n)"
        self.search_title = search_title
        self.search_author = search_author
        self.search_keywords = search_keywords
    
    def search(self, documents: List, terme: str) -> List:
        """Recherche selon les critères sélectionnés."""
        terme_lower = terme.lower()
        resultats = []
        
        for doc in documents:
            found = False
            
            if self.search_title and terme_lower in doc.titre.lower():
                found = True
            
            if not found and self.search_author and terme_lower in doc.auteur.lower():
                found = True
            
            if not found and self.search_keywords:
                for mot_cle in doc.mots_cles:
                    if terme_lower in mot_cle.lower():
                        found = True
                        break
            
            if found:
                resultats.append(doc)
        
        return resultats

