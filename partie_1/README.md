# Partie 1 - Gestion de Bibliothèque

## 📚 Description

Un système de gestion de bibliothèque numérique qui permet d'organiser, trier et rechercher des documents.

## ✨ Fonctionnalités

- Ajouter et supprimer des documents (titre, auteur, mots-clés)
- Trier les documents avec 7 algorithmes différents
- Rechercher des documents par titre, auteur ou mots-clés
- Sauvegarder et charger automatiquement les données
- Comparer les performances des algorithmes

## 📁 Structure du projet

```
partie_1/
├── document.py              # Gestion des documents
├── bibliotheque.py          # Collection de documents
├── gestionnaire_poo.py      # Gestionnaire principal
├── tri_algorithms.py        # Algorithmes de tri
├── search_algorithms.py     # Algorithmes de recherche
├── persistance.py           # Sauvegarde des données
└── README.md                # Documentation
```

## 🚀 Utilisation

### Exemple simple

```python
from partie_1 import BibliothequeManager

# Créer un gestionnaire
manager = BibliothequeManager()

# Ajouter des documents
manager.ajouter_document("1989", "George Orwell", "roman,dystopie")
manager.ajouter_document("Le Petit Prince", "Antoine de Saint-Exupéry", "conte,philosophie")

# Trier par titre
manager.trier('fusion')

# Rechercher un document
resultats = manager.rechercher_par_titre("1989")

# Afficher la bibliothèque
print(manager.afficher_bibliotheque())
```

## 📊 Algorithmes de tri disponibles

7 algorithmes de tri sont implémentés :

- **Insertion** - Simple et efficace pour petites listes
- **Sélection** - Nombre minimum d'échanges
- **Bulles** - Simple mais lent
- **Rapide** - Généralement le plus rapide
- **Fusion** - Stable et prévisible
- **Tas** - Bon compromis
- **Comptage** - Très rapide pour données limitées

### Utilisation

```python
manager.trier('fusion')      # Recommandé pour grandes collections
manager.trier('insertion')   # Bon pour petites collections
manager.trier('rapide')      # Le plus rapide en général
```

## 🔍 Recherche de documents

Plusieurs types de recherche sont disponibles :

```python
# Recherche par titre
resultats = manager.rechercher_par_titre("1989")

# Recherche par auteur
resultats = manager.rechercher_par_auteur("George")

# Recherche par mots-clés
resultats = manager.rechercher_par_mots_cles("roman")

# Recherche avancée (tous les champs)
resultats = manager.rechercher_avancee("dystopie")
```

## 💾 Sauvegarde des données

Les données sont automatiquement sauvegardées dans le fichier `bibliotheque_data.json` lors de l'ajout de documents.

```python
manager = BibliothequeManager()
manager.ajouter_document("Titre", "Auteur", "tags")
# ✅ Sauvegarde automatique
```

## 📈 Statistiques

Obtenez des informations sur votre bibliothèque :

```python
stats = manager.get_statistiques()
print(f"Nombre de documents: {stats['nombre_documents']}")
print(f"Nombre d'auteurs: {stats['nombre_auteurs']}")
print(f"Mots-clés uniques: {stats['nombre_mots_cles']}")
```

## 🎯 Fonctionnalités principales

### Gestion des documents

- Ajout et suppression de documents
- Modification des informations
- Affichage de la collection complète

### Tri

- 7 algorithmes différents pour trier par titre
- Comparaison des performances
- Choix adapté selon la taille de la collection

### Recherche

- Par titre (recherche exacte)
- Par auteur (recherche partielle)
- Par mots-clés
- Recherche globale dans tous les champs

### Persistance

- Sauvegarde automatique en JSON
- Chargement au démarrage
- Pas de perte de données

## 🛠️ Lancement du programme

### Interface graphique

```bash
python main.py
```

### Mode terminal

```bash
python mode_terminal.py
```

---

## 📋 Résumé

Ce projet propose un système complet pour gérer une bibliothèque de documents avec :

- ✅ 7 algorithmes de tri
- ✅ Multiples options de recherche
- ✅ Interface simple à utiliser
- ✅ Sauvegarde automatique
- ✅ Architecture orientée objet
