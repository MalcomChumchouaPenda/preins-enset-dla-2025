
from core.config import db
from core.utils import Stat, Alert
from .models import Admission


def init_stats(user):
    stats = []
    if user.has_role('developper'):
        stats.extend([
            Stat('Preinscriptions', 'Nombre', value='142', rank=0),
        ])
    return stats


def init_alerts(user):
    alerts = []
    if user.has_role('developper'):
        alerts.extend([
            Alert('Vos quitus ont ete generes', 'PC Portable Dell XPS 15 - Il y a 15 minutes', icon='bi bi-laptop', priority=1),
        ])
    return alerts


data = [dict(id="dev1", nom_complet='Developpeur Testeur', classe_id='BTP1', statut='AA', communique='Fake communique')]


def init_data():
    for row in data:
        admission = Admission(**row)
        db.session.merge(admission)
    db.session.commit()

    
