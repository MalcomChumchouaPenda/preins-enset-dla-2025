import os
from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask_login import current_user
from sqlalchemy import desc
from flask_mail import Mail, Message
import uuid
from services.blog_v0_0.models import *
from services.blog_v0_0.schemas import *
from flask import render_template, request, url_for, redirect, flash
from core.utils import (
    UiBlueprint, 
    read_json, 
    read_markdown, 
    paginate_items, 
    default_deadline,
    get_locale
)



ui = UiBlueprint(__name__)
static_dir = os.path.join(os.path.dirname(__file__), 'static')

upload_folder = 'pages/blog/static/images'
os.makedirs(upload_folder, exist_ok=True)


@ui.route('/')
def index():
    categorie = request.args.get('categorie')
    articles = Article.query.filter_by(statut="approuvé")
    # .order_by(Article.id.desc()).all()
    if categorie:
        articles = articles.filter_by(categorie_id=categorie).order_by(Article.id.desc()).all()
    else : 
        articles = articles.order_by(Article.id.desc()).all()

    categories = Categorie.query.all()
    return render_template("index.jinja", articles=articles, categories=categories)

@ui.route('/detail-article/<int:id>')
def get_article(id):
    categories = Categorie.query.all()
    article = Article.query.get_or_404(id)
    categorie = request.args.get('categorie')
    articles = Article.query.filter_by(statut="approuvé")
    # .order_by(Article.id.desc()).all()
    if categorie:
        articles = articles.filter_by(categorie_id=categorie).order_by(Article.id.desc()).all()
    else : 
        articles = articles.order_by(Article.id.desc()).all()
    return render_template("detail-post.jinja", article=article, categorieas=categories)


@ui.route('/detail-article/commenter/<int:id>', methods=['POST'])
def commenter_article(id):
    return redirect(url_for('blog.get_article', id=id))


@ui.route('/ajouter-un-article', methods=['POST','GET'])
@ui.roles_accepted('teacher','chef_dpt')
def create_article():
    categories = Categorie.query.all()

    if request.method == 'POST':
        schema = ArticleSchema()
        data = request.form.to_dict()
        data = schema.load(request.form)
        image = request.files.get('image')
        filename = None
        if image and image.filename :
            ext = os.path.splitext(image.filename)[1]
            filename = f"{uuid.uuid4().hex}{ext}"
            file_path = os.path.join(upload_folder, filename)

        os.makedirs(upload_folder, exist_ok=True)
        image.save(file_path)

        article = Article(
            titre = data.titre,
            categorie_id = data.categorie_id,
            image = filename,
            user_id = current_user.id,
            description = data.description
        )
        db.session.add(article)
        db.session.commit()
        flash("Article poster avec succes","success")
        return redirect(url_for("blog.get_all_teacher_post"))
    else :    
        return render_template("teacher/create-post.jinja", categories=categories)

@ui.route('/mes-articles/delete/<int:id>/')
@ui.roles_accepted('teacher','chef_dpt')
def delete_post(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash('Article supprimée avec succès.', 'success')
    return redirect(url_for('blog.get_all_teacher_post'))

@ui.route('/mes-articles')
@ui.roles_accepted('teacher','chef_dpt')
def get_all_teacher_post():
    articles = Article.query.filter_by(user_id=current_user.id).order_by(Article.id.desc()).all()
    return render_template("teacher/index.jinja", articles=articles)

@ui.route('/mes-articles/<int:id>')
@ui.roles_accepted('teacher','chef_dpt')
def get_one_teacher_post(id):
    article = Article.query.filter_by(id=id).one()
    return render_template("teacher/detail-post.jinja", article=article)


@ui.route('/gerer-articles')
@ui.roles_accepted('chef_dpt')
def manage_all_articles():
    articles = Article.query.order_by(Article.id.desc()).all()
    return render_template("chef_dpt/index.jinja", articles=articles)

@ui.route('/gerer-articles/<int:id>')
@ui.roles_accepted('chef_dpt')
def manage_one_article(id):
    article = Article.query.filter_by(id=id).one()
    return render_template("chef_dpt/detail-post.jinja", article=article)