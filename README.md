# 📚 Gestion d'une Bibliothèque Numérique

Projet de gestion de documents utilisant différentes structures de données et algorithmes en Python.

## 📋 Description

Application complète permettant de gérer une collection de documents (livres) avec trois structures de données différentes :

- **Liste Python** - Structure de base pour le stockage et le tri
- **Arbre Binaire de Recherche (BST)** - Pour des recherches optimisées
- **Table de Hachage** - Pour des accès ultra-rapides par auteur

## 🚀 Démarrage Rapide

### Prérequis

- Python 3.7 ou supérieur
- Tkinter (inclus avec Python)

### Installation

```bash
# Cloner ou télécharger le projet
cd TP1_Algo_python

# Lancer l'interface graphique
python main.py

# OU lancer le mode terminal
python mode_terminal.py
```

## 📁 Structure du Projet

```
TP1_Algo_python/
│
├── main.py                    # Point d'entrée de l'application
├── mode_terminal.py           # Interface en ligne de commande
├── tests_tri.py              # Tests unitaires des algorithmes
│
├── interface/                # Interface graphique
│   └── ui.py                 # Interface Tkinter complète
│
├── partie_1/                 # Liste Python et algorithmes de base
│   ├── document.py           # Classe Document
│   ├── bibliotheque.py       # Gestion de la bibliothèque
│   ├── tri_algorithms.py     # 7 algorithmes de tri
│   ├── search_algorithms.py  # Algorithmes de recherche
│   └── persistance.py        # Sauvegarde/Chargement JSON
│
├── partie_2/                 # Arbre Binaire de Recherche
│   ├── bst.py               # Implémentation du BST
│   ├── bst_manager.py       # Gestionnaire BST
│   └── search_algorithms_bst.py
│
└── partie_3/                 # Table de Hachage
    ├── hashing.py           # Implémentation Hash Table
    ├── hash_manager.py      # Gestionnaire Hash
    └── search_algorithms_hash.py
```

## ✨ Fonctionnalités

### 📖 Gestion des Documents

- Ajouter des documents (titre, auteur, mots-clés)
- Supprimer des documents
- Visualiser la collection

### 🔄 Algorithmes de Tri (7 au total)

- **O(n²)** : Tri par insertion, sélection, bulles
- **O(n log n)** : Tri rapide, fusion, tas
- **Spéciaux** : Tri comptage
- Comparaison des performances
- Visualisation en temps réel

### 🔍 Recherche

- **Recherche séquentielle** O(n) - Par titre, auteur, mots-clés
- **Recherche BST** O(log n) - Recherche optimisée par titre
- **Recherche Hash** O(1) - Recherche ultra-rapide par auteur
- Recherche avancée multi-critères

### 🧪 Tests Unitaires

- 42 tests automatisés
- 7 algorithmes × 6 scénarios
- Validation à 100%

## 🎯 Utilisation

### Interface Graphique

```bash
python main.py
```

**6 onglets disponibles** :

1. **Ajout Global** - Ajouter des documents dans toutes les structures
2. **Partie 1 (Liste)** - Gestion et recherche sur liste Python
3. **Partie 2 (BST)** - Arbre binaire et comparaisons de performances
4. **Partie 3 (Hachage)** - Table de hachage et analyse
5. **Suppression** - Supprimer des documents
6. **Affichage** - Visualisation et tests des algorithmes de tri

### Mode Terminal

```bash
python mode_terminal.py
```

Menu interactif avec options :

- Afficher tous les documents
- Ajouter un document
- Rechercher un document
- Trier la liste
- Comparer les algorithmes

## 📊 Performances

### Complexités

| Opération   | Liste              | BST      | Hash |
| ----------- | ------------------ | -------- | ---- |
| Insertion   | O(1)               | O(log n) | O(1) |
| Recherche   | O(n)               | O(log n) | O(1) |
| Suppression | O(n)               | O(log n) | O(1) |
| Tri         | O(n²) à O(n log n) | -        | -    |

### Résultats Typiques (77 documents)

- **BST vs Liste** : 30-50× plus rapide pour la recherche
- **Hash vs Liste** : 70× plus rapide pour la recherche par auteur

## 🧪 Tests

Exécuter les tests unitaires :

```bash
python tests_tri.py
```

Ou depuis l'interface graphique :

- Onglet **Affichage** → Bouton **"Exécuter les Tests Unitaires"**

## 💾 Persistance

Les données sont automatiquement sauvegardées dans :

- `bibliotheque_data.json` - Collection principale
- `bibliotheque_data_bst.json` - Données du BST
- `bibliotheque_data_hash.json` - Données de la table de hachage

## 📚 Documentation Détaillée

Chaque partie dispose de sa propre documentation :

- `partie_1/README.md` - Liste Python et algorithmes
- `partie_2/README.md` - Arbre binaire de recherche
- `partie_3/README.md` - Table de hachage

## 🎨 Captures d'Écran

L'interface graphique propose :

- Design moderne avec Tkinter
- Visualisation en temps réel
- Comparaisons de performances
- Tests intégrés
- Mélange aléatoire de la liste

## 🔧 Architecture

**Design Patterns utilisés** :

- **Strategy Pattern** - Pour les algorithmes de tri et recherche
- **Facade Pattern** - Pour les gestionnaires (Manager)
- **Iterator Pattern** - Pour parcourir les collections

**Principes POO** :

- Encapsulation des données
- Séparation des responsabilités
- Code modulaire et réutilisable

## 📝 Exemples de Code

### Ajouter un document

```python
from partie_1.document import Document
from partie_1.bibliotheque import Bibliotheque

bib = Bibliotheque()
doc = Document("1984", "George Orwell", "dystopie,politique")
bib.add_document(doc)
```

### Trier la collection

```python
from partie_1.tri_algorithms import TriRapide

tri = TriRapide()
tri.sort(bib.documents)
```

### Rechercher dans le BST

```python
from partie_2.bst import BinarySearchTree

bst = BinarySearchTree()
bst.insert(doc)
resultat = bst.search("1984")
```

## ⚙️ Détails Techniques

- **Langage** : Python 3.7+
- **Interface** : Tkinter
- **Persistance** : JSON
- **Tests** : Tests unitaires personnalisés
- **Mesure de performance** : `time.perf_counter()`

## 🎓 Concepts Couverts

- Structures de données (Liste, BST, Hash)
- Algorithmes de tri (7 algorithmes)
- Algorithmes de recherche (séquentielle, binaire, hachage)
- Complexité algorithmique
- Programmation orientée objet
- Tests unitaires
- Interface utilisateur
- Persistance de données

## 📞 Support

1. Consulter la documentation dans chaque dossier `partie_X/README.md`
2. Vérifier les tests unitaires avec `python tests_tri.py`
3. Lancer l'application avec `python main.py`

---

**Version** : 1.0  
**Date** : 23 Octobre 2025  
**Statut** : ✅ Opérationnel
