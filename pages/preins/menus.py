
from core.utils import sidebar
from flask_babel import lazy_gettext as _l


menu = sidebar.add('preins_menu', _l('Preinscription'), rank=0, accepted=['developper'])
menu.add('preins_info_pg', 'Fiche', endpoint='preins.info', rank=0)
menu.add('preins_error_pg', 'Requete', endpoint='preins.error', rank=1)

# menu = sidebar.add('parc-info', _l('Parc informatique'), rank=0, accepted=['developper'])
# menu.add('equipements', 'Équipements', endpoint='parc_info.equipements', rank=0)
# menu.add('mouvements', 'Mouvements', endpoint='parc_info.mouvements', rank=1)
# menu.add('tickets', 'Tickets', endpoint='parc_info.tickets', rank=2)
# menu.add('interventions', 'Interventions', endpoint='parc_info.interventions', rank=3)
# menu.add('rapports', 'Rapports', endpoint='parc_info.rapports', rank=4)

