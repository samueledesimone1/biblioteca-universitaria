from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo_libri, name='catalogo_libri'),
    path('libro/<int:libro_id>/', views.dettaglio_libro, name='dettaglio_libro'),
    path('registrazione/', views.registrazione, name='registrazione'),
    path('login/', views.login_utente, name='login'),
    path('logout/', views.logout_utente, name='logout'),
    path('copia/<int:copia_id>/prestito/', views.prestito_libro, name='prestito_libro'),
    path('prestito/<int:prestito_id>/restituzione/', views.restituzione_libro, name='restituzione_libro'),
    path('miei-prestiti/', views.miei_prestiti, name='miei_prestiti'),
]