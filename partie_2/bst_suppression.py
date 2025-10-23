
def supprimer_document_bst(bst):
    """
    Gère l'interface pour la suppression d'un document dans le BST (Partie 2 Supplément).
    Fait appel à la méthode delete() implémentée dans la classe BinarySearchTree.
    """
    if bst.root is None:
        print("\nℹ️ Le BST est vide, rien à supprimer.")
        return

    titre_supprimer = input("\nEntrez le TITRE EXACT du document à supprimer: ").strip()
    
    if bst.delete(titre_supprimer):
        print(f"\n✅ Document avec le titre '{titre_supprimer}' a été supprimé du BST.")
        try:
             from .bst import BinarySearchTree 
             print("Veuillez utiliser l'option 6 pour vérifier l'état de l'arbre.")
        except ImportError:
             pass
    else:
        print(f"\n❌ Document avec le titre '{titre_supprimer}' non trouvé dans le BST.")