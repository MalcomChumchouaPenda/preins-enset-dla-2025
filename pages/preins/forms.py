

from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, EmailField
from wtforms.validators import DataRequired


SEXES = [('F', 'Feminin'), ('M', 'Masculin')]
STATUTS = [('C', 'Celibataire'), ('M', 'Marie(e)'), ('V', 'Veuf(ve)')]
LANGUES = [('FR', 'Francais'), ('EN', 'Anglais')]


class InfoForm(FlaskForm):

    # Informations personnelles de base
    nom = StringField(_l('Noms'), validators=[])
    prenom = StringField(_l('Prenoms'))
    date_naissance = StringField(_l('Date de naissance'), validators=[])
    lieu_naissance = StringField(_l('Lieu de naissance'), validators=[])
    sexe = StringField(_l('Sexe'), validators=[])
    situation_matrimoniale = SelectField(_l('Situation Matrimoniale'), validators=[])

    # Origine géographique
    nationalite = StringField(_l('Nationalité'), validators=[])
    region_origine = StringField(_l("Region d'origine"), validators=[])
    departement_origine = StringField(_l("Departement d'origine"), validators=[])
    langue = StringField(_l('Langue'), validators=[])

    # Coordonnées
    telephone = StringField(_l('Téléphone'), validators=[DataRequired()])
    email = EmailField(_l('Email'))
    
    # Informations académiques
    departement_academique = StringField(_l('Departement'), validators=[])
    option = StringField(_l('Option'), validators=[])
    niveau = StringField(_l('Niveau'),  validators=[])
    diplome = StringField(_l("Diplôme d'entrée"), validators=[])
    annee_diplome = IntegerField(_l("Année d'obtention"), validators=[])

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
    

class EditInfoForm(FlaskForm):

    # Informations personnelles de base
    nom = StringField(_l('Noms'), validators=[DataRequired()])
    prenom = StringField(_l('Prenoms'))
    date_naissance = StringField(_l('Date de naissance'), validators=[DataRequired()])
    lieu_naissance = StringField(_l('Lieu de naissance'), validators=[DataRequired()])
    sexe = SelectField(_l('Sexe'), validators=[DataRequired()], choices=SEXES)
    situation_matrimoniale = SelectField(_l('Situation Matrimoniale'), 
                                         validators=[DataRequired()], 
                                         choices=STATUTS)

    # Origine géographique
    nationalite = SelectField(_l('Nationalité'), validators=[DataRequired()])
    region_origine = SelectField(_l("Region d'origine"), validators=[DataRequired()])
    departement_origine_id = SelectField(_l("Departement d'origine"), validators=[DataRequired()])
    langue = SelectField(_l('Langue'), validators=[DataRequired()], choices=LANGUES)

    # Coordonnées
    telephone = StringField(_l('Téléphone'), validators=[DataRequired()])
    email = EmailField(_l('Email'))
    
    # Informations académiques
    departement_academique = StringField(_l('Departement'), validators=[])
    option = StringField(_l('Option'), validators=[])
    niveau = StringField(_l('Niveau'),  validators=[])
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
    niveau_admis = SelectField(_l('Niveau sur le communiqué'))
    niveau_correct = SelectField(_l('Niveau corrigée'))

