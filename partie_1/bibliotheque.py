
from typing import List, Optional
from .document import Document


class Bibliotheque:
    """
    Classe pour gérer une collection de documents.
    Fournit des méthodes pour ajouter, supprimer, trier et rechercher des documents.
    """
    
    def __init__(self, documents: Optional[List[Document]] = None):
        """
        Initialise une nouvelle bibliothèque.
        
        Args:
            documents: Liste optionnelle de documents initiaux
        """
        self._documents = documents if documents is not None else []
    
    @property
    def documents(self) -> List[Document]:
        """Retourne la liste des documents (lecture seule)."""
        return self._documents.copy()
    
    @property
    def size(self) -> int:
        """Retourne le nombre de documents dans la bibliothèque."""
        return len(self._documents)
    
    def is_empty(self) -> bool:
        """Vérifie si la bibliothèque est vide."""
        return len(self._documents) == 0
    
    def add_document(self, document: Document) -> None:
        """
        Ajoute un document à la bibliothèque.
        
        Args:
            document: Le document à ajouter
        """
        self._documents.append(document)
    
    def remove_document(self, titre: str) -> bool:
        """
        Supprime un document par son titre.
        
        Args:
            titre: Le titre du document à supprimer
            
        Returns:
            True si le document a été supprimé, False sinon
        """
        for i, doc in enumerate(self._documents):
            if doc.titre.lower() == titre.lower():
                self._documents.pop(i)
                return True
        return False
    
    def get_document_by_title(self, titre: str) -> Optional[Document]:
        """
        Récupère un document par son titre.
        
        Args:
            titre: Le titre du document à rechercher
            
        Returns:
            Le document trouvé ou None
        """
        for doc in self._documents:
            if doc.titre.lower() == titre.lower():
                return doc
        return None
    
    def clear(self) -> None:
        """Vide la bibliothèque de tous ses documents."""
        self._documents.clear()
    
    def sort(self, algorithm) -> None:
        """
        Trie la bibliothèque en utilisant l'algorithme spécifié.
        
        Args:
            algorithm: Instance d'une classe qui hérite de TriAlgorithm
        """
        algorithm.sort(self._documents)
    
    def search(self, algorithm, terme: str) -> List[Document]:
        """
        Recherche des documents en utilisant l'algorithme spécifié.
        
        Args:
            algorithm: Instance d'une classe qui hérite de SearchAlgorithm
            terme: Le terme de recherche
            
        Returns:
            Liste des documents trouvés
        """
        return algorithm.search(self._documents, terme)
    
    def __len__(self) -> int:
        """Retourne le nombre de documents."""
        return len(self._documents)
    
    def __iter__(self):
        """Permet d'itérer sur les documents."""
        return iter(self._documents)
    
    def __getitem__(self, index: int) -> Document:
        """Permet d'accéder aux documents par index."""
        return self._documents[index]
    
    def __str__(self) -> str:
        """Représentation textuelle de la bibliothèque."""
        if self.is_empty():
            return "Bibliothèque vide"
        
        result = f"Bibliothèque ({self.size} document(s)):\n"
        for i, doc in enumerate(self._documents, 1):
            result += f"  [{i}] {doc}\n"
        return result.rstrip()
    
    def __repr__(self) -> str:
        """Représentation pour debug."""
        return f"Bibliotheque(documents={len(self._documents)})"

