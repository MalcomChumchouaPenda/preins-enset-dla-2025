
import os
from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask import render_template, request, url_for, redirect
from core.utils import UiBlueprint
from core.config import db
from . import choices
from .forms import InfoForm, ErrorForm
from services.preins_v0_0 import tasks
from services.preins_v0_0.models import Preinscription, Requete


ui = UiBlueprint(__name__)
static_dir = os.path.join(os.path.dirname(__file__), 'static')


@ui.route('/', methods=['GET', 'POST'])
def info():
    next = request.args.get('next')
    obj = Preinscription()
    form = InfoForm(obj=obj)
    print(form.errors)
    if form.validate_on_submit():
        new = form.data
        new.pop('csrf_token')
        print('\nnew\n', new)
        return render_template('preins-home-page.jinja')
    return render_template('preins-info.jinja', form=form, next=next)


@ui.route('/requete', methods=['GET', 'POST'])
def error():
    next = request.args.get('next')
    obj = Requete()
    form = ErrorForm(obj=obj)
    form.option_admis.choices = choices.options()
    form.option_correct.choices = choices.options()
    return render_template('preins-error.jinja', form=form, next=next)


