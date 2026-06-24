from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Libro, Copia, Prestito, Recensione, Evento, Iscrizione, Evento, Iscrizione
from .forms import RegistrazioneForm


def home(request):
    return render(request, 'catalogo/home.html')


def catalogo_libri(request):
    query = request.GET.get('q', '')
    libri = Libro.objects.all()
    if query:
        libri = libri.filter(
            Q(titolo__icontains=query) |
            Q(autori__nome__icontains=query) |
            Q(autori__cognome__icontains=query) |
            Q(categoria__icontains=query)
        ).distinct()
    return render(request, 'catalogo/catalogo_libri.html', {'libri': libri, 'query': query})


def dettaglio_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    recensioni = libro.recensioni.all().order_by('-data')
    return render(request, 'catalogo/dettaglio_libro.html', {'libro': libro, 'recensioni': recensioni})


def registrazione(request):
    if request.method == 'POST':
        form = RegistrazioneForm(request.POST)
        if form.is_valid():
            utente = form.save()
            login(request, utente)
            return redirect('catalogo_libri')
    else:
        form = RegistrazioneForm()
    return render(request, 'catalogo/registrazione.html', {'form': form})


def login_utente(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            utente = authenticate(request, username=username, password=password)
            if utente is not None:
                login(request, utente)
                return redirect('catalogo_libri')
    else:
        form = AuthenticationForm()
    return render(request, 'catalogo/login.html', {'form': form})


def logout_utente(request):
    logout(request)
    return redirect('home')


@login_required
def prestito_libro(request, copia_id):
    copia = get_object_or_404(Copia, id=copia_id)
    if copia.stato == 'disponibile':
        Prestito.objects.create(
            utente=request.user,
            copia=copia,
            data_restituzione_prevista=timezone.now().date() + timedelta(days=30),
        )
        copia.stato = 'prestata'
        copia.save()
        messages.success(request, 'Prestito registrato con successo.')
    else:
        messages.error(request, 'Questa copia non è disponibile per il prestito.')
    return redirect('dettaglio_libro', libro_id=copia.libro.id)


@login_required
def restituzione_libro(request, prestito_id):
    prestito = get_object_or_404(Prestito, id=prestito_id, utente=request.user)
    if prestito.data_restituzione_effettiva is None:
        prestito.data_restituzione_effettiva = timezone.now().date()
        prestito.save()
        prestito.copia.stato = 'disponibile'
        prestito.copia.save()
        messages.success(request, 'Restituzione registrata.')
    return redirect('miei_prestiti')


@login_required
def miei_prestiti(request):
    prestiti = Prestito.objects.filter(utente=request.user).order_by('-data_richiesta')
    return render(request, 'catalogo/miei_prestiti.html', {'prestiti': prestiti})


@login_required
def aggiungi_recensione(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if request.method == 'POST':
        voto = request.POST.get('voto')
        commento = request.POST.get('commento', '')
        if voto:
            Recensione.objects.update_or_create(
                utente=request.user,
                libro=libro,
                defaults={'voto': int(voto), 'commento': commento}
            )
            messages.success(request, 'Recensione salvata.')
    return redirect('dettaglio_libro', libro_id=libro_id)

def lista_eventi(request):
    eventi = Evento.objects.all().order_by('data')
    return render(request, 'catalogo/lista_eventi.html', {'eventi': eventi})


def dettaglio_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    iscritto = False
    if request.user.is_authenticated:
        iscritto = Iscrizione.objects.filter(utente=request.user, evento=evento).exists()
    return render(request, 'catalogo/dettaglio_evento.html', {'evento': evento, 'iscritto': iscritto})


@login_required
def iscrizione_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    iscrizione, creata = Iscrizione.objects.get_or_create(utente=request.user, evento=evento)
    if creata:
        messages.success(request, 'Iscrizione completata con successo.')
    else:
        messages.info(request, 'Sei gia iscritto a questo evento.')
    return redirect('dettaglio_evento', evento_id=evento_id)


@login_required
def cancella_iscrizione(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    Iscrizione.objects.filter(utente=request.user, evento=evento).delete()
    messages.success(request, 'Iscrizione cancellata.')
    return redirect('dettaglio_evento', evento_id=evento_id)
