
from core.utils import sidebar, navbar
from flask_babel import lazy_gettext as _l


navbar.add('preins_doc_pg', _l('Procedures'), endpoint='preins.doc')
navbar.add('preins_info_pg', _l('Inscriptions'), endpoint='preins.info')

dashmenu = sidebar.add('preins_menu', _l('Inscription'), rank=0, accepted=['developper', 'admis'])
dashmenu.add('preins_info_pg', 'Fiche', endpoint='preins.info', rank=0)
# dashmenu.add('preins_error_pg', 'Requete', endpoint='preins.error', rank=1)
dashmenu.add('preins_error_pg', 'Requete', endpoint='preins.coming', rank=1)


