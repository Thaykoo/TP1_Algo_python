# Fichier : partie_2/bst_suppression.py
# Fonctionnalité de suppression d'un document du BST.

def supprimer_document_bst(bst):
    """
    Gère l'interface pour la suppression d'un document dans le BST (Partie 2 Supplément).
    Fait appel à la méthode delete() implémentée dans la classe BinarySearchTree.
    """
    if bst.root is None:
        print("\nℹ️ Le BST est vide, rien à supprimer.")
        return

    titre_supprimer = input("\nEntrez le TITRE EXACT du document à supprimer: ").strip()
    
    # Appel de la méthode delete() du BST
    if bst.delete(titre_supprimer):
        print(f"\n✅ Document avec le titre '{titre_supprimer}' a été supprimé du BST.")
        # Afficher le nouvel ordre pour confirmation
        # Note: Nous avons besoin d'une fonction d'affichage ici, assumons qu'elle est importable.
        try:
             # On assume que la fonction d'affichage BST est accessible pour la confirmation
             from .bst import BinarySearchTree 
             # On ne peut pas facilement réutiliser la fonction afficher_bst_in_order ici
             # car elle est définie dans main.py. Affichons un message simple.
             print("Veuillez utiliser l'option 6 pour vérifier l'état de l'arbre.")
        except ImportError:
             pass
    else:
        print(f"\n❌ Document avec le titre '{titre_supprimer}' non trouvé dans le BST.")