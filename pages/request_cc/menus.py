
from core.utils import sidebar, navbar

menu = navbar.add('request', 'Requetes Test')
menu.add('soumettre', 'Soumettre une requete', endpoint='request_cc.index')
menu.add('traiter', 'Traiter des requetes', endpoint='request_cc.get_teacher')

menu = sidebar.add('request', 'Requetes CC')
menu.add('soumettre', 'Mes requetes', endpoint='request_cc.index', accepted=['student'])
menu.add('send-requete', 'Soumettre une requete', endpoint='request_cc.send_requete', accepted=['student'])
menu.add('traiter', 'Traitement', endpoint='request_cc.get_teacher', accepted=['teacher', 
                                                                               'chef_depart', 
                                                                               'cellule'])
