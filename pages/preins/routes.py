
import os
import re
import Levenshtein as lv
from datetime import datetime

from flask_login import current_user
from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask import render_template, url_for, redirect, send_file, flash
from flask import request, session, current_app

from core.config import db
from core.utils import UiBlueprint
from services.preins_v0_0 import tasks
from services.preins_v0_0.models import Inscription, Requete
from .forms import InfoForm, ErrorForm, choices


ui = UiBlueprint(__name__)
static_dir = os.path.join(os.path.dirname(__file__), 'static')
temp_dir = os.path.join(static_dir, 'temp')
os.makedirs(temp_dir, exist_ok=True)


@ui.before_request
def prepare_request():
    _clean_temp_files()

@ui.after_request
def cleanup_request(response):
    _clean_temp_files()
    return response


def _clean_temp_files():
    filenames = os.listdir(temp_dir)
    logger = current_app.logger
    logger.debug(f'cleaning temp {len(filenames)} files :')
    for filename in filenames:
        filepath = os.path.join(temp_dir, filename)
        try:
            os.remove(filepath)
            logger.debug(f'clean {filename}')
        except OSError as e:
            logger.warning(e)
            continue


@ui.route('/procedures')
@ui.login_required
def doc():
    nom_fichier = 'procedures_inscription_auditeurs_libres_2025_2026.jpg'
    chemin_doc = os.path.join(static_dir, 'images', 'procedures.jpg')
    return send_file(chemin_doc, as_attachment=True, download_name=nom_fichier)

@ui.route('/')
@ui.roles_accepted('admis')
def info():
    user_id = current_user.id
    inscription = tasks.rechercher_inscription(user_id)
    if inscription is None:
        return redirect(url_for('preins.new_info'))
    return render_template('preins-info.jinja', inscription=inscription)


def _pretraitement_inscription(data):
    # suppression des colonnes inutiles
    data['departement_origine_id'] = data['departement_origine_id'].split('-')[-1]
    inutiles = ['departement_academique', 'option', 'niveau', 'nationalite_id', 
                'region_origine_id', 'csrf_token']
    for name in inutiles:
        data.pop(name)

    # mise en majuscule des colonnes
    col_maj = ['nom', 'prenom', 'lieu_naissance', 'diplome',
               'nom_pere', 'profession_pere', 'residence_pere',
               'nom_mere', 'profession_mere', 'residence_mere']
    for name in col_maj:
        data[name] = data[name].upper()
    return data

def _verification_matricule(admission, data):
    matricule = data['matricule']
    if matricule:
        if admission.classe_id[-1] != '4':
            msg = f"Le matricule '{matricule}' est invalide "
            msg += '(Vous êtes un nouveau étudiant)'
            return False, msg
        elif 'dipet' not in data['diplome'].lower():
            msg = f"Le matricule '{matricule}' est invalide "
            msg += '(Vous êtes un nouveau étudiant)'
            return False, msg
    return True, ''

def _verification_noms(admission, data):
    nom_complet = tasks.former_nom(data['nom'], data['prenom'])
    ratio = lv.ratio(nom_complet, admission.nom_complet)
    if ratio > 0.8:
        return True, ''
    msg = f"Ce compte est reserve a l'etudiant <b>{admission.nom_complet}</b> "
    msg += "(Vous n'etes pas dans votre compte)"
    return False, msg


@ui.route('/new', methods=['GET', 'POST'])
@ui.roles_accepted('admis')
def new_info():
    user_id = current_user.id
    inscription = Inscription() 
    admission = tasks.chercher_admission(user_id)
        
    # create a edit form
    form = InfoForm(obj=inscription)
    form.nationalite_id.choices = choices(tasks.lister_nationalites())
    form.region_origine_id.choices = choices(tasks.lister_regions())
    form.departement_origine_id.choices = choices(tasks.lister_departements())
    
    # traitement et enregistrement des donnees
    # print('\ndata', form.data)
    # print('\nerrors', form.errors)
    # print('\nform', request.form)
    if form.validate_on_submit():
        data = form.data
        valid, msg = _verification_matricule(admission, data)
        if not valid:
            flash(msg, 'warning')
            return redirect(url_for('preins.new_info'))
        
        valid, msg = _verification_noms(admission, data)
        if not valid:
            flash(msg, 'danger')
            return redirect(url_for('preins.new_info'))

        # print('\n', valid, data)
        data['admission_id'] = admission.id
        data = _pretraitement_inscription(data)
        tasks.ajouter_inscription(current_user, data)
        flash('inscription effectue avec succes', 'success')
        return redirect(url_for('preins.info'))

    # fixation des valeurs par defaut
    classe = admission.classe
    form.matricule.data = admission.matricule
    form.departement_academique.data = classe.filiere.departement.nom.upper()
    form.option.data = classe.filiere.nom.upper()
    form.niveau.data = classe.niveau.nom.upper()
    return render_template('preins-info-new.jinja', form=form)


@ui.route('/edit', methods=['GET', 'POST'])
@ui.roles_accepted('admis')
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
    form.nationalite_id.choices = choices(tasks.lister_nationalites())
    form.region_origine_id.choices = choices(tasks.lister_regions())
    form.departement_origine_id.choices = choices(tasks.lister_departements())
    
    # traitement et enregistrement des donnees
    # print('\n', form.data)
    if form.validate_on_submit():
        data = form.data
        data['admission_id'] = admission.id
        data = _pretraitement_inscription(data)
        data.pop('matricule')
        tasks.modifier_inscription(current_user, data) 
        flash('modification effectue avec succes', 'success')
        return redirect(url_for('preins.info'))

    # fixation des valeurs par defaut
    classe = admission.classe
    form.matricule.data = admission.matricule
    departement_origine = inscription.departement_origine
    form.departement_academique.data = classe.filiere.departement.nom.upper()
    form.option.data = classe.filiere.nom.upper()
    form.niveau.data = classe.niveau.nom.upper()
    form.nationalite_id.data = departement_origine.region.pays.full_id
    form.region_origine_id.data = departement_origine.region.full_id
    form.departement_origine_id.data = departement_origine.full_id
    return render_template('preins-info-edit.jinja', form=form)


@ui.route('/print')
@ui.roles_accepted('admis')
def print_info():
    user_id = current_user.id
    inscription = tasks.rechercher_inscription(user_id)
    if inscription is None:
        return redirect(url_for('preins.edit_info'))
    nom_fichier_pdf = f"fiche_inscription_{user_id.lower()}.pdf"
    nom_fichier_pdf = nom_fichier_pdf.replace('-', '_')
    chemin_pdf_final = os.path.join(temp_dir, nom_fichier_pdf)
    fichier_pdf = tasks.generer_fiche_inscription(inscription, chemin_pdf_final)
    return send_file(fichier_pdf, as_attachment=True, download_name=nom_fichier_pdf)


@ui.route('/admin/inscriptions')
@ui.roles_accepted('admin_preins')
def search_infos():
    page = request.args.get('page', 1, type=int)
    query = db.session.query(Inscription)
    query = query.order_by(Inscription.date_inscription.desc())
    records = db.paginate(query, page=page, per_page=15, error_out=False)
    return render_template('preins-search-infos.jinja', records=records)


@ui.route('/admin/inscriptions/<search_id>')
@ui.roles_accepted('admin_preins')
def search_info(search_id):
    previous = request.referrer
    if url_for('preins.search_infos') not in previous:
        previous = url_for('preins.search_infos')
    record = db.session.query(Inscription).filter_by(id=search_id).one()
    if record.modified:
        flash('Cette fiche a ete modifiee!', 'danger')
    return render_template('preins-search-info.jinja', 
                           inscription=record, 
                           previous=previous)

@ui.route('/admin/inscriptions/<search_id>/debug', methods=['GET', 'POST'])
@ui.roles_accepted('admin_preins')
def debug_info(search_id):
    session = db.session
    inscription = session.query(Inscription).filter_by(id=search_id).one()
    form = InfoForm() if request.method == 'POST' else InfoForm(obj=inscription)
    
    # parametrage des options
    form.nationalite_id.choices = choices(tasks.lister_nationalites())
    form.region_origine_id.choices = choices(tasks.lister_regions())
    form.departement_origine_id.choices = choices(tasks.lister_departements())
    
    # traitement et enregistrement des donnees
    # print('\n', form.data)
    previous = request.args.get('previous', url_for('preins.search_infos'))
    if form.validate_on_submit():
        data = form.data
        data['admission_id'] = inscription.admission_id
        data = _pretraitement_inscription(data)
        tasks.corriger_inscription(data) 
        flash('modification effectue avec succes', 'success')
        return redirect(previous)

    # fixation des valeurs par defaut
    admission = inscription.admission
    classe = admission.classe
    form.matricule.data = admission.matricule
    departement_origine = inscription.departement_origine
    form.departement_academique.data = classe.filiere.departement.nom.upper()
    form.option.data = classe.filiere.nom.upper()
    form.niveau.data = classe.niveau.nom.upper()
    form.nationalite_id.data = departement_origine.region.pays.full_id
    form.region_origine_id.data = departement_origine.region.full_id
    form.departement_origine_id.data = departement_origine.full_id
    return render_template('preins-info-debug.jinja', search_id=search_id,  
                           form=form, previous=previous)


@ui.route('/admin/inscriptions/<search_id>/clean')
@ui.roles_accepted('admin_preins')
def clean_info(search_id):
    session = db.session
    record = session.query(Inscription).filter_by(id=search_id).one()
    clean_id = record.admission.id
    session.delete(record)
    session.commit()
    flash(f'Une fiche {clean_id} a ete supprimee', 'success')
    previous = request.args.get('previous')
    if previous:
        return redirect(previous)
    return redirect(url_for('preins.search_infos'))


@ui.route('/coming-soon')
@ui.login_required
def coming():
    return render_template('dashboard/coming-soon.jinja',
                           deadline=datetime(2025, 10, 30),
                           page_id="preins_error_pg")


@ui.route('/requete')
@ui.roles_accepted('admis')
def error():
    user_id = current_user.id
    requete = tasks.rechercher_requete(user_id)
    if requete is None:
        return redirect(url_for('preins.new_error'))
    return render_template('preins-error.jinja', requete=requete)


@ui.route('/requete/new', methods=['GET', 'POST'])
@ui.roles_accepted('admis')
def new_error():
    user_id = current_user.id
    requete = Requete() 
    admission = tasks.chercher_admission(user_id)       
    if tasks.rechercher_inscription(user_id) is None:
        flash("Vous devez d'abord vous inscrire", "warning")
        return redirect(url_for('preins.edit_info'))
    
    # create a edit form
    form = ErrorForm(obj=requete)
    form.filiere_correct_id.choices = choices(tasks.lister_filieres())
    form.niveau_correct_id.choices = choices(tasks.lister_niveaux())
    
    # traitement et enregistrement des donnees
    # print('\n', form.data)
    if form.validate_on_submit():
        data = form.data
        data['admission_id'] = admission.id
        inutiles = ['nom_admis', 'filiere_admis', 
                    'niveau_admis', 'csrf_token']
        for name in inutiles:
            data.pop(name)
        tasks.ajouter_requete(data)
        flash('Requete cree avec succes', 'success')
        return redirect(url_for('preins.error'))

    # fixation des valeurs par defaut
    classe = admission.classe
    form.nom_admis.data = admission.nom_complet.upper()
    form.filiere_admis.data = classe.filiere.nom.upper()
    form.niveau_admis.data = classe.niveau.nom.upper()
    return render_template('preins-error-new.jinja', form=form)


@ui.route('requete/edit', methods=['GET', 'POST'])
@ui.roles_accepted('admis')
def edit_error():
    user_id = current_user.id
    requete = tasks.rechercher_requete(user_id)
    if requete is None:
        return redirect(url_for('preins.new_error'))
    
    # creation du formulaire avce controle des modifications
    admission = requete.admission
    if request.method == 'POST':
        form = ErrorForm()
    else:
        count_max = admission.max_requetes
        count = len(admission.requetes)
        if count > count_max:
            flash(f'Vous ne pouvez modifier cette requete plus de {count_max} fois', 'danger')
            return redirect(url_for('preins.error'))
        flash(f'Vous pourrez encore modifier cette requete {count_max-count+1} fois', 'warning')
        form = ErrorForm(obj=requete)
    
    # parametrage des options
    form.filiere_correct_id.choices = choices(tasks.lister_filieres())
    form.niveau_correct_id.choices = choices(tasks.lister_niveaux())
    
    # traitement et enregistrement des donnees
    # print('\n', form.data)
    if form.validate_on_submit():
        data = form.data
        data['admission_id'] = admission.id
        inutiles = ['nom_admis', 'filiere_admis'
                    'niveau_admis', 'csrf_token']
        for name in inutiles:
            data.pop(name)
        tasks.ajouter_requete(data)
        flash('Requete modifiee avec succes', 'success')
        return redirect(url_for('preins.error'))

    # fixation des valeurs par defaut
    classe = admission.classe
    form.nom_admis.data = admission.nom_complet.upper()
    form.filiere_admis.data = classe.filiere.nom.upper()
    form.niveau_admis.data = classe.niveau.nom.upper()
    return render_template('preins-error-edit.jinja', form=form)


@ui.route('/requete/print')
@ui.roles_accepted('admis')
def print_error():
    user_id = current_user.id
    inscription = tasks.rechercher_inscription(user_id)
    requete = tasks.rechercher_requete(user_id)
    if requete is None:
        return redirect(url_for('preins.new_error')) 

    nom_fichier_pdf = f"requete_correction_{user_id.lower()}.pdf"
    nom_fichier_pdf = nom_fichier_pdf.replace('-', '_')
    chemin_pdf_final = os.path.join(temp_dir, nom_fichier_pdf)
    fichier_pdf = tasks.generer_fiche_correction(requete, inscription, chemin_pdf_final)
    return send_file(fichier_pdf, as_attachment=True, download_name=nom_fichier_pdf)

