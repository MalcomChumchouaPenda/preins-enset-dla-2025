
import os
import re
import csv
from io import BytesIO
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
from .models import db, Preinscription


store_dir = os.path.join(os.path.dirname(__file__), 'store')


def list_departements():
    filepath = os.path.join(store_dir, 'departements.csv')
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file, delimiter=';')
        records = list(reader)
    return records

def list_options():
    filepath = os.path.join(store_dir, 'options.csv')
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file, delimiter=";")
        records = list(reader)
    return records


def check_admis(data):
    filepath = os.path.join(store_dir, 'admis.csv')
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file, delimiter=';')
        records = []
        for row in reader:
            nom = ' '.join([data['nom'], data.get('prenom', '')])
            nom = re.sub('\s+', ' ', nom)
            if row['noms'] == nom  and row['option'] == data['option']:
                records.append(row)
    return len(records) > 0



def generer_fiche_inscription(data, nom_fichier):
    """
    Génère un PDF de fiche d'inscription ENSET avec des coordonnées fixes et la photo de l'étudiant.

    Args:
        data (dict): Dictionnaire contenant les informations de l'étudiant.
        nom_fichier (str): Nom du fichier de sortie.
    """

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
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "N° D'ORDRE :_________________")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value, y_pos, data.get('num_ordre', '').upper())
    y_pos -= line_spacing
    
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "NATIONALITÉ :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value, y_pos, data.get('nationalite', '').upper())
    y_pos -= line_spacing

    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "DÉPARTEMENT / FILIÈRE CHOISIE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value + 28*mm, y_pos, data.get('departement', '').upper())
    y_pos -= line_spacing

    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "OPTION CHOISIE :")
    c.setFont(font_bold_name, 11)
    option =f"{data.get('option', '').upper()} {data.get('niveau', '').upper()}"
    c.drawString(x_value, y_pos, option)
    y_pos -= line_spacing

    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "NOM ET PRÉNOMS :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value , y_pos, data.get('nom_prenom', '').upper())
    y_pos -= line_spacing
    
    # Champs sur la même ligne (Date de naissance et Lieu)
    x_label2 = width/2 + 5*mm
    x_value2 = width/2 + 20*mm

    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "DATE DE NAISSANCE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value , y_pos, date_formatee.upper())

    c.setFont(font_name, 9)
    c.drawString(x_label2 - 5*mm, y_pos, "LIEU :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2 - 5*mm, y_pos, data.get('lieu_naissance', '').upper())
    y_pos -= line_spacing

    # Champs sur la même ligne (Sexe et Situation matrimoniale)
    x_label2 = width/2 + -10*mm
    x_value2 = width/2 + 50*mm
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "SEXE (F/M) :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value, y_pos, data.get('sexe', '').upper())

    c.setFont(font_name, 9)
    c.drawString(x_label2, y_pos, "SITUATION MATRIMONIALE (M/C/D) :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2, y_pos, data.get('situation_matrimoniale', '').upper())
    y_pos -= line_spacing

    # Champs sur la même ligne (Région et Département d'origine)
    x_label2 = width/2 + -8*mm
    x_value2 = width/2 + 43*mm
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "RÉGION D'ORIGINE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value, y_pos, data.get('region_origine', '').upper())
    
    c.setFont(font_name, 9)
    c.drawString(x_label2 + 2*mm, y_pos, "DÉPARTEMENT D'ORIGINE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2- 2*mm, y_pos, data.get('departement_origine', '').upper())
    y_pos -= line_spacing

    # Champs sur la même ligne (Langue et Téléphone)
    x_label2 = width/2 - 2*mm
    x_value2 = width/2 + 25*mm
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "LANGUE (F/A) :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value, y_pos, data.get('langue', '').upper())
    
    c.setFont(font_name, 9)
    c.drawString(x_label2, y_pos, "TÉLÉPHONE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2, y_pos, data.get('telephone', '').upper())
    y_pos -= line_spacing

    x_label2 = width/2 + 10*mm
    x_value2 = width/2 + 33*mm
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "EMAIL :")
    c.setFont(font_bold_name, 9)
    c.drawString(x_value, y_pos, data.get('email', '').upper())
    
    c.setFont(font_bold_name, 9)
    c.drawString(x_label2, y_pos, "MATRICULE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2, y_pos, data.get('matricule', '').upper())
    y_pos -= line_spacing
    
    # Champs sur la même ligne (Diplôme et Année d'obtention)
    x_label2 = width/2 + 10*mm
    x_value2 = width/2 + 50*mm
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "DIPLÔME OBTENU :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value, y_pos, data.get('diplome', '').upper())
    
    c.setFont(font_name, 9)
    c.drawString(x_label2, y_pos, "ANNÉE D'OBTENTION :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2, y_pos, str(data.get('annee_diplome', '')))
    y_pos -= line_spacing  # Espace entre les sections
    
    x_label2 = width/2
    x_value2 = width/2 + 55*mm
    # Informations des parents
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "NOM DU PÈRE/TUTEUR :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value+ 9*mm, y_pos, data.get('nom_pere', '').upper())
    
    
    c.setFont(font_name, 9)
    c.drawString(x_label2, y_pos, "PROFESSION DU PÈRE/TUTEUR :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2, y_pos, data.get('profession_pere', '').upper())
    y_pos -= line_spacing
    
    x_label2 = width/2 + 2*mm
    x_value2 = width/2 + 56*mm
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "TÉLÉPHONE DU PÈRE/TUTEUR :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value+ 19*mm, y_pos, data.get('telephone_pere', '').upper())
   
    
    c.setFont(font_name, 9)
    c.drawString(x_label2, y_pos, "VILLE DE RÉSIDENCE DU PÈRE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2, y_pos, data.get('ville_residence_pere', '').upper())
    y_pos -= line_spacing

    x_label2 = width/2 - 5*mm
    x_value2 = width/2 + 45*mm
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "NOM DE LA MÈRE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value, y_pos, data.get('nom_mere', '').upper())
    
    
    c.setFont(font_name, 9)
    c.drawString(x_label2, y_pos, "PROFESSION DE LA MÈRE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2, y_pos, data.get('profession_mere', '').upper())
    y_pos -= line_spacing
    
    x_label2 = width/2 
    x_value2 = width/2 + 60*mm
    c.setFont(font_name, 9)
    c.drawString(x_label, y_pos, "TÉLÉPHONE DE LA MÈRE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value+ 19*mm, y_pos, data.get('telephone_mere', '').upper())
    
    
    c.setFont(font_name, 9)
    c.drawString(x_label2, y_pos, "VILLE DE RÉSIDENCE DE LA MÈRE :")
    c.setFont(font_bold_name, 11)
    c.drawString(x_value2, y_pos, data.get('ville_residence_mere', '').upper())
    y_pos -= line_spacing 
    
    
    # --- 5. SIGNATURE ET CACHET ---
    # c.setFont(font_name, 10)
    # c.drawString(width - 70*mm, y_pos-6*mm, "SIGNATURE")
    # # c.line(width - 90*mm, y_pos - 25*mm, width - 30*mm, y_pos - 25*mm)
   
    # Sauvegarder le PDF
    c.save()
    return nom_fichier



def generer_fiche_correction(data, output_path="fiche_correction.pdf"):
    """
    Génère un PDF de demande de correction des erreurs d'identité
    d’un candidat définitivement admis à l’ENSET Douala.

    Paramètres:
        data (dict): Contient les données de l'étudiant.
        output_path (str): Chemin du fichier de sortie.
    """

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
    c.drawCentredString(width/2, height - 60*mm, "DEMANDE DE CORRECTION DES ERREURS SUR L'IDENTITÉ D'UN")
    c.drawCentredString(width/2, height - 67*mm, "CANDIDAT DÉFINITIVEMENT ADMIS")

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
    row_heights = [13 * mm, 13 * mm, 13 * mm, 13 * mm]

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

