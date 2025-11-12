
import os
import csv
import json
import random
from datetime import datetime
from core.config import db
from core.utils import Stat, Alert
from core.auth.tasks import add_role, add_user, add_roles_to_user
from .models import Admission, Inscription, CommuniqueAdmission, Requete
from .tasks import upload_communiques, upload_admissions, upload_inscriptions, upload_requetes



def init_stats(user):
    stats = []
    if user.has_role('developper'):
        stats.extend([
            Stat('Inscriptions', 'Nombre', value='142', rank=0),
        ])
    return stats


def init_alerts(user):
    alerts = []
    if user.has_role('developper'):
        alerts.extend([
            Alert('Vos quitus ont ete generes', 'PC Portable Dell XPS 15 - Il y a 15 minutes', icon='bi bi-laptop', priority=1),
        ])
    return alerts


def init_data():
    session = db.session
    add_role(session, 'admis', 'Etudiants admis')
    add_role(session, 'admin_preins', 'Gestionnaire Inscription')
    add_roles_to_user(session, 'dev1', 'admin_preins')
    upload_communiques(session, 'communiques_demo.csv', sep=';')
    upload_admissions(session, 'admissions_demo.csv', sep=';')
    upload_inscriptions(session, 'inscriptions_demo.csv', sep=',')
    upload_requetes(session, 'requetes_demo.csv', sep=';')
    
