
from abc import ABC, abstractmethod
from typing import List
import time


class TriAlgorithm(ABC):
    """Classe abstraite pour les algorithmes de tri."""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.complexity = "O(?)"
    
    @abstractmethod
    def sort(self, documents: List) -> None:
        """
        Trie la liste de documents en place.
        
        Args:
            documents: Liste de documents à trier
        """
        pass
    
    def sort_and_measure(self, documents: List) -> float:
        """
        Trie et mesure le temps d'exécution.
        
        Args:
            documents: Liste de documents à trier
            
        Returns:
            Temps d'exécution en secondes
        """
        start_time = time.time()
        self.sort(documents)
        end_time = time.time()
        return end_time - start_time
    
    def __str__(self) -> str:
        return f"{self.name} ({self.complexity})"


class TriInsertion(TriAlgorithm):
    """
    Algorithme de Tri par Insertion (Insertion Sort).
    Complexité : O(n²).
    """
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n²)"
    
    def sort(self, documents: List) -> None:
        """Trie la liste par insertion."""
        n = len(documents)
        for i in range(1, n):
            cle_doc = documents[i]
            j = i - 1
            
            while j >= 0 and cle_doc.titre.lower() < documents[j].titre.lower():
                documents[j + 1] = documents[j]
                j -= 1
            
            documents[j + 1] = cle_doc


class TriSelection(TriAlgorithm):
    """
    Algorithme de Tri par Sélection (Selection Sort).
    Complexité : O(n²).
    """
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n²)"
    
    def sort(self, documents: List) -> None:
        """Trie la liste par sélection."""
        n = len(documents)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if documents[j].titre.lower() < documents[min_idx].titre.lower():
                    min_idx = j
            
            documents[i], documents[min_idx] = documents[min_idx], documents[i]


class TriBulles(TriAlgorithm):
    """
    Algorithme de Tri à Bulles (Bubble Sort).
    Complexité : O(n²).
    """
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n²)"
    
    def sort(self, documents: List) -> None:
        """Trie la liste par bulles."""
        n = len(documents)
        for i in range(n):
            echange = False
            for j in range(0, n - i - 1):
                if documents[j].titre.lower() > documents[j + 1].titre.lower():
                    documents[j], documents[j + 1] = documents[j + 1], documents[j]
                    echange = True
            
            if not echange:
                break


class TriRapide(TriAlgorithm):
    """
    Algorithme de Tri Rapide (Quick Sort).
    Complexité : O(n log n) en moyenne, O(n²) dans le pire cas.
    """
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n log n)"
    
    def sort(self, documents: List) -> None:
        """Trie la liste par tri rapide."""
        self._quick_sort(documents, 0, len(documents) - 1)
    
    def _quick_sort(self, documents: List, bas: int, haut: int) -> None:
        """Fonction récursive pour le tri rapide."""
        if bas < haut:
            pi = self._partition(documents, bas, haut)
            self._quick_sort(documents, bas, pi - 1)
            self._quick_sort(documents, pi + 1, haut)
    
    def _partition(self, documents: List, bas: int, haut: int) -> int:
        """Partitionne la liste."""
        pivot = documents[haut].titre.lower()
        i = bas - 1
        
        for j in range(bas, haut):
            if documents[j].titre.lower() <= pivot:
                i += 1
                documents[i], documents[j] = documents[j], documents[i]
        
        documents[i + 1], documents[haut] = documents[haut], documents[i + 1]
        return i + 1


class TriFusion(TriAlgorithm):
    """
    Algorithme de Tri Fusion (Merge Sort).
    Complexité : O(n log n).
    """
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n log n)"
    
    def sort(self, documents: List) -> None:
        """Trie la liste par tri fusion."""
        if len(documents) > 1:
            self._merge_sort(documents, 0, len(documents) - 1)
    
    def _merge_sort(self, documents: List, gauche: int, droite: int) -> None:
        """Fonction récursive pour le tri fusion."""
        if gauche < droite:
            milieu = (gauche + droite) // 2
            
            self._merge_sort(documents, gauche, milieu)
            self._merge_sort(documents, milieu + 1, droite)
            
            self._merge(documents, gauche, milieu, droite)
    
    def _merge(self, documents: List, gauche: int, milieu: int, droite: int) -> None:
        """Fusionne deux sous-listes triées."""
        gauche_copy = documents[gauche:milieu + 1]
        droite_copy = documents[milieu + 1:droite + 1]
        
        i = j = 0
        k = gauche
        
        while i < len(gauche_copy) and j < len(droite_copy):
            if gauche_copy[i].titre.lower() <= droite_copy[j].titre.lower():
                documents[k] = gauche_copy[i]
                i += 1
            else:
                documents[k] = droite_copy[j]
                j += 1
            k += 1
        
        while i < len(gauche_copy):
            documents[k] = gauche_copy[i]
            i += 1
            k += 1
        
        while j < len(droite_copy):
            documents[k] = droite_copy[j]
            j += 1
            k += 1


class TriTas(TriAlgorithm):
    """
    Algorithme de Tri par Tas (Heap Sort).
    Complexité : O(n log n).
    """
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n log n)"
    
    def sort(self, documents: List) -> None:
        """Trie la liste par tri par tas."""
        n = len(documents)
        
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(documents, n, i)
        
        for i in range(n - 1, 0, -1):
            documents[0], documents[i] = documents[i], documents[0]
            self._heapify(documents, i, 0)
    
    def _heapify(self, documents: List, n: int, i: int) -> None:
        """Crée un tas max."""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and documents[left].titre.lower() > documents[largest].titre.lower():
            largest = left
        
        if right < n and documents[right].titre.lower() > documents[largest].titre.lower():
            largest = right
        
        if largest != i:
            documents[i], documents[largest] = documents[largest], documents[i]
            self._heapify(documents, n, largest)


class TriComptage(TriAlgorithm):
    """
    Algorithme de Tri par Comptage adapté (Counting Sort).
    Complexité : O(n + k) où k est la plage des valeurs.
    """
    
    def __init__(self):
        super().__init__()
        self.complexity = "O(n + k)"
    
    def sort(self, documents: List) -> None:
        """Trie la liste par tri par comptage (basé sur la première lettre)."""
        if not documents:
            return
        
        buckets = {}
        
        for doc in documents:
            first_char = doc.titre[0].lower() if doc.titre else ' '
            if first_char not in buckets:
                buckets[first_char] = []
            buckets[first_char].append(doc)
        
        documents.clear()
        for key in sorted(buckets.keys()):
            bucket = buckets[key]
            bucket.sort(key=lambda d: d.titre.lower())
            documents.extend(bucket)

