"""
Tests unitaires pour les algorithmes de tri
Vérifie la validité et la cohérence de chaque algorithme
"""

from partie_1.document import Document
from partie_1.compat import (
    trier_par_titre, tri_selection, tri_bulles, 
    tri_rapide, tri_fusion, tri_tas, tri_comptage
)
import time


class TestsTriAlgorithmes:
    """Classe de tests pour tous les algorithmes de tri"""
    
    def __init__(self):
        self.resultats = {}
        
    def creer_liste_test_1(self):
        """Liste désordonnée simple - 5 éléments"""
        return [
            Document("Zazie dans le Métro", "Raymond Queneau", "roman"),
            Document("1984", "George Orwell", "dystopie"),
            Document("Dune", "Frank Herbert", "science-fiction"),
            Document("Alice au pays des merveilles", "Lewis Carroll", "conte"),
            Document("Le Petit Prince", "Antoine de Saint-Exupéry", "conte")
        ]
    
    def creer_liste_test_2(self):
        """Liste inversée - 10 éléments"""
        return [
            Document("Zazie dans le Métro", "Raymond Queneau", "roman"),
            Document("Voyage au centre de la Terre", "Jules Verne", "aventure"),
            Document("Ubik", "Philip K. Dick", "science-fiction"),
            Document("Le Seigneur des Anneaux", "J.R.R. Tolkien", "fantasy"),
            Document("Le Petit Prince", "Antoine de Saint-Exupéry", "conte"),
            Document("Harry Potter", "J.K. Rowling", "fantasy"),
            Document("Fondation", "Isaac Asimov", "science-fiction"),
            Document("Dune", "Frank Herbert", "science-fiction"),
            Document("Brave New World", "Aldous Huxley", "dystopie"),
            Document("1984", "George Orwell", "dystopie")
        ]
    
    def creer_liste_test_3(self):
        """Liste déjà triée - 7 éléments"""
        return [
            Document("1984", "George Orwell", "dystopie"),
            Document("Brave New World", "Aldous Huxley", "dystopie"),
            Document("Dune", "Frank Herbert", "science-fiction"),
            Document("Fondation", "Isaac Asimov", "science-fiction"),
            Document("Harry Potter", "J.K. Rowling", "fantasy"),
            Document("Le Petit Prince", "Antoine de Saint-Exupéry", "conte"),
            Document("Zazie dans le Métro", "Raymond Queneau", "roman")
        ]
    
    def creer_liste_test_4(self):
        """Liste avec doublons - 8 éléments"""
        return [
            Document("Dune", "Frank Herbert", "science-fiction"),
            Document("1984", "George Orwell", "dystopie"),
            Document("Dune", "Frank Herbert", "science-fiction"),
            Document("Alice", "Lewis Carroll", "conte"),
            Document("1984", "George Orwell", "dystopie"),
            Document("Le Petit Prince", "Antoine de Saint-Exupéry", "conte"),
            Document("Alice", "Lewis Carroll", "conte"),
            Document("Zazie", "Raymond Queneau", "roman")
        ]
    
    def creer_liste_test_5(self):
        """Liste avec un seul élément"""
        return [Document("Unique", "Auteur Unique", "test")]
    
    def creer_liste_test_6(self):
        """Liste vide"""
        return []
    
    def verifier_ordre_croissant(self, liste):
        """Vérifie que la liste est triée par ordre alphabétique des titres"""
        for i in range(len(liste) - 1):
            if liste[i].titre.lower() > liste[i + 1].titre.lower():
                return False
        return True
    
    def tester_algorithme(self, nom_algo, fonction_tri, liste_originale):
        """
        Teste un algorithme de tri sur une liste
        
        Retourne:
            dict: {
                'nom': str,
                'valide': bool,
                'temps': float,
                'taille': int,
                'erreur': str ou None
            }
        """
        liste_test = liste_originale.copy()
        taille = len(liste_test)
        
        try:
            start = time.perf_counter()
            
            if nom_algo in ["Tri Rapide", "Tri Fusion"]:
                resultat = fonction_tri(liste_test)
            else:
                fonction_tri(liste_test)
                resultat = liste_test
            
            end = time.perf_counter()
            temps_execution = end - start
            
            est_valide = self.verifier_ordre_croissant(resultat)
            
            if len(resultat) != taille:
                est_valide = False
                erreur = f"Taille modifiée: {taille} → {len(resultat)}"
            else:
                erreur = None
            
            return {
                'nom': nom_algo,
                'valide': est_valide,
                'temps': temps_execution,
                'taille': taille,
                'erreur': erreur if not est_valide else None
            }
            
        except Exception as e:
            return {
                'nom': nom_algo,
                'valide': False,
                'temps': 0.0,
                'taille': taille,
                'erreur': str(e)
            }
    
    def executer_tous_les_tests(self):
        """
        Exécute tous les tests sur tous les algorithmes
        
        Retourne:
            dict: {
                'algorithme': {
                    'test_1': {...},
                    'test_2': {...},
                    ...
                }
            }
        """
        algorithmes = {
            "Tri Insertion": trier_par_titre,
            "Tri Sélection": tri_selection,
            "Tri à Bulles": tri_bulles,
            "Tri Rapide": tri_rapide,
            "Tri Fusion": tri_fusion,
            "Tri Tas": tri_tas,
            "Tri Comptage": tri_comptage
        }
        
        listes_test = {
            "Test 1 - Liste désordonnée (5 éléments)": self.creer_liste_test_1(),
            "Test 2 - Liste inversée (10 éléments)": self.creer_liste_test_2(),
            "Test 3 - Liste déjà triée (7 éléments)": self.creer_liste_test_3(),
            "Test 4 - Liste avec doublons (8 éléments)": self.creer_liste_test_4(),
            "Test 5 - Liste à 1 élément": self.creer_liste_test_5(),
            "Test 6 - Liste vide": self.creer_liste_test_6()
        }
        
        resultats = {}
        
        for nom_algo, fonction in algorithmes.items():
            resultats[nom_algo] = {}
            for nom_test, liste in listes_test.items():
                resultat = self.tester_algorithme(nom_algo, fonction, liste)
                resultats[nom_algo][nom_test] = resultat
        
        return resultats
    
    def generer_rapport_texte(self, resultats):
        """Génère un rapport texte des résultats"""
        rapport = []
        rapport.append("="*80)
        rapport.append("RAPPORT DE TESTS DES ALGORITHMES DE TRI")
        rapport.append("="*80)
        rapport.append("")
        
        total_tests = 0
        tests_reussis = 0
        
        for nom_algo, tests in resultats.items():
            rapport.append(f"\n{'='*80}")
            rapport.append(f"🔍 {nom_algo}")
            rapport.append(f"{'='*80}")
            
            for nom_test, resultat in tests.items():
                total_tests += 1
                statut = "✅ RÉUSSI" if resultat['valide'] else "❌ ÉCHEC"
                if resultat['valide']:
                    tests_reussis += 1
                
                rapport.append(f"\n{nom_test}:")
                rapport.append(f"  Statut: {statut}")
                rapport.append(f"  Taille: {resultat['taille']} éléments")
                rapport.append(f"  Temps: {resultat['temps']:.6f} secondes")
                
                if resultat['erreur']:
                    rapport.append(f"  ⚠️ Erreur: {resultat['erreur']}")
        
        rapport.append(f"\n{'='*80}")
        rapport.append("📊 RÉSUMÉ GLOBAL")
        rapport.append(f"{'='*80}")
        rapport.append(f"Total de tests: {total_tests}")
        rapport.append(f"Tests réussis: {tests_reussis}")
        rapport.append(f"Tests échoués: {total_tests - tests_reussis}")
        rapport.append(f"Taux de réussite: {(tests_reussis/total_tests*100):.1f}%")
        rapport.append("="*80)
        
        return "\n".join(rapport)


def executer_tests_console():
    """Fonction pour exécuter les tests en console"""
    print("\n🧪 Démarrage des tests unitaires...\n")
    
    tests = TestsTriAlgorithmes()
    resultats = tests.executer_tous_les_tests()
    rapport = tests.generer_rapport_texte(resultats)
    
    print(rapport)
    
    return resultats


if __name__ == "__main__":
    executer_tests_console()

