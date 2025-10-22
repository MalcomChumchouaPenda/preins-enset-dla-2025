from .models import *
from core.config import ma


# Relation : un auteur a plusieurs livres
    # books = ma.Nested(BookSchema, many=True)

class RequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Requete
        load_instance = True

    id = ma.auto_field()
    objet = ma.auto_field()
    intitule_ec = ma.auto_field()
    # piece = ma.auto_field()
    responsable_id = ma.auto_field()
    description = ma.auto_field()
    # date_engr = ma.auto_field()
    # date_engr = ma.auto_field()
    # etudiant_id = ma.auto_field()

    justificatifs = ma.Nested(Justificatif, many=True)
    traitements = ma.Nested(Traitement, many=True)

requete_schema = RequestSchema()
requete_schema = RequestSchema(many=True)


class StudentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Etudiant
        load_instance = True

    id = ma.auto_field()
    nom = ma.auto_field()
    classe = ma.auto_field()
    email = ma.auto_field()
    telephone = ma.auto_field()
    requetes =  ma.Nested(RequestSchema, many=True)

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)


class JustificatifSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Justificatif
        load_instance = True

    # id = ma.auto_field()
    justificatif = ma.auto_field()
    libelle = ma.auto_field()
    requete_id = ma.auto_field()

justificatif_schema = JustificatifSchema()
justificatif_schema = JustificatifSchema(many=True)


class ResponsableSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Responsable
        load_instance = True

    id = ma.auto_field()
    nom = ma.auto_field()
    telephone = ma.auto_field()
    email = ma.auto_field()
    traitements = ma.Nested(Traitement, many=True)

responsable_schema = ResponsableSchema()
responsable_schema = ResponsableSchema(many=True)


class TraitementSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Traitement
        load_instance = True

    commentaire = ma.auto_field()
    requete_id = ma.auto_field()
    statut_id = ma.auto_field()

traitement_schema = TraitementSchema()
traitement_schema = TraitementSchema(many=True)


class StatutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Statut
        load_instance = True

    id = ma.auto_field()
    nom = ma.auto_field()
    color = ma.auto_field()
    traitements = ma.Nested(Traitement, many=True)

statut_schema = StatutSchema()
statut_schema = StatutSchema(many=True)
