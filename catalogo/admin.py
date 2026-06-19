from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Utente, Studente, Docente, Autore, Libro, Copia,
    Prestito, Recensione, Evento, Iscrizione, Personale
)

admin.site.register(Utente, UserAdmin)
admin.site.register(Studente)
admin.site.register(Docente)
admin.site.register(Autore)
admin.site.register(Libro)
admin.site.register(Copia)
admin.site.register(Prestito)
admin.site.register(Recensione)
admin.site.register(Evento)
admin.site.register(Iscrizione)
admin.site.register(Personale)