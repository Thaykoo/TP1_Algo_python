# Fichier : partie_1/persistance.py
# Gestion de la persistance des données via le format JSON.

import json
import os

# Nom du fichier de base de données
FICHIER_DONNEES = 'bibliotheque_data.json'

def save_data(bibliotheque_list: list):
    """
    Sauvegarde la liste des documents au format JSON.
    Chaque objet Document doit avoir une méthode to_dict() pour la sérialisation.
    """
    try:
        # Convertit chaque objet Document en dictionnaire
        data = [doc.to_dict() for doc in bibliotheque_list]
        
        with open(FICHIER_DONNEES, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        
        print(f"\n{VERT}✅ Sauvegarde réussie : {len(data)} documents enregistrés dans {FICHIER_DONNEES}{RESET}")
        return True
    except Exception as e:
        print(f"\n{ROUGE}❌ Erreur lors de la sauvegarde des données : {e}{RESET}")
        return False

def load_data(Document_Classe):
    """
    Charge les documents depuis le fichier JSON et les retourne sous forme de liste d'objets Document.
    """
    if not os.path.exists(FICHIER_DONNEES):
        print(f"\n{JAUNE}ℹ️ Fichier de données {FICHIER_DONNEES} non trouvé. Démarrage avec une bibliothèque vide.{RESET}")
        return []

    try:
        with open(FICHIER_DONNEES, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convertit chaque dictionnaire en objet Document
        bibliotheque_list = [Document_Classe(
            titre=item['titre'],
            auteur=item['auteur'],
            mots_cles=','.join(item['mots_cles']) # Reconvertir la liste de mots-clés en chaîne pour l'initialisation
        ) for item in data]
        
        print(f"\n{VERT}✅ Chargement réussi : {len(bibliotheque_list)} documents chargés depuis {FICHIER_DONNEES}{RESET}")
        return bibliotheque_list
        
    except json.JSONDecodeError:
        print(f"\n{ROUGE}❌ Erreur de format JSON dans {FICHIER_DONNEES}. Fichier corrompu.{RESET}")
        return []
    except Exception as e:
        print(f"\n{ROUGE}❌ Erreur lors du chargement des données : {e}{RESET}")
        return []

# Références aux couleurs pour le fichier (à adapter si vous n'utilisez pas colorama)
try:
    from colorama import Fore, Style
    VERT = Fore.GREEN + Style.BRIGHT
    ROUGE = Fore.RED + Style.BRIGHT
    JAUNE = Fore.YELLOW + Style.BRIGHT
    RESET = Style.RESET_ALL
except ImportError:
    VERT = ROUGE = JAUNE = RESET = ""