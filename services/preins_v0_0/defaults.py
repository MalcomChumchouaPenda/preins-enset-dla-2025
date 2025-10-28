
import random
from datetime import datetime
from core.config import db
from core.utils import Stat, Alert
from core.auth.tasks import add_role, add_user, add_roles_to_user
from .models import Admission, Inscription, CommuniqueAdmission, Requete


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
    add_roles_to_user(session, 'dev1', 'admis')

    # creation des communiques
    if not session.query(CommuniqueAdmission).filter_by(id='Fake').first():
        communique = CommuniqueAdmission(id="Fake")
        communique.numero = '001/Fake/ du 12/05/2006'
        communique.objet = 'Portant admission des candidats tests'
        communique.annee_academique = '2025/2026'
        session.add(communique)
        session.commit()


    # creation des developpers
    query = session.query(Admission).filter_by(id='dev2')
    if query.count() == 0:

        # creation des users et admissions
        for i in range(2, 5):
            id = f'dev{i}'
            nom = f'Developper {i}'
            add_user(session, id, nom, 'devpass')
            add_roles_to_user(session, id, 'developper', 'admis')
            data = {
                'id':id,
                'nom_complet':nom,
                'statut':'AA',
                'classe_id':'TER1',
                'communique_id': 'Fake',
                'matricule': f'25NTE00{i}A' if i > 2 else None,
            }
            session.add(Admission(**data))
            session.commit()

        # creation des inscriptions
        for i in range(3, 5):
            data = {
                'admission_id': f'dev{i}',
                'nom': f'Developper {i}',
                'date_naissance': datetime(2000+i, 1, 1),
                'lieu_naissance': f'Maternite de la ville {i}',
                'sexe_id': random.choice(['F', 'M']),
                'situation_matrimoniale_id': random.choice(['C', 'M']),
                'departement_origine_id': 'dep4',
                'telephone': f'6 70 70 90 9{i}',
                'email': f'dev{i}@yahoo.co',
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
            session.merge(Inscription(**data))
            session.commit()

        # creation des requetes
        for i in range(4, 5):
            data = {
                'admission_id': f'dev{i}',
                'nom_correct': f'Developper corrected {i}',
                'option_correct_id': 'CHI',
                'niveau_correct_id': 'N4',
                'justificatifs': 'Piece 01, Piece 02'
            }
            session.merge(Requete(**data))
            session.commit()

    # creation etudiants tests
    query = session.query(Admission).filter_by(id='BTP1-25AA-001')
    if query.count() == 0:

        # creation des users et admissions
        for i in range(1, 10):
            for n in 'AP':
                id = f'BTP1-25A{n}-00{i}'
                nom = f'Admis Liste {n} numero {i}'                    
                add_user(session, id, nom, '0000')
                add_roles_to_user(session, id, 'admis')

                if i < 5 and n == 'A':
                    matricule = f'25NBT00{i}A'
                else:
                    matricule = None
                data = {
                    'id':id,
                    'nom_complet':nom,
                    'statut':'A' + n,
                    'classe_id':'BTP1',
                    'communique_id': 'Fake',
                    'matricule': matricule
                }
                session.add(Admission(**data))
                session.commit()

        # creation des inscriptions
        for i in range(1, 5):
            data = {
                'admission_id': f'BTP1-25AA-00{i}',
                'nom': f'Admis Liste A numero {i}',
                'date_naissance': datetime(2000+i, 1, 1),
                'lieu_naissance': f'Maternite de la ville {i}',
                'sexe_id': random.choice(['F', 'M']),
                'situation_matrimoniale_id': random.choice(['C', 'M']),
                'departement_origine_id': 'dep4',
                'telephone': f'6 70 70 90 9{i}',
                'email': f'admis{i}@yahoo.co',
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
            session.merge(Inscription(**data))
            session.commit()

        # creation des requetes
        for i in range(1, 3):
            data = {
                'admission_id': f'BTP1-25AA-00{i}',
                'nom_correct': f'Correction Admis Liste A numero {i}',
                'option_correct_id': 'CHI',
                'niveau_correct_id': 'N3',
                'justificatifs': 'Piece 01, Piece 02, Piece 03'
            }
            session.merge(Requete(**data))
            session.commit()



    

    
