"""
Mode Terminal - Gestion de Bibliothèque Numérique
Interface en ligne de commande pour gérer la collection de documents
"""

import sys
import os
import time

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    VERT = Fore.GREEN
    ROUGE = Fore.RED
    BLEU = Fore.CYAN
    JAUNE = Fore.YELLOW
    MAGENTA = Fore.MAGENTA
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL
except ImportError:
    VERT = ROUGE = BLEU = JAUNE = MAGENTA = BOLD = RESET = ""

sys.path.append(os.path.dirname(__file__))

from partie_1 import Document, BibliothequeManager, Bibliotheque
from partie_1.persistance import save_all_structures, load_all_structures, create_default_data
from partie_2 import BinarySearchTree, BSTManager
from partie_3 import HashTable, HashTableManager


class MenuTerminal:
    """Classe principale pour l'interface terminal"""
    
    def __init__(self):
        """Initialise le menu terminal avec les structures de données"""
        self.liste_documents = []
        self.bst = BinarySearchTree()
        self.hash_table = HashTable(size=50)
        
        self.manager_liste = BibliothequeManager(Bibliotheque())
        self.manager_bst = BSTManager()
        self.manager_hash = HashTableManager()
        
        self.charger_donnees()
    
    def charger_donnees(self):
        """Charge les données depuis les fichiers JSON"""
        print(f"{BLEU}Chargement des données...{RESET}")
        
        self.liste_documents = load_all_structures(Document, self.bst, self.hash_table)
        
        if not self.liste_documents:
            print(f"{JAUNE}Aucune donnée trouvée. Création de données par défaut...{RESET}")
            self.liste_documents = create_default_data(Document)
            
            for doc in self.liste_documents:
                self.bst.insert(doc)
                self.hash_table.insert(doc)
            
            self.sauvegarder_donnees()
        
        for doc in self.liste_documents:
            self.manager_liste.bibliotheque.add_document(doc)
        
        print(f"{VERT}✓ {len(self.liste_documents)} documents chargés{RESET}\n")
    
    def sauvegarder_donnees(self):
        """Sauvegarde les données dans les fichiers JSON"""
        try:
            save_all_structures(self.liste_documents)
            return True
        except Exception as e:
            print(f"{ROUGE}Erreur lors de la sauvegarde: {e}{RESET}")
            return False
    
    def afficher_banniere(self):
        """Affiche la bannière d'accueil"""
        print("\n" + "=" * 70)
        print(f"{BOLD}{BLEU}{'GESTION DE BIBLIOTHÈQUE NUMÉRIQUE':^70}{RESET}")
        print("=" * 70)
        print(f"{JAUNE}Mode Terminal - Interface en ligne de commande{RESET:^70}")
        print("=" * 70 + "\n")
    
    def afficher_menu_principal(self):
        """Affiche le menu principal"""
        print(f"\n{BOLD}{BLEU}╔═══════════════════════ MENU PRINCIPAL ═══════════════════════╗{RESET}")
        print(f"{BOLD}{BLEU}║{RESET}                                                               {BOLD}{BLEU}║{RESET}")
        print(f"{BOLD}{BLEU}║{RESET}  {VERT}1.{RESET} 📚 Afficher tous les documents                        {BOLD}{BLEU}║{RESET}")
        print(f"{BOLD}{BLEU}║{RESET}  {VERT}2.{RESET} ➕ Ajouter un document                                {BOLD}{BLEU}║{RESET}")
        print(f"{BOLD}{BLEU}║{RESET}  {VERT}3.{RESET} 🔍 Rechercher un document                             {BOLD}{BLEU}║{RESET}")
        print(f"{BOLD}{BLEU}║{RESET}  {VERT}4.{RESET} 🔄 Trier la liste                                     {BOLD}{BLEU}║{RESET}")
        print(f"{BOLD}{BLEU}║{RESET}  {VERT}5.{RESET} 🗑️  Supprimer un document                             {BOLD}{BLEU}║{RESET}")
        print(f"{BOLD}{BLEU}║{RESET}  {VERT}6.{RESET} 📊 Comparaison des performances                       {BOLD}{BLEU}║{RESET}")
        print(f"{BOLD}{BLEU}║{RESET}  {VERT}7.{RESET} 🧪 Tests des algorithmes de tri                       {BOLD}{BLEU}║{RESET}")
        print(f"{BOLD}{BLEU}║{RESET}  {VERT}8.{RESET} 📈 Statistiques                                       {BOLD}{BLEU}║{RESET}")
        print(f"{BOLD}{BLEU}║{RESET}  {ROUGE}0.{RESET} 🚪 Quitter                                            {BOLD}{BLEU}║{RESET}")
        print(f"{BOLD}{BLEU}║{RESET}                                                               {BOLD}{BLEU}║{RESET}")
        print(f"{BOLD}{BLEU}╚═══════════════════════════════════════════════════════════════╝{RESET}\n")
    
    def afficher_documents(self):
        """Affiche tous les documents de la liste"""
        if not self.liste_documents:
            print(f"{JAUNE}Aucun document dans la bibliothèque.{RESET}")
            return
        
        print(f"\n{BOLD}{BLEU}{'='*70}{RESET}")
        print(f"{BOLD}{BLEU}LISTE DES DOCUMENTS ({len(self.liste_documents)} documents){RESET}")
        print(f"{BOLD}{BLEU}{'='*70}{RESET}\n")
        
        for i, doc in enumerate(self.liste_documents, 1):
            print(f"{VERT}{i:3d}.{RESET} {BOLD}{doc.titre}{RESET}")
            print(f"     Auteur: {doc.auteur}")
            print(f"     Mots-clés: {', '.join(doc.mots_cles) if doc.mots_cles else 'Aucun'}")
            print()
    
    def ajouter_document(self):
        """Ajoute un nouveau document"""
        print(f"\n{BOLD}{BLEU}{'AJOUT D\'UN NOUVEAU DOCUMENT':^70}{RESET}")
        print("=" * 70 + "\n")
        
        titre = input(f"{VERT}Titre:{RESET} ").strip()
        if not titre:
            print(f"{ROUGE}Le titre ne peut pas être vide.{RESET}")
            return
        
        auteur = input(f"{VERT}Auteur:{RESET} ").strip()
        if not auteur:
            print(f"{ROUGE}L'auteur ne peut pas être vide.{RESET}")
        return

        mots_cles = input(f"{VERT}Mots-clés (séparés par des virgules):{RESET} ").strip()
        
        nouveau_doc = Document(titre, auteur, mots_cles)
        self.liste_documents.append(nouveau_doc)
        self.bst.insert(nouveau_doc)
        self.hash_table.insert(nouveau_doc)
        self.manager_liste.bibliotheque.add_document(nouveau_doc)
        
        if self.sauvegarder_donnees():
            print(f"\n{VERT}✓ Document '{titre}' ajouté avec succès !{RESET}")
        else:
            print(f"\n{JAUNE}Document ajouté mais erreur lors de la sauvegarde.{RESET}")
    
    def rechercher_document(self):
        """Menu de recherche de documents"""
        print(f"\n{BOLD}{BLEU}{'RECHERCHE DE DOCUMENTS':^70}{RESET}")
        print("=" * 70)
        print(f"{VERT}1.{RESET} Recherche par titre (Liste - O(n))")
        print(f"{VERT}2.{RESET} Recherche par titre (BST - O(log n))")
        print(f"{VERT}3.{RESET} Recherche par auteur (Hash - O(1))")
        print(f"{VERT}4.{RESET} Recherche avancée (tous champs)")
        print(f"{ROUGE}0.{RESET} Retour")
        print("=" * 70)
        
        choix = input(f"\n{BLEU}Votre choix:{RESET} ").strip()
        
        if choix == "1":
            self._recherche_titre_liste()
        elif choix == "2":
            self._recherche_titre_bst()
        elif choix == "3":
            self._recherche_auteur_hash()
        elif choix == "4":
            self._recherche_avancee()
    
    def _recherche_titre_liste(self):
        """Recherche par titre dans la liste"""
        terme = input(f"\n{VERT}Titre à rechercher:{RESET} ").strip()
        
        start = time.perf_counter()
        resultats = [doc for doc in self.liste_documents if terme.lower() in doc.titre.lower()]
        end = time.perf_counter()
        
        self._afficher_resultats_recherche(resultats, f"Recherche Liste (O(n)) - {(end-start)*1000:.3f} ms")
    
    def _recherche_titre_bst(self):
        """Recherche par titre dans le BST"""
        terme = input(f"\n{VERT}Titre exact à rechercher:{RESET} ").strip()
        
        start = time.perf_counter()
        resultat = self.bst.search(terme)
        end = time.perf_counter()
        
        resultats = [resultat] if resultat else []
        self._afficher_resultats_recherche(resultats, f"Recherche BST (O(log n)) - {(end-start)*1000:.3f} ms")
    
    def _recherche_auteur_hash(self):
        """Recherche par auteur dans la hash table"""
        auteur = input(f"\n{VERT}Auteur à rechercher:{RESET} ").strip()
        
        start = time.perf_counter()
        resultats = self.hash_table.search_by_author(auteur)
        end = time.perf_counter()
        
        self._afficher_resultats_recherche(resultats, f"Recherche Hash (O(1)) - {(end-start)*1000:.3f} ms")
    
    def _recherche_avancee(self):
        """Recherche avancée dans tous les champs"""
        terme = input(f"\n{VERT}Terme à rechercher:{RESET} ").strip()
        
        start = time.perf_counter()
        resultats = self.manager_liste.rechercher_avancee(terme)
        end = time.perf_counter()
        
        self._afficher_resultats_recherche(resultats, f"Recherche Avancée - {(end-start)*1000:.3f} ms")
    
    def _afficher_resultats_recherche(self, resultats, titre):
        """Affiche les résultats d'une recherche"""
        print(f"\n{BOLD}{BLEU}{'='*70}{RESET}")
        print(f"{BOLD}{BLEU}{titre}{RESET}")
        print(f"{BOLD}{BLEU}{'='*70}{RESET}\n")
        
        if not resultats:
            print(f"{JAUNE}Aucun résultat trouvé.{RESET}")
        else:
            print(f"{VERT}{len(resultats)} résultat(s) trouvé(s):{RESET}\n")
            for i, doc in enumerate(resultats, 1):
                print(f"{VERT}{i}.{RESET} {BOLD}{doc.titre}{RESET} - {doc.auteur}")
                print(f"   Mots-clés: {', '.join(doc.mots_cles) if doc.mots_cles else 'Aucun'}\n")
    
    def trier_liste(self):
        """Menu de tri de la liste"""
        print(f"\n{BOLD}{BLEU}{'ALGORITHMES DE TRI':^70}{RESET}")
        print("=" * 70)
        print(f"{VERT}1.{RESET} Tri par Insertion - O(n²)")
        print(f"{VERT}2.{RESET} Tri par Sélection - O(n²)")
        print(f"{VERT}3.{RESET} Tri à Bulles - O(n²)")
        print(f"{VERT}4.{RESET} Tri Rapide - O(n log n)")
        print(f"{VERT}5.{RESET} Tri Fusion - O(n log n)")
        print(f"{VERT}6.{RESET} Tri Tas - O(n log n)")
        print(f"{ROUGE}0.{RESET} Retour")
        print("=" * 70)
        
        choix = input(f"\n{BLEU}Votre choix:{RESET} ").strip()
        
        if choix == "0":
            return

        algorithmes = {
            "1": ("Tri par Insertion", "insertion"),
            "2": ("Tri par Sélection", "selection"),
            "3": ("Tri à Bulles", "bulles"),
            "4": ("Tri Rapide", "rapide"),
            "5": ("Tri Fusion", "fusion"),
            "6": ("Tri Tas", "tas")
        }
        
        if choix in algorithmes:
            nom, algo = algorithmes[choix]
            self._executer_tri(nom, algo)
    
    def _executer_tri(self, nom, algo):
        """Exécute un algorithme de tri"""
        print(f"\n{JAUNE}Tri en cours avec {nom}...{RESET}")
        
        start = time.perf_counter()
        self.manager_liste.trier(algo)
        end = time.perf_counter()
        
        self.liste_documents = list(self.manager_liste.bibliotheque)
        
        print(f"{VERT}✓ Tri terminé en {(end-start)*1000:.3f} ms{RESET}")
        
        if self.sauvegarder_donnees():
            print(f"{VERT}✓ Liste sauvegardée{RESET}")
    
    def supprimer_document(self):
        """Supprime un document"""
        titre = input(f"\n{VERT}Titre du document à supprimer:{RESET} ").strip()
        
        doc_a_supprimer = None
        for doc in self.liste_documents:
            if doc.titre.lower() == titre.lower():
                doc_a_supprimer = doc
                break
        
        if not doc_a_supprimer:
            print(f"{ROUGE}Document non trouvé.{RESET}")
            return
        
        self.liste_documents.remove(doc_a_supprimer)
        self.bst.delete(doc_a_supprimer.titre)
        self.manager_liste.bibliotheque.remove_document(doc_a_supprimer.titre)
        
        if self.sauvegarder_donnees():
            print(f"{VERT}✓ Document '{titre}' supprimé avec succès !{RESET}")
    
    def comparer_performances(self):
        """Compare les performances des différentes structures"""
        print(f"\n{BOLD}{BLEU}{'COMPARAISON DES PERFORMANCES':^70}{RESET}")
        print("=" * 70 + "\n")
        
        if len(self.liste_documents) < 10:
            print(f"{JAUNE}Pas assez de documents pour une comparaison significative.{RESET}")
            return
        
        import random
        titres_test = random.sample([doc.titre for doc in self.liste_documents], 
                                    min(20, len(self.liste_documents)))
        
        temps_liste = 0
        temps_bst = 0
        temps_hash = 0
        
        for titre in titres_test:
            start = time.perf_counter()
            [doc for doc in self.liste_documents if doc.titre == titre]
            temps_liste += time.perf_counter() - start
            
            start = time.perf_counter()
            self.bst.search(titre)
            temps_bst += time.perf_counter() - start
        
        for doc in random.sample(self.liste_documents, min(20, len(self.liste_documents))):
            start = time.perf_counter()
            self.hash_table.search_by_author(doc.auteur)
            temps_hash += time.perf_counter() - start
        
        print(f"{VERT}Recherche dans Liste (O(n)):{RESET}      {temps_liste*1000:.3f} ms")
        print(f"{VERT}Recherche dans BST (O(log n)):{RESET}    {temps_bst*1000:.3f} ms")
        print(f"{VERT}Recherche dans Hash (O(1)):{RESET}       {temps_hash*1000:.3f} ms")
        
        if temps_liste > 0 and temps_bst > 0:
            gain = temps_liste / temps_bst
            print(f"\n{BLEU}→ BST est {gain:.1f}x plus rapide que la Liste{RESET}")
        
        if temps_liste > 0 and temps_hash > 0:
            gain = temps_liste / temps_hash
            print(f"{BLEU}→ Hash est {gain:.1f}x plus rapide que la Liste{RESET}")
    
    def tester_algorithmes_tri(self):
        """Teste tous les algorithmes de tri"""
        from tests_tri import TestsTriAlgorithmes
        
        print(f"\n{BOLD}{BLEU}{'TESTS UNITAIRES DES ALGORITHMES DE TRI':^70}{RESET}")
        print("=" * 70 + "\n")
        
        tests = TestsTriAlgorithmes()
        resultats = tests.executer_tous_les_tests()
        
        total_tests = sum(len(tests_algo) for tests_algo in resultats.values())
        tests_reussis = sum(1 for tests_algo in resultats.values() 
                          for test in tests_algo.values() if test['valide'])
        
        print(f"\n{BOLD}{VERT}Résultat: {tests_reussis}/{total_tests} tests réussis ({tests_reussis/total_tests*100:.1f}%){RESET}")
        
        if tests_reussis == total_tests:
            print(f"{VERT}✓ Tous les algorithmes fonctionnent correctement !{RESET}")
        else:
            print(f"{ROUGE}⚠ Certains tests ont échoué.{RESET}")
    
    def afficher_statistiques(self):
        """Affiche les statistiques de la bibliothèque"""
        print(f"\n{BOLD}{BLEU}{'STATISTIQUES':^70}{RESET}")
        print("=" * 70 + "\n")
        
        print(f"{VERT}Nombre total de documents:{RESET} {len(self.liste_documents)}")
        print(f"{VERT}Nombre d'auteurs uniques:{RESET} {len(set(doc.auteur for doc in self.liste_documents))}")
        
        tous_mots_cles = []
        for doc in self.liste_documents:
            tous_mots_cles.extend(doc.mots_cles)
        print(f"{VERT}Nombre de mots-clés uniques:{RESET} {len(set(tous_mots_cles))}")
        
        print(f"\n{VERT}Structure BST:{RESET}")
        print(f"  - Taille: {self.bst.size}")
        
        print(f"\n{VERT}Table de Hachage:{RESET}")
        print(f"  - Taille: {self.hash_table.size}")
        print(f"  - Buckets utilisés: {sum(1 for bucket in self.hash_table.table if bucket.items)}")
    
    def executer(self):
        """Boucle principale du menu"""
        self.afficher_banniere()
        
        while True:
            self.afficher_menu_principal()
            choix = input(f"{BLEU}Votre choix: {RESET}").strip()
            
            if choix == "1":
                self.afficher_documents()
            elif choix == "2":
                self.ajouter_document()
            elif choix == "3":
                self.rechercher_document()
            elif choix == "4":
                self.trier_liste()
            elif choix == "5":
                self.supprimer_document()
            elif choix == "6":
                self.comparer_performances()
            elif choix == "7":
                self.tester_algorithmes_tri()
            elif choix == "8":
                self.afficher_statistiques()
            elif choix == "0":
                print(f"\n{VERT}Merci d'avoir utilisé la Bibliothèque Numérique !{RESET}")
                print(f"{BLEU}Au revoir !{RESET}\n")
                break
            else:
                print(f"\n{ROUGE}Choix invalide. Veuillez réessayer.{RESET}")
            
            input(f"\n{JAUNE}Appuyez sur Entrée pour continuer...{RESET}")


def main():
    """Point d'entrée du programme"""
    try:
        menu = MenuTerminal()
        menu.executer()
    except KeyboardInterrupt:
        print(f"\n\n{JAUNE}Programme interrompu par l'utilisateur.{RESET}")
        print(f"{BLEU}Au revoir !{RESET}\n")
    except Exception as e:
        print(f"\n{ROUGE}Erreur: {e}{RESET}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
