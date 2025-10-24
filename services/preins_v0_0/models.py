
from datetime import datetime
from core.config import db


SEXES = {'F':'Feminin', 'M':'Masculin'}
SITUATIONS = {'C': 'Celibataire', 'M':'Marie(e)', 'V':'Veuf(ve)', 'D':'Divorce(e)'}
LANGUES = {'FR': 'Francais', 'EN': 'Anglais'}


class CommuniqueAdmission(db.Model):
    __bind_key__ = 'preins_v0'
    __tablename__ = 'communiques_admissions'
    
    id = db.Column(db.String(20), primary_key=True)
    numero = db.Column(db.String(50), nullable=False)
    objet = db.Column(db.String(150), nullable=False)
    annee_academique = db.Column(db.String(20), nullable=False)


class Admission(db.Model):
    __bind_key__ = 'preins_v0'
    __tablename__ = 'admissions'
    
    id = db.Column(db.String(12), primary_key=True)
    nom_complet = db.Column(db.String(400), nullable=False)
    classe_id = db.Column(db.String(10), nullable=False)
    statut = db.Column(db.String(10), nullable=False) # code type
    matricule = db.Column(db.String(9), nullable=True)
    communique_id = db.Column(db.String(20), db.ForeignKey('communiques_admissions.id'))
    communique = db.relationship('CommuniqueAdmission')
    inscriptions = db.relationship('Inscription', back_populates='admission')
    requetes = db.relationship('Requete', back_populates='admission')
    max_inscriptions = db.Column(db.Integer, default=3)

    
class Inscription(db.Model):
    __bind_key__ = 'preins_v0'
    __tablename__ = 'inscriptions'
    id = db.Column(db.Integer, primary_key=True)
    admission_id = db.Column(db.String(12), db.ForeignKey('admissions.id'))
    admission = db.relationship('Admission', back_populates='inscriptions')
    
    # Informations personnelles de base
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=True)
    date_naissance = db.Column(db.String(20), nullable=False)
    lieu_naissance = db.Column(db.String(100), nullable=False)
    sexe_id = db.Column(db.String(10), nullable=False)  
    situation_matrimoniale_id = db.Column(db.String(50), nullable=False)
    
    # Origine géographique
    departement_origine_id = db.Column(db.String(100), nullable=False)
    langue_id = db.Column(db.String(10), nullable=False)  
    
    # Coordonnées
    telephone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    
    # Informations académiques
    diplome = db.Column(db.String(200), nullable=False)
    annee_diplome = db.Column(db.Integer, nullable=False)
    
    # Informations du père/tuteur
    nom_pere = db.Column(db.String(200), nullable=True)
    profession_pere = db.Column(db.String(100), nullable=True)
    telephone_pere = db.Column(db.String(20), nullable=True)
    residence_pere = db.Column(db.String(100), nullable=True)
    
    # Informations de la mère
    nom_mere = db.Column(db.String(200), nullable=True)
    profession_mere = db.Column(db.String(100), nullable=True)
    telephone_mere = db.Column(db.String(20), nullable=True)
    residence_mere = db.Column(db.String(100), nullable=True)
    
    # Métadonnées
    date_inscription = db.Column(db.DateTime, default=datetime.now) 


    @property
    def nom_complet(self):
        return ' '.join([self.nom, self.prenom])
    
    @property
    def sexe(self):
        return SEXES[self.sexe_id]

    @property
    def situation_matrimoniale(self):
        return SITUATIONS[self.situation_matrimoniale_id]
    
    @property
    def langue(self):
        return LANGUES[self.langue_id]
    

class Requete(db.Model):
    __bind_key__ = 'preins_v0'
    __tablename__ = 'requetes'
    id = db.Column(db.Integer, primary_key=True)
    admission_id = db.Column(db.String(12), db.ForeignKey('admissions.id'))
    admission = db.relationship('Admission', back_populates='requetes')

    # erreur d'identite
    nom_admis = db.Column(db.String(200), nullable=True)
    nom_correct = db.Column(db.String(200), nullable=True)
    prenom_admis = db.Column(db.String(200), nullable=True)
    prenom_correct = db.Column(db.String(200), nullable=True)

    # erreur de filiere
    option_correct = db.Column(db.String(100), nullable=True)
    niveau_correct = db.Column(db.String(10), nullable=True)
