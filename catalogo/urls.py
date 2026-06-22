from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo_libri, name='catalogo_libri'),
    path('libro/<int:libro_id>/', views.dettaglio_libro, name='dettaglio_libro'),
    path('registrazione/', views.registrazione, name='registrazione'),
    path('login/', views.login_utente, name='login'),
    path('logout/', views.logout_utente, name='logout'),
    path('copia/<int:copia_id>/prestito/', views.prestito_libro, name='prestito_libro'),
    path('prestito/<int:prestito_id>/restituzione/', views.restituzione_libro, name='restituzione_libro'),
    path('miei-prestiti/', views.miei_prestiti, name='miei_prestiti'),
    path('libro/<int:libro_id>/recensione/', views.aggiungi_recensione, name='aggiungi_recensione'),
    path('eventi/', views.lista_eventi, name='lista_eventi'),
    path('evento/<int:evento_id>/', views.dettaglio_evento, name='dettaglio_evento'),
    path('evento/<int:evento_id>/iscrizione/', views.iscrizione_evento, name='iscrizione_evento'),
    path('evento/<int:evento_id>/cancella-iscrizione/', views.cancella_iscrizione, name='cancella_iscrizione'),
]