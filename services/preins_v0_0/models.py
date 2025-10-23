
from datetime import datetime
from core.config import db


class Admission(db.Model):
    __bind_key__ = 'preins_v0'
    __tablename__ = 'admissions'
    
    id = db.Column(db.String(12), primary_key=True)
    nom_complet = db.Column(db.String(400), nullable=False)
    classe_id = db.Column(db.String(10), nullable=False)
    statut = db.Column(db.String(10), nullable=False) # code type
    communique = db.Column(db.String(100), nullable=False) # numero
    preinscriptions = db.relationship('Preinscription', back_populates='admission')
    requetes = db.relationship('Requete', back_populates='admission')

    
class Preinscription(db.Model):
    __bind_key__ = 'preins_v0'
    __tablename__ = 'preinscriptions'
    id = db.Column(db.Integer, primary_key=True)
    admission_id = db.Column(db.String(12), db.ForeignKey('admissions.id'))
    admission = db.relationship('Admission', back_populates='preinscriptions')
    
    # Informations personnelles de base
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=True)
    date_naissance = db.Column(db.String(20), nullable=False)
    lieu_naissance = db.Column(db.String(100), nullable=False)
    sexe = db.Column(db.String(10), nullable=False)  
    situation_matrimoniale = db.Column(db.String(50), nullable=False)
    
    # Origine géographique
    departement_origine_id = db.Column(db.String(100), nullable=False)
    langue = db.Column(db.String(10), nullable=False)  
    
    # Coordonnées
    telephone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    
    # Informations académiques
    matricule = db.Column(db.String(50), nullable=True)
    diplome = db.Column(db.String(200), nullable=False)
    annee_diplome = db.Column(db.Integer, nullable=False)
    annee_academique = db.Column(db.String(20), nullable=False, default='2025-2026')
    
    # Informations du père/tuteur
    nom_pere = db.Column(db.String(200), nullable=True)
    profession_pere = db.Column(db.String(100), nullable=True)
    telephone_pere = db.Column(db.String(20), nullable=True)
    ville_residence_pere = db.Column(db.String(100), nullable=True)
    
    # Informations de la mère
    nom_mere = db.Column(db.String(200), nullable=True)
    profession_mere = db.Column(db.String(100), nullable=True)
    telephone_mere = db.Column(db.String(20), nullable=True)
    ville_residence_mere = db.Column(db.String(100), nullable=True)
    
    # Métadonnées
    date_inscription = db.Column(db.DateTime, default=datetime.now) 


    @property
    def nom_complet(self):
        return ' '.join([self.nom, self.prenom])
    
    # @property
    # def nationalite(self):
    #     if hasattr(self, 'departement_origine'):
    #         return self.departement_origine.region.pays.nom
    
    

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
