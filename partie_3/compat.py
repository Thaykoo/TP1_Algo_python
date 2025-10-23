
"""
Ce module fournit des wrappers pour l'ancienne API fonctionnelle
tout en utilisant la nouvelle architecture POO en arrière-plan.
"""

from .hashing import HashTable, comparer_recherche_hachage
from .hash_manager import HashTableManager
from typing import List

try:
    from ..partie_1.document import Document
except ImportError:
    from partie_1.document import Document


def rechercher_par_auteur_hash(hash_table: HashTable, auteur: str) -> List[Document]:
    """
    Wrapper fonctionnel pour la recherche par auteur dans la HashTable.
    
    Args:
        hash_table: La table de hachage
        auteur: Le nom de l'auteur
        
    Returns:
        Liste des documents trouvés
    """
    if isinstance(hash_table, HashTableManager):
        return hash_table.rechercher_par_auteur(auteur)
    return hash_table.search_by_author(auteur)


def rechercher_par_titre_hash(hash_table: HashTable, titre: str) -> List[Document]:
    """
    Wrapper fonctionnel pour la recherche par titre dans la HashTable.
    
    Args:
        hash_table: La table de hachage
        titre: Le titre à rechercher
        
    Returns:
        Liste des documents trouvés
    """
    if isinstance(hash_table, HashTableManager):
        return hash_table.rechercher_par_titre(titre)
    return hash_table.search_by_title(titre)


def rechercher_par_mots_cles_hash(hash_table: HashTable, mot_cle: str) -> List[Document]:
    """
    Wrapper fonctionnel pour la recherche par mots-clés dans la HashTable.
    
    Args:
        hash_table: La table de hachage
        mot_cle: Le mot-clé à rechercher
        
    Returns:
        Liste des documents trouvés
    """
    if isinstance(hash_table, HashTableManager):
        return hash_table.rechercher_par_mots_cles(mot_cle)
    return hash_table.search_by_keywords(mot_cle)


def recherche_avancee_hash(hash_table: HashTable, terme: str) -> List[Document]:
    """
    Wrapper fonctionnel pour la recherche avancée dans la HashTable.
    
    Args:
        hash_table: La table de hachage
        terme: Le terme à rechercher
        
    Returns:
        Liste des documents trouvés
    """
    if isinstance(hash_table, HashTableManager):
        return hash_table.rechercher_avancee(terme)
    return hash_table.search_advanced(terme)


def ajouter_document_hash(hash_table: HashTable, document: Document) -> bool:
    """
    Wrapper fonctionnel pour ajouter un document à la HashTable.
    
    Args:
        hash_table: La table de hachage
        document: Le document à ajouter
        
    Returns:
        True si l'ajout a réussi
    """
    try:
        if isinstance(hash_table, HashTableManager):
            return hash_table.ajouter_document(document.titre, document.auteur,
                                               ','.join(document.mots_cles))
        hash_table.insert(document)
        return True
    except Exception:
        return False


def afficher_hash_table(hash_table: HashTable) -> None:
    """
    Wrapper fonctionnel pour afficher la HashTable.
    
    Args:
        hash_table: La table de hachage
    """
    if isinstance(hash_table, HashTableManager):
        print(hash_table.afficher_hash_table())
    else:
        documents = []
        for bucket in hash_table.table:
            documents.extend(bucket.items)
        
        if not documents:
            print("\n📚 La table de hachage est vide.")
            return
        
        print(f"\n📚 Table de Hachage - {len(documents)} document(s) :")
        print("=" * 70)
        
        for i, doc in enumerate(documents, 1):
            print(f"{i}. {doc}")
        
        print("=" * 70)


def afficher_distribution_hash(hash_table: HashTable) -> None:
    """
    Wrapper fonctionnel pour afficher la distribution des buckets.
    
    Args:
        hash_table: La table de hachage
    """
    if isinstance(hash_table, HashTableManager):
        print(hash_table.afficher_distribution())
    else:
        print("\n📊 Distribution des buckets :")
        print("=" * 70)
        
        for i, bucket in enumerate(hash_table.table):
            if bucket.items:
                print(f"Bucket {i:3d} : {len(bucket.items)} document(s)")
                for doc in bucket.items[:3]:
                    print(f"  - {doc.titre} ({doc.auteur})")
                if len(bucket.items) > 3:
                    print(f"  ... et {len(bucket.items) - 3} autre(s)")
        
        print("=" * 70)


def obtenir_tous_documents_hash(hash_table: HashTable) -> List[Document]:
    """
    Wrapper fonctionnel pour obtenir tous les documents.
    
    Args:
        hash_table: La table de hachage
        
    Returns:
        Liste de tous les documents
    """
    if isinstance(hash_table, HashTableManager):
        return hash_table.obtenir_tous_documents()
    
    documents = []
    for bucket in hash_table.table:
        documents.extend(bucket.items)
    return documents


def get_statistiques_hash(hash_table: HashTable) -> dict:
    """
    Wrapper fonctionnel pour obtenir les statistiques de la HashTable.
    
    Args:
        hash_table: La table de hachage
        
    Returns:
        Dictionnaire avec les statistiques
    """
    if isinstance(hash_table, HashTableManager):
        return hash_table.get_statistiques()
    
    documents = obtenir_tous_documents_hash(hash_table)
    auteurs = set(doc.auteur for doc in documents)
    mots_cles = set()
    for doc in documents:
        mots_cles.update(doc.mots_cles)
    
    buckets_utilises = sum(1 for bucket in hash_table.table if bucket.items)
    collisions = sum(max(0, len(bucket.items) - 1) for bucket in hash_table.table)
    
    return {
        'nombre_documents': len(documents),
        'nombre_auteurs': len(auteurs),
        'nombre_mots_cles': len(mots_cles),
        'taille_table': hash_table.size,
        'buckets_utilises': buckets_utilises,
        'collisions': collisions,
        'est_vide': len(documents) == 0
    }


def charger_depuis_bst_hash(hash_table: HashTable, bst) -> int:
    """
    Wrapper fonctionnel pour charger depuis un BST.
    
    Args:
        hash_table: La table de hachage
        bst: L'arbre binaire source
        
    Returns:
        Nombre de documents chargés
    """
    if isinstance(hash_table, HashTableManager):
        return hash_table.charger_depuis_bst(bst)
    
    hash_table.populate_from_bst(bst)
    return len(obtenir_tous_documents_hash(hash_table))


__all__ = [
    'rechercher_par_auteur_hash',
    'rechercher_par_titre_hash',
    'rechercher_par_mots_cles_hash',
    'recherche_avancee_hash',
    'ajouter_document_hash',
    'afficher_hash_table',
    'afficher_distribution_hash',
    'obtenir_tous_documents_hash',
    'get_statistiques_hash',
    'charger_depuis_bst_hash',
    'comparer_recherche_hachage'
]

