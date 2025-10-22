
from datetime import datetime
from core.config import db

    
class Preinscription(db.Model):
    __bind_key__ = 'preins_v0'
    __tablename__ = 'preinscriptions'
    id = db.Column(db.Integer, primary_key=True)
    
    # Informations personnelles de base
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=True)
    date_naissance = db.Column(db.String(20), nullable=False)
    lieu_naissance = db.Column(db.String(100), nullable=False)
    sexe = db.Column(db.String(10), nullable=False)  
    situation_matrimoniale = db.Column(db.String(50), nullable=False)
    
    # Origine géographique
    nationalite = db.Column(db.String(100), nullable=False)
    region_origine = db.Column(db.String(100), nullable=False)
    departement_origine = db.Column(db.String(100), nullable=False)
    langue = db.Column(db.String(10), nullable=False)  
    
    # Coordonnées
    telephone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    
    # Informations académiques
    matricule = db.Column(db.String(50), unique=True, nullable=True)
    departement = db.Column(db.String(100), nullable=False)
    option = db.Column(db.String(100), nullable=False)
    niveau = db.Column(db.String(10), nullable=False)
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
    
    # Fichiers
    photo_filename = db.Column(db.String(200), nullable=True)
    pdf_filename = db.Column(db.String(200), nullable=True)
    
    # Métadonnées
    date_inscription = db.Column(db.DateTime, default=datetime.now)  


class Requete(db.Model):
    __bind_key__ = 'preins_v0'
    __tablename__ = 'requetes'
    id = db.Column(db.Integer, primary_key=True)

    # erreur d'identite
    nom_admis = db.Column(db.String(200), nullable=False)
    nom_correct = db.Column(db.String(200), nullable=False)
    prenom_admis = db.Column(db.String(200), nullable=True)
    prenom_correct = db.Column(db.String(200), nullable=True)

    # erreur de filiere
    option_admis = db.Column(db.String(100), nullable=False)
    option_correct = db.Column(db.String(100), nullable=False)
    niveau_admis = db.Column(db.String(10), nullable=False)
    niveau_correct = db.Column(db.String(10), nullable=False)
