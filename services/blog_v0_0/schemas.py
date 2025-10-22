from .models import *
from core.config import ma

class ArticleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Article
        load_instance = True

    id = ma.auto_field()
    titre = ma.auto_field()
    image = ma.auto_field()
    description = ma.auto_field()
    categorie_id = ma.auto_field()

course_schema = ArticleSchema()
courses_schema = ArticleSchema(many=True)

class CommentaireSchema(ma.SQLAlchemySchema):
    pass