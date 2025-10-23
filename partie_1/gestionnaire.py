# Fichier : partie_1/gestionnaire.py
# Contient les algorithmes de tri et de recherche séquentielle, ainsi que l'ajout.

# --- Algorithmes de Tri et de Recherche ---

def trier_par_titre(bibliotheque):
    """
    Algorithme de Tri par Insertion (Insertion Sort).
    Trie la liste des objets Document par titre (ordre alphabétique).
    Complexité : O(n^2).
    """
    n = len(bibliotheque)
    # Parcours de 1 à n-1
    for i in range(1, n):
        cle_doc = bibliotheque[i]
        j = i - 1
        
        # Comparaison des titres en minuscules
        while j >= 0 and cle_doc.titre.lower() < bibliotheque[j].titre.lower():
            bibliotheque[j + 1] = bibliotheque[j]
            j -= 1
        
        bibliotheque[j + 1] = cle_doc

    if bibliotheque:
        print("\n📚 La bibliothèque a été triée par titre (Tri par Insertion).")
    else:
        print("\nℹ️ La bibliothèque est vide, rien à trier.")

def rechercher_par_titre(bibliotheque):
    """
    Algorithme de Recherche Séquentielle (Linear Search).
    Recherche un document par son titre.
    Complexité : O(n).
    """
    if not bibliotheque:
        print("\nℹ️ La bibliothèque est vide, aucune recherche possible.")
        return

    terme_recherche = input("\nEntrez le titre exact à rechercher: ").strip().lower()
    
    resultats = []
    # Parcours séquentiel
    for document in bibliotheque:
        if document.titre.lower() == terme_recherche:
            resultats.append(document)

    if resultats:
        print(f"\n🎉 {len(resultats)} Résultat(s) trouvé(s) pour '{terme_recherche}':")
        for doc in resultats:
            print(f"- {doc}")
    else:
        print(f"\n😞 Aucun document trouvé avec le titre '{terme_recherche}'.")
        
def ajouter_document(bibliotheque, Document_Classe):
    """
    Gère la saisie utilisateur et ajoute un nouveau document à la liste.
    """
    print("\n--- Ajout d'un nouveau document ---")
    titre = input("Entrez le titre du document: ").strip()
    auteur = input("Entrez l'auteur du document: ").strip()
    mots_cles_str = input("Entrez les mots-clés (séparés par des virgules): ").strip()

    if titre and auteur:
        nouveau_doc = Document_Classe(titre, auteur, mots_cles_str)
        bibliotheque.append(nouveau_doc)
        print(f"\n✅ Document '{titre}' ajouté avec succès.")
    else:
        print("\n❌ Le titre et l'auteur sont obligatoires. Annulation de l'ajout.")
        
def afficher_bibliotheque(bibliotheque):
    """Affiche tous les documents de la bibliothèque."""
    if not bibliotheque:
        print("\nℹ️ La bibliothèque est actuellement vide.")
        return
    
    print("\n--- Contenu de la Bibliothèque (Total: "
          f"{len(bibliotheque)} documents) ---")
    for i, doc in enumerate(bibliotheque):
        print(f"[{i+1}] {doc}")
    print("-------------------------------------------------")
    