
import os
from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black, blue, grey, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

from services.formations_v0_0.models import Classe
from services.regions_v0_0.models import Pays, Region, Departement
from .models import db, Preinscription, Admission, Requete


store_dir = os.path.join(os.path.dirname(__file__), 'store')


def lister_nationalites():
    query = db.session.query(Pays)
    items = [('', 'Choisir...')]
    for record in query.all():
        val = record.id
        text = record.nom
        items.append((val, text))
    return items

def lister_regions():
    query = db.session.query(Region)
    items = [('', 'Choisir...')]
    for record in query.all():
        pays = record.pays
        val = pays.id + '-' + record.id 
        text = record.nom
        items.append((val, text))
    return items

def lister_departements():
    query = db.session.query(Departement)
    items = [('', 'Choisir...')]
    for record in query.all():
        region = record.region
        pays = region.pays
        val = pays.id + '-' + region.id + '-' + record.id 
        text = record.nom
        items.append((val, text))
    return items


def chercher_admission(id):
    query = db.session.query(Admission)
    query = query.filter_by(id=id)
    admission = query.one_or_none()
    if admission is not None:
        query = db.session.query(Classe)
        query = query.filter_by(id=admission.classe_id)
        classe = query.one_or_none()
        setattr(admission, 'classe', classe)
    return admission


def enregistrer_inscription(data):
    inscription = Preinscription(**data)
    db.session.add(inscription)
    db.session.commit()

def creer_inscription(user_id):
    inscription = Preinscription(admission_id=user_id)
    return inscription

def rechercher_inscription(user_id):
    query = db.session.query(Preinscription)
    query = query.filter_by(admission_id=user_id)
    query = query.order_by(Preinscription.id.desc())
    inscriptions = query.all()
    if len(inscriptions) == 0:
        return None

    inscription = inscriptions[0]
    query = db.session.query(Departement)
    query = query.filter_by(id=inscription.departement_origine_id)
    departement_origine = query.one_or_none()
    setattr(inscription, 'departement_origine', departement_origine)
    
    query = db.session.query(Classe)
    query = query.filter_by(id=inscription.admission.classe_id)
    classe = query.one_or_none()
    setattr(inscription.admission, 'classe', classe)
    return inscription


def enregistrer_requete(data):
    requete = Requete(**data)
    db.session.add(requete)
    db.session.commit()
    return requete


def generer_fiche_inscription(inscription, nom_fichier):
    """
    Génère un PDF de fiche d'inscription ENSET avec des coordonnées fixes et la photo de l'étudiant.

    Args:
        data (dict): Dictionnaire contenant les informations de l'étudiant.
        nom_fichier (str): Nom du fichier de sortie.
    """

    # recuperation des autres infos
    # admission = inscription.admission
    # departement = region_tasks.chercher_departement(inscription.departement_origine_id)
    # classe = format_tasks.chercher_classe(admission.classe_id)
    
    # Créer le canvas
    c = canvas.Canvas(nom_fichier, pagesize=A4)
    width, height = A4

    # Définir les couleurs
    couleur_bleu_ud = Color(0/255, 60/255, 120/255)
    couleur_texte_noir = black
  # --- 1. EN-TÊTE AVEC LOGOS ET TEXTE ---

    # Positions fixes pour les logos
    logo_ud_path = os.path.join(store_dir, 'imgs', 'udo.jpg')
    logo_enset_path = os.path.join(store_dir, 'imgs', 'enset.jpg')
    fili = os.path.join(store_dir, 'imgs', 'filigrane.jpg')
        
    # logo_ud_path = os.path.join(store_dir, 'logo_udo.jpg')
    # logo_enset_path = os.path.join(store_dir, 'logo_enset.jpg')
    # fili = os.path.join(store_dir, 'logo_enset.jpg')

    # Vérifier l'existence des fichiers d'image
    if os.path.exists(logo_ud_path):
         # Le logo ENSET est placé en haut à gauche
        c.drawImage(logo_ud_path, 15*mm, height - 40*mm, width=30*mm, height=30*mm)
    else:
        c.rect(20*mm, height - 40*mm, 20*mm, 20*mm, stroke=1)
        c.drawString(25*mm, height - 30*mm, "Logo ENSET")

    if os.path.exists(logo_enset_path):
        # Le logo de l'Université de Douala est placé en haut à droite, au-dessus de la photo
        c.drawImage(logo_enset_path, width - 45*mm, height - 40*mm, width=32*mm, height=32*mm)
    else:
        c.rect(width - 40*mm, height - 40*mm, 20*mm, 20*mm, stroke=1)
        c.drawString(width - 35*mm, height - 30*mm, "Logo UD")

    if os.path.exists(fili):
        c.drawImage(fili, (width-130*mm)/2, (height-130*mm)/2, width=130*mm, height=130*mm, mask='auto') 
    else:
        c.rect(width - 80*mm, height - 40*mm, 20*mm, 20*mm, stroke=0)
            
    # Texte principal de l'en-tête (centré)
    font_path = os.path.join(store_dir, 'fonts', 'times.ttf')
    font_name = 'times'

    font_bold_path = os.path.join(store_dir, 'fonts', 'Crimson-Bold.ttf')
    font_bold_name = 'Crimson-Bold'


    pdfmetrics.registerFont(TTFont(font_bold_name, font_bold_path))
    pdfmetrics.registerFont(TTFont(font_name, font_path))

    c.setFont(font_name, 20)
    c.setFillColor(couleur_bleu_ud)
    c.drawCentredString(width/2, height - 17*mm, "UNIVERSITÉ DE DOUALA")

    c.setStrokeColorRGB(0,0,0)
    c.setLineWidth(0.5)
    c.line(80*mm, height - 20*mm, width - 80*mm, height - 20*mm)

    c.setFont(font_name, 14)
    c.drawCentredString(width/2, height - 27*mm, "ÉCOLE NORMALE SUPÉRIEURE")
    c.drawCentredString(width/2, height - 32*mm, "D'ENSEIGNEMENT TECHNIQUE")

    c.setStrokeColorRGB(0,0,0)
    c.setLineWidth(0.5)
    c.line(85*mm, height - 35*mm, width - 85*mm, height - 35*mm)

    c.setFont(font_name, 10)
    c.drawCentredString(width/2, height - 40*mm, "BP 1872 Douala - Cameroun Tél: (Fax) (237) 33 42 44 39")
    c.drawCentredString(width/2, height - 43*mm, "www.enset-douala.cm - email: cabenset@yahoo.fr")

    
    # --- 2. TITRE DU FORMULAIRE ---
    c.setFont(font_bold_name, 20)
    c.setFillColor(couleur_bleu_ud)
    c.drawCentredString(width/2, height - 58*mm, "FICHE D'INSCRIPTION 2025-2026")
    
    c.setFont(font_bold_name, 14)
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

    # Dessin des champs, ligne par ligne
    c.setFillColor(couleur_texte_noir)
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "N° D'ORDRE :_________________")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value, y_pos, inscription.admission.id.upper())
    y_pos -= line_spacing
    
    departement_origine = inscription.departement_origine
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "NATIONALITÉ :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value, y_pos, departement_origine.region.pays.nom.upper())
    y_pos -= line_spacing

    classe = inscription.admission.classe
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "DÉPARTEMENT / FILIÈRE CHOISIE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value + 28*mm, y_pos, classe.filiere.departement.id.upper())
    y_pos -= line_spacing

    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "OPTION CHOISIE :")
    c.setFont(font_bold_name, 11)
    option =f"{classe.filiere.code_udo} {classe.niveau.id[-1]}"
    c.drawString(x_value, y_pos, option)
    y_pos -= line_spacing

    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "NOM ET PRÉNOMS :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value , y_pos, inscription.nom_complet.upper())
    y_pos -= line_spacing
    
    # Champs sur la même ligne (Date de naissance et Lieu)
    x_label2 = width/2 + 5*mm
    x_value2 = width/2 + 20*mm

    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "DATE DE NAISSANCE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value , y_pos, inscription.date_naissance.upper())

    c.setFont(font_name, 9)
    c.drawString(x_label2 - 5*mm, y_pos, "LIEU :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2 - 5*mm, y_pos, inscription.lieu_naissance.upper())
    y_pos -= line_spacing

    # Champs sur la même ligne (Sexe et Situation matrimoniale)
    x_label2 = width/2 + -10*mm
    x_value2 = width/2 + 50*mm
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "SEXE (F/M) :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value, y_pos, inscription.sexe.upper())

    c.setFont(font_name, 9)
    c.drawString(x_label2, y_pos, "SITUATION MATRIMONIALE (M/C/V) :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2, y_pos, inscription.situation_matrimoniale.upper())
    y_pos -= line_spacing

    # Champs sur la même ligne (Région et Département d'origine)
    x_label2 = width/2 + -8*mm
    x_value2 = width/2 + 43*mm
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "RÉGION D'ORIGINE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value, y_pos, departement_origine.region.nom.upper())
    
    c.setFont(font_name, 9)
    c.drawString(x_label2 + 2*mm, y_pos, "DÉPARTEMENT D'ORIGINE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2- 2*mm, y_pos, departement_origine.nom.upper())
    y_pos -= line_spacing

    # Champs sur la même ligne (Langue et Téléphone)
    x_label2 = width/2 - 2*mm
    x_value2 = width/2 + 25*mm
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "LANGUE (F/A) :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value, y_pos, inscription.langue.upper())
    
    c.setFont(font_name, 9)
    c.drawString(x_label2, y_pos, "TÉLÉPHONE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2, y_pos, inscription.telephone.upper())
    y_pos -= line_spacing

    x_label2 = width/2 + 10*mm
    x_value2 = width/2 + 33*mm
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "EMAIL :")
    c.setFont(font_bold_name, 9)
    c.drawString(x_value, y_pos, inscription.email.upper())
    
    c.setFont(font_bold_name, 9)
    c.drawString(x_label2, y_pos, "MATRICULE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2, y_pos, inscription.matricule.upper())
    y_pos -= line_spacing
    
    # Champs sur la même ligne (Diplôme et Année d'obtention)
    x_label2 = width/2 + 10*mm
    x_value2 = width/2 + 50*mm
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "DIPLÔME OBTENU :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value, y_pos, inscription.diplome.upper())
    
    c.setFont(font_name, 9)
    c.drawString(x_label2, y_pos, "ANNÉE D'OBTENTION :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2, y_pos, str(inscription.annee_diplome))
    y_pos -= line_spacing  # Espace entre les sections
    
    x_label2 = width/2
    x_value2 = width/2 + 55*mm
    # Informations des parents
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "NOM DU PÈRE/TUTEUR :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value+ 9*mm, y_pos, inscription.nom_pere.upper())
    
    
    c.setFont(font_name, 9)
    c.drawString(x_label2, y_pos, "PROFESSION DU PÈRE/TUTEUR :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2, y_pos, inscription.profession_pere.upper())
    y_pos -= line_spacing
    
    x_label2 = width/2 + 2*mm
    x_value2 = width/2 + 56*mm
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "TÉLÉPHONE DU PÈRE/TUTEUR :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value+ 19*mm, y_pos, inscription.telephone_pere.upper())
   
    
    c.setFont(font_name, 9)
    c.drawString(x_label2, y_pos, "VILLE DE RÉSIDENCE DU PÈRE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2, y_pos, inscription.ville_residence_pere.upper())
    y_pos -= line_spacing

    x_label2 = width/2 - 5*mm
    x_value2 = width/2 + 45*mm
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "NOM DE LA MÈRE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value, y_pos, inscription.nom_mere.upper())
    
    
    c.setFont(font_name, 9)
    c.drawString(x_label2, y_pos, "PROFESSION DE LA MÈRE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2, y_pos, inscription.profession_mere.upper())
    y_pos -= line_spacing
    
    x_label2 = width/2 
    x_value2 = width/2 + 60*mm
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "TÉLÉPHONE DE LA MÈRE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value+ 19*mm, y_pos, inscription.telephone_mere.upper())
    
    
    c.setFont(font_name, 9)
    c.drawString(x_label2, y_pos, "VILLE DE RÉSIDENCE DE LA MÈRE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2, y_pos, inscription.ville_residence_mere.upper())
    y_pos -= line_spacing 
    
    
    # --- 5. SIGNATURE ET CACHET ---
    # c.setFont(font_name, 10)
    # c.drawString(width - 70*mm, y_pos-6*mm, "SIGNATURE")
    # # c.line(width - 90*mm, y_pos - 25*mm, width - 30*mm, y_pos - 25*mm)
   
    # Sauvegarder le PDF
    c.save()
    return nom_fichier



def generer_fiche_correction(data, output_path):
    """
    Génère un PDF de demande de correction des erreurs d'identité
    d'un candidat définitivement admis à l'ENSET Douala.

    Paramètres:
        data (dict): Contient les données de l'étudiant.
        output_path (str): Chemin du fichier de sortie.
    """

    # tests
    data = {
        "reference": "une erreur sur mon nom et sr ma date de naissance",
        "nom": "KAPSON NJIPGUEP",
        "prenom": "ARLETTE KEVRANE",
        "date_lieu_naissance": "02 mars 2003 à DOUALA",
        "nationalite": "CAMEROUNAISE",
        "matricule": "23NII001A",
        "filiere": "Génie Informatique / Informatique Industrielle",
        "niveau": "3",
        "erreurs": [
            # {"champ": "Nom ou/et prénom", "ancien": "KAPSON NJIPGUE", "nouveau": "KAPSOH NJIPGUEP"},
            # {"champ": "Option ou/et filière choisie", "ancien": "Génie Informatique", "nouveau": "Informatique Industrielle"},
            # {"champ": "Cycle d'entrée", "ancien": "1er Cycle", "nouveau": "2e Cycle"}
        ],
        "pieces": [
            "Copie du baccalauréat",
            "Copie de la carte d'identité",
            "Attestation d'admission signée"
        ],
        "fichier_sortie": "fiche_preinscription_test.pdf"
    }

    # === Initialisation du canvas ===
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # === Couleurs ===
    couleur_bleu_ud = Color(0/255, 60/255, 120/255)
    couleur_texte_noir = black

    # === Logos et filigrane ===
    logo_ud_path = os.path.join(store_dir, 'imgs', 'udo.jpg')
    logo_enset_path = os.path.join(store_dir, 'imgs', 'enset.jpg')
    fili = os.path.join(store_dir, 'imgs', 'filigrane.jpg')
    # logo_ud_path = "static/images/univ.png"
    # logo_enset_path = "static/images/enset_.png"
    # fili = "static/images/filigrane_finale.png"

    # Logo Université de Douala (gauche)
    if os.path.exists(logo_ud_path):
        c.drawImage(logo_ud_path, 15*mm, height - 40*mm, width=30*mm, height=30*mm)
    else:
        c.rect(20*mm, height - 40*mm, 20*mm, 20*mm, stroke=1)
        c.drawString(25*mm, height - 30*mm, "Logo ENSET")

    # Logo ENSET (droite)
    if os.path.exists(logo_enset_path):
        c.drawImage(logo_enset_path, width - 45*mm, height - 40*mm, width=32*mm, height=32*mm)
    else:
        c.rect(width - 40*mm, height - 40*mm, 20*mm, 20*mm, stroke=1)
        c.drawString(width - 35*mm, height - 30*mm, "Logo UD")

    # Filigrane (centre)
    if os.path.exists(fili):
        c.drawImage(fili, (width-130*mm)/2, (height-130*mm)/2, width=130*mm, height=130*mm, mask='auto')

    # === Polices ===
    # font_path = 'static/font/times.ttf' 
    # font_name = 'times'
    # font_bold_path = 'static/font/Crimson-Bold.ttf'
    # font_bold_name = 'Crimson-Bold'

    font_path = os.path.join(store_dir, 'fonts', 'times.ttf')
    font_name = 'times'

    font_bold_path = os.path.join(store_dir, 'fonts', 'Crimson-Bold.ttf')
    font_bold_name = 'Crimson-Bold'

    pdfmetrics.registerFont(TTFont(font_bold_name, font_bold_path))
    pdfmetrics.registerFont(TTFont(font_name, font_path))

    # === En-tête principal ===
    c.setFont(font_name, 20)
    c.setFillColor(couleur_bleu_ud)
    c.drawCentredString(width/2, height - 17*mm, "UNIVERSITÉ DE DOUALA")

    c.setStrokeColorRGB(0,0,0)
    c.setLineWidth(0.5)
    c.line(80*mm, height - 20*mm, width - 80*mm, height - 20*mm)

    c.setFont(font_name, 14)
    c.drawCentredString(width/2, height - 27*mm, "ÉCOLE NORMALE SUPÉRIEURE")
    c.drawCentredString(width/2, height - 32*mm, "D'ENSEIGNEMENT TECHNIQUE")

    c.setStrokeColorRGB(0,0,0)
    c.line(85*mm, height - 35*mm, width - 85*mm, height - 35*mm)

    c.setFont(font_name, 10)
    c.drawCentredString(width/2, height - 40*mm, "BP 1872 Douala - Cameroun Tél: (Fax) (237) 33 42 44 39")
    c.drawCentredString(width/2, height - 43*mm, "www.enset-douala.cm - email: cabenset@yahoo.fr")

    c.setFillColorRGB(0,0,0)
    c.setFont(font_bold_name, 13)
    c.drawCentredString(width/2, height - 60*mm, "DEMANDE DE CORRECTION DES ERREURS RELATIVES")
    c.drawCentredString(width/2, height - 67*mm, " A UN CANDIDAT ADMIS")

    # === Informations de l'étudiant ===
    y_pos = height - 80*mm
    x_label = 20*mm
    x_value = 70*mm
    line_spacing = 8*mm

    c.setFont(font_name, 12)
    c.drawString(x_label, y_pos, "Référence du communiqué d'entrée :")
    y_pos -= line_spacing
    c.setFont(font_bold_name, 12)
    c.drawString(x_label, y_pos, data.get("reference", "Référence non précisée"))
    y_pos -= line_spacing + 5*mm

    infos = [
        ("Nom de l'étudiant :", data.get("nom", "")),
        ("Prénom(s) :", data.get("prenom", "")),
        ("Date et lieu de naissance :", data.get("naissance", "")),
        ("Matricule :", data.get("matricule", "")),
        ("Filière :", data.get("filiere", "")),
        ("Niveau :", data.get("niveau", "")),
    ]

    for label, value in infos:
        c.setFont(font_name, 12)
        c.drawString(x_label, y_pos, label)
        c.setFont(font_bold_name, 12)
        c.drawString(x_value, y_pos, value)
        y_pos -= line_spacing 
    y_pos -= 5*mm    
    c.setFont(font_name, 12) 
    c.drawString(x_label, y_pos, "Nature de l'erreur constatée: ")
    # === Tableau des erreurs ===
    y_table_start = height - 157*mm
    data_table = [
        ["L'Erreur porte sur", "Il est écrit (erreur mentionnée sur \n le communiqué)", 'Lire (correction sollicitée)'],
        ["Le Nom ou/et le prénom", "", ""],
        ["L'option ou/et filière choisie", "", ""],
        ["Cycle d'entrée", "", ""]
    ]
    table_data = [
    ["L'Erreur porte sur", "Il est écrit (erreur mentionnée sur \n le communiqué)", "Lire (correction sollicitée)"]
    ]

    for err in data.get("erreurs", []):
        table_data.append([
            str(err.get("champ", "")),
            str(err.get("ancien", "")),
            str(err.get("nouveau", ""))
        ])

    # Si aucune erreur
    if len(table_data) == 1:
        table_data.append(["(aucune erreur spécifiée)", "", ""])

    col_widths = [50 * mm, 62 * mm, 62 * mm] 
    row_heights = [13 * mm for _ in range(len(table_data))]
    # row_heights = [13 * mm, 13 * mm, 13 * mm, 13 * mm]

    t = Table(table_data, colWidths=col_widths, rowHeights=row_heights)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
        ('FONTNAME', (0, 0), (-1, 0), font_bold_name),
        ('FONTNAME', (0,1), (-1,-1), font_name),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    table_width, table_height = t.wrapOn(c, 0, 0)
    y_table_pos = y_table_start - table_height
    t.drawOn(c, x_label, y_table_pos)

    y_pos = y_table_pos - 15*mm
    c.setFont(font_name, 12)
    c.drawString(x_label, y_pos, "Pièces justificatives fournies :")
    y_pos -= line_spacing
    c.setFont(font_bold_name, 12)
    pieces_text = ", ".join(data.get("pieces", [])) if isinstance(data.get("pieces"), list) else str(data.get("pieces"))
    c.drawString(x_label, y_pos, pieces_text)


    y_pos -= 25*mm
    c.setFont(font_name, 12)
    c.drawString(x_label + 120*mm, y_pos, "Signature de l'étudiant")

    # === Sauvegarde ===
    c.save()
    return output_path

