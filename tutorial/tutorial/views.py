from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import get_renderer
from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    Dossier,
    )

def testage():
    print('c ok')


def site_layout():
    renderer = get_renderer("templates/global.pt")
    layout = renderer.implementation().macros['layout']
    return layout

@view_config(route_name='home', renderer='templates/accueil.pt')
def my_view(request):
    if request.method == 'POST':
        entree=request.POST.getone('caca2')
        nouveau_doss = Dossier(nom_dos=entree)
        DBSession.add(nouveau_doss)
        return {"nom_dossier_donne": entree, "layout": site_layout(), "page_title": "Accueil"}
    else:
        return {"nom_dossier_donne": "'C\'est votre première visite, ajoutez donc un dossier.", "layout": site_layout(), "page_title": "Accueil"}
        

@view_config(route_name='list', renderer='templates/liste.pt')
def reservations(request):
    liste_dossiers=DBSession.query(Dossier).all()
    rendu=dict()
    for i in range(len(liste_dossiers)):
        dossier = liste_dossiers[i]
        nom = dossier.nom_dos
        print(dossier)
        rendu[i]=nom
        i+=1
    liste = str()
    for i in range(len(rendu)):
        liste+=(rendu.get(i))
        liste+="\n | "
        i+=1
    return {"rendu": liste, "layout": site_layout(), "page_title": "LaListe"}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_tutorial_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

