
import os
import re
import pandas as pd
from .models import db, Preinscription


store_dir = os.path.join(os.path.dirname(__file__), 'store')




def list_departements():
    filepath = os.path.join(store_dir, 'departements.csv')
    df = pd.read_csv(filepath, sep=';')
    records = df.to_dict('records')
    return records

def list_options():
    filepath = os.path.join(store_dir, 'options.csv')
    df = pd.read_csv(filepath, sep=';')
    records = df.to_dict('records')
    return records


def check_admis(data):
    filepath = os.path.join(store_dir, 'admis.csv')
    df = pd.read_csv(filepath, sep=';')
    nom = ' '.join([data['nom'], data.get('prenom', '')])
    nom = re.sub('\s+', ' ', nom)
    filtre = df[(df['noms']==nom) & (df['option']==data['option'])]
    return not filtre.empty


def save_request(data):
    pass

def save_preinscription(data):
    pass


def generate_request(matricule):
    pass


def generate_inscription(matricule):
    pass

