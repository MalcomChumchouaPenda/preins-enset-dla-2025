
from datetime import datetime
from core.config import db
from core.auth.models import User


class Participant(User):
    email = db.Column(db.String(255), nullable=True)


class Categorie(db.Model):
    __bind_key__ = 'blog_v0'
    id=db.Column(db.Integer, primary_key=True)
    libelle=db.Column(db.String(100), nullable=False)
    articles=db.relationship('Article', backref='categorie')


class Article(db.Model):
    __bind_key__ = 'blog_v0'
    id=db.Column(db.Integer, primary_key=True)
    titre=db.Column(db.String(100), nullable=False)
    image=db.Column(db.String(100), nullable=True)
    description=db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.String(255), db.ForeignKey(User.id))
    date=db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(100), nullable=True, default="en attente")
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'))
    commentaires = db.relationship('Commentaire')
    likes=db.relationship('Like')
    dislikes=db.relationship('Dislike')

    @property
    def nb_likes(self):
        return len(self.likes)
    
    @property
    def nb_dislikes(self):
        return len(self.dislikes)

    @property
    def nb_commentaires(self):
        return len(self.commentaires)
    
    @property
    def color(self):
        if self.statut == 'rejeté':
            color = 'danger'
        elif self.statut == 'approuvé':
            color = 'success'
        else:
            color = 'warning'
        return color

    def avis_participant(self, id):
        nb_likes = len([like for like in self.likes if like.user_id==id])
        if nb_likes > 0:
            return 'positif'
        nb_dislikes = len([dislike for dislike in self.dislikes if dislike.user_id==id])
        if nb_dislikes > 0:
            return 'negatif'
        return 'aucun'


class Observation(db.Model):
    __bind_key__ = 'blog_v0'
    id =db.Column(db.Integer, primary_key=True)
    commentaire=db.Column(db.String(255), primary_key=True, nullable=True)
    # statut = db.Column(db.String(100), nullable=False, default="en attente")
    # statut:: en attente(delete, update), rejeter(modifier,delete), approuver


class Like(db.Model):
    __bind_key__ = 'blog_v0'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey(User.id))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

class Dislike(db.Model):
    __bind_key__ = 'blog_v0'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey(User.id))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

class Commentaire(db.Model):
    __bind_key__ = 'blog_v0'
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text, nullable=False)
    date=db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String(255), db.ForeignKey(User.id))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    auteur = db.relationship('Participant')
