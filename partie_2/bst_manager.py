
from .bst import BinarySearchTree, Node
from typing import List, Optional, Dict, Any
import time

try:
    from ..partie_1.document import Document
except ImportError:
    from partie_1.document import Document


class BSTManager:
    """
    Gestionnaire principal pour le BST (Facade Pattern).
    Simplifie l'utilisation du BST et fournit une interface cohérente.
    """
    
    def __init__(self, bst: Optional[BinarySearchTree] = None):
        """
        Initialise le gestionnaire avec un BST existant ou en crée un nouveau.
        
        Args:
            bst: Un BST existant (optionnel)
        """
        self.bst = bst if bst is not None else BinarySearchTree()
    
    
    def ajouter_document(self, titre: str, auteur: str, mots_cles: str) -> bool:
        """
        Ajoute un nouveau document au BST.
        
        Args:
            titre: Le titre du document
            auteur: L'auteur du document
            mots_cles: Les mots-clés (séparés par des virgules)
            
        Returns:
            True si l'ajout a réussi
        """
        try:
            document = Document(titre, auteur, mots_cles)
            self.bst.insert(document)
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout : {e}")
            return False
    
    def supprimer_document(self, titre: str) -> bool:
        """
        Supprime un document du BST par son titre.
        
        Args:
            titre: Le titre du document à supprimer
            
        Returns:
            True si la suppression a réussi
        """
        return self.bst.delete(titre)
    
    def rechercher_par_titre(self, titre: str) -> Optional[Document]:
        """
        Recherche un document par son titre exact.
        
        Args:
            titre: Le titre à rechercher
            
        Returns:
            Le document trouvé ou None
        """
        return self.bst.search(titre)
    
    def rechercher_par_auteur(self, auteur: str) -> List[Document]:
        """
        Recherche tous les documents d'un auteur.
        
        Args:
            auteur: Le nom de l'auteur (recherche partielle)
            
        Returns:
            Liste des documents trouvés
        """
        return self.bst.search_by_author(auteur)
    
    def rechercher_par_mots_cles(self, mot_cle: str) -> List[Document]:
        """
        Recherche tous les documents contenant un mot-clé.
        
        Args:
            mot_cle: Le mot-clé à rechercher
            
        Returns:
            Liste des documents trouvés
        """
        return self.bst.search_by_keywords(mot_cle)
    
    def rechercher_avancee(self, terme: str) -> List[Document]:
        """
        Recherche avancée dans tous les champs.
        
        Args:
            terme: Le terme à rechercher
            
        Returns:
            Liste des documents trouvés
        """
        return self.bst.search_advanced(terme)
    
    
    def obtenir_documents_tries(self) -> List[Document]:
        """
        Retourne tous les documents triés par titre.
        
        Returns:
            Liste des documents triés
        """
        return self.bst.in_order_traversal()
    
    def afficher_bst(self) -> str:
        """
        Retourne une représentation textuelle de tous les documents triés.
        
        Returns:
            Chaîne formatée avec tous les documents
        """
        documents = self.obtenir_documents_tries()
        
        if not documents:
            return "📚 Le BST est vide."
        
        resultat = [f"📚 BST - {self.bst.size} document(s) :\n"]
        resultat.append("=" * 70)
        
        for i, doc in enumerate(documents, 1):
            resultat.append(f"{i}. {doc}")
        
        resultat.append("=" * 70)
        return "\n".join(resultat)
    
    def get_statistiques(self) -> Dict[str, Any]:
        """
        Retourne des statistiques sur le BST.
        
        Returns:
            Dictionnaire avec les statistiques
        """
        documents = self.obtenir_documents_tries()
        
        auteurs = set(doc.auteur for doc in documents)
        
        mots_cles = set()
        for doc in documents:
            mots_cles.update(doc.mots_cles)
        
        hauteur = self._calculer_hauteur(self.bst.root)
        
        return {
            'nombre_documents': self.bst.size,
            'nombre_auteurs': len(auteurs),
            'nombre_mots_cles': len(mots_cles),
            'hauteur_arbre': hauteur,
            'est_vide': self.bst.size == 0
        }
    
    def _calculer_hauteur(self, node: Optional[Node]) -> int:
        """
        Calcule la hauteur de l'arbre.
        
        Args:
            node: Le nœud racine
            
        Returns:
            La hauteur de l'arbre
        """
        if node is None:
            return 0
        
        hauteur_gauche = self._calculer_hauteur(node.left)
        hauteur_droite = self._calculer_hauteur(node.right)
        
        return 1 + max(hauteur_gauche, hauteur_droite)
    
    
    def vider(self) -> None:
        """Vide complètement le BST."""
        self.bst.root = None
        self.bst.size = 0
    
    def est_vide(self) -> bool:
        """
        Vérifie si le BST est vide.
        
        Returns:
            True si le BST est vide
        """
        return self.bst.root is None
    
    def taille(self) -> int:
        """
        Retourne le nombre de documents dans le BST.
        
        Returns:
            Le nombre de documents
        """
        return self.bst.size
    
    
    def rechercher_avec_mesure(self, titre: str) -> Dict[str, Any]:
        """
        Recherche un document et mesure le temps d'exécution.
        
        Args:
            titre: Le titre à rechercher
            
        Returns:
            Dictionnaire avec le résultat et le temps
        """
        start_time = time.time()
        resultat = self.bst.search(titre)
        end_time = time.time()
        
        return {
            'document': resultat,
            'trouve': resultat is not None,
            'temps': end_time - start_time,
            'complexite': 'O(log n)'
        }
    
    
    def __len__(self) -> int:
        """Retourne la taille du BST."""
        return self.bst.size
    
    def __str__(self) -> str:
        """Retourne une représentation textuelle du BST."""
        return self.afficher_bst()
    
    def __bool__(self) -> bool:
        """Retourne True si le BST n'est pas vide."""
        return not self.est_vide()

