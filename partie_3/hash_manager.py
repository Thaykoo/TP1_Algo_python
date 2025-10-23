
from .hashing import HashTable, Bucket
from typing import List, Optional, Dict, Any
import time

try:
    from ..partie_1.document import Document
except ImportError:
    from partie_1.document import Document


class HashTableManager:
    """
    Gestionnaire principal pour la Table de Hachage (Facade Pattern).
    Simplifie l'utilisation de la HashTable et fournit une interface cohérente.
    """
    
    def __init__(self, size: int = 50, hash_table: Optional[HashTable] = None):
        """
        Initialise le gestionnaire avec une HashTable existante ou en crée une nouvelle.
        
        Args:
            size: La taille de la table de hachage
            hash_table: Une HashTable existante (optionnel)
        """
        self.hash_table = hash_table if hash_table is not None else HashTable(size)
    
    
    def ajouter_document(self, titre: str, auteur: str, mots_cles: str) -> bool:
        """
        Ajoute un nouveau document à la table de hachage.
        
        Args:
            titre: Le titre du document
            auteur: L'auteur du document (clé d'indexation)
            mots_cles: Les mots-clés (séparés par des virgules)
            
        Returns:
            True si l'ajout a réussi
        """
        try:
            document = Document(titre, auteur, mots_cles)
            self.hash_table.insert(document)
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout : {e}")
            return False
    
    def rechercher_par_auteur(self, auteur: str) -> List[Document]:
        """
        Recherche tous les documents d'un auteur.
        Utilise l'index de hachage pour une recherche O(1).
        
        Args:
            auteur: Le nom de l'auteur
            
        Returns:
            Liste des documents trouvés
        """
        return self.hash_table.search_by_author(auteur)
    
    def rechercher_par_titre(self, titre: str) -> List[Document]:
        """
        Recherche des documents par titre.
        Note: O(n) car la table est indexée par auteur, pas par titre.
        
        Args:
            titre: Le titre à rechercher
            
        Returns:
            Liste des documents trouvés
        """
        return self.hash_table.search_by_title(titre)
    
    def rechercher_par_mots_cles(self, mot_cle: str) -> List[Document]:
        """
        Recherche tous les documents contenant un mot-clé.
        
        Args:
            mot_cle: Le mot-clé à rechercher
            
        Returns:
            Liste des documents trouvés
        """
        return self.hash_table.search_by_keywords(mot_cle)
    
    def rechercher_avancee(self, terme: str) -> List[Document]:
        """
        Recherche avancée dans tous les champs.
        
        Args:
            terme: Le terme à rechercher
            
        Returns:
            Liste des documents trouvés
        """
        return self.hash_table.search_advanced(terme)
    
    
    def obtenir_tous_documents(self) -> List[Document]:
        """
        Retourne tous les documents de la table de hachage.
        
        Returns:
            Liste de tous les documents
        """
        documents = []
        for bucket in self.hash_table.table:
            documents.extend(bucket.items)
        return documents
    
    def afficher_hash_table(self) -> str:
        """
        Retourne une représentation textuelle de tous les documents.
        
        Returns:
            Chaîne formatée avec tous les documents
        """
        documents = self.obtenir_tous_documents()
        
        if not documents:
            return "📚 La table de hachage est vide."
        
        resultat = [f"📚 Table de Hachage - {len(documents)} document(s) :\n"]
        resultat.append("=" * 70)
        
        for i, doc in enumerate(documents, 1):
            resultat.append(f"{i}. {doc}")
        
        resultat.append("=" * 70)
        return "\n".join(resultat)
    
    def get_statistiques(self) -> Dict[str, Any]:
        """
        Retourne des statistiques sur la table de hachage.
        
        Returns:
            Dictionnaire avec les statistiques
        """
        documents = self.obtenir_tous_documents()
        
        auteurs = set(doc.auteur for doc in documents)
        
        mots_cles = set()
        for doc in documents:
            mots_cles.update(doc.mots_cles)
        
        buckets_utilises = sum(1 for bucket in self.hash_table.table if bucket.items)
        collisions = sum(max(0, len(bucket.items) - 1) for bucket in self.hash_table.table)
        
        max_bucket_size = max(len(bucket.items) for bucket in self.hash_table.table)
        
        load_factor = len(documents) / self.hash_table.size if self.hash_table.size > 0 else 0
        
        return {
            'nombre_documents': len(documents),
            'nombre_auteurs': len(auteurs),
            'nombre_mots_cles': len(mots_cles),
            'taille_table': self.hash_table.size,
            'buckets_utilises': buckets_utilises,
            'collisions': collisions,
            'max_bucket_size': max_bucket_size,
            'facteur_charge': load_factor,
            'est_vide': len(documents) == 0
        }
    
    def afficher_distribution(self) -> str:
        """
        Affiche la distribution des documents dans les buckets.
        
        Returns:
            Chaîne formatée avec la distribution
        """
        resultat = ["📊 Distribution des buckets :\n"]
        resultat.append("=" * 70)
        
        for i, bucket in enumerate(self.hash_table.table):
            if bucket.items:
                resultat.append(f"Bucket {i:3d} : {len(bucket.items)} document(s)")
                for doc in bucket.items[:3]:
                    resultat.append(f"  - {doc.titre} ({doc.auteur})")
                if len(bucket.items) > 3:
                    resultat.append(f"  ... et {len(bucket.items) - 3} autre(s)")
        
        resultat.append("=" * 70)
        return "\n".join(resultat)
    
    
    def vider(self) -> None:
        """Vide complètement la table de hachage."""
        for bucket in self.hash_table.table:
            bucket.items.clear()
    
    def est_vide(self) -> bool:
        """
        Vérifie si la table de hachage est vide.
        
        Returns:
            True si la table est vide
        """
        return all(not bucket.items for bucket in self.hash_table.table)
    
    def taille(self) -> int:
        """
        Retourne le nombre total de documents dans la table.
        
        Returns:
            Le nombre de documents
        """
        return len(self.obtenir_tous_documents())
    
    def charger_depuis_bst(self, bst) -> int:
        """
        Charge les documents depuis un BST.
        
        Args:
            bst: L'arbre binaire de recherche source
            
        Returns:
            Le nombre de documents chargés
        """
        try:
            self.hash_table.populate_from_bst(bst)
            return self.taille()
        except Exception as e:
            print(f"❌ Erreur lors du chargement : {e}")
            return 0
    
    
    def rechercher_avec_mesure(self, auteur: str) -> Dict[str, Any]:
        """
        Recherche un auteur et mesure le temps d'exécution.
        
        Args:
            auteur: Le nom de l'auteur
            
        Returns:
            Dictionnaire avec les résultats et le temps
        """
        start_time = time.time()
        resultats = self.hash_table.search_by_author(auteur)
        end_time = time.time()
        
        return {
            'resultats': resultats,
            'nombre_resultats': len(resultats),
            'temps': end_time - start_time,
            'complexite': 'O(1)'
        }
    
    
    def __len__(self) -> int:
        """Retourne le nombre de documents."""
        return self.taille()
    
    def __str__(self) -> str:
        """Retourne une représentation textuelle de la table."""
        return self.afficher_hash_table()
    
    def __bool__(self) -> bool:
        """Retourne True si la table n'est pas vide."""
        return not self.est_vide()
    
    def __iter__(self):
        """Permet d'itérer sur tous les documents."""
        return iter(self.obtenir_tous_documents())

