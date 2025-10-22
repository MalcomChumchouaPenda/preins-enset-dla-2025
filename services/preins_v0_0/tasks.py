
import os
import re
import csv
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


def save_request(data):
    pass

def save_preinscription(data):
    pass


def generate_request(matricule):
    pass


def generate_inscription(matricule):
    pass

