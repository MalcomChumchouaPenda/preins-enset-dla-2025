

from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, EmailField
from wtforms.validators import DataRequired
from . import choices


class InfoForm(FlaskForm):

    # Informations personnelles de base
    nom = StringField(_l('Noms'), validators=[DataRequired()])
    prenom = StringField(_l('Prenoms'))
    date_naissance = StringField(_l('Date de naissance'), validators=[DataRequired()])
    lieu_naissance = StringField(_l('Lieu de naissance'), validators=[DataRequired()])
    sexe = SelectField(_l('Sexe'), validators=[DataRequired()], choices=choices.SEXES)
    situation_matrimoniale = SelectField(_l('Situation Matrimoniale'), validators=[DataRequired()], 
                                        choices=choices.STATUTS)

    # Origine géographique
    nationalite = SelectField(_l('Nationalité'), validators=[DataRequired()], choices=choices.NATIONALITE)
    region_origine = SelectField(_l("Region d'origine"), validators=[DataRequired()])
    departement_origine = SelectField(_l("Departement d'origine"), validators=[DataRequired()])
    langue = SelectField(_l('Langue'), validators=[DataRequired()], choices=choices.LANGUES)

    # Coordonnées
    telephone = StringField(_l('Téléphone'), validators=[DataRequired()])
    email = EmailField(_l('Email'))
    
    # Informations académiques
    departement = SelectField(_l('Departement'), validators=[DataRequired()])
    option = SelectField(_l('Option'), validators=[DataRequired()])
    niveau = SelectField(_l('Niveau'),  validators=[DataRequired()], choices=choices.NIVEAUX)
    diplome = StringField(_l("Diplôme d'entrée"), validators=[DataRequired()])
    annee_diplome = IntegerField(_l("Année d'obtention"), validators=[DataRequired()])

    # Informations du père/tuteur
    nom_pere = StringField(_l('Nom du pere'))
    profession_pere = StringField(_l('Profession du pere'))
    telephone_pere = StringField(_l('Téléphone du pere'))
    ville_residence_pere = StringField(_l('Residence du pere'))

    # Informations de la mère
    nom_mere = StringField(_l('Nom de la mere'))
    profession_mere = StringField(_l('Profession de la mere'))
    telephone_mere = StringField(_l('Téléphone de la mere'))
    ville_residence_mere = StringField(_l('Residence de la mere'))
    

class ErrorForm(FlaskForm):

    nom_admis = StringField(_l('Noms sur le communiqué'))
    nom_correct = StringField(_l('Noms corrigés'))
    prenom_admis = StringField(_l('Prénoms sur le communiqué'))
    prenom_correct = StringField(_l('Prénoms corrigés'))

    option_admis = SelectField(_l('Option sur le communiqué'))
    option_correct = SelectField(_l('Option corrigée'))
    niveau_admis = SelectField(_l('Niveau sur le communiqué'), choices=choices.NIVEAUX)
    niveau_correct = SelectField(_l('Niveau corrigée'), choices=choices.NIVEAUX)

