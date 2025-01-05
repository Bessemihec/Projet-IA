class Book:
    """
    Classe représentant un livre avec diverses propriétés.

    Args:
        _id (str): Identifiant unique du livre.
        N (str): Numéro N.
        BIBID (str): Identifiant de la bibliothèque.
        ITEMID (str): Identifiant de l'item.
        Code_barre (str): Code barre de l'item.
        D_Object (str): Objet D.
        CREATION (str): Date de création.
        MODIF (str): Date de modification.
        Cote (str): Cote de l'item.
        Inventaire (str): Inventaire.
        epn (str): Champ epn.
        Titre (str): Titre du livre.
        Auteur (str): Auteur du livre.
        Locale (str): Localisation.
        Staff_Note (str): Note pour le staff.
        Public_Note (str): Note publique.
        ISBN_A (str): ISBN-A.
        ISBN_Z (str): ISBN-Z.
        Item_class (str): Classe de l'item.
        Specialite (str): Spécialité.
        Nb_Page (str): Nombre de pages.
        Date_edition (str): Date d'édition.
        Editeur (str): Éditeur du livre.
        Prix (str): Prix du livre.
    """

    def __init__(self, _id, N,BIBID,ITEMID,Code_barre,D_CREATION,D_MODIF,Cote,Inventaire,epn,Titre,Auteur,Locale,Staff_Note,Public_Note,ISBN_A,ISBN_Z,Item_class,Specialite,Nb_Page,Date_edition,Editeur,Prix,Etas):
        """
        Initialise une nouvelle instance de Book avec des colonnes spécifiques.
        """
        self._id = _id
        self.N = N
        self.BIBID = BIBID
        self.ITEMID = ITEMID
        self.Code_barre = Code_barre
        self.D_MODIF = D_MODIF
        self.D_CREATION = D_CREATION
        self.Cote = Cote
        self.Inventaire = Inventaire
        self.epn = epn
        self.Titre = Titre
        self.Auteur = Auteur
        self.Locale = Locale
        self.Staff_Note = Staff_Note
        self.Public_Note = Public_Note
        self.ISBN_A = ISBN_A
        self.ISBN_Z = ISBN_Z
        self.Item_class = Item_class
        self.Specialite = Specialite
        self.Nb_Page = Nb_Page
        self.Date_edition = Date_edition
        self.Editeur = Editeur
        self.Prix = Prix
        self.Etas = Etas
        

    def to_dict(self):
        """
        Convertit l'instance de Book en dictionnaire.
        
        Returns:
            dict: Une représentation dictionnaire de l'instance Book.
        """
        return {
            "_id": self._id,
            "N": self.N,
            "BIBID": self.BIBID,
            "ITEMID": self.ITEMID,
            "Code_barre": self.Code_barre,
            "D_Object": self.D_Object,
            "D_CREATION": self.D_CREATION,
            "D_MODIF": self.D_MODIF,
            "Cote": self.Cote,
            "Inventaire": self.Inventaire,
            "epn": self.epn,
            "Titre": self.Titre,
            "Auteur": self.Auteur,
            "Locale": self.Locale,
            "Staff_Note": self.Staff_Note,
            "Public_Note": self.Public_Note,
            "ISBN_A": self.ISBN_A,
            "ISBN_Z": self.ISBN_Z,
            "Item_class": self.Item_class,
            "Specialite": self.Specialite,
            "Nb_Page": self.Nb_Page,
            "Date_edition": self.Date_edition,
            "Editeur": self.Editeur,
            "Prix": self.Prix,
            "Etas": self.Etas,
          
        }