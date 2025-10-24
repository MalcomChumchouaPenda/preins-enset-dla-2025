
import random
from core.config import db
from core.utils import Stat, Alert
from core.auth.tasks import add_role, add_user, add_roles_to_user
from .models import Admission, Inscription, CommuniqueAdmission


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
    # creation du role admis
    session = db.session
    add_role(session, 'admis', 'Etudiants admis')

    # creation des communiques
    communique = CommuniqueAdmission(id="Fake")
    communique.numero = '001/Fake/ du 12/05/2006'
    communique.objet = 'Portant admission des candidats tests'
    communique.annee_academique = '2025/2026'
    session.add(communique)
    session.commit()

    # creation des users et admissions
    admissions = {}
    for i in range(1, 10):
        for n in 'AP':
            id = f'BTP1-25A{n}-00{i}'
            nom = f'Admis Liste {n} numero {i}'
            classe_id = 'BTP1'
            statut = 'A' + n
            communique_id = 'Fake'
            add_user(session, id, nom, '0000')
            add_roles_to_user(session, id, 'student', 'admis')
            admission = Admission(id=id, nom_complet=nom, statut=statut,
                                  classe_id=classe_id, communique_id=communique_id)
            admissions[id] = admission
            session.add(admission)
    session.commit()

    # creation des inscriptions
    for i in range(1, 5):
        data = {
            'admission_id': f'BTP1-25AA-00{i}',
            'nom': f'Nom Admis {i}',
            'prenom': f'Prenom Admis {i}',
            'date_naissance': f'01/01/200{i}',
            'lieu_naissance': f'Maternite de la ville {i}',
            'sexe_id': random.choice(['F', 'M']),
            'situation_matrimoniale_id': random.choice(['C', 'M']),
            'departement_origine_id': 'dep4',
            'telephone': f'6 70 70 90 9{i}',
            'email': f'admis_demo{i}@yahoo.cm',
            'langue_id': random.choice(['FR', 'EN']),
            'diplome': f'Diplome demo type {i}',
            'annee_diplome': f'201{i}',
            'nom_pere': 'Fotso Epoh Atangana Mahamat Luc',
            'profession_pere': 'Agriculteur, pecheur, ecrivain',
            'telephone_pere': '6 75 75 75 / 6 99 98 98 98',
            'residence_pere': 'Makenene-Garoua-Sangmelima',
            'nom_mere': 'Ngo Nyemb Nana Epse Hamidou',
            'profession_mere': "Cadre contractuelle d'administration",
            'telephone_mere': '6 20 20 20',
            'residence_mere': 'Makenene-Garoua-Sangmelima'
        }
        matricule = f'25NBT00{i}A'
        add_user(session, matricule, data['nom'], '0000', first_name=data['prenom'])
        admission = admissions[data['admission_id']]
        admission.matricule = matricule
        session.merge(Inscription(**data))
        session.commit()

    

    
