# Partie 3 - Table de Hachage (HashTable)

## 📚 Description

Un système de gestion de bibliothèque utilisant une **Table de Hachage** pour permettre des recherches ultra-rapides par auteur (complexité O(1)).

## ✨ Fonctionnalités

- Insertion rapide de documents
- Recherche instantanée par auteur (O(1)) grâce au hachage
- Recherche par titre, mots-clés ou dans tous les champs
- Gestion automatique des collisions (chaînage)
- Analyse de la distribution des données
- Comparaison de performances avec la recherche séquentielle

## 📁 Structure du projet

```
partie_3/
├── hashing.py                 # Classes Bucket et HashTable
├── hash_manager.py            # Gestionnaire principal (POO)
├── search_algorithms_hash.py  # Algorithmes de recherche
├── compat.py                  # Module de compatibilité
└── README.md                  # Documentation
```

## 🚀 Utilisation

### Exemple simple

```python
from partie_3 import HashTableManager

# Créer un gestionnaire HashTable
manager = HashTableManager(size=50)

# Ajouter des documents
manager.ajouter_document("1984", "George Orwell", "dystopie,roman")
manager.ajouter_document("Dune", "Frank Herbert", "science-fiction")
manager.ajouter_document("Fondation", "Isaac Asimov", "science-fiction")

# Rechercher par auteur (ULTRA RAPIDE - O(1) !)
docs = manager.rechercher_par_auteur("Orwell")
print(f"Trouvé {len(docs)} document(s)")

# Afficher tous les documents
print(manager.afficher_hash_table())
```

## 🎯 Avantages de la Table de Hachage

### Comparaison avec Liste et BST

| Opération                | Liste (P1) | BST (P2)    | HashTable (P3) | Meilleur         |
| ------------------------ | ---------- | ----------- | -------------- | ---------------- |
| **Recherche par auteur** | O(n)       | O(n)        | O(1)           | 🏆 **HashTable** |
| **Recherche par titre**  | O(n)       | O(log n)    | O(n)           | 🏆 BST           |
| **Insertion**            | O(1)       | O(log n)    | O(1)           | 🏆 Liste/Hash    |
| **Tri**                  | O(n log n) | Automatique | ❌ Pas trié    | BST              |

### Pourquoi la HashTable est ultra-rapide ?

- **Liste** : Doit parcourir tous les documents → O(n)
- **BST** : Doit parcourir tout l'arbre pour les auteurs → O(n)
- **HashTable** : Calcule directement l'emplacement → **O(1)** ! ⚡

**Exemple concret** :

- 10 000 documents dans une liste → ~5 000 comparaisons
- 10 000 documents dans un BST → ~10 000 comparaisons (auteur)
- 10 000 documents dans une HashTable → **~1 comparaison** ! 🚀

## 🔍 Recherche de documents

Plusieurs types de recherche sont disponibles :

```python
manager = HashTableManager()

# Recherche par auteur (O(1) - INSTANTANÉ !)
docs = manager.rechercher_par_auteur("Orwell")

# Recherche par titre (O(n))
docs = manager.rechercher_par_titre("1984")

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

# Les documents sont automatiquement placés dans le bon bucket
# selon le hash de l'auteur
```

### Affichage

```python
# Afficher tous les documents
print(manager.afficher_hash_table())

# Voir la distribution des buckets
print(manager.afficher_distribution())

# Obtenir la liste des documents
documents = manager.obtenir_tous_documents()
for doc in documents:
    print(doc)
```

## 📈 Statistiques

Obtenez des informations sur votre table de hachage :

```python
stats = manager.get_statistiques()
print(f"Documents: {stats['nombre_documents']}")
print(f"Buckets utilisés: {stats['buckets_utilises']}")
print(f"Collisions: {stats['collisions']}")
print(f"Facteur de charge: {stats['facteur_charge']:.2f}")
```

### Comprendre les statistiques

- **Facteur de charge** : documents / taille_table

  - < 0.7 : Excellent, peu de collisions
  - 0.7-1.0 : Bon, quelques collisions
  - \> 1.0 : Augmenter la taille de la table

- **Collisions** : Nombre de buckets contenant plusieurs documents
  - Normal et géré automatiquement par chaînage

## 🎓 Comment fonctionne une Table de Hachage ?

### Structure

```
Table de Hachage (size=5)
─────────────────────────
Bucket 0: []
Bucket 1: [Doc1: "1984" par Orwell]
Bucket 2: [Doc2: "Dune" par Herbert, Doc3: "Fondation" par Asimov]  ← Collision !
Bucket 3: []
Bucket 4: [Doc4: "Neuromancien" par Gibson]
```

### Principe du hachage

1. **Insertion** :

   - Calculer hash("Orwell") → 1
   - Placer le document dans Bucket 1
   - Temps : **O(1)** ! ⚡

2. **Recherche** :

   - Calculer hash("Orwell") → 1
   - Aller directement au Bucket 1
   - Temps : **O(1)** ! ⚡

3. **Collision** :
   - Si hash("Herbert") = hash("Asimov") = 2
   - Les deux documents vont dans Bucket 2
   - Chaînage : liste dans le même bucket

## 💾 Comparaison de performances

Comparez la HashTable avec la recherche séquentielle :

```python
from partie_3 import comparer_recherche_hachage, Document

# Compare sur 10 000 documents
comparer_recherche_hachage(Document, 10000)
```

Résultat typique :

```
Recherche Séquentielle : 0.00234567s
Recherche HashTable   : 0.00000123s
Conclusion : La HashTable est environ 1900x plus rapide !
```

## 🛠️ Architecture POO

### Classes principales

- **`Bucket`** : Représente un seau (liste de documents)
- **`HashTable`** : La table elle-même avec tous les buckets
- **`HashTableManager`** : Gestionnaire simplifié (recommandé)

### Algorithmes de recherche

- **`SearchByAuthorHash`** : Recherche optimisée O(1)
- **`SearchByTitleHash`** : Recherche par titre O(n)
- **`SearchByKeywordsHash`** : Recherche par mots-clés O(n)
- **`SearchAdvancedHash`** : Recherche globale O(n)

## 🎯 Quand utiliser la HashTable ?

### ✅ Utiliser la HashTable quand :

- **Beaucoup de recherches par auteur**
- Besoin de performances maximales
- Clé d'indexation bien définie (auteur)
- Ordre des documents n'est pas important

### ⚠️ Ne PAS utiliser la HashTable quand :

- Besoin d'affichage trié
- Recherches principalement par titre
- Ordre d'insertion important
- Petite collection (< 50 documents)

## 🔧 Utilisation avancée

### Approche directe avec les classes

```python
from partie_3 import HashTable, SearchByAuthorHash
from partie_1 import Document

# Créer une HashTable
ht = HashTable(size=50)

# Ajouter des documents
doc1 = Document("Python Basics", "John Doe", "python,tutorial")
doc2 = Document("Advanced Python", "John Doe", "python,advanced")
ht.insert(doc1)
ht.insert(doc2)

# Utiliser un algorithme de recherche spécifique
search_algo = SearchByAuthorHash()
results = search_algo.search(ht, "John Doe")
print(f"Trouvé {len(results)} document(s)")
```

### Chargement depuis un BST

```python
from partie_2 import BinarySearchTree
from partie_3 import HashTableManager

# Créer un BST avec des données
bst = BinarySearchTree()
# ... ajouter des documents ...

# Charger dans la HashTable
manager = HashTableManager(size=100)
nb_docs = manager.charger_depuis_bst(bst)
print(f"{nb_docs} documents chargés")
```

### Analyse de distribution

```python
from partie_3 import analyser_distribution_hash

# Analyser la qualité de la fonction de hachage
stats = analyser_distribution_hash(manager.hash_table)
```

## 📝 Complexités algorithmiques

| Opération                   | Meilleur cas | Cas moyen | Pire cas |
| --------------------------- | ------------ | --------- | -------- |
| **Recherche par auteur**    | O(1)         | O(1)      | O(n) \*  |
| **Insertion**               | O(1)         | O(1)      | O(1)     |
| **Recherche par titre**     | O(n)         | O(n)      | O(n)     |
| **Recherche par mots-clés** | O(n)         | O(n)      | O(n)     |

\* Le pire cas O(n) arrive si tous les documents sont dans le même bucket (très rare avec une bonne fonction de hachage).

## 🤝 Compatibilité

Le code existant continue de fonctionner grâce au module de compatibilité :

```python
# Ancienne API fonctionnelle
from partie_3 import HashTable, rechercher_par_auteur_hash

ht = HashTable(size=50)
# ... ajouter des documents ...
docs = rechercher_par_auteur_hash(ht, "Orwell")
```

## 🛠️ Lancement du programme

### Interface graphique

```bash
python main.py
```

Sélectionnez l'onglet **"Partie 3 (Hash)"** pour utiliser la table de hachage.

### Mode terminal

```bash
python mode_terminal.py
```

Choisissez l'option pour la Partie 3.

---

## 📋 Résumé

La Partie 3 propose un système ultra-optimisé avec :

- ✅ Recherche instantanée par auteur (O(1))
- ✅ Gestion automatique des collisions
- ✅ Performance maximale pour la clé d'indexation
- ✅ Architecture POO moderne
- ✅ Compatible avec les Parties 1 et 2

**🎯 Idéal quand les recherches par auteur sont prioritaires !**

---

**Version** : 2.0.0  
**Date** : Octobre 2025
