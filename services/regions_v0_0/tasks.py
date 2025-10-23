
from .models import db, Pays, Region, Departement


def chercher_departement(id):
    query = db.session.query(Departement)
    query = query.filter_by(id=id)
    return query.one_or_none()

def list_nationalites():
    query = db.session.query(Pays)
    return [(obj.id, obj.nom) for obj in query.all()]

def list_regions():
    query = db.session.query(Region)
    return [(obj.id, obj.nom) for obj in query.all()]

def list_departements():
    query = db.session.query(Departement)
    return [(obj.id, obj.nom) for obj in query.all()]

