# Partie 2 - Arbre Binaire de Recherche (BST)

## 📚 Description

Un système de gestion de bibliothèque utilisant un **Arbre Binaire de Recherche (BST)** pour optimiser les performances de recherche et maintenir les documents triés automatiquement.

## ✨ Fonctionnalités

- Insertion optimisée de documents dans l'arbre
- Recherche ultra-rapide par titre (O(log n))
- Recherche par auteur, mots-clés ou dans tous les champs
- Suppression de documents
- Affichage trié automatique (parcours in-order)
- Comparaison de performances avec la recherche séquentielle

## 📁 Structure du projet

```
partie_2/
├── bst.py                    # Classes Node et BinarySearchTree
├── bst_manager.py            # Gestionnaire principal (POO)
├── search_algorithms_bst.py  # Algorithmes de recherche
├── compat.py                 # Module de compatibilité
├── bst_suppression.py        # Suppression interactive
└── README.md                 # Documentation
```

## 🚀 Utilisation

### Exemple simple

```python
from partie_2 import BSTManager

# Créer un gestionnaire BST
manager = BSTManager()

# Ajouter des documents
manager.ajouter_document("1984", "George Orwell", "dystopie,roman")
manager.ajouter_document("Le Petit Prince", "Antoine de Saint-Exupéry", "conte")
manager.ajouter_document("Dune", "Frank Herbert", "science-fiction")

# Rechercher un document (très rapide !)
doc = manager.rechercher_par_titre("1984")
print(doc)

# Afficher tous les documents (déjà triés)
print(manager.afficher_bst())
```

## 🎯 Avantages du BST

### Comparaison avec la liste (Partie 1)

| Opération               | Liste (Partie 1) | BST (Partie 2) | Gain                 |
| ----------------------- | ---------------- | -------------- | -------------------- |
| **Recherche par titre** | O(n)             | O(log n)       | 🚀 100x+ plus rapide |
| **Insertion**           | O(1)             | O(log n)       | Légèrement plus lent |
| **Tri**                 | O(n log n)       | Automatique    | ✅ Toujours trié     |
| **Affichage trié**      | O(n log n)       | O(n)           | ✅ Déjà en ordre     |

### Pourquoi le BST est plus rapide ?

- **Liste** : Pour trouver un document, on doit parcourir toute la liste (en moyenne N/2 éléments)
- **BST** : Grâce à sa structure d'arbre, on élimine la moitié des éléments à chaque étape

**Exemple concret** :

- 10 000 documents dans une liste → ~5 000 comparaisons
- 10 000 documents dans un BST → ~13 comparaisons seulement !

## 🔍 Recherche de documents

Plusieurs types de recherche sont disponibles :

```python
manager = BSTManager()

# Recherche par titre (O(log n) - RAPIDE !)
doc = manager.rechercher_par_titre("1984")

# Recherche par auteur (O(n))
docs = manager.rechercher_par_auteur("Orwell")

# Recherche par mots-clés (O(n))
docs = manager.rechercher_par_mots_cles("dystopie")

# Recherche avancée dans tous les champs (O(n))
docs = manager.rechercher_avancee("science")
```

## 📊 Opérations disponibles

### Ajout de documents

```python
# Ajout simple
manager.ajouter_document("Titre", "Auteur", "tag1,tag2")
```

**Via l'interface graphique** :

- Dans l'onglet **"Partie 2 (BST)"**, utilisez le formulaire d'ajout
- Champs disponibles :
  - **Titre** : Obligatoire
  - **Auteur** : Obligatoire
  - **Mots-clés** : Optionnel, séparés par des virgules

**⚠️ Important** : Le formulaire d'ajout de la Partie 2 ajoute les documents **uniquement dans le BST**, pas dans les autres structures (Liste, HashTable). Pour ajouter dans toutes les structures, utilisez le formulaire global de l'onglet "Partie 1".

**Fonctionnement** :

- Les documents sont automatiquement placés au bon endroit dans l'arbre
- Plus petit à gauche, plus grand à droite
- Complexité : **O(log n)**
- Sauvegarde automatique dans `bibliotheque_data_bst.json`

### Suppression de documents

```python
# Supprimer par titre
success = manager.supprimer_document("1984")

if success:
    print("✅ Document supprimé")
else:
    print("❌ Document non trouvé")
```

### Affichage

```python
# Afficher tous les documents triés
print(manager.afficher_bst())

# Obtenir la liste des documents
documents = manager.obtenir_documents_tries()
for doc in documents:
    print(doc)
```

## 📈 Statistiques

Obtenez des informations sur votre BST :

```python
stats = manager.get_statistiques()
print(f"Documents: {stats['nombre_documents']}")
print(f"Auteurs: {stats['nombre_auteurs']}")
print(f"Hauteur de l'arbre: {stats['hauteur_arbre']}")
```

La **hauteur** de l'arbre indique sa performance :

- **Hauteur idéale** : log₂(n) → arbre équilibré, recherche optimale
- **Hauteur maximale** : n → arbre dégénéré, performances réduites

## 🎓 Comment fonctionne un BST ?

### Structure de l'arbre

```
        "Le Petit Prince"
              /      \
           "Dune"    "Voyage"
           /    \
       "1984"  "Harry Potter"
```

- Chaque nœud a un document
- Fils **gauche** : titres plus petits (alphabétiquement)
- Fils **droite** : titres plus grands

### Recherche dans le BST

Pour chercher "Harry Potter" :

1. Comparer avec "Le Petit Prince" → plus petit → aller à gauche
2. Comparer avec "Dune" → plus grand → aller à droite
3. **Trouvé !** (seulement 3 comparaisons)

## 💾 Comparaison de performances

### Via l'interface graphique

Dans l'onglet **"Partie 2 (BST)"**, cliquez sur le bouton **"Comparer BST vs Liste"** pour :

- Comparer en temps réel les performances
- Voir les temps d'exécution détaillés
- Analyser le gain de performance
- Comprendre les complexités algorithmiques

**Résultats affichés** :

- Temps total et moyen par recherche
- Facteur d'amélioration (ex: "BST est 190x plus rapide")
- Analyse théorique (nombre de comparaisons)
- Recommandations selon la taille de la collection

### Via le code Python

```python
from partie_2 import comparer_recherche_performance, Document

# Compare sur 10 000 documents
comparer_recherche_performance(Document, 10000)
```

Résultat typique :

```
Recherche Séquentielle : 0.00234567s
Recherche BST         : 0.00001234s
Conclusion : Le BST est environ 190x plus rapide !
```

### Pourquoi le BST est si rapide ?

- **Liste** : Doit parcourir en moyenne N/2 éléments → O(n)
- **BST** : Élimine la moitié des candidats à chaque étape → O(log n)

**Exemple concret** :

- Collection de 1000 documents
  - Liste : ~500 comparaisons en moyenne
  - BST : ~10 comparaisons seulement !
  - **Gain : 50x plus rapide** 🚀

## 🛠️ Architecture POO

### Classes principales

- **`Node`** : Représente un nœud de l'arbre
- **`BinarySearchTree`** : L'arbre lui-même avec toutes les opérations
- **`BSTManager`** : Gestionnaire simplifié (recommandé)

### Algorithmes de recherche

- **`SearchByTitleBST`** : Recherche optimisée O(log n)
- **`SearchByAuthorBST`** : Recherche par auteur O(n)
- **`SearchByKeywordsBST`** : Recherche par mots-clés O(n)
- **`SearchAdvancedBST`** : Recherche globale O(n)

## 🎯 Quand utiliser le BST ?

### ✅ Utiliser le BST quand :

- Beaucoup de recherches par titre
- Collection de grande taille (> 100 documents)
- Besoin d'affichage trié fréquent
- Recherches plus importantes que les insertions

### ⚠️ Utiliser la liste (Partie 1) quand :

- Petite collection (< 50 documents)
- Beaucoup d'insertions/suppressions
- Ordre d'insertion important
- Accès par index nécessaire

## 🔧 Utilisation avancée

### Approche directe avec les classes

```python
from partie_2 import BinarySearchTree, SearchByTitleBST
from partie_1 import Document

# Créer un BST
bst = BinarySearchTree()

# Ajouter des documents
doc1 = Document("Python Basics", "John Doe", "python,tutorial")
doc2 = Document("Advanced Python", "Jane Smith", "python,advanced")
bst.insert(doc1)
bst.insert(doc2)

# Utiliser un algorithme de recherche spécifique
search_algo = SearchByTitleBST()
result = search_algo.search(bst, "Python Basics")
print(result)
```

### Parcours personnalisé

```python
def parcours_pre_order(node):
    """Parcours préfixe de l'arbre"""
    if node:
        print(node.document)
        parcours_pre_order(node.left)
        parcours_pre_order(node.right)

# Utiliser
parcours_pre_order(bst.root)
```

## 📝 Complexités algorithmiques

| Opération                | Meilleur cas | Cas moyen | Pire cas |
| ------------------------ | ------------ | --------- | -------- |
| **Recherche par titre**  | O(log n)     | O(log n)  | O(n)     |
| **Insertion**            | O(log n)     | O(log n)  | O(n)     |
| **Suppression**          | O(log n)     | O(log n)  | O(n)     |
| **Parcours in-order**    | O(n)         | O(n)      | O(n)     |
| **Recherche par auteur** | O(n)         | O(n)      | O(n)     |

**Note** : Le pire cas O(n) arrive quand l'arbre est déséquilibré (devient une liste).

## 🤝 Compatibilité

Le code existant continue de fonctionner grâce au module de compatibilité :

```python
# Ancienne API fonctionnelle
from partie_2 import BinarySearchTree, rechercher_par_titre_bst

bst = BinarySearchTree()
# ... ajouter des documents ...
doc = rechercher_par_titre_bst(bst, "1984")
```

## 🛠️ Lancement du programme

### Interface graphique

```bash
python main.py
```

Sélectionnez l'onglet **"Partie 2 (BST)"** pour utiliser l'arbre binaire.

### Mode terminal

```bash
python mode_terminal.py
```

Choisissez l'option pour la Partie 2.

---

## 📋 Résumé

La Partie 2 propose un système optimisé avec :

- ✅ Recherche ultra-rapide (O(log n))
- ✅ Tri automatique des documents
- ✅ Structure d'arbre efficace
- ✅ Architecture POO moderne
- ✅ Compatible avec la Partie 1

**🎯 Idéal pour les grandes collections avec beaucoup de recherches !**

---

**Version** : 2.0.0  
**Date** : Octobre 2025
