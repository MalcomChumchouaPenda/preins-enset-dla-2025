
from core.config import db
from core.utils import Stat, Alert
from core.auth.tasks import add_role, add_user, add_roles_to_user
from .models import Admission, Preinscription


def init_stats(user):
    stats = []
    if user.has_role('developper'):
        stats.extend([
            Stat('Preinscriptions', 'Nombre', value='142', rank=0),
        ])
    return stats


def init_alerts(user):
    alerts = []
    if user.has_role('developper'):
        alerts.extend([
            Alert('Vos quitus ont ete generes', 'PC Portable Dell XPS 15 - Il y a 15 minutes', icon='bi bi-laptop', priority=1),
        ])
    return alerts


admission_data = [
    dict(id='BTP1-25AA-001', nom_complet='Demo Admis 01', 
         classe_id='BTP1', statut='AA', communique_id='Fake'),
    dict(id='BTP1-25AP-002', nom_complet='Demo Admis 02', 
         classe_id='BTP1', statut='AA', communique_id='Fake'),
]

preins_data = {
    'admission_id': 'BTP1-25AA-001',
    'matricule': '25NBT001A',
    'nom': 'Fotso Epoh Atangana Mahamat',
    'prenom': 'Moussa Jean-Marie-Luc',
    'date_naissance': '05/05/1985',
    'lieu_naissance': 'Makenene-Garoua-Sangmelima',
    'sexe': 'F',
    'situation_matrimoniale': 'C',
    'departement_origine_id': 'dep4',
    'telephone': '678995966 / 566899 222',
    'email': 'fotso-epoh-atangana-mahamat@yahoo.cm',
    'langue': 'FR',
    'diplome': 'Baccalaureat A4 Allemand',
    'annee_diplome': '2025',
    'nom_pere': 'Fotso Epoh Atangana Mahamat Luc',
    'profession_pere': 'Agriculteur, pecheur, ecrivain',
    'telephone_pere': '6 75 75 75 / 6 99 98 98 98',
    'residence_pere': 'Makenene-Garoua-Sangmelima',
    'nom_mere': 'Ngo Nyemb Nana Epse Hamidou',
    'profession_mere': "Cadre contractuelle d'administration",
    'telephone_mere': '6 20 20 20',
    'residence_mere': 'Makenene-Garoua-Sangmelima'
}

def init_data():
    # creation du role admis
    session = db.session
    add_role(session, 'admis', 'Etudiants admis')

    # creation des users et admissions
    for row in admission_data:
        add_user(session, row['id'], row['nom_complet'], '0000')
        add_roles_to_user(session, row['id'], 'student', 'developper', 'admis')
        session.merge(Admission(**row))
    session.commit()

    # creation d'une inscription
    session.merge(Preinscription(**preins_data))
    session.commit()

    
