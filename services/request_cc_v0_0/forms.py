from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired

class RequeteForm(FlaskForm):
    objet = StringField('Objet', validators=[DataRequired()],render_kw={"class": "form-control"})
    intitule_ec = StringField('Intitule de la matiere', validators=[DataRequired()], render_kw={"class": "form-control", "placeholder":"EC4093(securite informatique)"})
    piece = FileField('Fichier à joindre', validators=[
        FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'Fichiers autorisés: PDF, PNG, JPG')])
    responsable_id = SelectField('Nom', render_kw={"class": "form-select"})
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={"class": "form-control h-100"})
    submit = SubmitField('Deposer', render_kw={"class": "btn btn-primary form-control"})