
import os
import re
from flask_login import current_user
from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask import render_template, request, url_for, redirect, send_file
from core.utils import UiBlueprint
from core.config import db
from .forms import InfoForm, ErrorForm
from services.preins_v0_0 import tasks
from services.preins_v0_0.models import Preinscription, Requete
from services.formations_v0_0 import tasks as format_tasks
from services.formations_v0_0.models import Classe


ui = UiBlueprint(__name__)
static_dir = os.path.join(os.path.dirname(__file__), 'static')
temp_dir = os.path.join(static_dir, 'temp')
os.makedirs(temp_dir, exist_ok=True)


@ui.route('/', methods=['GET', 'POST'])
@ui.login_required
def info():
    next = request.args.get('next')
    obj = Preinscription()
    form = InfoForm(obj=obj)
    form.nationalite.choices = tasks.lister_nationalites()
    form.region_origine.choices = tasks.lister_regions()
    form.departement_origine_id.choices = tasks.lister_departements()

    # print('\n', form.data)
    admission = tasks.chercher_admission(current_user.id)
    if form.validate_on_submit():
        data = form.data

        # traitement et enregistrement des donnees
        data['admission_id'] = admission.id
        data['matricule'] = 'test'
        data['departement_origine_id'] = data['departement_origine_id'].split('-')[-1]
        inutiles = ['departement_academique', 'option', 'niveau', 
                    'nationalite', 'region_origine', 'csrf_token']
        for name in inutiles:
            data.pop(name)
        inscription = tasks.enregistrer_inscription(data)

        identifiant = current_user.id.lower()
        nom_fichier_pdf = f"fiche_inscription_{identifiant}.pdf"
        chemin_pdf_final = os.path.join(temp_dir, nom_fichier_pdf)
        fichier_pdf = tasks.generer_fiche_inscription(inscription, chemin_pdf_final)
        return send_file(fichier_pdf, as_attachment=True, download_name=nom_fichier_pdf)
    
    # recherche de la classe
    query = db.session.query(Classe)
    query = query.filter_by(id=admission.classe_id)
    classe = query.one_or_none()

    # fixation des valeurs par defaut
    form.departement_academique.data = classe.filiere.departement.nom.upper()
    form.option.data = classe.filiere.nom
    form.niveau.data = classe.niveau.nom
    return render_template('preins-info.jinja', form=form, next=next)


@ui.route('/requete', methods=['GET', 'POST'])
@ui.login_required
def error():
    next = request.args.get('next')
    obj = Requete()
    form = ErrorForm(obj=obj)
    niveaux = format_tasks.list_niveaux()
    filieres = format_tasks.list_filieres()
    form.option_admis.choices = filieres
    form.option_correct.choices = filieres
    form.niveau_admis.choices = niveaux
    form.niveau_correct.choices = niveaux
    if form.validate_on_submit():
        data = form.data
        data.pop('csrf_token')
        # if data['nom_correct'] or data['prenom_correct']:
        #     nom_complet_errone = former_nom(data['nom_admis'], data['prenom_admis'])
        #     if not data['nom_admis']
        identifiant = current_user.id.replace(' ', '_').lower()
        nom_fichier_pdf = f"fiche_correction_{identifiant}.pdf"
        chemin_pdf_final = os.path.join(temp_dir, nom_fichier_pdf)
        fichier_pdf = tasks.generer_fiche_correction(data, chemin_pdf_final)
        return send_file(fichier_pdf, as_attachment=True, download_name=nom_fichier_pdf)
    return render_template('preins-error.jinja', form=form, next=next)


def former_nom(nom, prenom=''):
    resultat = ' '.join([nom, prenom])
    return nettoyer_nom(resultat)

def nettoyer_nom(nom):
    nom = re.sub('\s+', ' ', nom)
    nom = nom.strip()
    nom = nom.upper()
    return nom
