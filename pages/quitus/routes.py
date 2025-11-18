
import os
import re
import json
import csv
from io import StringIO
from datetime import datetime

import Levenshtein as lv
from flask_login import current_user
from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask import render_template, url_for, redirect, send_file, flash
from flask import request, session, current_app
from sqlalchemy import or_, and_

from core.config import db
from core.utils import UiBlueprint
from services.preins_v0_0 import models as pmdl
from services.formations_v0_0 import models as fmdl
# from services.preins_v0_0.models import Inscription, Requete


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


@ui.route('/')
@ui.route('/files')
def files():
    return render_template('quitus-files.jinja')


def _verification_matricule(admission, inscription):
    matricule = admission.matricule
    if not matricule:
        return False
    return True

def _verification_noms(admission, inscription):
    nom1 = admission.nom_complet.upper()
    nom2 = inscription.nom_complet.upper()
    ratio = lv.ratio(nom1, nom2)
    print('\t', ratio, nom1, nom2)
    return ratio >= 0.65


@ui.route('/download-quitus')
@ui.roles_accepted('admin_quitus')
def download_quitus():
    num_inscr = 0
    session = db.session
    inscriptions = session.query(pmdl.Inscription).all()
    output_name = 'etudiants.csv'
    output_path = os.path.join(temp_dir, output_name)
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['matricule', 'nom', 'prenom', 'date_naiss', 
                         'lieu_naiss', 'sexe', 'situation_mat', 'pays',
                         'region', 'dept_orig', 'dept_acad', 'filiere',
                         'etape_inscr', 'etape_paiement', 'formation', 
                         'niveau', 'langue', 'annee_acad', 'date_inscr'])
        for inscr in inscriptions:
            if inscr.modified:
                continue
            admission = inscr.admission
            if not _verification_matricule(admission, inscr):
                continue
            if not _verification_noms(admission, inscr):
                continue
            classe = admission.classe 
            departement = inscr.departement_origine
            writer.writerow([admission.matricule, 
                             inscr.nom.upper(), 
                             inscr.prenom.upper() if inscr.prenom else " ",
                             inscr.date_naissance.strftime('="%Y-%m-%d"'),
                             inscr.lieu_naissance.upper(), 
                             inscr.sexe_id, 
                             'c',
                             departement.region.pays.code_udo,
                             departement.region.code_udo,
                             departement.code_udo,
                             classe.filiere.departement_id,
                             classe.filiere.code_udo,
                             classe.id,
                             admission.classe_paiement,
                             classe.filiere.formation.code_systhag,
                             classe.niveau.code_cycle,
                             inscr.langue_id.lower(),
                             admission.communique.annee_academique,
                             inscr.date_inscription.strftime('="%Y-%m-%d %H:%M:%S"')])
            num_inscr += 1
    flash(f'{num_inscr} quitus telecharge et a generer', 'success')
    return send_file(output_path,
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='quitus_a_generer.csv')
