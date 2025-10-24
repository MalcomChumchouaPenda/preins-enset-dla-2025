
import os
import re
from datetime import datetime

from flask_login import current_user
from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask import render_template, request, url_for, redirect, send_file, flash

from core.utils import UiBlueprint
from services.preins_v0_0 import tasks
from services.preins_v0_0.models import Inscription, Requete
from services.formations_v0_0 import tasks as format_tasks
from .forms import InfoForm, ErrorForm


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
        return redirect(url_for('preins.new_info'))
    return render_template('preins-view-form.jinja', inscription=inscription)


@ui.route('/new', methods=['GET', 'POST'])
@ui.login_required
def new_info():
    user_id = current_user.id
    inscription = Inscription() 
    admission = tasks.chercher_admission(user_id)
        
    # create a edit form
    form = InfoForm(obj=inscription)
    form.nationalite_id.choices = tasks.lister_nationalites()
    form.region_origine_id.choices = tasks.lister_regions()
    form.departement_origine_id.choices = tasks.lister_departements()
    
    # traitement et enregistrement des donnees
    # print('\n', form.data)
    if form.validate_on_submit():
        data = form.data
        data['admission_id'] = admission.id
        data['departement_origine_id'] = data['departement_origine_id'].split('-')[-1]
        inutiles = ['departement_academique', 'option', 'niveau', 
                    'nationalite_id', 'region_origine_id', 
                    'csrf_token']
        for name in inutiles:
            data.pop(name)
        tasks.ajouter_inscription(data)
        flash('inscription effectue avec succes', 'success')
        return redirect(url_for('preins.info'))

    # fixation des valeurs par defaut
    classe = admission.classe
    form.departement_academique.data = classe.filiere.departement.nom.upper()
    form.option.data = classe.filiere.nom
    form.niveau.data = classe.niveau.nom
    return render_template('preins-new-form.jinja', form=form)


@ui.route('/edit', methods=['GET', 'POST'])
@ui.login_required
def edit_info():
    user_id = current_user.id
    inscription = tasks.rechercher_inscription(user_id)
    if inscription is None:
        return redirect(url_for('preins.new_info'))
    
    # creation du formulaire avce controle des modifications
    admission = inscription.admission
    if request.method == 'POST':
        form = InfoForm()
    else:
        count_max = admission.max_inscriptions
        count = len(admission.inscriptions)
        if count > count_max:
            flash(f'Vous ne pouvez modifier cette fiche plus de {count_max} fois', 'danger')
            return redirect(url_for('preins.info'))
        flash(f'Vous pourrez encore modifier cette fiche {count_max-count+1} fois', 'warning')
        form = InfoForm(obj=inscription)
    
    # parametrage des options
    form.nationalite_id.choices = tasks.lister_nationalites()
    form.region_origine_id.choices = tasks.lister_regions()
    form.departement_origine_id.choices = tasks.lister_departements()
    
    # traitement et enregistrement des donnees
    print('\n', form.data)
    if form.validate_on_submit():
        data = form.data
        data['admission_id'] = admission.id
        data['departement_origine_id'] = data['departement_origine_id'].split('-')[-1]
        inutiles = ['departement_academique', 'option', 'niveau', 
                    'nationalite_id', 'region_origine_id', 
                    'csrf_token']
        for name in inutiles:
            data.pop(name)
        tasks.modifier_inscription(data)
        flash('modification effectue avec succes', 'success')
        return redirect(url_for('preins.info'))

    # fixation des valeurs par defaut
    classe = admission.classe
    departement_origine = inscription.departement_origine
    form.departement_academique.data = classe.filiere.departement.nom.upper()
    form.option.data = classe.filiere.nom
    form.niveau.data = classe.niveau.nom
    form.nationalite_id.data = departement_origine.region.pays.full_id
    form.region_origine_id.data = departement_origine.region.full_id
    form.departement_origine_id.data = departement_origine.full_id
    return render_template('preins-edit-form.jinja', form=form)


@ui.route('/print')
@ui.login_required
def print_info():
    user_id = current_user.id
    inscription = tasks.rechercher_inscription(user_id)
    if inscription is None:
        return redirect(url_for('preins.edit_info'))
    nom_fichier_pdf = f"fiche_inscription_{user_id.lower()}.pdf"
    chemin_pdf_final = os.path.join(temp_dir, nom_fichier_pdf)
    fichier_pdf = tasks.generer_fiche_inscription(inscription, chemin_pdf_final)
    return send_file(fichier_pdf, as_attachment=True, download_name=nom_fichier_pdf)


@ui.route('/coming-soon')
@ui.login_required
def coming():
    return render_template('dashboard/coming-soon.jinja',
                           deadline=datetime(2025, 10, 30),
                           page_id="preins_error_pg")


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
