
import os
from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask import render_template, request, url_for, redirect, send_file
from core.utils import UiBlueprint
from core.config import db
from . import choices
from .forms import InfoForm, ErrorForm
from services.preins_v0_0.tasks import generer_fiche_inscription, generer_fiche_correction
from services.preins_v0_0.models import Preinscription, Requete


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
    form.region_origine.choices = [('A', 'Option A'), ('B', 'Option B')]
    form.departement_origine.choices = [('A', 'Option A'), ('B', 'Option B')]
    form.departement.choices = [('A', 'Option A'), ('B', 'Option B')]
    form.option.choices = [('A', 'Option A'), ('B', 'Option B')]
    if form.validate_on_submit():
        data = form.data
        data.pop('csrf_token')
        nom_etud = data['nom'].replace(' ', '_').lower()
        nom_fichier_pdf = f"fiche_inscription_{nom_etud}.pdf"
        chemin_pdf_final = os.path.join(temp_dir, nom_fichier_pdf)
        fichier_pdf = generer_fiche_inscription(data, chemin_pdf_final)
        return send_file(fichier_pdf, as_attachment=True, download_name=nom_fichier_pdf)
    return render_template('preins-info.jinja', form=form, next=next)


@ui.route('/requete', methods=['GET', 'POST'])
def error():
    next = request.args.get('next')
    obj = Requete()
    form = ErrorForm(obj=obj)
    form.option_admis.choices = choices.options()
    form.option_correct.choices = choices.options()
    if form.validate_on_submit():
        data = form.data
        data.pop('csrf_token')
        nom_etud = data['nom'].replace(' ', '_').lower()
        nom_fichier_pdf = f"fiche_correction_{nom_etud}.pdf"
        # dossier_destination = os.path.join(static_dir, 'temp')
        # os.makedirs(dossier_destination, exist_ok=True)
        # chemin_pdf_final = os.path.join(dossier_destination, nom_fichier_pdf)
        # fichier_pdf = generer_fiche_correction(data, chemin_pdf_final)
        # print('\ndata\n', data)
        # return send_file(fichier_pdf, as_attachment=True, download_name=os.path.basename(fichier_pdf))
        fichier = generer_fiche_inscription(data)
        return send_file(fichier, as_attachment=True, download_name=nom_fichier_pdf)
    return render_template('preins-error.jinja', form=form, next=next)


