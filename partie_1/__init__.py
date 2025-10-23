
from .document import Document

from .bibliotheque import Bibliotheque
from .gestionnaire_poo import BibliothequeManager
from .tri_algorithms import (
    TriAlgorithm, TriInsertion, TriSelection, TriBulles,
    TriRapide, TriFusion, TriTas, TriComptage
)
from .search_algorithms import (
    SearchAlgorithm, SearchByTitle, SearchByAuthor,
    SearchByKeywords, SearchAdvanced
)

from .compat import (
    trier_par_titre, 
    rechercher_par_titre, 
    rechercher_par_auteur,
    rechercher_par_mots_cles,
    rechercher_avancee,
    ajouter_document, 
    afficher_bibliotheque,
    tri_fusion,
    tri_rapide,
    tri_selection,
    tri_bulles,
    tri_tas,
    tri_comptage,
    comparer_temps_execution,
    comparer_tous_algorithmes_tri,
    comparer_tous_algorithmes_tri_gui
)

from .persistance import (
    save_data, load_data, save_all_structures, 
    load_all_structures, create_default_data
)

from .suppression_avancee import (
    supprimer_document_complet, 
    supprimer_par_criteres, 
    supprimer_documents_multiples,
    vider_toutes_structures,
    obtenir_statistiques_suppression
)