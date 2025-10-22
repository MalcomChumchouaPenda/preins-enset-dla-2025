
import os
import pandas as pd
from core.config import db
from core.auth.tasks import add_user, add_role, add_roles_to_user
from .models import *


cur_dir = os.path.dirname(__file__)
store_dir = os.path.join(cur_dir, 'store')


roles_data = [
    dict(id='chef_dpt', name='Chef departement'),
]

users_data = [
    dict(id='nneme1', last_name='Nneme Nneme', first_name='Leandre', password='adminpass'),
]

user_roles_data = [
    dict(id='dev1', roles=['chef_dpt', 'teacher']),
    dict(id='nneme1', roles=['chef_dpt']),
]

def init_data():
    session = db.session
    for row in roles_data:
        add_role(session, **row)
    for row in users_data:
        add_user(session, **row)
    for row in user_roles_data:
        add_roles_to_user(session, row['id'], *row['roles'])

    categorie_path = os.path.join(store_dir, 'demo_categories.csv')
    categorie_data = pd.read_csv(categorie_path)
    categorie_data = categorie_data.to_dict('records')
    for row in categorie_data:
        categorie = Categorie(**row)
        session.merge(categorie)
    session.commit()

    article_path = os.path.join(store_dir, 'demo_articles.csv')
    article_data = pd.read_csv(article_path, parse_dates=[5])
    article_data['statut'] = article_data['statut'].fillna('en attente')
    article_data = article_data.to_dict('records')
    for row in article_data:
        article = Article(**row)
        session.merge(article)
    session.commit()

    commentaire_path = os.path.join(store_dir, 'demo_commentaires.csv')
    commentaire_data = pd.read_csv(commentaire_path, parse_dates=[2])
    commentaire_data = commentaire_data.to_dict('records')
    for row in commentaire_data:
        commentaire = Commentaire(**row)
        session.merge(commentaire)
    session.commit()
    
    like_path = os.path.join(store_dir, 'demo_likes.csv')
    like_data = pd.read_csv(like_path)
    like_data = like_data.to_dict('records')
    for row in like_data:
        like = Like(**row)
        session.merge(like)
    session.commit()
    
    dislike_path = os.path.join(store_dir, 'demo_dislikes.csv')
    dislike_data = pd.read_csv(dislike_path)
    dislike_data = dislike_data.to_dict('records')
    for row in dislike_data:
        dislike = Dislike(**row)
        session.merge(dislike)
    session.commit()
        