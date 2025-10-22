from core.config import db
from .models import *
from core.utils import Stat, Alert
from core.auth.models import User, Role
from datetime import datetime

student_data = [
    dict(id="student1", nom="KENFACK ROMEO", classe="II2", email="nanaromeo237@gmail.com", telephone="655927237"),
    dict(id="student2", nom="KENFACK ROMEO", classe="II2", email="nanaromeo2397@gmail.com", telephone="655927237"),
    dict(id="student3", nom="MAKOUHO ORNELLE ALICE", classe="TIC3", email="prodistributionltb1@gmail.com", telephone="655521434"),
    dict(id="student4", nom="TENEKE CARLOS ARNAUD", classe="GCI3", email="nanaromeo233@gmail.com", telephone="657501933"),
]

responsable_data = [
    dict(id="staff1", nom="MANGA BETENE FABRICE", email="nanaromeo237@gmail.com", telephone="679243290"),
    dict(id="staff2", nom="TACHIUEM YVES BRYAN", email="prodistributionltd3@gmail.com", telephone="679243290"),
    dict(id="staff3", nom="MOTSO LAURA", email="65750193t@gmail.com", telephone="679243220"),
    dict(id="staff4", nom="NNEME JORDAN", email="prodistributionltd5@gmail.com", telephone="679243220"),
]

# justificatif_data = [
#     dict(requete_id=1, justificatif="fca00629b0b64a9ba54b3911e7df247c.pdf", libelle="mes recus paiement de la scolarite")
# ]

role_data = [
    dict(id="chef_dpt", name="chef_departement"),
    dict(id="cellule", name="cellule"),
    dict(id="directeur", name="directeur"),
]

user_data = [
    dict(id="student1", last_name="KENFACK ROMEO", pwd="password1", role="student"),
    dict(id="student2", last_name="KENFACK ROMEO", pwd="password1", role="student"),
    dict(id="student3", last_name="KENFACK ROMEO", pwd="password1", role="student"),
    dict(id="student4", last_name="KENFACK ROMEO", pwd="password1", role="student"),

    dict(id="staff1", last_name="KENFACK ROMEO", pwd="password1", role="teacher"),
    dict(id="staff2", last_name="KENFACK ROMEO", pwd="password1", role="chef_dpt"),
    dict(id="staff3", last_name="KENFACK ROMEO", pwd="password1", role="cellule"),
    dict(id="staff4", last_name="KENFACK ROMEO", pwd="password1", role="teacher"),
    # dict(id="staff4", pwd="password1", role="directeur"),
]

requete_data = [
    dict(id=1, objet="absence de note", description="J'etais malade", responsable_id="staff1", etudiant_id="student1", intitule_ec="Modelisation", status="terminer"),
    dict(id=2, objet="absence de note", description="J'etais malade", responsable_id="staff1", etudiant_id="student1", intitule_ec="Anglais", status="suspendu"),
    dict(id=3, objet="absence de note", description="J'etais malade", responsable_id="staff1", etudiant_id="student1", intitule_ec="Informatique", status="rejeter"),
    dict(id=4, objet="absence de note", description="J'etais malade", responsable_id="staff1", etudiant_id="student1", intitule_ec="Geographie", status="approuver"),
    dict(id=5, objet="absence de note", description="J'etais malade", responsable_id="staff1", etudiant_id="student1", intitule_ec="Geographie", status="approuver"),
    dict(id=6, objet="absence de note", description="J'etais malade", responsable_id="staff1", etudiant_id="student1", intitule_ec="Modelisation", status="en attente"),
    dict(id=7, objet="absence de note", description="J'etais malade", responsable_id="staff1", etudiant_id="student1", intitule_ec="Modelisation", status="valider"),


] 

statut_data = [
    dict(id="suspendu", nom="suspendu", color="dark"),
    dict(id="terminer", nom="terminer", color="success"),
    dict(id="rejeter", nom="rejeter", color="danger"),
    dict(id="approuver", nom="approuver", color="warning"),
    dict(id="en attente", nom="en attente", color="secondary"),
    dict(id="valider", nom="valider", color="warning"),
    ]

traitement_data =[
    dict(id=1, commentaire="Les requetes ne sont plus recevable", requete_id=5, responsable_id="staff1", statut_id="approuver", date_tr=datetime.utcnow()),
    dict(id=2, commentaire="Les requetes ne sont plus recevable", requete_id=3, responsable_id="staff1",statut_id="rejeter", date_tr=datetime.utcnow()),
    dict(id=3, commentaire="envoyer vos recus de paiement", requete_id=2, responsable_id="staff1", statut_id="suspendu", date_tr=datetime.utcnow()),
    dict(id=4, commentaire="Les requetes ne sont plus recevable", requete_id=4, responsable_id="staff1", statut_id="approuver", date_tr=datetime.utcnow()),
    dict(id=5, commentaire="Votre note a ete modifier 13 au lieu de 10", requete_id=1, responsable_id="staff1",statut_id="en attente", date_tr=datetime.utcnow()),
    dict(id=6, commentaire="envoyer vos recus de paiement", requete_id=1, responsable_id="staff1",statut_id="suspendu", date_tr=datetime.utcnow()),
    dict(id=7, commentaire="", requete_id=1, responsable_id="staff2",statut_id="approuver", date_tr=datetime.utcnow()),
    dict(id=8, commentaire="Votre note a ete modifier 13 au lieu de 10", requete_id=1, responsable_id="staff1",statut_id="terminer", date_tr=datetime.utcnow()),
    dict(id=9, commentaire="Votre note a ete modifier 13 au lieu de 10", requete_id=6, responsable_id="staff1",statut_id="en attente", date_tr=datetime.utcnow()),
    dict(id=10, commentaire="Votre note a ete modifier", requete_id=7, responsable_id="staff1",statut_id="valider", date_tr=datetime.utcnow())
    # dict(id=11, commentaire="Votre note a ete modifier", requete_id=7, responsable_id="staff1",statut_id="valider", date_tr=datetime.utcnow())

]

def init_data():
    for row in statut_data:
        statut = Statut(**row)
        db.session.merge(statut)
    db.session.commit()
    
    for row in student_data:
        student = Etudiant(**row)
        db.session.merge(student)
    db.session.commit()
    
    for row in responsable_data:
        responsable = Responsable(**row)
        db.session.merge(responsable)
    db.session.commit()
    
    for row in role_data:
        role = Role(**row)
        db.session.merge(role)
    db.session.commit()
    
    for row in user_data:
        role = Role.query.filter_by(id=row['role']).one()
        user = User(id=row['id'], last_name=row['last_name'], roles=[role])
        user.set_password(row['pwd'])
        db.session.merge(user)
    db.session.commit()

    for row in requete_data:
        requete = Requete(**row)
        # user.set_password(row['pwd'])
        db.session.merge(requete)
    db.session.commit()

    for row in traitement_data:
        traitement = Traitement(**row)
        # user.set_password(row['pwd'])
        db.session.merge(traitement)
    db.session.commit()

    # for row in justificatif_data:
    #     justificatif = Justificatif(**row)
    #     # user.set_password(row['pwd'])
    #     db.session.merge(justificatif)
    # db.session.commit()

def init_stats(user):
    stats = []
    if user.has_roles(['student']):
        stats.extend([
            Stat('Requetes CC', 'Requetes soumises', value='07 requetes')
        ])
    if user.has_roles(['teacher']):
        stats.extend([
            Stat('Requetes CC', 'Requetes en attentes', value='01 requete'),
            Stat('Requetes CC', 'Requetes suspendues', value='01 requetes'),

        ])
    if user.has_roles(['chef_depart']):
        stats.extend([
            Stat('Requetes CC', 'Requetes approuvees', value='02 requetes'),
            Stat('Requetes CC', 'Requetes rejetees', value='01 requetes')

        ])
    if user.has_roles(['cellule']):
        stats.extend([
            Stat('Requetes CC', 'Requetes terminees', value='01 requetes')

        ])
    return stats

