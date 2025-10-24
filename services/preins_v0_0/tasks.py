
import os
from datetime import datetime
from sqlalchemy.exc import IntegrityError

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

from core.auth.tasks import add_user, add_roles_to_user
from core.auth.models import User
from services.formations_v0_0.models import Classe
from services.regions_v0_0.models import Departement
from services.regions_v0_0 import tasks as region_tasks
from .models import db, Inscription, Admission, Requete


store_dir = os.path.join(os.path.dirname(__file__), 'store')


def lister_nationalites():
    items = region_tasks.list_nationalites(full_id=True)
    items.insert(0, ('', 'Choisir...'))
    return items

def lister_regions():
    items = region_tasks.list_regions(full_id=True)
    items.insert(0, ('', 'Choisir...'))
    return items

def lister_departements():
    items = region_tasks.list_departements(full_id=True)
    print(items)
    items.insert(0, ('', 'Choisir...'))
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


def ajouter_inscription(data):
    session = db.session
    inscription = Inscription(**data)
    creer_matricule(session, inscription)
    session.add(inscription)
    session.commit()
    
def creer_matricule(session, inscription):
    admission = chercher_admission(inscription.admission_id)
    # print(admission.communique_id, admission.communique)
    annee = admission.communique.annee_academique[2:4]
    statut = admission.statut[0]
    classe = admission.classe
    prefix = classe.filiere.prefix
    niveau = classe.niveau.id[-1]

    if niveau == '4':
        num_size = 2
        filtre = f'{annee}N{prefix}L%{statut}'
    elif niveau == '3':
        num_size = 2
        filtre = f'{annee}N{prefix}B%{statut}'
    else:
        num_size = 3
        filtre = f'{annee}N{prefix}%{statut}'

    # print('\nfuser', session.query(User).all())
    for i in range(10):
        try:
            count = session.query(User).filter(User.id.like(filtre)).count()
            # print('\n\tfilter', i, filtre, count)
            num = str(count + 1).rjust(num_size, '0')
            matricule = filtre.replace('%', num)
            add_user(session, matricule, inscription.nom, '0000', first_name=inscription.prenom)
            add_roles_to_user(session, matricule, 'student')
            admission.matricule = matricule
            return matricule
        except IntegrityError as e:
            session.rollback()


def modifier_inscription(data):
    session = db.session
    inscription = Inscription(**data)
    session.add(inscription)
    session.commit()
    

def creer_inscription(user_id):
    inscription = Inscription(admission_id=user_id)
    return inscription

def rechercher_inscription(user_id):
    query = db.session.query(Inscription)
    query = query.filter_by(admission_id=user_id)
    query = query.order_by(Inscription.id.desc())
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

    c.setFont(font_name, 16)
    c.setFillColor(couleur_bleu_ud)
    c.drawCentredString(width/2, height - 15*mm, "UNIVERSITÉ DE DOUALA")

    c.setStrokeColorRGB(0,0,0)
    c.setLineWidth(0.5)
    c.line(80*mm, height - 18*mm, width - 80*mm, height - 18*mm)

    c.setFont(font_name, 12)
    c.drawCentredString(width/2, height - 25*mm, "ÉCOLE NORMALE SUPÉRIEURE")
    c.drawCentredString(width/2, height - 30*mm, "D'ENSEIGNEMENT TECHNIQUE")

    c.setStrokeColorRGB(0,0,0)
    c.setLineWidth(0.5)
    c.line(85*mm, height - 33*mm, width - 85*mm, height - 33*mm)

    c.setFont(font_name, 10)
    c.drawCentredString(width/2, height - 39*mm, "BP 1872 Douala - Cameroun Tél: (Fax) (237) 33 42 44 39")
    c.drawCentredString(width/2, height - 43*mm, "www.enset-douala.cm - email: cabenset@yahoo.fr")

    
    # --- 2. TITRE DU FORMULAIRE ---
    admission = inscription.admission
    communique = admission.communique
    c.setFont(font_bold_name, 18)
    c.setFillColor(couleur_bleu_ud)
    c.drawCentredString(width/2, height - 58*mm, f"FICHE D'INSCRIPTION {communique.annee_academique}")
    
    classe = admission.classe
    formation = classe.filiere.formation
    c.setFont(font_bold_name, 14)
    c.drawCentredString(width/2, height - 68*mm, formation.nom.upper())

    # --- 3. NOTE IMPORTANTE ---
    # c.setFont("Helvetica-Oblique", 9)
    # c.setFillColor(couleur_texte_noir)
    # c.drawString(20*mm, height - 71*mm, "NB : À faire remplir par le candidat lui-même car ses informations sont d'une importance capitale pour la")
    # c.drawString(20*mm, height - 75*mm, "délivrance des effets académiques.")

    # --- 4. CHAMPS DU FORMULAIRE AVEC COORDONNÉES FIXES ---

    # DEFINITION DES COORDONNEES

    # le premier systeme de coordonnee a deux colonnes
    x_a1 = 20*mm
    x_a2 = width/2

    # le second systeme de coordonnee a trois colonnes
    x_b1 = x_a1
    x_b2 = x_a2 - 20*mm
    x_b3 = x_a2 + 25*mm

    # le systeme d'ecart entre les lignes
    y_a = height - 85*mm
    dy_a = 9*mm
    dy_b = 12*mm


    # MATRICULE + NUM DOSSIER PHYSIQUE

    c.setFillColor(couleur_texte_noir)
    c.setFont(font_name, 9)
    c.drawString(x_b1, y_a, "N° D'ORDRE :")
    c.setFillColor(couleur_bleu_ud)
    c.setFont(font_bold_name, 10)
    c.drawString(x_b1 + 22*mm, y_a, admission.id)

    c.setFillColor(couleur_texte_noir)
    c.setFont(font_name, 9)
    c.drawString(x_b3, y_a, "MATRICULE :")
    c.setFillColor(couleur_bleu_ud)
    c.setFont(font_bold_name, 10)
    c.drawString(x_b3 + 22*mm, y_a, admission.matricule)
    y_a -= dy_b


    # INFORMATIONS GENERALES
        
    c.setFillColor(couleur_texte_noir)
    c.setFont(font_name, 9)
    c.drawString(x_a1, y_a, "NOM ET PRÉNOMS :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_a1 + 32*mm, y_a, inscription.nom_complet.upper())
    y_a -= dy_a

    c.setFont(font_name, 9)
    c.drawString(x_b1, y_a, "DATE DE NAISSANCE :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_b1 + 36*mm, y_a, inscription.date_naissance)

    c.setFont(font_name, 9)
    c.drawString(x_b2, y_a, "LIEU :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_b2 + 11*mm, y_a, inscription.lieu_naissance.upper())
    y_a -= dy_a

    c.setFont(font_name, 9)
    c.drawString(x_b1, y_a, "SEXE (F/M) :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_b1 + 20*mm, y_a, inscription.sexe_complet.upper())

    c.setFont(font_name, 9)
    c.drawString(x_b2, y_a, "SITUATION MATRIMONIALE (M/C/D) :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_b2 + 58*mm, y_a, inscription.situation_matrimoniale_complete.upper())
    y_a -= dy_b


    # ORIGINE GEOGRAPHIQUE

    c.setFont(font_name, 9)
    c.drawString(x_b1, y_a, "LANGUE (F/A) :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_b1 + 25*mm, y_a, inscription.langue_complete.upper())

    departement_origine = inscription.departement_origine
    region = departement_origine.region
    pays = region.pays
    
    c.setFont(font_name, 9)
    c.drawString(x_b2, y_a, "NATIONALITÉ :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_b2 + 25*mm, y_a, pays.nationalite.upper())
    y_a -= dy_a

    c.setFont(font_name, 9)
    c.drawString(x_b1, y_a, "RÉGION D'ORIGINE :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_b1 + 31*mm, y_a, region.nom.upper())
    
    c.setFont(font_name, 9)
    c.drawString(x_b2, y_a, "DÉPARTEMENT D'ORIGINE :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_b2 + 43*mm, y_a, departement_origine.nom.upper())
    y_a -= dy_b


    # TELEPHONES + EMAIL

    c.setFont(font_name, 9)
    c.drawString(x_a1, y_a, "TÉLÉPHONE :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_a1 + 22*mm, y_a, inscription.telephone)

    c.setFont(font_name, 9)
    c.drawString(x_a2, y_a, "EMAIL :")
    c.setFont(font_bold_name, 9)
    c.drawString(x_a2 + 14*mm, y_a, inscription.email)
    y_a -= dy_b


    # INFORMATIONS ACADEMIQUES
    departement_acad = classe.filiere.departement
    c.setFont(font_name, 9)
    c.drawString(x_a1, y_a, "DÉPARTEMENT CHOISIE :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_a1 + 40*mm, y_a, f'{departement_acad.id}-{departement_acad.nom}'.upper())
    y_a -= dy_a

    c.setFont(font_name, 9)
    c.drawString(x_a1, y_a, "OPTION CHOISIE :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_a1 + 28*mm, y_a, f"{classe.code_complet}-{classe.filiere.nom}".upper())
    y_a -= dy_a

    c.setFont(font_name, 9)
    c.drawString(x_b1, y_a, "DIPLÔME OBTENU :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_b1 + 31*mm, y_a, inscription.diplome.upper())
    
    c.setFont(font_name, 9)
    c.drawString(x_b3, y_a, "ANNÉE D'OBTENTION :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_b3 + 36*mm, y_a, str(inscription.annee_diplome))
    y_a -= dy_b

    
    # INFO DU PERE
    c.setFont(font_name, 9)
    c.drawString(x_b1, y_a, "NOM DU PÈRE/TUTEUR :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_b1 + 38*mm, y_a, inscription.nom_pere.upper())
    y_a -= dy_a
    
    c.setFont(font_name, 9)
    c.drawString(x_b1, y_a, "PROFESSION DU PÈRE/TUTEUR :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_b1 + 50*mm, y_a, inscription.profession_pere.upper())
    y_a -= dy_a
    
    c.setFont(font_name, 9)
    c.drawString(x_a1, y_a, "TÉL. DU PÈRE/TUTEUR :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_a1 + 37*mm, y_a, inscription.telephone_pere.upper())
   
    
    c.setFont(font_name, 9)
    c.drawString(x_a2, y_a, "RÉSIDENCE :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_a2 + 20*mm, y_a, inscription.residence_pere.upper())
    y_a -= dy_b


    # INFO DE LA MERE

    c.setFont(font_name, 9)
    c.drawString(x_b1, y_a, "NOM DE LA MÈRE :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_b1 + 30*mm, y_a, inscription.nom_mere.upper())
    y_a -= dy_a
    
    c.setFont(font_name, 9)
    c.drawString(x_b1, y_a, "PROFESSION DE LA MÈRE :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_b1 + 42*mm, y_a, inscription.profession_mere.upper())
    y_a -= dy_a
    
    c.setFont(font_name, 9)
    c.drawString(x_a1, y_a, "TÉL. DE LA MÈRE :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_a1 + 30*mm, y_a, inscription.telephone_mere.upper())
    
    c.setFont(font_name, 9)
    c.drawString(x_a2, y_a, "RÉSIDENCE :")
    c.setFont(font_bold_name, 10)
    c.drawString(x_a2 + 20*mm, y_a, inscription.residence_mere.upper())
    y_a -= dy_b 
    
   
    
    # SIGNATURE ET CACHET
    c.setFont(font_name, 10)
    c.drawString(width - 70*mm, y_a-10*mm, "SIGNATURE DE L'ETUDIANT(E)")
    c.line(width - 190*mm, y_a, width - 15*mm, y_a)


    # METADONNEES ---
    print_date = datetime.now().strftime('%d/%m/%Y')
    create_date = inscription.date_inscription.strftime('%d/%m/%Y')
    footer = f"fiche créée le {create_date} et generée le {print_date}"
    c.setFont(font_name, 9)
    c.drawCentredString(width/2, y_a-40*mm, footer)

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

