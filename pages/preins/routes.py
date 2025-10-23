
import os
import re
from flask_login import current_user
from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask import render_template, request, url_for, redirect, send_file
from core.utils import UiBlueprint
from core.config import db
from .forms import InfoForm, EditInfoForm, ErrorForm
from services.preins_v0_0 import tasks
from services.preins_v0_0.models import Preinscription, Requete
from services.formations_v0_0 import tasks as format_tasks
from services.formations_v0_0.models import Classe


ui = UiBlueprint(__name__)
static_dir = os.path.join(os.path.dirname(__file__), 'static')
temp_dir = os.path.join(static_dir, 'temp')
os.makedirs(temp_dir, exist_ok=True)


@ui.route('/')
@ui.login_required
def info():
    user_id = current_user.id
    inscription = tasks.rechercher_inscription(user_id)
    if inscription is None:
        return redirect(url_for('preins.edit_info'))
    
    departement_origine = inscription.departement_origine
    classe = inscription.admission.classe
    form = InfoForm(obj=inscription)    
    form.nationalite.data = departement_origine.region.pays.nom
    form.region_origine.data = departement_origine.region.nom
    form.departement_origine.data = departement_origine.nom
    form.departement_academique.data = classe.filiere.departement.nom.upper()
    form.option.data = classe.filiere.nom
    form.niveau.data = classe.niveau.nom
    return render_template('preins-info.jinja', form=form)


@ui.route('/edit', methods=['GET', 'POST'])
@ui.login_required
def edit_info():
    next = request.args.get('next')
    obj = Preinscription()
    form = EditInfoForm(obj=obj)
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
        tasks.enregistrer_inscription(data)
        return redirect(url_for('preins.info'))

    # fixation des valeurs par defaut
    classe = admission.classe
    form.departement_academique.data = classe.filiere.departement.nom.upper()
    form.option.data = classe.filiere.nom
    form.niveau.data = classe.niveau.nom
    return render_template('preins-info-edit.jinja', form=form, next=next)


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
