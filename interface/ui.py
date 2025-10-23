
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import font

from partie_1.document import Document
from partie_1.compat import (
    trier_par_titre,
    tri_fusion, tri_rapide, tri_selection, tri_bulles, tri_tas, tri_comptage,
    comparer_tous_algorithmes_tri, comparer_tous_algorithmes_tri_gui
)
from partie_1.persistance import save_all_structures, load_all_structures, create_default_data
from partie_1.suppression_avancee import (
    supprimer_document_complet, 
    supprimer_par_criteres, 
    supprimer_documents_multiples,
    vider_toutes_structures,
    obtenir_statistiques_suppression
)
try:
    from partie_2.bst import BinarySearchTree
    from partie_3 import HashTable
except ImportError:
    BinarySearchTree = None 
    HashTable = None
    pass


def initialiser_structures_gui():
    """Crée et initialise les TROIS structures (Liste, BST, Hachage) pour la GUI avec persistance."""
    list_bib = [] 
    bst_bib = BinarySearchTree() if BinarySearchTree else None
    hash_bib = HashTable(size=50) if HashTable else None
    
    list_bib = load_all_structures(Document, bst_bib, hash_bib)
    
    if not list_bib:
        list_bib = create_default_data(Document)
        
        for doc in list_bib:
            if bst_bib:
                bst_bib.insert(doc)
            if hash_bib:
                hash_bib.insert(doc)
            
    return list_bib, bst_bib, hash_bib

def lancer_interface_graphique(structures):
    """Point d'entrée pour lancer la fenêtre Tkinter."""
    list_bib, bst_bib, hash_bib = structures
    root = tk.Tk()
    app = BibliothequeGUI(root, list_bib, bst_bib, hash_bib)
    root.mainloop()


class BibliothequeGUI:
    def __init__(self, master, list_bib, bst_bib, hash_bib):
        self.master = master
        self.list_bib = list_bib
        self.bst_bib = bst_bib
        self.hash_bib = hash_bib
        
        style = ttk.Style()
        style.theme_use('clam')
        
        self.COLORS = {
            'primary': '#2E86AB',
            'primary_dark': '#1B5E7A',
            'secondary': '#A23B72',
            'accent': '#F18F01',
            'success': '#2ECC71',
            'warning': '#F39C12',
            'danger': '#E74C3C',
            'background': '#F8F9FA',
            'surface': '#FFFFFF',
            'text_primary': '#2C3E50',
            'text_secondary': '#7F8C8D',
            'border': '#E9ECEF',
            'hover': '#E3F2FD'
        }
        
        style.configure('TFrame', background=self.COLORS['background'])
        style.configure('TLabel', background=self.COLORS['background'], 
                       foreground=self.COLORS['text_primary'], 
                       font=('Segoe UI', 10))
        
        style.configure('TNotebook', background=self.COLORS['background'], borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background=self.COLORS['surface'],
                       foreground=self.COLORS['text_primary'],
                       font=('Segoe UI', 11, 'bold'), 
                       padding=[20, 12],
                       borderwidth=1,
                       relief='flat')
        style.map('TNotebook.Tab',
                 background=[('selected', self.COLORS['primary']),
                            ('active', self.COLORS['hover'])],
                 foreground=[('selected', 'white'),
                            ('active', self.COLORS['text_primary'])])
        
        style.configure('Primary.TButton', 
                       background=self.COLORS['primary'], 
                       foreground='white', 
                       font=('Segoe UI', 10, 'bold'), 
                       padding=[16, 10],
                       borderwidth=0,
                       relief='flat')
        style.map('Primary.TButton', 
                 background=[('active', self.COLORS['primary_dark']),
                            ('pressed', self.COLORS['primary_dark'])])
        
        style.configure('Secondary.TButton', 
                       background=self.COLORS['surface'], 
                       foreground=self.COLORS['text_primary'], 
                       font=('Segoe UI', 10), 
                       padding=[12, 8],
                       borderwidth=1,
                       relief='solid')
        style.map('Secondary.TButton', 
                 background=[('active', self.COLORS['hover']),
                            ('pressed', self.COLORS['border'])])
        
        style.configure('Card.TLabelframe', 
                       background=self.COLORS['surface'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.COLORS['border'])
        style.configure('Card.TLabelframe.Label', 
                       background=self.COLORS['surface'],
                       foreground=self.COLORS['primary'],
                       font=('Segoe UI', 11, 'bold'))
        
        style.configure('Modern.TEntry',
                       fieldbackground=self.COLORS['surface'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.COLORS['border'],
                       font=('Segoe UI', 10))
        style.map('Modern.TEntry',
                 bordercolor=[('focus', self.COLORS['primary']),
                             ('active', self.COLORS['primary'])])
        
        style.configure('Modern.TText',
                       background=self.COLORS['surface'],
                       foreground=self.COLORS['text_primary'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.COLORS['border'],
                       font=('Consolas', 9))

        self.master.title("📚 Bibliothèque Numérique Avancée - P1, P2, P3")
        self.master.geometry("900x750")
        self.master.resizable(True, True)
        self.master.configure(bg=self.COLORS['background'])
        self.master.minsize(800, 600)

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(pady=15, padx=15, expand=True, fill="both")
        
        padding = "25 20 25 20"
        self.frame_global = ttk.Frame(self.notebook, padding=padding)
        self.frame_p1 = ttk.Frame(self.notebook, padding="0 0 0 0")
        self.frame_p2 = ttk.Frame(self.notebook, padding="0 0 0 0")
        self.frame_p3 = ttk.Frame(self.notebook, padding=padding)
        self.frame_suppression = ttk.Frame(self.notebook, padding=padding)
        self.frame_affichage = ttk.Frame(self.notebook, padding=padding)

        self.notebook.add(self.frame_global, text="➕ Ajout Global")
        self.notebook.add(self.frame_p1, text="📋 Partie 1 (Liste)")
        self.notebook.add(self.frame_p2, text="🌳 Partie 2 (BST)")
        self.notebook.add(self.frame_p3, text="🔍 Partie 3 (Hachage)")
        self.notebook.add(self.frame_suppression, text="🗑️ Suppression")
        self.notebook.add(self.frame_affichage, text="📊 Affichage")
        
        self.setup_global_tab()
        self.setup_p1_tab()
        self.setup_p2_tab()
        self.setup_p3_tab()
        self.setup_suppression_tab()
        self.setup_affichage_tab()

        self.notebook.bind("<<NotebookTabChanged>>", self.update_affichage)
        self.update_affichage() 

    
    def setup_global_tab(self):
        frame = self.frame_global
        
        self.titre_var = tk.StringVar()
        self.auteur_var = tk.StringVar()
        self.mots_cles_var = tk.StringVar()
        
        header_frame = ttk.Frame(frame)
        header_frame.pack(fill='x', pady=(0, 25))
        
        title_label = ttk.Label(header_frame, text="➕ Ajout de Document", 
                               font=('Segoe UI', 16, 'bold'),
                               foreground=self.COLORS['primary'])
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(header_frame, text="Synchronise automatiquement avec toutes les structures (Liste, BST, Hachage)", 
                                 font=('Segoe UI', 10),
                                 foreground=self.COLORS['text_secondary'])
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        form_card = ttk.LabelFrame(frame, text="📝 Informations du Document", 
                                  style='Card.TLabelframe', padding="20 15")
        form_card.pack(fill='x', pady=(0, 20))
        
        input_frame = ttk.Frame(form_card)
        input_frame.pack(fill='x')
        
        ttk.Label(input_frame, text="Titre du Document:", 
                 font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, sticky='w', padx=(0, 15), pady=12)
        titre_entry = ttk.Entry(input_frame, textvariable=self.titre_var, 
                               style='Modern.TEntry', width=45)
        titre_entry.grid(row=0, column=1, sticky='ew', padx=(0, 0), pady=12)
        
        ttk.Label(input_frame, text="Auteur Principal:", 
                 font=('Segoe UI', 11, 'bold')).grid(row=1, column=0, sticky='w', padx=(0, 15), pady=12)
        auteur_entry = ttk.Entry(input_frame, textvariable=self.auteur_var, 
                                style='Modern.TEntry', width=45)
        auteur_entry.grid(row=1, column=1, sticky='ew', padx=(0, 0), pady=12)
        
        ttk.Label(input_frame, text="Mots-clés:", 
                 font=('Segoe UI', 11, 'bold')).grid(row=2, column=0, sticky='w', padx=(0, 15), pady=12)
        mots_cles_entry = ttk.Entry(input_frame, textvariable=self.mots_cles_var, 
                                   style='Modern.TEntry', width=45)
        mots_cles_entry.grid(row=2, column=1, sticky='ew', padx=(0, 0), pady=12)
        
        ttk.Label(input_frame, text="(séparés par des virgules)", 
                 font=('Segoe UI', 9),
                 foreground=self.COLORS['text_secondary']).grid(row=3, column=1, sticky='w', padx=(0, 0), pady=(0, 12))
        
        input_frame.columnconfigure(1, weight=1)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        add_button = ttk.Button(button_frame, text="➕ Ajouter et Synchroniser", 
                               command=self.ajouter_global, style='Primary.TButton')
        add_button.pack(side='left')
        
        self.status_label = ttk.Label(button_frame, text="", 
                                     font=('Segoe UI', 9),
                                     foreground=self.COLORS['text_secondary'])
        self.status_label.pack(side='left', padx=(20, 0))

    def ajouter_global(self):
        titre = self.titre_var.get().strip()
        auteur = self.auteur_var.get().strip()
        mots_cles = self.mots_cles_var.get().strip()
        
        if titre and auteur:
            if not mots_cles:
                mots_cles = ""
            
            nouveau_doc = Document(titre, auteur, mots_cles)
            
            self.list_bib.append(nouveau_doc)
            
            if self.bst_bib:
                 self.bst_bib.insert(nouveau_doc)
            if self.hash_bib:
                 self.hash_bib.insert(nouveau_doc)
            
            if save_all_structures(self.list_bib, self.bst_bib, self.hash_bib):
                self.status_label.configure(text=f"✅ '{titre}' ajouté et sauvegardé", 
                                          foreground=self.COLORS['success'])
            else:
                self.status_label.configure(text=f"✅ '{titre}' ajouté (sauvegarde échouée)", 
                                          foreground=self.COLORS['warning'])
            self.titre_var.set("")
            self.auteur_var.set("")
            self.mots_cles_var.set("")
            self.update_affichage()
            
            self.master.after(3000, lambda: self.status_label.configure(text=""))
        else:
            self.status_label.configure(text="❌ Titre et Auteur sont requis", 
                                      foreground=self.COLORS['danger'])


    def setup_p1_tab(self):
        frame = self.frame_p1
        self.recherche_terme_var = tk.StringVar()
        
        canvas = tk.Canvas(frame, bg=self.COLORS['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        content_frame = scrollable_frame
        
        padded_frame = ttk.Frame(content_frame)
        padded_frame.pack(fill='both', expand=True, padx=25, pady=20)
        
        header_frame = ttk.Frame(padded_frame)
        header_frame.pack(fill='x', pady=(0, 25))
        
        title_label = ttk.Label(header_frame, text="📋 Partie 1 - Liste Python", 
                               font=('Segoe UI', 16, 'bold'),
                               foreground=self.COLORS['primary'])
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(header_frame, text="Structure de données de base avec algorithmes O(n) et O(n²)", 
                                 font=('Segoe UI', 10),
                                 foreground=self.COLORS['text_secondary'])
        subtitle_label.pack(anchor='w', pady=(5, 0))

        tri_card = ttk.LabelFrame(padded_frame, text="🔄 Opérations de Tri", 
                                 style='Card.TLabelframe', padding="20 15")
        tri_card.pack(fill='x', pady=(0, 20))
        
        redirect_frame = ttk.Frame(tri_card)
        redirect_frame.pack(fill='x', pady=15)
        
        ttk.Label(redirect_frame, text="📊 Les opérations de tri sont disponibles dans l'onglet 'Affichage'", 
                font=('Segoe UI', 12, 'bold'),
                foreground=self.COLORS['primary']).pack(pady=10)
        
        ttk.Label(redirect_frame, text="• Visualisation en temps réel du tri\n• Affichage du temps d'exécution de chaque algorithme\n• Fonction de mélange aléatoire de la liste\n• 7 algorithmes de tri disponibles", 
                font=('Segoe UI', 10),
                foreground=self.COLORS['text_secondary'],
                justify='left').pack(pady=5)
        
        ttk.Button(redirect_frame, text="➡️ Aller à l'onglet Affichage", 
                  command=lambda: self.notebook.select(5), 
                  style='Primary.TButton').pack(pady=10)


        recherche_card = ttk.LabelFrame(padded_frame, text="🔍 Recherche Complète", 
                                       style='Card.TLabelframe', padding="20 15")
        recherche_card.pack(fill='x', pady=(0, 15))
        
        desc_frame = ttk.Frame(recherche_card)
        desc_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(desc_frame, text="Recherche dans tous les champs (titre, auteur, mots-clés)", 
                font=('Segoe UI', 11, 'bold'),
                foreground=self.COLORS['text_primary']).pack(anchor='w')
        
        ttk.Label(desc_frame, text="Saisissez un terme de recherche qui sera recherché dans le titre, l'auteur et les mots-clés", 
                font=('Segoe UI', 9),
                foreground=self.COLORS['text_secondary']).pack(anchor='w', pady=(5, 0))
        
        recherche_frame = ttk.Frame(recherche_card)
        recherche_frame.pack(fill='x', expand=True)
        
        entry = ttk.Entry(recherche_frame, textvariable=self.recherche_terme_var, 
                         style='Modern.TEntry')
        entry.pack(side="left", fill='x', expand=True, padx=(0, 10))
        ttk.Button(recherche_frame, text="🔍 Rechercher Tout", 
                  command=self.rechercher_complete_list, style='Primary.TButton').pack(side="left")
        
        ttk.Label(recherche_card, text="📊 Performance: O(n) - Recherche séquentielle dans tous les champs", 
                 font=('Segoe UI', 9),
                 foreground=self.COLORS['text_secondary']).pack(pady=(8, 0))


    def trier_list(self):
        trier_par_titre(self.list_bib) 
        messagebox.showinfo("Triage", "La liste a été triée par Tri par Insertion.")
        self.update_affichage()

    def trier_insertion(self):
        trier_par_titre(self.list_bib) 
        messagebox.showinfo("Triage", "La liste a été triée par Tri par Insertion (O(n²)).")
        self.update_affichage()

    def trier_selection(self):
        tri_selection(self.list_bib)
        messagebox.showinfo("Triage", "La liste a été triée par Tri par Sélection (O(n²)).")
        self.update_affichage()

    def trier_bulles(self):
        tri_bulles(self.list_bib)
        messagebox.showinfo("Triage", "La liste a été triée par Tri à Bulles (O(n²)).")
        self.update_affichage()

    def trier_rapide(self):
        resultat = tri_rapide(self.list_bib)
        self.list_bib.clear()
        self.list_bib.extend(resultat)
        messagebox.showinfo("Triage", "La liste a été triée par Tri Rapide (O(n log n)).")
        self.update_affichage()

    def trier_fusion(self):
        resultat = tri_fusion(self.list_bib)
        self.list_bib.clear()
        self.list_bib.extend(resultat)
        messagebox.showinfo("Triage", "La liste a été triée par Tri Fusion (O(n log n)).")
        self.update_affichage()

    def trier_tas(self):
        tri_tas(self.list_bib)
        messagebox.showinfo("Triage", "La liste a été triée par Tri par Tas (O(n log n)).")
        self.update_affichage()

    def trier_comptage(self):
        tri_comptage(self.list_bib)
        messagebox.showinfo("Triage", "La liste a été triée par Tri par Comptage (O(n + k)).")
        self.update_affichage()

    def comparer_algorithmes(self):
        """Lance la comparaison de tous les algorithmes de tri et affiche les résultats dans une fenêtre contextuelle."""
        try:
            resultats = comparer_tous_algorithmes_tri_gui(Document)
            
            self.afficher_comparaison_resultats(resultats)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la comparaison: {str(e)}")

    def afficher_comparaison_resultats(self, resultats):
        """Affiche les résultats de comparaison dans une fenêtre contextuelle."""
        fenetre_resultats = tk.Toplevel(self.master)
        fenetre_resultats.title("📊 Comparaison des Algorithmes de Tri")
        fenetre_resultats.geometry("1000x750")
        fenetre_resultats.configure(bg=self.COLORS['background'])
        fenetre_resultats.resizable(True, True)
        
        fenetre_resultats.transient(self.master)
        fenetre_resultats.grab_set()
        
        header_frame = ttk.Frame(fenetre_resultats)
        header_frame.pack(fill='x', padx=20, pady=15)
        
        title_label = ttk.Label(header_frame, text="📊 Comparaison des Algorithmes de Tri", 
                               font=('Segoe UI', 18, 'bold'),
                               foreground=self.COLORS['primary'])
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(header_frame, text="Analyse de performance sur différentes tailles de données", 
                                 font=('Segoe UI', 11),
                                 foreground=self.COLORS['text_secondary'])
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        content_frame = ttk.Frame(fenetre_resultats)
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        canvas = tk.Canvas(content_frame, bg=self.COLORS['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, taille_resultats in enumerate(resultats):
            taille = taille_resultats['taille']
            
            section_frame = ttk.LabelFrame(scrollable_frame, 
                                         text=f"📈 Taille: {taille} documents", 
                                         style='Card.TLabelframe', 
                                         padding="15 10")
            section_frame.pack(fill='x', pady=(0 if i == 0 else 15, 0))
            
            tableau_frame = ttk.Frame(section_frame)
            tableau_frame.pack(fill='x')
            
            header_row = ttk.Frame(tableau_frame)
            header_row.pack(fill='x', pady=(0, 5))
            
            ttk.Label(header_row, text="Algorithme", font=('Segoe UI', 10, 'bold'), 
                     width=15).pack(side='left', padx=(0, 10))
            ttk.Label(header_row, text="Complexité", font=('Segoe UI', 10, 'bold'), 
                     width=12).pack(side='left', padx=(0, 10))
            ttk.Label(header_row, text="Temps (ms)", font=('Segoe UI', 10, 'bold'), 
                     width=12).pack(side='left', padx=(0, 10))
            ttk.Label(header_row, text="Performance", font=('Segoe UI', 10, 'bold'), 
                     width=25).pack(side='left')
            
            separator = ttk.Separator(tableau_frame, orient='horizontal')
            separator.pack(fill='x', pady=5)
            
            algorithmes_tries = sorted(taille_resultats['algorithmes'], key=lambda x: x['temps'])
            temps_min = algorithmes_tries[0]['temps']
            
            for j, algo in enumerate(algorithmes_tries):
                row_frame = ttk.Frame(tableau_frame)
                row_frame.pack(fill='x', pady=2)
                
                ratio = algo['temps'] / temps_min if temps_min > 0 else 1
                
                if j == 0:
                    bg_color = '#2ecc71'
                    fg_color = 'white'
                    performance_text = "🏆 Le plus rapide"
                elif j == 1:
                    bg_color = '#3498db'
                    fg_color = 'white'
                    performance_text = f"🥈 Top 2 ({ratio:.1f}×)"
                elif j == 2:
                    bg_color = '#9b59b6'
                    fg_color = 'white'
                    performance_text = f"🥉 Top 3 ({ratio:.1f}×)"
                else:
                    bg_color = '#ecf0f1'
                    fg_color = '#2c3e50'
                    if ratio > 10:
                        performance_text = f"🐌 Plus lent ({ratio:.0f}×)"
                    else:
                        performance_text = f"⏱️ Plus lent ({ratio:.1f}×)"
                
                colored_frame = tk.Frame(row_frame, bg=bg_color, height=30)
                colored_frame.pack(fill='x')
                colored_frame.pack_propagate(False)
                
                ttk.Label(colored_frame, text=algo['nom'], 
                         font=('Segoe UI', 9, 'bold' if j < 3 else 'normal'), width=15, 
                         background=bg_color, foreground=fg_color).pack(side='left', padx=5, pady=4)
                ttk.Label(colored_frame, text=algo['complexite'], 
                         font=('Segoe UI', 9), width=12, background=bg_color,
                         foreground=fg_color).pack(side='left', padx=5, pady=4)
                ttk.Label(colored_frame, text=f"{algo['temps']*1000:.4f}", 
                         font=('Segoe UI', 9), width=12, background=bg_color,
                         foreground=fg_color).pack(side='left', padx=5, pady=4)
                ttk.Label(colored_frame, text=performance_text, 
                         font=('Segoe UI', 9, 'bold' if j == 0 else 'normal'), width=25, 
                         background=bg_color, foreground=fg_color).pack(side='left', padx=5, pady=4)
        
        conclusions_frame = ttk.LabelFrame(scrollable_frame, 
                                         text="📝 Conclusions", 
                                         style='Card.TLabelframe', 
                                         padding="15 10")
        conclusions_frame.pack(fill='x', pady=(15, 0))
        
        conclusions_list = [
            "• Les algorithmes O(n²) sont lents sur de grandes listes",
            "• Les algorithmes O(n log n) sont plus efficaces",
            "• Le Tri par Comptage est très rapide mais limité par la plage des valeurs",
            "• Le Tri Rapide peut être O(n²) dans le pire cas",
            "• Le Tri Fusion est généralement le plus stable en performance"
        ]
        
        if len(resultats) >= 3:
            derniers_res = resultats[-1]['algorithmes']
            derniers_tries = sorted(derniers_res, key=lambda x: x['temps'])
            plus_lent = derniers_tries[-1]
            plus_rapide = derniers_tries[0]
            ratio_final = plus_lent['temps'] / plus_rapide['temps'] if plus_rapide['temps'] > 0 else 1
            
            if ratio_final > 50:
                conclusions_list.append(f"\n⚠️ Sur {resultats[-1]['taille']} documents, {plus_lent['nom']} est {ratio_final:.0f}× plus lent que {plus_rapide['nom']} !")
        
        conclusions_text = "\n".join(conclusions_list)
        
        ttk.Label(conclusions_frame, text=conclusions_text, 
                 font=('Segoe UI', 10),
                 foreground=self.COLORS['text_primary'], justify='left').pack(anchor='w')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        button_frame = ttk.Frame(fenetre_resultats)
        button_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        close_button = ttk.Button(button_frame, text="Fermer", 
                                command=fenetre_resultats.destroy,
                                style='Primary.TButton')
        close_button.pack(side='right')
        
        fenetre_resultats.focus_set()

    
    def melanger_liste(self):
        """Mélange aléatoirement la liste"""
        import random
        random.shuffle(self.list_bib)
        self.temps_execution_var.set("🔀 Liste mélangée aléatoirement !")
        self.update_affichage()
    
    def trier_insertion_affichage(self):
        """Tri par insertion avec mesure de temps PRÉCISE (sans GUI)"""
        import time
        start_time = time.perf_counter()
        trier_par_titre(self.list_bib)
        end_time = time.perf_counter()
        temps = end_time - start_time
        self.temps_execution_var.set(f"⏱️ Tri Insertion: {temps:.6f} secondes ({len(self.list_bib)} docs)")
        self.update_affichage()
    
    def trier_selection_affichage(self):
        """Tri par sélection avec mesure de temps PRÉCISE (sans GUI)"""
        import time
        start_time = time.perf_counter()
        tri_selection(self.list_bib)
        end_time = time.perf_counter()
        temps = end_time - start_time
        self.temps_execution_var.set(f"⏱️ Tri Sélection: {temps:.6f} secondes ({len(self.list_bib)} docs)")
        self.update_affichage()
    
    def trier_bulles_affichage(self):
        """Tri à bulles avec mesure de temps PRÉCISE (sans GUI)"""
        import time
        start_time = time.perf_counter()
        tri_bulles(self.list_bib)
        end_time = time.perf_counter()
        temps = end_time - start_time
        self.temps_execution_var.set(f"⏱️ Tri à Bulles: {temps:.6f} secondes ({len(self.list_bib)} docs)")
        self.update_affichage()
    
    def trier_rapide_affichage(self):
        """Tri rapide avec mesure de temps PRÉCISE (sans GUI)"""
        import time
        start_time = time.perf_counter()
        resultat = tri_rapide(self.list_bib)
        self.list_bib.clear()
        self.list_bib.extend(resultat)
        end_time = time.perf_counter()
        temps = end_time - start_time
        self.temps_execution_var.set(f"⏱️ Tri Rapide: {temps:.6f} secondes ({len(self.list_bib)} docs)")
        self.update_affichage()
    
    def trier_fusion_affichage(self):
        """Tri fusion avec mesure de temps PRÉCISE (sans GUI)"""
        import time
        start_time = time.perf_counter()
        resultat = tri_fusion(self.list_bib)
        self.list_bib.clear()
        self.list_bib.extend(resultat)
        end_time = time.perf_counter()
        temps = end_time - start_time
        self.temps_execution_var.set(f"⏱️ Tri Fusion: {temps:.6f} secondes ({len(self.list_bib)} docs)")
        self.update_affichage()
    
    def trier_tas_affichage(self):
        """Tri tas avec mesure de temps PRÉCISE (sans GUI)"""
        import time
        start_time = time.perf_counter()
        tri_tas(self.list_bib)
        end_time = time.perf_counter()
        temps = end_time - start_time
        self.temps_execution_var.set(f"⏱️ Tri Tas: {temps:.6f} secondes ({len(self.list_bib)} docs)")
        self.update_affichage()
    
    def trier_comptage_affichage(self):
        """Tri comptage avec mesure de temps PRÉCISE (sans GUI)"""
        import time
        start_time = time.perf_counter()
        tri_comptage(self.list_bib)
        end_time = time.perf_counter()
        temps = end_time - start_time
        self.temps_execution_var.set(f"⏱️ Tri Comptage: {temps:.6f} secondes ({len(self.list_bib)} docs)")
        self.update_affichage()
    
    def executer_tests_unitaires(self):
        """Exécute les tests unitaires et affiche les résultats dans une fenêtre"""
        from tests_tri import TestsTriAlgorithmes
        
        result_window = tk.Toplevel(self.master)
        result_window.title("Tests Unitaires des Algorithmes de Tri")
        result_window.geometry("900x700")
        result_window.configure(bg=self.COLORS['background'])
        
        main_frame = ttk.Frame(result_window, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(header_frame, text="🧪 Tests Unitaires des Algorithmes de Tri", 
                 font=('Segoe UI', 16, 'bold'),
                 foreground=self.COLORS['primary']).pack(anchor='w')
        
        ttk.Label(header_frame, text="Validation du bon fonctionnement avec listes prédéfinies", 
                 font=('Segoe UI', 10),
                 foreground=self.COLORS['text_secondary']).pack(anchor='w', pady=(5, 0))
        
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill='x', pady=(0, 15))
        
        progress_label = ttk.Label(progress_frame, text="⏳ Exécution des tests en cours...", 
                                   font=('Segoe UI', 10, 'bold'))
        progress_label.pack()
        
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        
        result_text = tk.Text(text_frame, wrap="word", 
                             yscrollcommand=scrollbar.set,
                             bg=self.COLORS['surface'],
                             fg=self.COLORS['text_primary'],
                             font=('Consolas', 9),
                             padx=10, pady=10)
        result_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=result_text.yview)
        
        result_window.update()
        
        tests = TestsTriAlgorithmes()
        resultats = tests.executer_tous_les_tests()
        
        rapport = tests.generer_rapport_texte(resultats)
        result_text.insert('1.0', rapport)
        result_text.config(state='disabled')
        
        total_tests = sum(len(tests_algo) for tests_algo in resultats.values())
        tests_reussis = sum(1 for tests_algo in resultats.values() 
                           for test in tests_algo.values() if test['valide'])
        
        if tests_reussis == total_tests:
            progress_label.config(text=f"✅ Tous les tests ont réussi ! ({tests_reussis}/{total_tests})",
                                 foreground=self.COLORS['success'])
        else:
            progress_label.config(text=f"⚠️ {total_tests - tests_reussis} test(s) échoué(s) ({tests_reussis}/{total_tests})",
                                 foreground=self.COLORS['danger'])
        
        ttk.Button(main_frame, text="Fermer", 
                  command=result_window.destroy,
                  style='Primary.TButton').pack(pady=10)

    def rechercher_complete_list(self):
        """Recherche complète dans tous les champs (titre, auteur, mots-clés)."""
        terme = self.recherche_terme_var.get().strip()
        if not terme: 
            messagebox.showwarning("Attention", "Veuillez saisir un terme de recherche.")
            return
        
        terme_lower = terme.lower()
        resultats = []
        champs_trouves = []
        
        for doc in self.list_bib:
            trouve = False
            champs = []
            
            if terme_lower in doc.titre.lower():
                trouve = True
                champs.append("titre")
            
            if terme_lower in doc.auteur.lower():
                trouve = True
                champs.append("auteur")
            
            for mot_cle in doc.mots_cles:
                if terme_lower in mot_cle.lower():
                    trouve = True
                    champs.append("mots-clés")
                    break
            
            if trouve:
                resultats.append(doc)
                champs_trouves.append(f"{doc.titre} (dans: {', '.join(champs)})")
        
        if resultats:
            message_detail = f"Terme '{terme}' trouvé dans {len(resultats)} document(s):\n\n"
            for champ_info in champs_trouves:
                message_detail += f"• {champ_info}\n"
            
            self.afficher_resultats_temp(resultats, f"Résultats P1 (Recherche Complète) pour '{terme}'", message_detail)
        else:
            messagebox.showinfo("Recherche", f"Aucun document trouvé contenant '{terme}' dans le titre, l'auteur ou les mots-clés.")


    def setup_p2_tab(self):
        frame = self.frame_p2
        self.recherche_bst_var = tk.StringVar()
        self.recherche_bst_auteur_var = tk.StringVar()
        self.recherche_bst_mots_cles_var = tk.StringVar()
        self.recherche_bst_avancee_var = tk.StringVar()
        self.suppression_bst_var = tk.StringVar()

        canvas = tk.Canvas(frame, bg=self.COLORS['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        content_frame = scrollable_frame

        ttk.Label(content_frame, text="Optimisation avec l'Arbre Binaire de Recherche (BST)", font=('Segoe UI', 14, 'bold')).pack(pady=10)
        ttk.Label(content_frame, text="Performance: O(log n) pour titre, O(n) pour autres critères.", 
                 font=('Segoe UI', 10),
                 foreground=self.COLORS['text_secondary']).pack(pady=(0, 20))

        if not self.bst_bib:
            ttk.Label(content_frame, text="Module BST non disponible. Vérifiez les imports.", fg="red").pack(pady=20)
            return

        search_frame = ttk.LabelFrame(content_frame, text="Recherche par Titre (O(log n))", padding="15 10")
        search_frame.pack(pady=15, fill="x")
        
        search_input_frame = ttk.Frame(search_frame)
        search_input_frame.pack(fill='x')
        
        search_entry = ttk.Entry(search_input_frame, textvariable=self.recherche_bst_var)
        search_entry.pack(side="left", fill='x', expand=True, padx=(0, 10))
        ttk.Button(search_input_frame, text="Rechercher Titre", command=self.rechercher_bst, style='Primary.TButton').pack(side="left")
        
        ttk.Label(search_frame, text="Recherche rapide basée sur la structure arborescente.", 
                 foreground=self.COLORS['text_secondary'], font=('Segoe UI', 9)).pack(pady=(8, 0))

        auteur_frame = ttk.LabelFrame(content_frame, text="Recherche par Auteur (O(n))", padding="15 10")
        auteur_frame.pack(pady=15, fill="x")
        
        auteur_input_frame = ttk.Frame(auteur_frame)
        auteur_input_frame.pack(fill='x')
        
        auteur_entry = ttk.Entry(auteur_input_frame, textvariable=self.recherche_bst_auteur_var)
        auteur_entry.pack(side="left", fill='x', expand=True, padx=(0, 10))
        ttk.Button(auteur_input_frame, text="Rechercher Auteur", command=self.rechercher_auteur_bst, style='Primary.TButton').pack(side="left")
        
        ttk.Label(auteur_frame, text="Recherche par auteur dans le BST.", 
                 foreground=self.COLORS['text_secondary'], font=('Segoe UI', 9)).pack(pady=(8, 0))

        mots_cles_frame = ttk.LabelFrame(content_frame, text="Recherche par Mots-clés (O(n))", padding="15 10")
        mots_cles_frame.pack(pady=15, fill="x")
        
        mots_cles_input_frame = ttk.Frame(mots_cles_frame)
        mots_cles_input_frame.pack(fill='x')
        
        mots_cles_entry = ttk.Entry(mots_cles_input_frame, textvariable=self.recherche_bst_mots_cles_var)
        mots_cles_entry.pack(side="left", fill='x', expand=True, padx=(0, 10))
        ttk.Button(mots_cles_input_frame, text="Rechercher Mots-clés", command=self.rechercher_mots_cles_bst, style='Primary.TButton').pack(side="left")
        
        ttk.Label(mots_cles_frame, text="Recherche par mots-clés dans le BST.", 
                 foreground=self.COLORS['text_secondary'], font=('Segoe UI', 9)).pack(pady=(8, 0))

        avancee_frame = ttk.LabelFrame(content_frame, text="Recherche Avancée (O(n))", padding="15 10")
        avancee_frame.pack(pady=15, fill="x")
        
        avancee_input_frame = ttk.Frame(avancee_frame)
        avancee_input_frame.pack(fill='x')
        
        avancee_entry = ttk.Entry(avancee_input_frame, textvariable=self.recherche_bst_avancee_var)
        avancee_entry.pack(side="left", fill='x', expand=True, padx=(0, 10))
        ttk.Button(avancee_input_frame, text="Rechercher Avancée", command=self.rechercher_avancee_bst, style='Primary.TButton').pack(side="left")
        
        ttk.Label(avancee_frame, text="Recherche dans tous les champs du BST.", 
                 foreground=self.COLORS['text_secondary'], font=('Segoe UI', 9)).pack(pady=(8, 0))

        ajout_frame = ttk.LabelFrame(content_frame, text="Ajout de Document dans le BST (O(log n))", padding="15 10")
        ajout_frame.pack(pady=15, fill="x")
        
        self.ajout_bst_titre_var = tk.StringVar()
        self.ajout_bst_auteur_var = tk.StringVar()
        self.ajout_bst_mots_cles_var = tk.StringVar()
        
        titre_row = ttk.Frame(ajout_frame)
        titre_row.pack(fill='x', pady=5)
        ttk.Label(titre_row, text="Titre:", width=15).pack(side="left")
        ttk.Entry(titre_row, textvariable=self.ajout_bst_titre_var).pack(side="left", fill='x', expand=True, padx=5)
        
        auteur_row = ttk.Frame(ajout_frame)
        auteur_row.pack(fill='x', pady=5)
        ttk.Label(auteur_row, text="Auteur:", width=15).pack(side="left")
        ttk.Entry(auteur_row, textvariable=self.ajout_bst_auteur_var).pack(side="left", fill='x', expand=True, padx=5)
        
        mots_cles_row = ttk.Frame(ajout_frame)
        mots_cles_row.pack(fill='x', pady=5)
        ttk.Label(mots_cles_row, text="Mots-clés:", width=15).pack(side="left")
        ttk.Entry(mots_cles_row, textvariable=self.ajout_bst_mots_cles_var).pack(side="left", fill='x', expand=True, padx=5)
        
        ttk.Button(ajout_frame, text="Ajouter au BST", command=self.ajouter_bst, style='Primary.TButton').pack(pady=10)
        
        ttk.Label(ajout_frame, text="Ajoute le document dans le BST tout en maintenant l'ordre trié.", 
                 foreground=self.COLORS['text_secondary'], font=('Segoe UI', 9)).pack()

        perf_frame = ttk.LabelFrame(content_frame, text="Comparaison des Performances de Recherche", padding="15 10")
        perf_frame.pack(pady=15, fill="x")
        
        ttk.Label(perf_frame, text="Compare la vitesse de recherche entre Liste (O(n)) et BST (O(log n))", 
                 foreground=self.COLORS['text_secondary'], font=('Segoe UI', 9)).pack(pady=5)
        
        ttk.Button(perf_frame, text="Comparer BST vs Liste", 
                  command=self.comparer_performances_bst_liste, 
                  style='Primary.TButton').pack(pady=10)
        
        ttk.Label(perf_frame, text="Affiche les temps de recherche pour démontrer le gain de performance du BST.", 
                 foreground=self.COLORS['text_secondary'], font=('Segoe UI', 9)).pack()

        delete_frame = ttk.LabelFrame(content_frame, text="Suppression de Document (O(log n))", padding="15 10")
        delete_frame.pack(pady=15, fill="x")
        
        delete_input_frame = ttk.Frame(delete_frame)
        delete_input_frame.pack(fill='x')
        
        delete_entry = ttk.Entry(delete_input_frame, textvariable=self.suppression_bst_var)
        delete_entry.pack(side="left", fill='x', expand=True, padx=(0, 10))
        ttk.Button(delete_input_frame, text="Supprimer par Titre", command=self.supprimer_bst, style='Primary.TButton').pack(side="left")
        
        ttk.Label(delete_frame, text="Maintient l'intégrité du BST après la suppression (O(log n)).", 
                 foreground=self.COLORS['text_secondary'], font=('Segoe UI', 9)).pack(pady=(8, 0))

    def rechercher_bst(self):
        terme = self.recherche_bst_var.get().strip()
        if not terme: return
        
        resultat = self.bst_bib.search(terme)
        
        self.afficher_resultats_temp([resultat] if resultat else [], 
                                    f"Résultat P2 (BST O(log n)) pour '{terme}'")

    def rechercher_auteur_bst(self):
        auteur = self.recherche_bst_auteur_var.get().strip()
        if not auteur: return
        
        resultats = self.bst_bib.search_by_author(auteur)
        self.afficher_resultats_temp(resultats, f"Résultats P2 (BST Auteur) pour '{auteur}'")

    def rechercher_mots_cles_bst(self):
        mot_cle = self.recherche_bst_mots_cles_var.get().strip()
        if not mot_cle: return
        
        resultats = self.bst_bib.search_by_keywords(mot_cle)
        self.afficher_resultats_temp(resultats, f"Résultats P2 (BST Mots-clés) pour '{mot_cle}'")

    def rechercher_avancee_bst(self):
        terme = self.recherche_bst_avancee_var.get().strip()
        if not terme: return
        
        resultats = self.bst_bib.search_advanced(terme)
        self.afficher_resultats_temp(resultats, f"Résultats P2 (BST Avancée) pour '{terme}'")

    def ajouter_bst(self):
        """Ajoute un document uniquement dans le BST """
        titre = self.ajout_bst_titre_var.get().strip()
        auteur = self.ajout_bst_auteur_var.get().strip()
        mots_cles = self.ajout_bst_mots_cles_var.get().strip()
        
        if not titre or not auteur:
            messagebox.showwarning("Champs manquants", "Le titre et l'auteur sont obligatoires.")
            return
        
        try:
            from partie_1.document import Document
            nouveau_doc = Document(titre, auteur, mots_cles)
            
            self.bst_bib.insert(nouveau_doc)
            
            try:
                import json
                import os
                bst_file = 'bibliotheque_data_bst.json'
                documents_data = []
                for doc in self.bst_bib.in_order_traversal():
                    documents_data.append({
                        'titre': doc.titre,
                        'auteur': doc.auteur,
                        'mots_cles': doc.mots_cles
                    })
                with open(bst_file, 'w', encoding='utf-8') as f:
                    json.dump(documents_data, f, indent=4, ensure_ascii=False)
            except Exception as e:
                print(f"Erreur lors de la sauvegarde du BST: {e}")
            
            self.ajout_bst_titre_var.set("")
            self.ajout_bst_auteur_var.set("")
            self.ajout_bst_mots_cles_var.set("")
            
            self.update_affichage()
            
            messagebox.showinfo("Succès", f"Document '{titre}' ajouté au BST avec succès !\n\nTaille du BST: {self.bst_bib.size} documents\n\nNote: Ajouté uniquement dans le BST, pas dans les autres structures.")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout : {str(e)}")
    
    def comparer_performances_bst_liste(self):
        """Compare les performances de recherche entre BST et Liste"""
        if not self.bst_bib or not self.list_bib:
            messagebox.showwarning("Structures vides", "BST ou Liste vide. Ajoutez des documents d'abord.")
            return
        
        try:
            import time
            import random
            
            result_window = tk.Toplevel(self.master)
            result_window.title("Comparaison des Performances : BST vs Liste")
            result_window.geometry("700x600")
            result_window.configure(bg=self.COLORS['background'])
            
            main_frame = ttk.Frame(result_window, padding="20")
            main_frame.pack(fill="both", expand=True)
            
            ttk.Label(main_frame, text="Comparaison des Performances de Recherche", 
                     font=('Segoe UI', 14, 'bold')).pack(pady=(0, 10))
            
            ttk.Label(main_frame, text="Recherche par titre : Liste O(n) vs BST O(log n)", 
                     font=('Segoe UI', 10), 
                     foreground=self.COLORS['text_secondary']).pack(pady=(0, 20))
            
            text_frame = ttk.Frame(main_frame)
            text_frame.pack(fill="both", expand=True)
            
            scrollbar = ttk.Scrollbar(text_frame)
            scrollbar.pack(side="right", fill="y")
            
            result_text = tk.Text(text_frame, wrap="word", 
                                 yscrollcommand=scrollbar.set,
                                 bg=self.COLORS['background'],
                                 fg=self.COLORS['text_primary'],
                                 font=('Consolas', 10),
                                 padx=10, pady=10)
            result_text.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=result_text.yview)
            
            result_text.insert('end', "🔄 Test en cours...\n\n")
            result_window.update()
            
            nb_tests = min(100, len(self.list_bib))
            titres_test = random.sample([doc.titre for doc in self.list_bib], nb_tests)
            
            result_text.insert('end', f"{'='*60}\n")
            result_text.insert('end', f"Nombre de documents dans la collection : {len(self.list_bib)}\n")
            result_text.insert('end', f"Nombre de recherches à effectuer : {nb_tests}\n")
            result_text.insert('end', f"{'='*60}\n\n")
            
            result_text.insert('end', "📊 Test 1 : Recherche Séquentielle (Liste)\n")
            result_text.insert('end', "-" * 60 + "\n")
            start_liste = time.time()
            for titre in titres_test:
                for doc in self.list_bib:
                    if doc.titre.lower() == titre.lower():
                        break
            end_liste = time.time()
            temps_liste = end_liste - start_liste
            temps_moyen_liste = temps_liste / nb_tests
            
            result_text.insert('end', f"Algorithme        : Recherche Séquentielle\n")
            result_text.insert('end', f"Complexité        : O(n)\n")
            result_text.insert('end', f"Temps total       : {temps_liste:.6f} secondes\n")
            result_text.insert('end', f"Temps moyen/recherche : {temps_moyen_liste:.8f} secondes\n\n")
            result_window.update()
            
            result_text.insert('end', "🌳 Test 2 : Recherche BST (Arbre Binaire)\n")
            result_text.insert('end', "-" * 60 + "\n")
            start_bst = time.time()
            for titre in titres_test:
                self.bst_bib.search(titre)
            end_bst = time.time()
            temps_bst = end_bst - start_bst
            temps_moyen_bst = temps_bst / nb_tests
            
            result_text.insert('end', f"Algorithme        : Recherche BST\n")
            result_text.insert('end', f"Complexité        : O(log n)\n")
            result_text.insert('end', f"Temps total       : {temps_bst:.6f} secondes\n")
            result_text.insert('end', f"Temps moyen/recherche : {temps_moyen_bst:.8f} secondes\n\n")
            result_window.update()
            
            gain = temps_liste / temps_bst if temps_bst > 0 else 0
            result_text.insert('end', f"{'='*60}\n")
            result_text.insert('end', "🏆 RÉSULTAT DE LA COMPARAISON\n")
            result_text.insert('end', f"{'='*60}\n\n")
            
            if gain > 1:
                result_text.insert('end', f"✅ Le BST est {gain:.2f}x plus rapide que la liste !\n\n")
            elif gain < 1:
                result_text.insert('end', f"⚠️ La liste est {1/gain:.2f}x plus rapide (collection très petite)\n\n")
            else:
                result_text.insert('end', f"Les performances sont similaires\n\n")
            
            result_text.insert('end', f"Différence de temps : {abs(temps_liste - temps_bst):.6f} secondes\n")
            result_text.insert('end', f"Gain relatif      : {((temps_liste - temps_bst) / temps_liste * 100):.2f}%\n\n")
            
            result_text.insert('end', f"{'='*60}\n")
            result_text.insert('end', "💡 ANALYSE\n")
            result_text.insert('end', f"{'='*60}\n\n")
            
            result_text.insert('end', f"Pour {len(self.list_bib)} documents :\n")
            result_text.insert('end', f"  • Liste : parcourt en moyenne {len(self.list_bib)//2} éléments\n")
            
            import math
            hauteur_theorique = math.ceil(math.log2(len(self.list_bib))) if len(self.list_bib) > 0 else 0
            result_text.insert('end', f"  • BST : parcourt environ {hauteur_theorique} niveaux\n\n")
            
            if len(self.list_bib) < 50:
                result_text.insert('end', "ℹ️ Note : Pour les petites collections (< 50), la différence\n")
                result_text.insert('end', "   est minime. Le BST montre ses avantages avec plus de données.\n")
            else:
                result_text.insert('end', "✨ Le BST démontre clairement son avantage en termes de\n")
                result_text.insert('end', "   performance pour les grandes collections !\n")
            
            result_text.config(state='disabled')
            
            ttk.Button(main_frame, text="Fermer", 
                      command=result_window.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la comparaison : {str(e)}")
    
    def supprimer_bst(self):
        titre = self.suppression_bst_var.get().strip()
        if not titre: return
        
        resultat = supprimer_document_complet(titre, self.list_bib, self.bst_bib, self.hash_bib)
        
        if resultat['succes']:
            message = f"Document '{titre}' supprimé avec succès !\n\n"
            message += f"Supprimé de: {', '.join(resultat['supprime_de'])}\n"
            
            if resultat.get('sauvegarde', False):
                message += "✅ Sauvegarde automatique réussie"
            else:
                message += "⚠️ Problème de sauvegarde"
            
            if resultat['erreurs']:
                message += f"\n\nErreurs: {', '.join(resultat['erreurs'])}"
            
            messagebox.showinfo("Suppression réussie", message)
            self.update_affichage()
        else:
            message = f"Document '{titre}' non trouvé.\n\n"
            if resultat['non_trouve_dans']:
                message += f"Non trouvé dans: {', '.join(resultat['non_trouve_dans'])}\n"
            if resultat['erreurs']:
                message += f"Erreurs: {', '.join(resultat['erreurs'])}"
            
            messagebox.showerror("Suppression échouée", message)
        
        self.suppression_bst_var.set("")


    def setup_p3_tab(self):
        frame = self.frame_p3
        self.recherche_hash_auteur_var = tk.StringVar()
        self.recherche_hash_titre_var = tk.StringVar()
        self.recherche_hash_mots_cles_var = tk.StringVar()
        self.recherche_hash_avancee_var = tk.StringVar()
        
        ttk.Label(frame, text="Partie 3 : Indexation par Table de Hachage", font=('Segoe UI', 14, 'bold')).pack(pady=10)
        ttk.Label(frame, text="Performance : O(1) pour auteur, O(n) pour autres critères.", 
                 font=('Segoe UI', 10),
                 foreground=self.COLORS['text_secondary']).pack(pady=(0, 20))

        if not self.hash_bib:
            ttk.Label(frame, text="Module Hachage non disponible. Vérifiez les imports.", fg="red").pack(pady=20)
            return

        auteur_frame = ttk.LabelFrame(frame, text="Recherche par Auteur (O(1))", padding="15 10")
        auteur_frame.pack(pady=15, fill="x")
        
        ttk.Entry(auteur_frame, textvariable=self.recherche_hash_auteur_var, width=40).pack(side="left", padx=10)
        ttk.Button(auteur_frame, text="Rechercher Auteur", command=self.rechercher_auteur_hash, style='Primary.TButton').pack(side="left")
        ttk.Label(auteur_frame, text="Trouve tous les documents d'un auteur en calculant directement l'index.", foreground="gray").pack(pady=5)

        titre_frame = ttk.LabelFrame(frame, text="Recherche par Titre (O(n))", padding="15 10")
        titre_frame.pack(pady=15, fill="x")
        
        ttk.Entry(titre_frame, textvariable=self.recherche_hash_titre_var, width=40).pack(side="left", padx=10)
        ttk.Button(titre_frame, text="Rechercher Titre", command=self.rechercher_titre_hash, style='Primary.TButton').pack(side="left")
        ttk.Label(titre_frame, text="Recherche par titre dans la table de hachage.", foreground="gray").pack(pady=5)

        mots_cles_frame = ttk.LabelFrame(frame, text="Recherche par Mots-clés (O(n))", padding="15 10")
        mots_cles_frame.pack(pady=15, fill="x")
        
        ttk.Entry(mots_cles_frame, textvariable=self.recherche_hash_mots_cles_var, width=40).pack(side="left", padx=10)
        ttk.Button(mots_cles_frame, text="Rechercher Mots-clés", command=self.rechercher_mots_cles_hash, style='Primary.TButton').pack(side="left")
        ttk.Label(mots_cles_frame, text="Recherche par mots-clés dans la table de hachage.", foreground="gray").pack(pady=5)

        avancee_frame = ttk.LabelFrame(frame, text="Recherche Avancée (O(n))", padding="15 10")
        avancee_frame.pack(pady=15, fill="x")
        
        ttk.Entry(avancee_frame, textvariable=self.recherche_hash_avancee_var, width=40).pack(side="left", padx=10)
        ttk.Button(avancee_frame, text="Rechercher Avancée", command=self.rechercher_avancee_hash, style='Primary.TButton').pack(side="left")
        ttk.Label(avancee_frame, text="Recherche dans tous les champs de la table de hachage.", foreground="gray").pack(pady=5)

    def rechercher_auteur_hash(self):
        auteur = self.recherche_hash_auteur_var.get().strip()
        if not auteur: return
        
        resultats = self.hash_bib.search_by_author(auteur)
        self.afficher_resultats_temp(resultats, f"Résultats P3 (Hachage Auteur O(1)) pour '{auteur}'")

    def rechercher_titre_hash(self):
        titre = self.recherche_hash_titre_var.get().strip()
        if not titre: return
        
        resultats = self.hash_bib.search_by_title(titre)
        self.afficher_resultats_temp(resultats, f"Résultats P3 (Hachage Titre O(n)) pour '{titre}'")

    def rechercher_mots_cles_hash(self):
        mot_cle = self.recherche_hash_mots_cles_var.get().strip()
        if not mot_cle: return
        
        resultats = self.hash_bib.search_by_keywords(mot_cle)
        self.afficher_resultats_temp(resultats, f"Résultats P3 (Hachage Mots-clés O(n)) pour '{mot_cle}'")

    def rechercher_avancee_hash(self):
        terme = self.recherche_hash_avancee_var.get().strip()
        if not terme: return
        
        resultats = self.hash_bib.search_advanced(terme)
        self.afficher_resultats_temp(resultats, f"Résultats P3 (Hachage Avancée O(n)) pour '{terme}'")


    def setup_suppression_tab(self):
        """Configure l'onglet de suppression avancée."""
        frame = self.frame_suppression
        
        self.suppression_titre_var = tk.StringVar()
        self.suppression_auteur_var = tk.StringVar()
        self.suppression_mots_cles_var = tk.StringVar()
        
        header_frame = ttk.Frame(frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="🗑️ Suppression Avancée de Documents", 
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Supprimez des documents de toutes les structures avec sauvegarde automatique",
                                  font=('Segoe UI', 10),
                                  foreground=self.COLORS['text_secondary'])
        subtitle_label.pack(pady=(5, 0))
        
        titre_card = ttk.LabelFrame(frame, text="Suppression par Titre Exact", padding="15 10")
        titre_card.pack(pady=15, fill="x")
        
        titre_frame = ttk.Frame(titre_card)
        titre_frame.pack(fill='x')
        
        ttk.Entry(titre_frame, textvariable=self.suppression_titre_var, 
                 style='Modern.TEntry', width=40).pack(side="left", padx=(0, 10))
        ttk.Button(titre_frame, text="🗑️ Supprimer par Titre", 
                  command=self.supprimer_par_titre_avance, style='Primary.TButton').pack(side="left")
        
        ttk.Label(titre_card, text="Supprime le document avec le titre exact spécifié", 
                 font=('Segoe UI', 9),
                 foreground=self.COLORS['text_secondary']).pack(pady=(8, 0))
        
        auteur_card = ttk.LabelFrame(frame, text="Suppression par Auteur", padding="15 10")
        auteur_card.pack(pady=15, fill="x")
        
        auteur_frame = ttk.Frame(auteur_card)
        auteur_frame.pack(fill='x')
        
        ttk.Entry(auteur_frame, textvariable=self.suppression_auteur_var, 
                 style='Modern.TEntry', width=40).pack(side="left", padx=(0, 10))
        ttk.Button(auteur_frame, text="🗑️ Supprimer par Auteur", 
                  command=self.supprimer_par_auteur_avance, style='Primary.TButton').pack(side="left")
        
        ttk.Label(auteur_card, text="Supprime tous les documents de l'auteur spécifié", 
                 font=('Segoe UI', 9),
                 foreground=self.COLORS['text_secondary']).pack(pady=(8, 0))
        
        mots_cles_card = ttk.LabelFrame(frame, text="Suppression par Mots-clés", padding="15 10")
        mots_cles_card.pack(pady=15, fill="x")
        
        mots_cles_frame = ttk.Frame(mots_cles_card)
        mots_cles_frame.pack(fill='x')
        
        ttk.Entry(mots_cles_frame, textvariable=self.suppression_mots_cles_var, 
                 style='Modern.TEntry', width=40).pack(side="left", padx=(0, 10))
        ttk.Button(mots_cles_frame, text="🗑️ Supprimer par Mots-clés", 
                  command=self.supprimer_par_mots_cles_avance, style='Primary.TButton').pack(side="left")
        
        ttk.Label(mots_cles_card, text="Supprime tous les documents contenant le mot-clé spécifié", 
                 font=('Segoe UI', 9),
                 foreground=self.COLORS['text_secondary']).pack(pady=(8, 0))
        
        massive_card = ttk.LabelFrame(frame, text="⚠️ Suppression Massive", padding="15 10")
        massive_card.pack(pady=15, fill="x")
        
        ttk.Button(massive_card, text="🗑️ SUPPRIMER TOUS LES DOCUMENTS", 
                  command=self.supprimer_tous_documents, style='Secondary.TButton').pack(pady=10)
        
        ttk.Label(massive_card, text="⚠️ ATTENTION: Cette action supprimera TOUS les documents de la bibliothèque !", 
                 font=('Segoe UI', 9),
                 foreground=self.COLORS['danger']).pack()
    
    def supprimer_par_titre_avance(self):
        """Supprime un document par titre exact."""
        titre = self.suppression_titre_var.get().strip()
        if not titre:
            messagebox.showwarning("Attention", "Veuillez entrer un titre.")
            return
        
        resultat = supprimer_document_complet(titre, self.list_bib, self.bst_bib, self.hash_bib)
        
        if resultat['succes']:
            message = f"✅ Document '{titre}' supprimé avec succès !\n\n"
            message += f"Supprimé de: {', '.join(resultat['supprime_de'])}\n"
            if resultat.get('sauvegarde', False):
                message += "💾 Sauvegarde automatique réussie"
            else:
                message += "⚠️ Problème de sauvegarde"
            messagebox.showinfo("Suppression réussie", message)
            self.update_affichage()
        else:
            message = f"❌ Document '{titre}' non trouvé.\n"
            if resultat['non_trouve_dans']:
                message += f"Non trouvé dans: {', '.join(resultat['non_trouve_dans'])}"
            messagebox.showerror("Suppression échouée", message)
        
        self.suppression_titre_var.set("")
    
    def supprimer_par_auteur_avance(self):
        """Supprime tous les documents d'un auteur."""
        auteur = self.suppression_auteur_var.get().strip()
        if not auteur:
            messagebox.showwarning("Attention", "Veuillez entrer un nom d'auteur.")
            return
        
        resultat = supprimer_par_criteres('auteur', auteur, self.list_bib, self.bst_bib, self.hash_bib)
        
        if resultat['succes']:
            message = f"✅ {len(resultat['documents_supprimes'])} document(s) supprimé(s) pour l'auteur '{auteur}'\n\n"
            message += "Documents supprimés:\n"
            for doc in resultat['documents_supprimes']:
                message += f"• {doc}\n"
            messagebox.showinfo("Suppression réussie", message)
            self.update_affichage()
        else:
            messagebox.showwarning("Aucune suppression", f"Aucun document trouvé pour l'auteur '{auteur}'")
        
        self.suppression_auteur_var.set("")
    
    def supprimer_par_mots_cles_avance(self):
        """Supprime tous les documents contenant un mot-clé."""
        mot_cle = self.suppression_mots_cles_var.get().strip()
        if not mot_cle:
            messagebox.showwarning("Attention", "Veuillez entrer un mot-clé.")
            return
        
        resultat = supprimer_par_criteres('mots_cles', mot_cle, self.list_bib, self.bst_bib, self.hash_bib)
        
        if resultat['succes']:
            message = f"✅ {len(resultat['documents_supprimes'])} document(s) supprimé(s) pour le mot-clé '{mot_cle}'\n\n"
            message += "Documents supprimés:\n"
            for doc in resultat['documents_supprimes']:
                message += f"• {doc}\n"
            messagebox.showinfo("Suppression réussie", message)
            self.update_affichage()
        else:
            messagebox.showwarning("Aucune suppression", f"Aucun document trouvé pour le mot-clé '{mot_cle}'")
        
        self.suppression_mots_cles_var.set("")
    
    def supprimer_tous_documents(self):
        """Supprime tous les documents avec confirmation."""
        if not self.list_bib:
            messagebox.showinfo("Information", "Aucun document à supprimer.")
            return
        
        confirmation = messagebox.askyesno(
            "Confirmation de suppression massive",
            f"⚠️ ATTENTION: Cette action supprimera TOUS les {len(self.list_bib)} documents de la bibliothèque !\n\n"
            "Cette action est IRRÉVERSIBLE.\n\n"
            "Êtes-vous sûr de vouloir continuer ?"
        )
        
        if confirmation:
            for doc in self.list_bib[:]:
                supprimer_document_complet(doc.titre, self.list_bib, self.bst_bib, self.hash_bib)
            
            messagebox.showinfo("Suppression terminée", "🗑️ Tous les documents ont été supprimés.")
            self.update_affichage()


    def setup_affichage_tab(self):
        frame = self.frame_affichage
        
        canvas = tk.Canvas(frame, bg=self.COLORS['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        content_frame = ttk.Frame(scrollable_frame)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        header_frame = ttk.Frame(content_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="📊 Visualisation et Opérations de Tri", 
                               font=('Segoe UI', 16, 'bold'),
                               foreground=self.COLORS['primary'])
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(header_frame, text="Visualisation en temps réel avec affichage du temps d'exécution", 
                                 font=('Segoe UI', 10),
                                 foreground=self.COLORS['text_secondary'])
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        tri_operations_card = ttk.LabelFrame(content_frame, text="🔄 Opérations de Tri", 
                                            style='Card.TLabelframe', padding="15 10")
        tri_operations_card.pack(fill='x', pady=(0, 15))
        
        melange_frame = ttk.Frame(tri_operations_card)
        melange_frame.pack(fill='x', pady=(5, 15))
        
        ttk.Label(melange_frame, text="🎲 Mélange aléatoire:", 
                 font=('Segoe UI', 10, 'bold')).pack(side='left', padx=(0, 10))
        ttk.Button(melange_frame, text="🔀 Mélanger la liste", 
                  command=self.melanger_liste, 
                  style='Warning.TButton').pack(side='left')
        ttk.Label(melange_frame, text="Permet de mélanger aléatoirement la liste pour tester les algorithmes", 
                 font=('Segoe UI', 9),
                 foreground=self.COLORS['text_secondary']).pack(side='left', padx=(15, 0))
        
        self.temps_execution_var = tk.StringVar(value="")
        self.temps_label = ttk.Label(tri_operations_card, textvariable=self.temps_execution_var,
                                     font=('Segoe UI', 10, 'bold'),
                                     foreground=self.COLORS['success'])
        self.temps_label.pack(pady=(0, 10))
        
        tri_buttons_frame = ttk.Frame(tri_operations_card)
        tri_buttons_frame.pack(fill='x')
        
        ttk.Label(tri_buttons_frame, text="Algorithmes O(n²):", 
                 font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 5))
        
        ttk.Button(tri_buttons_frame, text="🔄 Tri Insertion", 
                  command=self.trier_insertion_affichage, style='Secondary.TButton').grid(row=1, column=0, padx=(0, 5), pady=2, sticky='ew')
        
        ttk.Button(tri_buttons_frame, text="🔍 Tri Sélection", 
                  command=self.trier_selection_affichage, style='Secondary.TButton').grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        
        ttk.Button(tri_buttons_frame, text="🫧 Tri Bulles", 
                  command=self.trier_bulles_affichage, style='Secondary.TButton').grid(row=1, column=2, padx=(5, 0), pady=2, sticky='ew')
        
        ttk.Label(tri_buttons_frame, text="Algorithmes O(n log n):", 
                 font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, columnspan=3, sticky='w', pady=(15, 5))
        
        ttk.Button(tri_buttons_frame, text="⚡ Tri Rapide", 
                  command=self.trier_rapide_affichage, style='Primary.TButton').grid(row=3, column=0, padx=(0, 5), pady=2, sticky='ew')
        
        ttk.Button(tri_buttons_frame, text="🔀 Tri Fusion", 
                  command=self.trier_fusion_affichage, style='Primary.TButton').grid(row=3, column=1, padx=5, pady=2, sticky='ew')
        
        ttk.Button(tri_buttons_frame, text="📚 Tri Tas", 
                  command=self.trier_tas_affichage, style='Primary.TButton').grid(row=3, column=2, padx=(5, 0), pady=2, sticky='ew')
        
        ttk.Label(tri_buttons_frame, text="Algorithmes Spéciaux:", 
                 font=('Segoe UI', 10, 'bold')).grid(row=4, column=0, columnspan=3, sticky='w', pady=(15, 5))
        
        ttk.Button(tri_buttons_frame, text="📊 Tri Comptage", 
                  command=self.trier_comptage_affichage, style='Secondary.TButton').grid(row=5, column=0, padx=(0, 5), pady=2, sticky='ew')
        
        ttk.Button(tri_buttons_frame, text="📈 Comparer Tous", 
                  command=self.comparer_algorithmes, style='Primary.TButton').grid(row=5, column=1, padx=5, pady=2, sticky='ew')
        
        for i in range(3):
            tri_buttons_frame.columnconfigure(i, weight=1, uniform="buttons")
        
        tests_card = ttk.LabelFrame(content_frame, text="🧪 Tests Unitaires des Algorithmes", 
                                    style='Card.TLabelframe', padding="15 10")
        tests_card.pack(fill='x', pady=(0, 15))
        
        tests_info_frame = ttk.Frame(tests_card)
        tests_info_frame.pack(fill='x', pady=(5, 10))
        
        ttk.Label(tests_info_frame, text="Validez le bon fonctionnement de tous les algorithmes avec des listes prédéfinies", 
                 font=('Segoe UI', 10),
                 foreground=self.COLORS['text_secondary']).pack(anchor='w')
        
        tests_button_frame = ttk.Frame(tests_card)
        tests_button_frame.pack(fill='x')
        
        ttk.Button(tests_button_frame, text="🧪 Exécuter les Tests Unitaires", 
                  command=self.executer_tests_unitaires, 
                  style='Primary.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Label(tests_button_frame, text="42 tests (7 algorithmes × 6 scénarios)", 
                 font=('Segoe UI', 9),
                 foreground=self.COLORS['text_secondary']).pack(side='left')
        
        list_card = ttk.LabelFrame(content_frame, text="📋 Liste Python (P1) - Ordre actuel", 
                                  style='Card.TLabelframe', padding="15 10")
        list_card.pack(pady=(0, 15), fill="both", expand=True)
        
        self.text_list = tk.Text(list_card, height=12, wrap='word', 
                                bg=self.COLORS['surface'],
                                fg=self.COLORS['text_primary'],
                                font=('Consolas', 9),
                                bd=0, relief='flat')
        self.text_list.pack(padx=10, pady=10, fill="both", expand=True)
        
        bst_card = ttk.LabelFrame(content_frame, text="🌳 BST (P2) - Ordre In-order (Automatiquement Trié)", 
                                 style='Card.TLabelframe', padding="15 10")
        bst_card.pack(pady=(0, 0), fill="both", expand=True)
        
        self.text_bst = tk.Text(bst_card, height=12, wrap='word', 
                               bg=self.COLORS['surface'],
                               fg=self.COLORS['text_primary'],
                               font=('Consolas', 9),
                               bd=0, relief='flat')
        self.text_bst.pack(padx=10, pady=10, fill="both", expand=True)
        
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


    def afficher_resultats_temp(self, documents, titre, message_detail=None):
        """Affiche les résultats d'une recherche dans une nouvelle fenêtre modale avec style moderne."""
        
        fenetre_resultat = tk.Toplevel(self.master)
        fenetre_resultat.title(f"🔍 {titre}")
        fenetre_resultat.transient(self.master)
        fenetre_resultat.grab_set()
        fenetre_resultat.geometry("600x400")
        fenetre_resultat.configure(bg=self.COLORS['background'])
        fenetre_resultat.resizable(True, True)
        
        header_frame = ttk.Frame(fenetre_resultat)
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        title_label = ttk.Label(header_frame, text=f"🔍 {titre}", 
                               font=('Segoe UI', 14, 'bold'),
                               foreground=self.COLORS['primary'])
        title_label.pack(anchor='w')
        
        content_frame = ttk.Frame(fenetre_resultat)
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        texte_affichage = tk.Text(content_frame, 
                                 height=12, 
                                 width=70,
                                 bg=self.COLORS['surface'],
                                 fg=self.COLORS['text_primary'],
                                 font=('Consolas', 9),
                                 bd=0, relief='flat',
                                 wrap='word')
        texte_affichage.pack(fill='both', expand=True, pady=(0, 15))
        
        if not documents or documents == [None] or documents == []:
            texte_affichage.insert(tk.END, "❌ Aucun document trouvé.")
        else:
            if message_detail:
                texte_affichage.insert(tk.END, message_detail + "\n\n")
                texte_affichage.insert(tk.END, "=" * 50 + "\n\n")
            
            texte_affichage.insert(tk.END, f"✅ {len(documents)} résultat(s) trouvé(s):\n\n")
            for i, doc in enumerate(documents, 1):
                texte_affichage.insert(tk.END, f"{i}. {doc}\n\n")
        
        button_frame = ttk.Frame(fenetre_resultat)
        button_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        ttk.Button(button_frame, text="✖️ Fermer", 
                  command=fenetre_resultat.destroy, 
                  style='Primary.TButton').pack(side='right')
        
        self.master.wait_window(fenetre_resultat)