
"""
Ce module fournit des wrappers pour l'ancienne API fonctionnelle
tout en utilisant la nouvelle architecture POO en arrière-plan.
"""

from .bst import BinarySearchTree, comparer_recherche_performance
from .bst_manager import BSTManager
from typing import List, Optional

try:
    from ..partie_1.document import Document
except ImportError:
    from partie_1.document import Document


def rechercher_par_titre_bst(bst: BinarySearchTree, titre: str) -> Optional[Document]:
    """
    Wrapper fonctionnel pour la recherche par titre dans le BST.
    
    Args:
        bst: L'arbre binaire de recherche
        titre: Le titre à rechercher
        
    Returns:
        Le document trouvé ou None
    """
    if isinstance(bst, BSTManager):
        return bst.rechercher_par_titre(titre)
    return bst.search(titre)


def rechercher_par_auteur_bst(bst: BinarySearchTree, auteur: str) -> List[Document]:
    """
    Wrapper fonctionnel pour la recherche par auteur dans le BST.
    
    Args:
        bst: L'arbre binaire de recherche
        auteur: Le nom de l'auteur
        
    Returns:
        Liste des documents trouvés
    """
    if isinstance(bst, BSTManager):
        return bst.rechercher_par_auteur(auteur)
    return bst.search_by_author(auteur)


def rechercher_par_mots_cles_bst(bst: BinarySearchTree, mot_cle: str) -> List[Document]:
    """
    Wrapper fonctionnel pour la recherche par mots-clés dans le BST.
    
    Args:
        bst: L'arbre binaire de recherche
        mot_cle: Le mot-clé à rechercher
        
    Returns:
        Liste des documents trouvés
    """
    if isinstance(bst, BSTManager):
        return bst.rechercher_par_mots_cles(mot_cle)
    return bst.search_by_keywords(mot_cle)


def recherche_avancee_bst(bst: BinarySearchTree, terme: str) -> List[Document]:
    """
    Wrapper fonctionnel pour la recherche avancée dans le BST.
    
    Args:
        bst: L'arbre binaire de recherche
        terme: Le terme à rechercher
        
    Returns:
        Liste des documents trouvés
    """
    if isinstance(bst, BSTManager):
        return bst.rechercher_avancee(terme)
    return bst.search_advanced(terme)


def ajouter_document_bst(bst: BinarySearchTree, document: Document) -> bool:
    """
    Wrapper fonctionnel pour ajouter un document au BST.
    
    Args:
        bst: L'arbre binaire de recherche
        document: Le document à ajouter
        
    Returns:
        True si l'ajout a réussi
    """
    try:
        if isinstance(bst, BSTManager):
            return bst.ajouter_document(document.titre, document.auteur, 
                                       ','.join(document.mots_cles))
        bst.insert(document)
        return True
    except Exception:
        return False


def supprimer_document_bst_func(bst: BinarySearchTree, titre: str) -> bool:
    """
    Wrapper fonctionnel pour supprimer un document du BST.
    
    Args:
        bst: L'arbre binaire de recherche
        titre: Le titre du document à supprimer
        
    Returns:
        True si la suppression a réussi
    """
    if isinstance(bst, BSTManager):
        return bst.supprimer_document(titre)
    return bst.delete(titre)


def afficher_bst_in_order(bst: BinarySearchTree) -> None:
    """
    Wrapper fonctionnel pour afficher le BST en ordre.
    
    Args:
        bst: L'arbre binaire de recherche
    """
    if isinstance(bst, BSTManager):
        print(bst.afficher_bst())
    else:
        documents = bst.in_order_traversal()
        
        if not documents:
            print("\n📚 Le BST est vide.")
            return
        
        print(f"\n📚 BST - {bst.size} document(s) :")
        print("=" * 70)
        
        for i, doc in enumerate(documents, 1):
            print(f"{i}. {doc}")
        
        print("=" * 70)


def obtenir_documents_tries_bst(bst: BinarySearchTree) -> List[Document]:
    """
    Wrapper fonctionnel pour obtenir tous les documents triés.
    
    Args:
        bst: L'arbre binaire de recherche
        
    Returns:
        Liste des documents triés
    """
    if isinstance(bst, BSTManager):
        return bst.obtenir_documents_tries()
    return bst.in_order_traversal()


def get_statistiques_bst(bst: BinarySearchTree) -> dict:
    """
    Wrapper fonctionnel pour obtenir les statistiques du BST.
    
    Args:
        bst: L'arbre binaire de recherche
        
    Returns:
        Dictionnaire avec les statistiques
    """
    if isinstance(bst, BSTManager):
        return bst.get_statistiques()
    
    documents = bst.in_order_traversal()
    auteurs = set(doc.auteur for doc in documents)
    mots_cles = set()
    for doc in documents:
        mots_cles.update(doc.mots_cles)
    
    return {
        'nombre_documents': bst.size,
        'nombre_auteurs': len(auteurs),
        'nombre_mots_cles': len(mots_cles),
        'est_vide': bst.size == 0
    }


def supprimer_document_bst_interactif(bst: BinarySearchTree) -> None:
    """
    Gère l'interface interactive pour la suppression d'un document.
    Maintient la compatibilité avec l'ancienne fonction de bst_suppression.py
    
    Args:
        bst: L'arbre binaire de recherche
    """
    if bst.root is None:
        print("\nℹ️ Le BST est vide, rien à supprimer.")
        return

    titre_supprimer = input("\nEntrez le TITRE EXACT du document à supprimer: ").strip()
    
    if bst.delete(titre_supprimer):
        print(f"\n✅ Document avec le titre '{titre_supprimer}' a été supprimé du BST.")
        print("Veuillez utiliser l'option d'affichage pour vérifier l'état de l'arbre.")
    else:
        print(f"\n❌ Document avec le titre '{titre_supprimer}' non trouvé dans le BST.")


__all__ = [
    'rechercher_par_titre_bst',
    'rechercher_par_auteur_bst',
    'rechercher_par_mots_cles_bst',
    'recherche_avancee_bst',
    'ajouter_document_bst',
    'supprimer_document_bst_func',
    'supprimer_document_bst_interactif',
    'afficher_bst_in_order',
    'obtenir_documents_tries_bst',
    'get_statistiques_bst',
    'comparer_recherche_performance'
]

