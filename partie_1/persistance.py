
import json
import os
from copy import deepcopy

FICHIER_DONNEES = 'bibliotheque_data.json'

def save_data(bibliotheque_list: list):
    """
    Sauvegarde la liste des documents au format JSON.
    Chaque objet Document doit avoir une méthode to_dict() pour la sérialisation.
    """
    try:
        data = [doc.to_dict() for doc in bibliotheque_list]
        
        with open(FICHIER_DONNEES, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"\n[OK] Sauvegarde réussie : {len(data)} documents enregistrés dans {FICHIER_DONNEES}")
        return True
    except Exception as e:
        print(f"\n[ERREUR] Erreur lors de la sauvegarde des données : {e}")
        return False

def load_data(Document_Classe):
    """
    Charge les documents depuis le fichier JSON et les retourne sous forme de liste d'objets Document.
    """
    if not os.path.exists(FICHIER_DONNEES):
        print(f"\n[INFO] Fichier de données {FICHIER_DONNEES} non trouvé. Démarrage avec une bibliothèque vide.")
        return []

    try:
        with open(FICHIER_DONNEES, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        bibliotheque_list = []
        for item in data:
            if isinstance(item['mots_cles'], list):
                mots_cles_str = ','.join(item['mots_cles'])
            else:
                mots_cles_str = item['mots_cles']
            
            doc = Document_Classe(
                titre=item['titre'],
                auteur=item['auteur'],
                mots_cles=mots_cles_str
            )
            bibliotheque_list.append(doc)
        
        print(f"\n[OK] Chargement réussi : {len(bibliotheque_list)} documents chargés depuis {FICHIER_DONNEES}")
        return bibliotheque_list
        
    except json.JSONDecodeError:
        print(f"\n[ERREUR] Erreur de format JSON dans {FICHIER_DONNEES}. Fichier corrompu.")
        return []
    except Exception as e:
        print(f"\n[ERREUR] Erreur lors du chargement des données : {e}")
        return []

def save_all_structures(list_bib, bst_bib=None, hash_bib=None):
    """
    Sauvegarde toutes les structures de données (liste, BST, Hash) en utilisant la liste comme source principale.
    """
    try:
        success = save_data(list_bib)
        
        if success:
            print("[OK] Toutes les structures ont été synchronisées avec le fichier de persistance.")
            return True
        else:
            print("[ERREUR] Échec de la sauvegarde des structures.")
            return False
            
    except Exception as e:
        print(f"[ERREUR] Erreur lors de la sauvegarde des structures : {e}")
        return False

def load_all_structures(Document_Classe, bst_bib=None, hash_bib=None):
    """
    Charge les données depuis le fichier et les synchronise avec toutes les structures.
    """
    try:
        list_bib = load_data(Document_Classe)
        
        if bst_bib is not None:
            bst_bib.root = None
            bst_bib.size = 0
            for doc in list_bib:
                bst_bib.insert(doc)
            print(f"[OK] BST synchronisé avec {len(list_bib)} documents")
        
        if hash_bib is not None:
            from partie_3.hashing import Bucket
            hash_bib.table = [Bucket() for _ in range(hash_bib.size)]
            for doc in list_bib:
                hash_bib.insert(doc)
            print(f"[OK] Table de hachage synchronisée avec {len(list_bib)} documents")
        
        return list_bib
        
    except Exception as e:
        print(f"[ERREUR] Erreur lors du chargement des structures : {e}")
        return []

def create_default_data(Document_Classe):
    """
    Crée des données par défaut si aucun fichier de persistance n'existe.
    """
    docs = [
        Document_Classe("Le Petit Prince", "Antoine de Saint-Exupéry", "conte, amitié, philosophie"),
        Document_Classe("1984", "George Orwell", "dystopie, politique, surveillance"),
        Document_Classe("Zazie dans le Métro", "Raymond Queneau", "roman, humour, argot"),
        Document_Classe("Le Guide du voyageur galactique", "Douglas Adams", "science-fiction, humour"),
        Document_Classe("Le vieil homme et la mer", "Ernest Hemingway", "littérature, mer"),
        Document_Classe("L'Étranger", "Albert Camus", "roman, philosophie, absurde")
    ]
    
    save_data(docs)
    print("[OK] Données par défaut créées et sauvegardées.")
    return docs