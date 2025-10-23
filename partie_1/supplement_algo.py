# Fichier : partie_1/supplement_algo.py
# Implémentation du Tri Fusion et de la comparaison de performance.

import time
import random
from copy import deepcopy

# ==============================================================================
# 1. Algorithme de Tri Fusion (Merge Sort)
# ==============================================================================

def tri_fusion(bibliotheque):
    """
    Implémente l'algorithme de Tri Fusion (Merge Sort) pour trier
    la liste des documents par titre (ordre alphabétique).
    Complexité : O(n log n).
    """
    if len(bibliotheque) <= 1:
        return bibliotheque

    # Diviser la liste en deux moitiés
    milieu = len(bibliotheque) // 2
    gauche = bibliotheque[:milieu]
    droite = bibliotheque[milieu:]

    # Appels récursifs pour trier les deux moitiés
    gauche = tri_fusion(gauche)
    droite = tri_fusion(droite)

    # Fusionner les deux moitiés triées
    return fusionner(gauche, droite)

def fusionner(gauche, droite):
    """
    Fonction auxiliaire pour fusionner deux listes triées.
    """
    resultat = []
    i = j = 0 # Indices pour les listes gauche et droite

    # Parcourir et comparer les éléments des deux listes
    while i < len(gauche) and j < len(droite):
        # Comparaison par titre (non sensible à la casse)
        if gauche[i].titre.lower() <= droite[j].titre.lower():
            resultat.append(gauche[i])
            i += 1
        else:
            resultat.append(droite[j])
            j += 1

    # Ajouter les restes (s'il y en a)
    resultat.extend(gauche[i:])
    resultat.extend(droite[j:])
    return resultat

# ==============================================================================
# 2. Fonction de Comparaison de Temps d'Exécution
# ==============================================================================

def generer_donnees_test(Document_Classe, taille=5000):
    """
    Génère une liste de documents aléatoires de la taille spécifiée
    pour les tests de performance.
    """
    documents = []
    for i in range(taille):
        titre = f"Titre {random.randint(1000, 9999)}{i}"
        auteur = f"Auteur {random.randint(1, 100)}"
        mots_cles = "test, performance"
        documents.append(Document_Classe(titre, auteur, mots_cles))
    # On mélange les documents pour garantir un ordre non trié
    random.shuffle(documents)
    return documents

def comparer_temps_execution(Document_Classe, tri_insertion, tri_fusion):
    """
    Compare le temps d'exécution du Tri par Insertion (O(n^2)) et du Tri Fusion (O(n log n)).
    """
    print("\n" + "="*50)
    print("        COMPARAISON DES ALGORITHMES DE TRI")
    print("="*50)

    # On teste sur des tailles de données croissantes pour voir l'effet de la complexité
    tailles = [100, 500, 2000] 

    print(f"| {'Taille de la liste':<20} | {'Tri Insertion (s)':<20} | {'Tri Fusion (s)':<20} |")
    print("-" * 75)

    for taille in tailles:
        # Générer et dupliquer les données
        donnees_base = generer_donnees_test(Document_Classe, taille)
        
        # --- Mesure du Tri par Insertion ---
        donnees_insertion = deepcopy(donnees_base)
        start_time_ins = time.time()
        tri_insertion(donnees_insertion) 
        end_time_ins = time.time()
        temps_insertion = end_time_ins - start_time_ins
        
        # --- Mesure du Tri Fusion ---
        donnees_fusion = deepcopy(donnees_base)
        start_time_fus = time.time()
        # tri_fusion renvoie une NOUVELLE liste, contrairement à tri_insertion qui modifie l'originale
        _ = tri_fusion(donnees_fusion) 
        end_time_fus = time.time()
        temps_fusion = end_time_fus - start_time_fus
        
        print(f"| {taille:<20} | {temps_insertion:<20.4f} | {temps_fusion:<20.4f} |")
        
    print("-" * 75)
    print("\nConclusion : Le Tri Fusion est nettement plus rapide sur de grandes listes car il est en O(n log n).")