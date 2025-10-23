# Fichier : interface/ui.py
# Interface graphique (GUI) Tkinter/TTK intégrant P1, P2 et P3.

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import font

# Imports des modules de logique (chemins directs après correction du sys.path)
from partie_1.document import Document
from partie_1.gestionnaire import trier_par_titre
try:
    from partie_2.bst import BinarySearchTree
    from partie_3 import HashTable
except ImportError:
    BinarySearchTree = None 
    HashTable = None
    pass


# --- Fonctions de Démarrage et Initialisation ---

def initialiser_structures_gui():
    """Crée et initialise les TROIS structures (Liste, BST, Hachage) pour la GUI."""
    list_bib = [] 
    bst_bib = BinarySearchTree() if BinarySearchTree else None
    hash_bib = HashTable(size=50) if HashTable else None
    
    docs = [
        Document("Le Petit Prince", "Antoine de Saint-Exupéry", "conte, amitié, philosophie"),
        Document("1984", "George Orwell", "dystopie, politique, surveillance"),
        Document("Zazie dans le Métro", "Raymond Queneau", "roman, humour, argot")
    ]
    
    list_bib.extend(docs)
    for doc in docs:
        if bst_bib:
            bst_bib.insert(doc)
        if hash_bib:
            hash_bib.insert(doc)
            
    return list_bib, bst_bib, hash_bib # Retourne le tuple (Liste P1, BST P2, Hash P3)

def lancer_interface_graphique(structures):
    """Point d'entrée pour lancer la fenêtre Tkinter."""
    list_bib, bst_bib, hash_bib = structures
    root = tk.Tk()
    app = BibliothequeGUI(root, list_bib, bst_bib, hash_bib)
    root.mainloop()


# --- Classe de l'Interface Graphique ---

class BibliothequeGUI:
    def __init__(self, master, list_bib, bst_bib, hash_bib):
        self.master = master
        self.list_bib = list_bib
        self.bst_bib = bst_bib
        self.hash_bib = hash_bib
        
        self.master.title("Gestion de Bibliothèque Numérique Avancée (P1, P2, P3)")
        self.master.geometry("750x650")
        self.master.resizable(True, True)
        
        # 1. Configuration du Thème et des Styles
        style = ttk.Style()
        style.theme_use('clam')
        self.PRIMARY_COLOR = "#007ACC"
        self.ACCENT_COLOR = "#308B4B"
        self.BACKGROUND_COLOR = "#F0F0F0" 
        style.configure('TFrame', background=self.BACKGROUND_COLOR)
        style.configure('TLabel', background=self.BACKGROUND_COLOR, font=('Segoe UI', 10))
        style.configure('TNotebook', background=self.BACKGROUND_COLOR, borderwidth=0)
        style.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'), padding=[10, 5])
        style.configure('Primary.TButton', background=self.PRIMARY_COLOR, foreground='white', font=('Segoe UI', 10, 'bold'), padding=8)
        style.map('Primary.TButton', background=[('active', '#005FA8')])

        # 2. Le Notebook (système d'onglets)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")
        
        self.frame_global = ttk.Frame(self.notebook, padding="20 15 20 15")
        self.frame_p1 = ttk.Frame(self.notebook, padding="20 15 20 15")
        self.frame_p2 = ttk.Frame(self.notebook, padding="20 15 20 15")
        self.frame_p3 = ttk.Frame(self.notebook, padding="20 15 20 15") # Nouveau cadre
        self.frame_affichage = ttk.Frame(self.notebook, padding="20 15 20 15")

        self.notebook.add(self.frame_global, text="Ajout Global")
        self.notebook.add(self.frame_p1, text="Partie 1 (Liste)")
        self.notebook.add(self.frame_p2, text="Partie 2 (BST)")
        self.notebook.add(self.frame_p3, text="Partie 3 (Hachage)") # Nouvel onglet
        self.notebook.add(self.frame_affichage, text="Affichage Structures")
        
        # 3. Initialiser les sous-interfaces
        self.setup_global_tab()
        self.setup_p1_tab()
        self.setup_p2_tab()
        self.setup_p3_tab() # Nouvel appel
        self.setup_affichage_tab()

        self.notebook.bind("<<NotebookTabChanged>>", self.update_affichage)
        self.update_affichage() 

    # --------------------------- 1. Onglet Ajout Global -------------------------
    
    def setup_global_tab(self):
        frame = self.frame_global
        
        self.titre_var = tk.StringVar()
        self.auteur_var = tk.StringVar()
        
        ttk.Label(frame, text="AJOUTER DOCUMENT (Synchronisation Liste, BST, Hachage)", font=('Segoe UI', 14, 'bold')).pack(pady=(10, 5))
        ttk.Label(frame, text="Ajoute un document à toutes les structures pour maintenir la cohérence.", foreground="#666").pack(pady=(0, 20))
        
        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Titre du Document:", font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, sticky='w', padx=10, pady=10)
        ttk.Entry(input_frame, textvariable=self.titre_var, width=50).grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(input_frame, text="Auteur Principal:", font=('Segoe UI', 11, 'bold')).grid(row=1, column=0, sticky='w', padx=10, pady=10)
        ttk.Entry(input_frame, textvariable=self.auteur_var, width=50).grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(frame, text="Ajouter et Synchroniser", command=self.ajouter_global, style='Primary.TButton').pack(pady=30)

    def ajouter_global(self):
        titre = self.titre_var.get().strip()
        auteur = self.auteur_var.get().strip()
        
        if titre and auteur:
            nouveau_doc = Document(titre, auteur, "GUI")
            
            self.list_bib.append(nouveau_doc)
            
            if self.bst_bib:
                 self.bst_bib.insert(nouveau_doc)
            if self.hash_bib:
                 self.hash_bib.insert(nouveau_doc) # AJOUT HACHAGE
            
            messagebox.showinfo("Succès", f"'{titre}' ajouté aux structures.")
            self.titre_var.set("")
            self.auteur_var.set("")
            self.update_affichage()
        else:
            messagebox.showerror("Erreur", "Titre et Auteur sont requis.")


    # --------------------------- 2. Onglet Partie 1 (Liste) -------------------------
    
    def setup_p1_tab(self):
        frame = self.frame_p1
        self.recherche_list_var = tk.StringVar()
        self.recherche_terme_var = tk.StringVar()
        
        ttk.Label(frame, text="Opérations LISTE PYTHON (Partie 1)", font=('Segoe UI', 14, 'bold')).pack(pady=10)
        ttk.Label(frame, text="Performance: O(n) ou O(n²).", foreground="#CC0000").pack(pady=(0, 20))


        # 1. Tri (Tri Insertion)
        ttk.Button(frame, text="Trier Liste (Tri Insertion O(n²))", command=self.trier_list).pack(pady=5)
        ttk.Label(frame, text="Explication: Nécessite de comparer et de déplacer les éléments, très lent avec l'augmentation du nombre de documents.", foreground="gray").pack(pady=(0, 15))


        # 2. Recherche Séquentielle Classique (Titre exact)
        search_frame = ttk.LabelFrame(frame, text="Recherche Séquentielle par Titre Exact (O(n))", padding="15 10")
        search_frame.pack(pady=15, fill="x")
        
        ttk.Entry(search_frame, textvariable=self.recherche_list_var, width=40).pack(side="left", padx=10)
        ttk.Button(search_frame, text="Rechercher Titre", command=self.rechercher_list).pack(side="left")
        ttk.Label(search_frame, text="Parcourt tous les documents un par un. Performance: O(n).", foreground="gray").pack(pady=5)


        # 3. Recherche Avancée (Terme)
        terme_frame = ttk.LabelFrame(frame, text="Recherche Avancée (Titre/Auteur/Mots-clés) (O(n))", padding="15 10")
        terme_frame.pack(pady=15, fill="x")
        
        ttk.Entry(terme_frame, textvariable=self.recherche_terme_var, width=40).pack(side="left", padx=10)
        ttk.Button(terme_frame, text="Rechercher Terme", command=self.rechercher_terme_list).pack(side="left")
        ttk.Label(terme_frame, text="Recherche flexible, mais toujours lente (séquentielle).", foreground="gray").pack(pady=5)


    def trier_list(self):
        trier_par_titre(self.list_bib) 
        messagebox.showinfo("Triage", "La liste a été triée par Tri par Insertion.")
        self.update_affichage()

    def rechercher_list(self):
        terme = self.recherche_list_var.get().strip()
        if not terme: return
        
        resultats = [doc for doc in self.list_bib if doc.titre.lower() == terme.lower()]
        self.afficher_resultats_temp(resultats, f"Résultats P1 (Titre Exact) pour '{terme}'")

    def rechercher_terme_list(self):
        terme = self.recherche_terme_var.get().strip()
        if not terme: return
        
        terme_lower = terme.lower()
        resultats = [doc for doc in self.list_bib if terme_lower in doc.titre.lower() or terme_lower in doc.auteur.lower()]
        
        self.afficher_resultats_temp(resultats, f"Résultats P1 (Avancée) pour '{terme}'")


    # --------------------------- 3. Onglet Partie 2 (BST) -------------------------

    def setup_p2_tab(self):
        frame = self.frame_p2
        self.recherche_bst_var = tk.StringVar()
        self.suppression_bst_var = tk.StringVar()

        ttk.Label(frame, text="Optimisation avec l'Arbre Binaire de Recherche (BST)", font=('Segoe UI', 14, 'bold')).pack(pady=10)
        ttk.Label(frame, text="Performance: O(log n) en moyenne.", foreground=self.ACCENT_COLOR).pack(pady=(0, 20))

        if not self.bst_bib:
            ttk.Label(frame, text="Module BST non disponible. Vérifiez les imports.", fg="red").pack(pady=20)
            return

        # 1. Recherche BST
        search_frame = ttk.LabelFrame(frame, text="Recherche par Titre (O(log n))", padding="15 10")
        search_frame.pack(pady=15, fill="x")
        
        ttk.Entry(search_frame, textvariable=self.recherche_bst_var, width=40).pack(side="left", padx=10)
        ttk.Button(search_frame, text="Rechercher", command=self.rechercher_bst, style='Primary.TButton').pack(side="left")
        ttk.Label(search_frame, text="Recherche rapide basée sur la structure arborescente.", foreground="gray").pack(pady=5)


        # 2. Suppression BST
        delete_frame = ttk.LabelFrame(frame, text="Suppression de Document (O(log n))", padding="15 10")
        delete_frame.pack(pady=15, fill="x")
        
        ttk.Entry(delete_frame, textvariable=self.suppression_bst_var, width=40).pack(side="left", padx=10)
        ttk.Button(delete_frame, text="Supprimer par Titre", command=self.supprimer_bst, style='Primary.TButton').pack(side="left")
        ttk.Label(delete_frame, text="Maintient l'intégrité du BST après la suppression (O(log n)).", foreground="gray").pack(pady=5)

    def rechercher_bst(self):
        terme = self.recherche_bst_var.get().strip()
        if not terme: return
        
        resultat = self.bst_bib.search(terme)
        
        self.afficher_resultats_temp([resultat] if resultat else [], 
                                    f"Résultat P2 (BST O(log n)) pour '{terme}'")

    def supprimer_bst(self):
        titre = self.suppression_bst_var.get().strip()
        if not titre: return
        
        if self.bst_bib.delete(titre):
            messagebox.showinfo("Succès", f"Document '{titre}' supprimé du BST.")
            self.update_affichage()
        else:
            messagebox.showerror("Erreur", f"Document '{titre}' non trouvé dans le BST.")
        self.suppression_bst_var.set("")


    # --------------------------- 4. Onglet Partie 3 (Hachage) -------------------------

    def setup_p3_tab(self):
        frame = self.frame_p3
        self.recherche_hash_var = tk.StringVar()
        
        ttk.Label(frame, text="Partie 3 : Indexation par Table de Hachage", font=('Segoe UI', 14, 'bold')).pack(pady=10)
        ttk.Label(frame, text="Performance Optimale : Recherche instantanée (O(1) en moyenne).", foreground=self.ACCENT_COLOR).pack(pady=(0, 20))

        if not self.hash_bib:
            ttk.Label(frame, text="Module Hachage non disponible. Vérifiez les imports.", fg="red").pack(pady=20)
            return

        # Recherche Hachage
        hash_frame = ttk.LabelFrame(frame, text="Recherche par Auteur (O(1))", padding="15 10")
        hash_frame.pack(pady=15, fill="x")
        
        ttk.Entry(hash_frame, textvariable=self.recherche_hash_var, width=40).pack(side="left", padx=10)
        ttk.Button(hash_frame, text="Rechercher Auteur", command=self.rechercher_hash, style='Primary.TButton').pack(side="left")
        ttk.Label(hash_frame, text="Trouve tous les documents d'un auteur en calculant directement l'index.", foreground="gray").pack(pady=5)

    def rechercher_hash(self):
        auteur = self.recherche_hash_var.get().strip()
        if not auteur: return
        
        resultats = self.hash_bib.search_by_author(auteur)
        
        self.afficher_resultats_temp(resultats, f"Résultats P3 (Hachage O(1)) pour l'auteur '{auteur}'")


    # --------------------------- 5. Onglet Affichage Global -------------------------

    def setup_affichage_tab(self):
        frame = self.frame_affichage
        
        ttk.Label(frame, text="Comparaison Visuelle des Structures", font=('Segoe UI', 14, 'bold')).pack(pady=10)
        
        # Zone pour la liste
        list_frame = ttk.LabelFrame(frame, text="LISTE Python (P1) - Ordre actuel", padding="10 10")
        list_frame.pack(pady=10, fill="x", expand=True)
        self.text_list = tk.Text(list_frame, height=9, wrap='word', bd=1, relief=tk.SUNKEN)
        self.text_list.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Zone pour le BST
        bst_frame = ttk.LabelFrame(frame, text="BST (P2) - Ordre In-order (Automatiquement Trié)", padding="10 10")
        bst_frame.pack(pady=10, fill="x", expand=True)
        self.text_bst = tk.Text(bst_frame, height=9, wrap='word', bd=1, relief=tk.SUNKEN)
        self.text_bst.pack(padx=5, pady=5, fill="both", expand=True)
        
    def update_affichage(self, event=None):
        """Met à jour les zones d'affichage de la LISTE et du BST."""
        
        self.text_list.delete('1.0', tk.END)
        if self.list_bib:
            for i, doc in enumerate(self.list_bib):
                self.text_list.insert(tk.END, f"[{i+1}] {doc}\n")
        else:
            self.text_list.insert(tk.END, "La liste est vide.")

        self.text_bst.delete('1.0', tk.END)
        if self.bst_bib:
            documents_tries = self.bst_bib.in_order_traversal()
            if documents_tries:
                for i, doc in enumerate(documents_tries):
                    self.text_bst.insert(tk.END, f"[{i+1}] {doc}\n")
            else:
                 self.text_bst.insert(tk.END, "Le BST est vide.")
        else:
            self.text_bst.insert(tk.END, "Le module BST est non fonctionnel.")


    # --------------------------- Utilitaires -------------------------

    def afficher_resultats_temp(self, documents, titre):
        """Affiche les résultats d'une recherche dans une nouvelle fenêtre modale."""
        
        fenetre_resultat = tk.Toplevel(self.master)
        fenetre_resultat.title(titre)
        fenetre_resultat.transient(self.master)
        fenetre_resultat.grab_set()
        fenetre_resultat.geometry("500x350")
        
        ttk.Label(fenetre_resultat, text=titre, font=('Segoe UI', 11, 'bold')).pack(pady=10)
        
        texte_affichage = tk.Text(fenetre_resultat, height=10, width=60)
        texte_affichage.pack(padx=10, pady=10, fill='both', expand=True)
        
        if not documents or documents == [None] or documents == []:
            texte_affichage.insert(tk.END, "Aucun document trouvé.")
        else:
            for doc in documents:
                texte_affichage.insert(tk.END, f"• {doc}\n")
        
        ttk.Button(fenetre_resultat, text="Fermer", command=fenetre_resultat.destroy).pack(pady=10)
        self.master.wait_window(fenetre_resultat)