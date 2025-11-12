

from sqlalchemy.exc import IntegrityError
from core.auth.tasks import get_user, add_user, add_roles_to_user
from core.auth.models import User
from services.formations_v0_0.models import Classe, Filiere, Niveau
from services.regions_v0_0.models import Departement
from services.regions_v0_0 import tasks as region_tasks
from services.formations_v0_0 import tasks as format_tasks
from ..models import db, Inscription, Admission, Requete, CommuniqueAdmission

def chercher_admission(id):
    query = db.session.query(Admission)
    query = query.filter_by(id=id)
    admission = query.one_or_none()
    return admission


def ajouter_inscription(user, data):
    session = db.session
    matricule = data.pop('matricule')
    inscription = Inscription(**data)
    if matricule:
        query = session.query(Admission)
        query = query.filter_by(id=data['admission_id'])
        admission = query.one()
        admission.matricule = matricule
    else:
        creer_matricule(session, inscription)
    user.first_name = inscription.prenom
    user.last_name = inscription.nom
    session.add(inscription)
    session.commit()
    
def creer_matricule(session, inscription):
    admission = chercher_admission(inscription.admission_id)
    # print(admission.communique_id, admission.communique)
    annee = admission.communique.annee_academique[2:4]
    statut = admission.statut[0]
    classe = admission.classe
    prefix = classe.filiere.prefix
    niveau = classe.niveau.id[-1]

    if niveau == '4':
        num_size = 2
        filtre = f'{annee}N{prefix}L%{statut}'
    elif niveau == '3':
        num_size = 2
        filtre = f'{annee}N{prefix}B%{statut}'
    else:
        num_size = 3
        filtre = f'{annee}N{prefix}%{statut}'

    # print('\nfuser', session.query(User).all())
    for i in range(10):
        try:
            count = session.query(User).filter(User.id.like(filtre)).count()
            # print('\n\tfilter', i, filtre, count)
            num = str(count + 1).rjust(num_size, '0')
            matricule = filtre.replace('%', num)
            add_user(session, matricule, inscription.nom, '0000', first_name=inscription.prenom)
            add_roles_to_user(session, matricule, 'student')
            admission.matricule = matricule
            session.commit()
            return matricule
        except IntegrityError as e:
            session.rollback()


def modifier_inscription(user, data):
    session = db.session
    inscription = Inscription(**data)
    user.first_name = inscription.prenom
    user.last_name = inscription.nom 
    session.add(inscription)
    session.commit()
    

def creer_inscription(user_id):
    inscription = Inscription(admission_id=user_id)
    return inscription

def rechercher_inscription(user_id):
    query = db.session.query(Inscription)
    query = query.filter_by(admission_id=user_id)
    query = query.order_by(Inscription.id.desc())
    inscriptions = query.all()
    if len(inscriptions) == 0:
        return None

    # inscription = inscriptions[0]
    # query = db.session.query(Departement)
    # query = query.filter_by(id=inscription.departement_origine_id)
    # departement_origine = query.one_or_none()
    # setattr(inscription, 'departement_origine', departement_origine)
    
    # query = db.session.query(Classe)
    # query = query.filter_by(id=inscription.admission.classe_id)
    # classe = query.one_or_none()
    # setattr(inscription.admission, 'classe', classe)
    return inscriptions[0]


def ajouter_requete(data):
    requete = Requete(**data)
    db.session.add(requete)
    db.session.commit()
    return requete


def rechercher_requete(user_id):
    query = db.session.query(Requete)
    query = query.filter_by(admission_id=user_id)
    query = query.order_by(Requete.id.desc())
    requetes = query.all()
    if len(requetes) == 0:
        return None

    requete = requetes[0]
    query = db.session.query(Filiere)
    query = query.filter_by(id=requete.filiere_correct_id)
    filiere_correct = query.one_or_none()
    setattr(requete, 'filiere_correct', filiere_correct)
    
    query = db.session.query(Niveau)
    query = query.filter_by(id=requete.niveau_correct_id)
    niveau_correct = query.one_or_none()
    setattr(requete, 'niveau_correct', niveau_correct)
    
    query = db.session.query(Classe)
    query = query.filter_by(id=requete.admission.classe_id)
    classe = query.one_or_none()
    setattr(requete.admission, 'classe', classe)
    return requete

