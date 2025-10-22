from flask import Flask, request, render_template, redirect ,send_from_directory,send_file, jsonify,flash,url_for
import os
from datetime import datetime
import uuid
import math
from database.models import db,Student
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black, blue, grey, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont




app = Flask(__name__)

config_dir = os.path.dirname(__file__)
db_dir = os.path.join(config_dir, 'database/student.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ db_dir  # ou une autre BDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'e8e7e1d941a735f9f09cad5f0fcd4d58299fcd7f67b46e61'

db.init_app(app) 
with app.app_context():
    db.create_all()
    print("Base de données initialisée avec succès.")

# Configuration
UPLOAD_FOLDER = 'uploads'
PDF_FOLDER = 'Fiches d\'inscription'
TEMPLATE_PATH = 'template_carte.png'  # Template de base de la carte

# Créer les dossiers nécessaires
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)

def generer_matricule_structure():
    # 1. Obtenir l'année académique courante (ex: 2024/2025)
    annee_courante = datetime.now().year
    
    dept = request.form.get('departement', '').strip()
    
    # 2. Compter le nombre d'étudiants pour l'année en cours
    # Cette étape nécessite que vous stockiez l'année académique dans votre modèle Student
    # Pour un exemple simple, on compte juste le nombre total d'étudiants
    nombre_etudiants = db.session.query(Student).count()
    
    # 3. Incrémenter le compteur
    nouveau_numero = nombre_etudiants + 1
    
    # 4. Formater le numéro pour qu'il ait une longueur fixe (ex: 3 chiffres)
    # Ex: 1 -> 001, 25 -> 025
    numero_formate = f"{nouveau_numero:03d}"
    
    # 5. Combinez l'année, le département, et le numéro pour créer le matricule
    # Ex: '24' pour 2024, 'NII' pour 'Génie Informatique Industrielle'
    # NOTE : 'NII' ou 'GCI' doivent être récupérés d'une manière ou d'une autre (ex: depuis le formulaire)
    
    matricule_final = f"{annee_courante % 100}N{dept}{numero_formate}A"
    # Exemple de résultat: '24NII001A'
    
    return matricule_final

def generer_matricule():
    
    return str(uuid.uuid4().hex[:8]).upper()  




def generer_fiche_inscription_pdf(data, nom_fichier="fiche_inscription.pdf", photo_path=None):
    """
    Génère un PDF de fiche d'inscription ENSET avec des coordonnées fixes et la photo de l'étudiant.

    Args:
        data (dict): Dictionnaire contenant les informations de l'étudiant.
        nom_fichier (str): Nom du fichier de sortie.
        photo_path (str): Chemin vers le fichier de la photo de l'étudiant.
    """

    # Créer le canvas
    c = canvas.Canvas(nom_fichier, pagesize=A4)
    width, height = A4

    # Définir les couleurs
    couleur_bleu_ud = Color(0/255, 60/255, 120/255)
    couleur_texte_noir = black

    # --- 1. EN-TÊTE AVEC LOGOS ET TEXTE ---

    # Positions fixes pour les logos
    logo_enset_path = "static/images/logo_udo.jpg"
    logo_ud_path = "static/images/logo enset.jpg"
    
    # Vérifier l'existence des fichiers d'image
    if os.path.exists(logo_enset_path):
        # Le logo ENSET est placé en haut à gauche
        c.drawImage(logo_enset_path, 20*mm, height - 40*mm, width=30*mm, height=30*mm)
    else:
        c.rect(20*mm, height - 40*mm, 20*mm, 20*mm, stroke=1)
        c.drawString(25*mm, height - 30*mm, "Logo ENSET")

    if os.path.exists(logo_ud_path):
        # Le logo de l'Université de Douala est placé en haut à droite, au-dessus de la photo
        c.drawImage(logo_ud_path, width - 40*mm, height - 40*mm, width=30*mm, height=30*mm)
    else:
        c.rect(width - 40*mm, height - 40*mm, 20*mm, 20*mm, stroke=1)
        c.drawString(width - 35*mm, height - 30*mm, "Logo UD")

    # Placement de la photo de l'étudiant
    photo_width = 39*mm
    photo_height = 43*mm
    photo_x = width - photo_width - 30*mm
    photo_y = height - 80*mm - photo_height
    
    if photo_path and os.path.exists(photo_path):
        try:
            c.drawImage(photo_path, photo_x, photo_y, width=photo_width, height=photo_height)
        except Exception:
            c.rect(photo_x, photo_y, photo_width, photo_height, stroke=1)
            c.drawCentredString(photo_x + photo_width/2, photo_y + photo_height/2, "PHOTO ICI")
    else:
        c.rect(photo_x, photo_y, photo_width, photo_height, stroke=1)
        c.drawCentredString(photo_x + photo_width/2, photo_y + photo_height/2, "PHOTO ICI")
    
    # Texte principal de l'en-tête (centré)
    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(couleur_bleu_ud)
    c.drawCentredString(width/2, height - 17*mm, "UNIVERSITÉ DE DOUALA")

    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, height - 23*mm, "ÉCOLE NORMALE SUPÉRIEURE")
    c.drawCentredString(width/2, height - 29*mm, "D'ENSEIGNEMENT TECHNIQUE")

    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 34*mm, "BP 1872 Douala - Cameroun")
    c.drawCentredString(width/2, height - 39*mm, "Tél: (Fax) (237) 33 42 44 39")

    # --- 2. TITRE DU FORMULAIRE ---
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(couleur_bleu_ud)
    c.drawCentredString(width/2, height - 58*mm, "FICHE D'INSCRIPTION 2025-2026")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height - 68*mm, "FORMATION INITIALE")

    # --- 3. NOTE IMPORTANTE ---
    # c.setFont("Helvetica-Oblique", 9)
    # c.setFillColor(couleur_texte_noir)
    # c.drawString(20*mm, height - 71*mm, "NB : À faire remplir par le candidat lui-même car ses informations sont d'une importance capitale pour la")
    # c.drawString(20*mm, height - 75*mm, "délivrance des effets académiques.")

        # --- 4. CHAMPS DU FORMULAIRE AVEC COORDONNÉES FIXES ---
    y_pos = height - 85*mm
    x_label = 20*mm
    x_value = 58*mm
    line_spacing = 12*mm
    
    # Formater la date de naissance
    date_naissance = data.get('date_naissance', '')
    if date_naissance:
        try:
            date_obj = datetime.strptime(date_naissance, '%Y-%m-%d')
            date_formatee = date_obj.strftime('%d/%m/%Y')
        except:
            date_formatee = date_naissance
    else:
        date_formatee = ''

    # Dessin des champs, ligne par ligne
    c.setFillColor(couleur_texte_noir)
    c.setFont("Helvetica", 9)
    c.drawString(x_label, y_pos, "N° D'ORDRE :_________________")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value, y_pos, data.get('num_ordre', '').upper())
    y_pos -= line_spacing
    
    c.setFont("Helvetica", 9)
    c.drawString(x_label, y_pos, "NATIONALITÉ :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value, y_pos, data.get('nationalite', '').upper())
    y_pos -= line_spacing

    c.setFont("Helvetica", 9)
    c.drawString(x_label, y_pos, "DÉPARTEMENT / FILIÈRE CHOISIE :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value + 28*mm, y_pos, data.get('departement', '').upper())
    y_pos -= line_spacing

    c.setFont("Helvetica", 9)
    c.drawString(x_label, y_pos, "OPTION CHOISIE :")
    c.setFont("Helvetica-Bold", 11)
    option =f"{data.get('option', '').upper()} {data.get('niveau', '').upper()}"
    c.drawString(x_value, y_pos, option)
    y_pos -= line_spacing

    c.setFont("Helvetica", 9)
    c.drawString(x_label, y_pos, "NOM ET PRÉNOMS :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value , y_pos, data.get('nom_prenom', '').upper())
    y_pos -= line_spacing
    
    # Champs sur la même ligne (Date de naissance et Lieu)
    x_label2 = width/2 + 5*mm
    x_value2 = width/2 + 20*mm

    c.setFont("Helvetica", 9)
    c.drawString(x_label, y_pos, "DATE DE NAISSANCE :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value , y_pos, date_formatee.upper())

    c.setFont("Helvetica", 9)
    c.drawString(x_label2 - 5*mm, y_pos, "LIEU :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value2 - 5*mm, y_pos, data.get('lieu_naissance', '').upper())
    y_pos -= line_spacing

    # Champs sur la même ligne (Sexe et Situation matrimoniale)
    x_label2 = width/2 + -10*mm
    x_value2 = width/2 + 50*mm
    c.setFont("Helvetica", 9)
    c.drawString(x_label, y_pos, "SEXE (F/M) :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value, y_pos, data.get('sexe', '').upper())

    c.setFont("Helvetica", 9)
    c.drawString(x_label2, y_pos, "SITUATION MATRIMONIALE (M/C/D) :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value2, y_pos, data.get('situation_matrimoniale', '').upper())
    y_pos -= line_spacing

    # Champs sur la même ligne (Région et Département d'origine)
    x_label2 = width/2 + -8*mm
    x_value2 = width/2 + 43*mm
    c.setFont("Helvetica", 9)
    c.drawString(x_label, y_pos, "RÉGION D'ORIGINE :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value, y_pos, data.get('region_origine', '').upper())
    
    c.setFont("Helvetica", 9)
    c.drawString(x_label2 + 2*mm, y_pos, "DÉPARTEMENT D'ORIGINE :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value2- 2*mm, y_pos, data.get('departement_origine', '').upper())
    y_pos -= line_spacing

    # Champs sur la même ligne (Langue et Téléphone)
    x_label2 = width/2 - 2*mm
    x_value2 = width/2 + 25*mm
    c.setFont("Helvetica", 9)
    c.drawString(x_label, y_pos, "LANGUE (F/A) :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value, y_pos, data.get('langue', '').upper())
    
    c.setFont("Helvetica", 9)
    c.drawString(x_label2, y_pos, "TÉLÉPHONE :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value2, y_pos, data.get('telephone', '').upper())
    y_pos -= line_spacing

    x_label2 = width/2 + 10*mm
    x_value2 = width/2 + 33*mm
    c.setFont("Helvetica", 9)
    c.drawString(x_label, y_pos, "EMAIL :")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x_value, y_pos, data.get('email', '').upper())
    
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x_label2, y_pos, "MATRICULE :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value2, y_pos, data.get('matricule', '').upper())
    y_pos -= line_spacing
    
    # Champs sur la même ligne (Diplôme et Année d'obtention)
    x_label2 = width/2 + 10*mm
    x_value2 = width/2 + 50*mm
    c.setFont("Helvetica", 9)
    c.drawString(x_label, y_pos, "DIPLÔME OBTENU :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value, y_pos, data.get('diplome', '').upper())
    
    c.setFont("Helvetica", 9)
    c.drawString(x_label2, y_pos, "ANNÉE D'OBTENTION :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value2, y_pos, data.get('annee_diplome', '').upper())
    y_pos -= line_spacing  # Espace entre les sections
    
    x_label2 = width/2
    x_value2 = width/2 + 55*mm
    # Informations des parents
    c.setFont("Helvetica", 9)
    c.drawString(x_label, y_pos, "NOM DU PÈRE/TUTEUR :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value+ 9*mm, y_pos, data.get('nom_pere', '').upper())
    
    
    c.setFont("Helvetica", 9)
    c.drawString(x_label2, y_pos, "PROFESSION DU PÈRE/TUTEUR :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value2, y_pos, data.get('profession_pere', '').upper())
    y_pos -= line_spacing
    
    x_label2 = width/2 + 2*mm
    x_value2 = width/2 + 56*mm
    c.setFont("Helvetica", 9)
    c.drawString(x_label, y_pos, "TÉLÉPHONE DU PÈRE/TUTEUR :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value+ 19*mm, y_pos, data.get('telephone_pere', '').upper())
   
    
    c.setFont("Helvetica", 9)
    c.drawString(x_label2, y_pos, "VILLE DE RÉSIDENCE DU PÈRE :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value2, y_pos, data.get('ville_residence_pere', '').upper())
    y_pos -= line_spacing

    x_label2 = width/2 - 5*mm
    x_value2 = width/2 + 45*mm
    c.setFont("Helvetica", 9)
    c.drawString(x_label, y_pos, "NOM DE LA MÈRE :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value, y_pos, data.get('nom_mere', '').upper())
    
    
    c.setFont("Helvetica", 9)
    c.drawString(x_label2, y_pos, "PROFESSION DE LA MÈRE :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value2, y_pos, data.get('profession_mere', '').upper())
    y_pos -= line_spacing
    
    x_label2 = width/2 
    x_value2 = width/2 + 60*mm
    c.setFont("Helvetica", 9)
    c.drawString(x_label, y_pos, "TÉLÉPHONE DE LA MÈRE :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value+ 19*mm, y_pos, data.get('telephone_mere', '').upper())
    
    
    c.setFont("Helvetica", 9)
    c.drawString(x_label2, y_pos, "VILLE DE RÉSIDENCE DE LA MÈRE :")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_value2, y_pos, data.get('ville_residence_mere', '').upper())
    y_pos -= line_spacing 
    
   
    
    # --- 5. SIGNATURE ET CACHET ---
    # c.setFont("Helvetica", 10)
    # c.drawString(width - 70*mm, y_pos-6*mm, "SIGNATURE")
    # # c.line(width - 90*mm, y_pos - 25*mm, width - 30*mm, y_pos - 25*mm)

   
    # Sauvegarder le PDF
    c.save()
    return nom_fichier


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generer', methods=['POST'])
def generate_card():
    if request.method == 'POST':
        # matricule = request.form.get('matricule')
        #  # Vérifie si le matricule existe déjà
        # if Student.query.filter_by(matricule= matricule).first():
        #     flash("Ce matricule existe déjà. Veuillez en saisir un autre.", "error")
        #     return redirect(url_for('index'))
        try:
            # 1. RÉCUPÉRATION DES DONNÉES DU FORMULAIRE
            print("=== RÉCUPÉRATION DES DONNÉES ===")
            
            # Informations personnelles de base
            nationalite = request.form.get('nationalite', '').strip().upper()
            nom_prenom = request.form.get('nom_prenom', '').upper()
            date_naissance = request.form.get('date_naissance', '').strip()
            lieu_naissance = request.form.get('lieu_naissance', '').strip().upper()
            sexe = request.form.get('sexe', '').strip().capitalize()
            situation_matrimoniale = request.form.get('situation_matrimoniale', '').strip().capitalize()
            
            # Origine géographique
            region_origine = request.form.get('region_origine', '').strip().upper()
            departement_origine = request.form.get('departement_origine', '').strip()
            
            # Coordonnées
            telephone = request.form.get('telephone', '').strip()
            email = request.form.get('email', '').strip().lower()
            langue = request.form.get('langue', '').strip()
            
            # Informations académiques
            departement = request.form.get('departement', '').strip()
            option = request.form.get('option', '').strip()
            niveau = request.form.get('niveau', '').strip()
            diplome = request.form.get('diplome', '')
            annee_diplome = request.form.get('annee_diplome', '').strip()
            
            # Informations du père/tuteur
            nom_pere = request.form.get('nom_pere', '').upper()
            profession_pere = request.form.get('profession_pere', '').upper()
            telephone_pere = request.form.get('telephone_pere', '').strip()
            ville_residence_pere = request.form.get('ville_residence_pere', '')
            
            # Informations de la mère
            nom_mere = request.form.get('nom_mere', '').upper()
            profession_mere = request.form.get('profession_mere', '').upper()
            telephone_mere = request.form.get('telephone_mere', '').strip()
            ville_residence_mere = request.form.get('ville_residence_mere', '')
            
            # matricule
            # matricule = generer_matricule()
            matricule = generer_matricule()
            
            # Gérer le fichier photo
            photo_path = None
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo.filename != '':
                    photo_filename = f"photo_{matricule}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    photo_path = os.path.join(UPLOAD_FOLDER, photo_filename)
                    photo.save(photo_path)
                    
            # Générer la carte
            nom_fichier_pdf = f"fiche_inscription_{nom_prenom.replace(' ', '_').lower()}.pdf"
            base_pdf_dir = 'Fiches_inscriptions'
            dossier_destination = os.path.join(base_pdf_dir, departement, niveau, option)

            # Créez le chemin du dossier si il n'existe pas
            os.makedirs(dossier_destination, exist_ok=True)
            chemin_pdf_final = os.path.join(dossier_destination, nom_fichier_pdf)
            data = {
                'matricule': matricule,
                'nom_prenom': nom_prenom,
                'date_naissance': date_naissance,
                'lieu_naissance': lieu_naissance,
                'sexe': sexe,
                'situation_matrimoniale': situation_matrimoniale,
                'nationalite': nationalite,
                'region_origine': region_origine,
                'departement_origine': departement_origine,
                'telephone': telephone,
                'photo_filename': photo_path,
                'email': email,
                'langue': langue,
                'departement': departement,
                'option': option,
                'niveau': niveau,
                'diplome': diplome,
                'annee_diplome': annee_diplome,
                'nom_pere': nom_pere,
                'profession_pere': profession_pere,
                'telephone_pere': telephone_pere,
                'ville_residence_pere': ville_residence_pere,
                'nom_mere': nom_mere,
                'profession_mere': profession_mere,
                'telephone_mere': telephone_mere,
                'ville_residence_mere': ville_residence_mere
            }
            
            # Sauvegarde en base de données
            etudiant = Student(
                nom_prenom=nom_prenom,
                date_naissance=date_naissance,
                lieu_naissance=lieu_naissance,
                sexe=sexe,
                situation_matrimoniale=situation_matrimoniale,
                nationalite=nationalite,
                region_origine=region_origine,
                departement_origine=departement_origine,
                telephone=telephone,
                email=email,
                langue=langue,
                
                # Informations académiques
                departement=departement,
                option=option,
                niveau=niveau,
                diplome=diplome,
                annee_diplome=annee_diplome,

                # Informations du père/tuteur
                nom_pere=nom_pere,
                profession_pere=profession_pere,
                telephone_pere=telephone_pere,
                ville_residence_pere=ville_residence_pere,

                # Informations de la mère
                nom_mere=nom_mere,
                profession_mere=profession_mere,
                telephone_mere=telephone_mere,
                ville_residence_mere=ville_residence_mere,

                # Les champs matricule et photo_filename seront ajoutés plus tard
                matricule=matricule,
                photo_filename=photo_filename # Assurez-vous que cette colonne existe dans votre modèle
            )
            db.session.add(etudiant)
            db.session.commit()
            fichier_pdf = generer_fiche_inscription_pdf(data, chemin_pdf_final,photo_path)
        except Exception as e:
            # En cas d'autre erreur de base de données (moins probable ici, mais bonne pratique)
            db.session.rollback() # Annule les changements si une erreur survient
            print(f"Erreur lors de la génération du PDF : {e}")
            flash(f"Une erreur est survenue lors de la création de la fiche d'inscription. Détails : {e}", 'error')
            return redirect(url_for('index'))


        return send_file(fichier_pdf, as_attachment=True, download_name=os.path.basename(fichier_pdf))
if __name__ == '__main__':
    app.run(debug=True)