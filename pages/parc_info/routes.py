import os
from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask import render_template, request, url_for, redirect
from core.utils import (
    UiBlueprint, 
    read_json, 
    read_markdown, 
    paginate_items, 
    default_deadline,
    get_locale
)


ui = UiBlueprint(__name__)


@ui.route('/equipements')
def equipements():
    return render_template('equipement.jinja')

@ui.route('/mouvements')
def mouvements():
    return render_template('mouvement.jinja')

@ui.route('/interventions')
def interventions():
    return render_template('intervention.jinja')

@ui.route('/rapports')
def rapports():
    return render_template('rapports.jinja')

@ui.route('/tickets')
def tickets():
    return render_template('tickets.jinja')

