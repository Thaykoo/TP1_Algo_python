# Fichier : partie_1/__init__.py

from .document import Document
from .gestionnaire import (
    trier_par_titre, 
    rechercher_par_titre, 
    ajouter_document, 
    afficher_bibliotheque
)
# Ajout des fonctions du supplément
from .supplement_algo import (
    tri_fusion,
    comparer_temps_execution
)

from .persistance import save_data, load_data