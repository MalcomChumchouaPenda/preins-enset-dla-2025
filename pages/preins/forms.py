

from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, EmailField
from wtforms.validators import DataRequired
from services.preins_v0_0.models import SEXES, SITUATIONS, LANGUES


def choices(data):
    items = sorted([(k,v) for k,v in data.items()])
    items.insert(0, ('', 'Choisir...'))
    return items

def validators1():
    return [DataRequired()]


class InfoForm(FlaskForm):

    # Informations personnelles de base
    nom = StringField(_l('Noms'), validators=validators1())
    prenom = StringField(_l('Prenoms'))
    date_naissance = StringField(_l('Date de naissance'), validators=validators1())
    lieu_naissance = StringField(_l('Lieu de naissance'), validators=validators1())
    sexe_id = SelectField(_l('Sexe'), validators=validators1(), choices=choices(SEXES))
    situation_matrimoniale_id = SelectField(_l('Situation Matrimoniale'), 
                                            validators=validators1(), 
                                            choices=choices(SITUATIONS))

    # Origine géographique
    nationalite_id = SelectField(_l('Nationalité'), validators=validators1())    
    region_origine_id = SelectField(_l("Region d'origine"), validators=validators1())    
    departement_origine_id = SelectField(_l("Departement d'origine"), validators=validators1())    
    langue_id = SelectField(_l('Langue'), validators=validators1(), choices=choices(LANGUES))

    # Coordonnées
    telephone = StringField(_l('Téléphone'), validators=validators1())    
    email = EmailField(_l('Email'))
    
    # Informations académiques
    departement_academique = StringField(_l('Departement'))
    option = StringField(_l('Option'))
    niveau = StringField(_l('Niveau'))
    diplome = StringField(_l("Diplôme d'entrée"), validators=validators1())
    annee_diplome = IntegerField(_l("Année d'obtention"), validators=validators1())

    # Informations du père/tuteur
    nom_pere = StringField(_l('Nom du pere'))
    profession_pere = StringField(_l('Profession du pere'))
    telephone_pere = StringField(_l('Téléphone du pere'))
    residence_pere = StringField(_l('Residence du pere'))

    # Informations de la mère
    nom_mere = StringField(_l('Nom de la mere'))
    profession_mere = StringField(_l('Profession de la mere'))
    telephone_mere = StringField(_l('Téléphone de la mere'))
    residence_mere = StringField(_l('Residence de la mere'))
    

class ErrorForm(FlaskForm):

    nom_admis = StringField(_l('Noms sur le communiqué'))
    nom_correct = StringField(_l('Noms corrigés'))
    prenom_admis = StringField(_l('Prénoms sur le communiqué'))
    prenom_correct = StringField(_l('Prénoms corrigés'))

    option_admis = SelectField(_l('Option sur le communiqué'))
    option_correct = SelectField(_l('Option corrigée'))
    niveau_admis = SelectField(_l('Niveau sur le communiqué'))
    niveau_correct = SelectField(_l('Niveau corrigée'))

