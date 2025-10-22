from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    
    # Informations personnelles de base
    nationalite = db.Column(db.String(100), nullable=False)
    nom_prenom = db.Column(db.String(200), nullable=False)
    date_naissance = db.Column(db.String(20), nullable=False)
    lieu_naissance = db.Column(db.String(100), nullable=False)
    sexe = db.Column(db.String(10), nullable=False)  
    situation_matrimoniale = db.Column(db.String(50), nullable=False)
    
    # Origine géographique
    region_origine = db.Column(db.String(100), nullable=False)
    departement_origine = db.Column(db.String(100), nullable=False)
    
    # Coordonnées
    telephone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    langue = db.Column(db.String(10), nullable=False)  
    
    # Informations académiques
    matricule = db.Column(db.String(50), unique=True, nullable=True)
    departement = db.Column(db.String(100), nullable=False)
    option = db.Column(db.String(100), nullable=False)
    niveau = db.Column(db.String(10), nullable=False)
    diplome = db.Column(db.String(200), nullable=False)
    annee_diplome = db.Column(db.Integer, nullable=False)
    annee_academique = db.Column(db.String(20), nullable=False, default='2025-2026')
    
    # Informations du père/tuteur
    nom_pere = db.Column(db.String(200), nullable=False)
    profession_pere = db.Column(db.String(100), nullable=False)
    telephone_pere = db.Column(db.String(20), nullable=False)
    ville_residence_pere = db.Column(db.String(100), nullable=False)
    
    # Informations de la mère
    nom_mere = db.Column(db.String(200), nullable=False)
    profession_mere = db.Column(db.String(100), nullable=False)
    telephone_mere = db.Column(db.String(20), nullable=False)
    ville_residence_mere = db.Column(db.String(100), nullable=False)
    
    # Fichiers
    photo_filename = db.Column(db.String(200), nullable=True)
    pdf_filename = db.Column(db.String(200), nullable=True)
    
    # Métadonnées
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)  
