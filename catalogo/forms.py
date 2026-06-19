from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utente, Studente, Docente


class RegistrazioneForm(UserCreationForm):
    tipo_utente = forms.ChoiceField(choices=Utente.TIPO_CHOICES, label="Tipo di utente")
    first_name = forms.CharField(label="Nome", max_length=150)
    last_name = forms.CharField(label="Cognome", max_length=150)
    email = forms.EmailField(label="Email")

    matricola = forms.CharField(required=False, label="Matricola")
    corso_laurea = forms.CharField(required=False, label="Corso di laurea")
    anno_iscrizione = forms.IntegerField(required=False, label="Anno di iscrizione")

    codice_docente = forms.CharField(required=False, label="Codice docente")
    dipartimento = forms.CharField(required=False, label="Dipartimento")
    ambito_ricerca = forms.CharField(required=False, label="Ambito di ricerca")

    class Meta:
        model = Utente
        fields = ['username', 'first_name', 'last_name', 'email', 'tipo_utente', 'password1', 'password2']

    def save(self, commit=True):
        utente = super().save(commit=False)
        utente.tipo_utente = self.cleaned_data['tipo_utente']
        if commit:
            utente.save()
            if utente.tipo_utente == 'studente':
                Studente.objects.create(
                    utente=utente,
                    matricola=self.cleaned_data['matricola'],
                    corso_laurea=self.cleaned_data['corso_laurea'],
                    anno_iscrizione=self.cleaned_data['anno_iscrizione'],
                )
            elif utente.tipo_utente == 'docente':
                Docente.objects.create(
                    utente=utente,
                    codice_docente=self.cleaned_data['codice_docente'],
                    dipartimento=self.cleaned_data['dipartimento'],
                    ambito_ricerca=self.cleaned_data['ambito_ricerca'],
                )
        return utente