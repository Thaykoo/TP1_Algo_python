
from typing import List
from .document import Document
from .bibliotheque import Bibliotheque
from .gestionnaire_poo import BibliothequeManager
from .tri_algorithms import (
    TriInsertion, TriSelection, TriBulles,
    TriRapide, TriFusion, TriTas, TriComptage
)
from .search_algorithms import SearchByTitle, SearchByAuthor, SearchByKeywords, SearchAdvanced


def trier_par_titre(bibliotheque: List[Document]) -> None:
    """
    Tri par insertion (ancienne API, wrapper POO).
    Trie la liste en place.
    """
    tri = TriInsertion()
    tri.sort(bibliotheque)
    if bibliotheque:
        print("\n[OK] La bibliothèque a été triée par titre (Tri par Insertion).")
    else:
        print("\n[INFO] La bibliothèque est vide, rien à trier.")


def tri_fusion(bibliotheque: List[Document]) -> List[Document]:
    """Tri fusion (ancienne API, wrapper POO)."""
    tri = TriFusion()
    from copy import deepcopy
    result = deepcopy(bibliotheque)
    tri.sort(result)
    return result


def tri_rapide(bibliotheque: List[Document]) -> List[Document]:
    """Tri rapide (ancienne API, wrapper POO)."""
    tri = TriRapide()
    from copy import deepcopy
    result = deepcopy(bibliotheque)
    tri.sort(result)
    return result


def tri_selection(bibliotheque: List[Document]) -> None:
    """Tri par sélection (ancienne API, wrapper POO)."""
    tri = TriSelection()
    tri.sort(bibliotheque)


def tri_bulles(bibliotheque: List[Document]) -> None:
    """Tri à bulles (ancienne API, wrapper POO)."""
    tri = TriBulles()
    tri.sort(bibliotheque)


def tri_tas(bibliotheque: List[Document]) -> None:
    """Tri par tas (ancienne API, wrapper POO)."""
    tri = TriTas()
    tri.sort(bibliotheque)


def tri_comptage(bibliotheque: List[Document]) -> None:
    """Tri par comptage (ancienne API, wrapper POO)."""
    tri = TriComptage()
    tri.sort(bibliotheque)


def rechercher_par_titre(bibliotheque: List[Document]) -> None:
    """
    Recherche par titre (ancienne API, wrapper POO).
    Affiche les résultats directement.
    """
    if not bibliotheque:
        print("\nℹ️ La bibliothèque est vide, aucune recherche possible.")
        return

    terme_recherche = input("\nEntrez le titre exact à rechercher: ").strip()
    
    search = SearchByTitle()
    bib = Bibliotheque(bibliotheque)
    resultats = bib.search(search, terme_recherche)

    if resultats:
        print(f"\n🎉 {len(resultats)} Résultat(s) trouvé(s) pour '{terme_recherche}':")
        for doc in resultats:
            print(f"- {doc}")
    else:
        print(f"\n😞 Aucun document trouvé avec le titre '{terme_recherche}'.")


def rechercher_par_auteur(bibliotheque: List[Document]) -> None:
    """Recherche par auteur (ancienne API, wrapper POO)."""
    if not bibliotheque:
        print("\nℹ️ La bibliothèque est vide, aucune recherche possible.")
        return

    terme_recherche = input("\nEntrez le nom de l'auteur à rechercher: ").strip()
    
    search = SearchByAuthor()
    bib = Bibliotheque(bibliotheque)
    resultats = bib.search(search, terme_recherche)

    if resultats:
        print(f"\n🎉 {len(resultats)} Résultat(s) trouvé(s) pour l'auteur '{terme_recherche}':")
        for doc in resultats:
            print(f"- {doc}")
    else:
        print(f"\n😞 Aucun document trouvé pour l'auteur '{terme_recherche}'.")


def rechercher_par_mots_cles(bibliotheque: List[Document]) -> None:
    """Recherche par mots-clés (ancienne API, wrapper POO)."""
    if not bibliotheque:
        print("\nℹ️ La bibliothèque est vide, aucune recherche possible.")
        return

    terme_recherche = input("\nEntrez le mot-clé à rechercher: ").strip()
    
    search = SearchByKeywords()
    bib = Bibliotheque(bibliotheque)
    resultats = bib.search(search, terme_recherche)

    if resultats:
        print(f"\n🎉 {len(resultats)} Résultat(s) trouvé(s) pour le mot-clé '{terme_recherche}':")
        for doc in resultats:
            print(f"- {doc}")
    else:
        print(f"\n😞 Aucun document trouvé avec le mot-clé '{terme_recherche}'.")


def rechercher_avancee(bibliotheque: List[Document]) -> None:
    """Recherche avancée (ancienne API, wrapper POO)."""
    if not bibliotheque:
        print("\nℹ️ La bibliothèque est vide, aucune recherche possible.")
        return

    terme_recherche = input("\nEntrez le terme à rechercher dans tous les champs: ").strip()
    
    search = SearchAdvanced()
    bib = Bibliotheque(bibliotheque)
    resultats = bib.search(search, terme_recherche)

    if resultats:
        print(f"\n🎉 {len(resultats)} Résultat(s) trouvé(s) pour '{terme_recherche}':")
        for doc in resultats:
            print(f"- {doc}")
    else:
        print(f"\n😞 Aucun document trouvé avec le terme '{terme_recherche}'.")


def ajouter_document(bibliotheque: List[Document], Document_Classe) -> None:
    """Ajoute un document (ancienne API, wrapper POO)."""
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


def afficher_bibliotheque(bibliotheque: List[Document]) -> None:
    """Affiche la bibliothèque (ancienne API, wrapper POO)."""
    if not bibliotheque:
        print("\nℹ️ La bibliothèque est actuellement vide.")
        return
    
    print("\n--- Contenu de la Bibliothèque (Total: "
          f"{len(bibliotheque)} documents) ---")
    for i, doc in enumerate(bibliotheque):
        print(f"[{i+1}] {doc}")
    print("-------------------------------------------------")


def comparer_temps_execution(Document_Classe, tri_insertion_func, tri_fusion_func):
    """Compare les temps d'exécution (wrapper POO)."""
    import time
    import random
    
    tailles = [10, 50, 100, 500, 1000]
    print("\n" + "=" * 70)
    print(" COMPARAISON DE PERFORMANCE : Tri Insertion vs Tri Fusion ")
    print("=" * 70)
    
    for taille in tailles:
        docs = [Document_Classe(f"Document {random.randint(1000, 9999)}", f"Auteur {i % 10}", f"tag{i % 5}") for i in range(taille)]
        random.shuffle(docs)
        
        from copy import deepcopy
        docs_copy = deepcopy(docs)
        start = time.perf_counter()
        tri_insertion = TriInsertion()
        tri_insertion.sort(docs_copy)
        temps_insertion = time.perf_counter() - start
        
        docs_copy = deepcopy(docs)
        start = time.perf_counter()
        tri_fusion = TriFusion()
        tri_fusion.sort(docs_copy)
        temps_fusion = time.perf_counter() - start
        
        print(f"\nTaille: {taille} documents")
        print(f"  Tri Insertion (O(n²)): {temps_insertion:.6f}s")
        print(f"  Tri Fusion (O(n log n)): {temps_fusion:.6f}s")
        if temps_insertion > 0:
            gain = (temps_insertion - temps_fusion) / temps_insertion * 100
            print(f"  Gain: {gain:.2f}%")


def comparer_tous_algorithmes_tri(Document_Classe):
    """Compare tous les algorithmes (wrapper POO)."""
    manager = BibliothequeManager()
    return manager.comparer_algorithmes_tri([10, 50, 100])


def comparer_tous_algorithmes_tri_gui(Document_Classe):
    """Compare tous les algorithmes pour l'interface (wrapper POO)."""
    manager = BibliothequeManager()
    return manager.comparer_algorithmes_tri([10, 50, 100])

