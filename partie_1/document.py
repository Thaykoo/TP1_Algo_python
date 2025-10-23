
class Document:
    """
    Structure de données représentant un document dans la bibliothèque
    avec ses attributs (titre, auteur, mots_cles).
    """
    def __init__(self, titre, auteur, mots_cles):
        self.titre = titre
        self.auteur = auteur
        if isinstance(mots_cles, str):
            self.mots_cles = [mc.strip().lower() for mc in mots_cles.split(',') if mc.strip()]
        else:
            self.mots_cles = mots_cles

    def __str__(self):
        """
        Représentation textuelle du document.
        """
        return (f"Titre: '{self.titre}' | Auteur: {self.auteur} | "
                f"Mots-clés: {', '.join(self.mots_cles)}")
    
    def to_dict(self):
        """Convertit l'objet Document en dictionnaire pour la sérialisation JSON."""
        return {
            'titre': self.titre,
            'auteur': self.auteur,
            'mots_cles': self.mots_cles
        }