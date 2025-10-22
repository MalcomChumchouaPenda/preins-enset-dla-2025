

from services.preins_v0_0 import tasks


SEXES = [('F', 'Feminin'), ('M', 'Masculin')]
STATUTS = [('C', 'Celibataire'), ('M', 'Marie(e)'), ('V', 'Veuf(ve)')]
LANGUES = [('FR', 'Francais'), ('EN', 'Anglais')]
NIVEAUX = ['Niveau 1', 'Niveau 3', 'Niveau 4']
NATIONALITE = ['Camerounaise', 'Tchadienne', 'Centrafricaine',
               'Congolaise', 'Gabonaise', 'Equato-guineenne']


def departements():
    return [(r['numero'], r['departement']) for r in tasks.list_departements()]

def options():
    return list(set([(r['code_filiere'], r['nom']) for r in tasks.list_options()]))

