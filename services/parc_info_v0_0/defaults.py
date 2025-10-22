
from core.config import db
from core.utils import Stat, Alert


def init_stats(user):
    stats = []
    if user.has_role('developper'):
        stats.extend([
            Stat('Parc informatique', 'Équipements', value='142 (dont 12 en panne)', rank=0),
            Stat('Parc informatique', 'Tickets ouverts', value="8 (dont 2 urgents)", rank=1),
            Stat('Parc informatique', 'Mouvements du mois', value='24 (12 entrées, 12 sorties)', rank=2),
            Stat('Parc informatique', 'Interventions', value='15', rank=3)
        ])
    return stats


def init_alerts(user):
    alerts = []
    if user.has_role('developper'):
        alerts.extend([
            Alert('Nouvel équipement ajouté', 'PC Portable Dell XPS 15 - Il y a 15 minutes', icon='bi bi-laptop', priority=1),
            Alert('Nouveau ticket créé', '#TKT-2023-045 - Il y a 2 heures', icon='bi bi-ticket', priority=1),
            Alert('Mouvement enregistré', 'Sortie matériel pour M. Dupont - Hier, 14:30', icon='bi bi-box-arrow-down', priority=1),
            Alert('Intervention terminée', 'Intervention terminée sur imprimante salle B12 - Hier, 11:45', icon='bi bi-tools', priority=1)
        ])
    return alerts

