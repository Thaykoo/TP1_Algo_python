
from typing import List, Dict, Any
import time
from copy import deepcopy

from .bibliotheque import Bibliotheque
from .document import Document
from .tri_algorithms import (
    TriAlgorithm, TriInsertion, TriSelection, TriBulles,
    TriRapide, TriFusion, TriTas, TriComptage
)
from .search_algorithms import (
    SearchAlgorithm, SearchByTitle, SearchByAuthor,
    SearchByKeywords, SearchAdvanced
)


class BibliothequeManager:
    """
    Gestionnaire principal pour la bibliothèque.
    Centralise les opérations de tri, recherche et gestion.
    """
    
    def __init__(self, bibliotheque: Bibliotheque = None):
        """
        Initialise le gestionnaire.
        
        Args:
            bibliotheque: Instance de Bibliotheque (optionnel)
        """
        self.bibliotheque = bibliotheque if bibliotheque else Bibliotheque()
        
        self.tri_algorithms = {
            'insertion': TriInsertion(),
            'selection': TriSelection(),
            'bulles': TriBulles(),
            'rapide': TriRapide(),
            'fusion': TriFusion(),
            'tas': TriTas(),
            'comptage': TriComptage()
        }
        
        self.search_algorithms = {
            'titre': SearchByTitle(),
            'auteur': SearchByAuthor(),
            'mots_cles': SearchByKeywords(),
            'avancee': SearchAdvanced()
        }
    
    
    def ajouter_document(self, titre: str, auteur: str, mots_cles: str = "") -> Document:
        """
        Ajoute un nouveau document à la bibliothèque.
        
        Args:
            titre: Titre du document
            auteur: Auteur du document
            mots_cles: Mots-clés séparés par des virgules
            
        Returns:
            Le document créé
        """
        doc = Document(titre, auteur, mots_cles)
        self.bibliotheque.add_document(doc)
        return doc
    
    def supprimer_document(self, titre: str) -> bool:
        """
        Supprime un document par son titre.
        
        Args:
            titre: Titre du document à supprimer
            
        Returns:
            True si supprimé, False sinon
        """
        return self.bibliotheque.remove_document(titre)
    
    def vider_bibliotheque(self) -> None:
        """Vide complètement la bibliothèque."""
        self.bibliotheque.clear()
    
    
    def trier(self, algorithm_name: str = 'insertion') -> None:
        """
        Trie la bibliothèque avec l'algorithme spécifié.
        
        Args:
            algorithm_name: Nom de l'algorithme ('insertion', 'fusion', etc.)
        """
        algorithm = self.tri_algorithms.get(algorithm_name)
        if algorithm:
            self.bibliotheque.sort(algorithm)
        else:
            raise ValueError(f"Algorithme de tri '{algorithm_name}' non disponible")
    
    def trier_avec_mesure(self, algorithm_name: str = 'insertion') -> Dict[str, Any]:
        """
        Trie et mesure les performances.
        
        Args:
            algorithm_name: Nom de l'algorithme
            
        Returns:
            Dictionnaire avec les résultats (temps, algorithme, complexité)
        """
        algorithm = self.tri_algorithms.get(algorithm_name)
        if not algorithm:
            raise ValueError(f"Algorithme de tri '{algorithm_name}' non disponible")
        
        start_time = time.time()
        self.bibliotheque.sort(algorithm)
        end_time = time.time()
        
        return {
            'algorithme': algorithm.name,
            'complexite': algorithm.complexity,
            'temps': end_time - start_time,
            'nombre_documents': self.bibliotheque.size
        }
    
    def comparer_algorithmes_tri(self, tailles: List[int] = None) -> List[Dict[str, Any]]:
        """
        Compare les performances de tous les algorithmes de tri.
        
        Args:
            tailles: Liste des tailles à tester
            
        Returns:
            Liste de dictionnaires avec les résultats
        """
        if tailles is None:
            tailles = [10, 50, 100, 500, 1000]
        
        resultats = []
        
        for taille in tailles:
            import random
            test_docs = [Document(f"Document {random.randint(1000, 9999)}", f"Auteur {i % 10}", f"tag{i % 5}") for i in range(taille)]
            random.shuffle(test_docs)
            
            taille_resultats = {
                'taille': taille,
                'algorithmes': []
            }
            
            for nom, algorithm in self.tri_algorithms.items():
                docs_copy = deepcopy(test_docs)
                
                start_time = time.perf_counter()
                algorithm.sort(docs_copy)
                end_time = time.perf_counter()
                
                taille_resultats['algorithmes'].append({
                    'nom': nom.capitalize(),
                    'complexite': algorithm.complexity,
                    'temps': end_time - start_time
                })
            
            resultats.append(taille_resultats)
        
        return resultats
    
    
    def rechercher(self, terme: str, algorithm_name: str = 'avancee') -> List[Document]:
        """
        Recherche des documents avec l'algorithme spécifié.
        
        Args:
            terme: Terme de recherche
            algorithm_name: Nom de l'algorithme ('titre', 'auteur', etc.)
            
        Returns:
            Liste des documents trouvés
        """
        algorithm = self.search_algorithms.get(algorithm_name)
        if algorithm:
            return self.bibliotheque.search(algorithm, terme)
        else:
            raise ValueError(f"Algorithme de recherche '{algorithm_name}' non disponible")
    
    def rechercher_par_titre(self, titre: str) -> List[Document]:
        """Recherche par titre exact."""
        return self.rechercher(titre, 'titre')
    
    def rechercher_par_auteur(self, auteur: str) -> List[Document]:
        """Recherche par auteur."""
        return self.rechercher(auteur, 'auteur')
    
    def rechercher_par_mots_cles(self, mot_cle: str) -> List[Document]:
        """Recherche par mots-clés."""
        return self.rechercher(mot_cle, 'mots_cles')
    
    def rechercher_avancee(self, terme: str) -> List[Document]:
        """Recherche avancée dans tous les champs."""
        return self.rechercher(terme, 'avancee')
    
    
    def afficher_bibliotheque(self) -> str:
        """
        Retourne une représentation textuelle de la bibliothèque.
        
        Returns:
            Chaîne formatée avec tous les documents
        """
        return str(self.bibliotheque)
    
    def get_statistiques(self) -> Dict[str, Any]:
        """
        Retourne des statistiques sur la bibliothèque.
        
        Returns:
            Dictionnaire avec les statistiques
        """
        if self.bibliotheque.is_empty():
            return {
                'nombre_documents': 0,
                'nombre_auteurs': 0,
                'nombre_mots_cles': 0
            }
        
        auteurs = set()
        mots_cles = set()
        
        for doc in self.bibliotheque:
            auteurs.add(doc.auteur)
            mots_cles.update(doc.mots_cles)
        
        return {
            'nombre_documents': self.bibliotheque.size,
            'nombre_auteurs': len(auteurs),
            'nombre_mots_cles': len(mots_cles),
            'auteurs': sorted(list(auteurs)),
            'mots_cles_uniques': sorted(list(mots_cles))
        }
    
    
    def __str__(self) -> str:
        """Représentation textuelle du gestionnaire."""
        stats = self.get_statistiques()
        return f"BibliothequeManager({stats['nombre_documents']} documents)"
    
    def __repr__(self) -> str:
        """Représentation pour debug."""
        return f"BibliothequeManager(bibliotheque={repr(self.bibliotheque)})"

