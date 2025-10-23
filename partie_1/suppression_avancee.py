
from partie_1.persistance import save_all_structures

def supprimer_document_complet(titre, list_bib, bst_bib=None, hash_bib=None):
    """
    Supprime un document par titre exact de toutes les structures disponibles.
    
    Args:
        titre (str): Titre exact du document à supprimer
        list_bib (list): Liste principale des documents
        bst_bib (BinarySearchTree, optional): Arbre BST
        hash_bib (HashTable, optional): Table de hachage
    
    Returns:
        dict: Résultat de la suppression avec détails
    """
    resultat = {
        'succes': False,
        'supprime_de': [],
        'non_trouve_dans': [],
        'erreurs': [],
        'sauvegarde': False
    }
    
    try:
        documents_avant = len(list_bib)
        list_bib[:] = [doc for doc in list_bib if doc.titre != titre]
        if len(list_bib) < documents_avant:
            resultat['supprime_de'].append('Liste principale')
            resultat['succes'] = True
        
        if bst_bib:
            try:
                if bst_bib.delete(titre):
                    resultat['supprime_de'].append('BST')
                    resultat['succes'] = True
                else:
                    resultat['non_trouve_dans'].append('BST')
            except Exception as e:
                resultat['erreurs'].append(f'BST: {str(e)}')
        
        if hash_bib:
            try:
                supprime_hash = False
                for bucket in hash_bib.table:
                    if bucket.items:
                        bucket.items[:] = [doc for doc in bucket.items if doc.titre != titre]
                        if len(bucket.items) < len([doc for doc in bucket.items if doc.titre == titre]):
                            supprime_hash = True
                
                if supprime_hash:
                    resultat['supprime_de'].append('Table de hachage')
                    resultat['succes'] = True
                else:
                    resultat['non_trouve_dans'].append('Table de hachage')
            except Exception as e:
                resultat['erreurs'].append(f'Hash: {str(e)}')
        
        if resultat['succes']:
            try:
                if save_all_structures(list_bib, bst_bib, hash_bib):
                    resultat['sauvegarde'] = True
            except Exception as e:
                resultat['erreurs'].append(f'Sauvegarde: {str(e)}')
        
        return resultat
        
    except Exception as e:
        resultat['erreurs'].append(f'Général: {str(e)}')
        return resultat

def supprimer_par_criteres(critere, valeur, list_bib, bst_bib=None, hash_bib=None):
    """
    Supprime tous les documents correspondant à un critère spécifique.
    
    Args:
        critere (str): 'auteur', 'mots_cles', ou 'titre'
        valeur (str): Valeur à rechercher
        list_bib (list): Liste principale des documents
        bst_bib (BinarySearchTree, optional): Arbre BST
        hash_bib (HashTable, optional): Table de hachage
    
    Returns:
        dict: Résultat de la suppression avec détails
    """
    resultat = {
        'succes': False,
        'documents_supprimes': [],
        'erreurs': [],
        'sauvegarde': False
    }
    
    try:
        documents_a_supprimer = []
        
        for doc in list_bib:
            correspondance = False
            
            if critere == 'auteur' and valeur.lower() in doc.auteur.lower():
                correspondance = True
            elif critere == 'mots_cles':
                for mot_cle in doc.mots_cles:
                    if valeur.lower() in mot_cle.lower():
                        correspondance = True
                        break
            elif critere == 'titre' and valeur.lower() in doc.titre.lower():
                correspondance = True
            
            if correspondance:
                documents_a_supprimer.append(doc)
        
        for doc in documents_a_supprimer:
            supprimer_document_complet(doc.titre, list_bib, bst_bib, hash_bib)
            resultat['documents_supprimes'].append(doc)
        
        if documents_a_supprimer:
            resultat['succes'] = True
            
            try:
                if save_all_structures(list_bib, bst_bib, hash_bib):
                    resultat['sauvegarde'] = True
            except Exception as e:
                resultat['erreurs'].append(f'Sauvegarde: {str(e)}')
        
        return resultat
        
    except Exception as e:
        resultat['erreurs'].append(f'Général: {str(e)}')
        return resultat

def supprimer_documents_multiples(titres, list_bib, bst_bib=None, hash_bib=None):
    """
    Supprime plusieurs documents par leurs titres.
    
    Args:
        titres (list): Liste des titres à supprimer
        list_bib (list): Liste principale des documents
        bst_bib (BinarySearchTree, optional): Arbre BST
        hash_bib (HashTable, optional): Table de hachage
    
    Returns:
        dict: Résultat de la suppression avec détails
    """
    resultat = {
        'succes': False,
        'supprimes': [],
        'non_trouves': [],
        'erreurs': [],
        'sauvegarde': False
    }
    
    try:
        for titre in titres:
            doc_resultat = supprimer_document_complet(titre, list_bib, bst_bib, hash_bib)
            if doc_resultat['succes']:
                resultat['supprimes'].append(titre)
                resultat['succes'] = True
            else:
                resultat['non_trouves'].append(titre)
            
            if doc_resultat['erreurs']:
                resultat['erreurs'].extend(doc_resultat['erreurs'])
        
        if resultat['succes']:
            try:
                if save_all_structures(list_bib, bst_bib, hash_bib):
                    resultat['sauvegarde'] = True
            except Exception as e:
                resultat['erreurs'].append(f'Sauvegarde: {str(e)}')
        
        return resultat
        
    except Exception as e:
        resultat['erreurs'].append(f'Général: {str(e)}')
        return resultat

def vider_toutes_structures(list_bib, bst_bib=None, hash_bib=None):
    """
    Supprime tous les documents de toutes les structures.
    
    Args:
        list_bib (list): Liste principale des documents
        bst_bib (BinarySearchTree, optional): Arbre BST
        hash_bib (HashTable, optional): Table de hachage
    
    Returns:
        dict: Résultat de la suppression avec détails
    """
    resultat = {
        'succes': False,
        'documents_supprimes': len(list_bib),
        'erreurs': [],
        'sauvegarde': False
    }
    
    try:
        list_bib.clear()
        
        if bst_bib:
            try:
                bst_bib.root = None
                bst_bib.size = 0
            except Exception as e:
                resultat['erreurs'].append(f'BST: {str(e)}')
        
        if hash_bib:
            try:
                for bucket in hash_bib.table:
                    bucket.items.clear()
            except Exception as e:
                resultat['erreurs'].append(f'Hash: {str(e)}')
        
        resultat['succes'] = True
        
        try:
            if save_all_structures(list_bib, bst_bib, hash_bib):
                resultat['sauvegarde'] = True
        except Exception as e:
            resultat['erreurs'].append(f'Sauvegarde: {str(e)}')
        
        return resultat
        
    except Exception as e:
        resultat['erreurs'].append(f'Général: {str(e)}')
        return resultat

def obtenir_statistiques_suppression(list_bib, bst_bib=None, hash_bib=None):
    """
    Obtient des statistiques sur les structures de données.
    
    Args:
        list_bib (list): Liste principale des documents
        bst_bib (BinarySearchTree, optional): Arbre BST
        hash_bib (HashTable, optional): Table de hachage
    
    Returns:
        dict: Statistiques des structures
    """
    stats = {
        'liste': len(list_bib),
        'bst': 0,
        'hash': 0,
        'total_unique': 0
    }
    
    try:
        if bst_bib:
            stats['bst'] = bst_bib.size
        
        if hash_bib:
            total_hash = 0
            for bucket in hash_bib.table:
                total_hash += len(bucket.items)
            stats['hash'] = total_hash
        
        stats['total_unique'] = len(list_bib)
        
        return stats
        
    except Exception as e:
        stats['erreur'] = str(e)
        return stats
