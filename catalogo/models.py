from django.db import models
from django.contrib.auth.models import AbstractUser


class Utente(AbstractUser):
    TIPO_CHOICES = [
        ('studente', 'Studente'),
        ('docente', 'Docente'),
    ]
    tipo_utente = models.CharField(max_length=10, choices=TIPO_CHOICES)

    class Meta:
        verbose_name = "Utente"
        verbose_name_plural = "Utenti"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Studente(models.Model):
    utente = models.OneToOneField(Utente, on_delete=models.CASCADE, related_name='profilo_studente')
    matricola = models.CharField(max_length=20, unique=True)
    corso_laurea = models.CharField(max_length=100)
    anno_iscrizione = models.IntegerField()

    class Meta:
        verbose_name = "Studente"
        verbose_name_plural = "Studenti"

    def __str__(self):
        return f"Studente {self.matricola}"


class Docente(models.Model):
    utente = models.OneToOneField(Utente, on_delete=models.CASCADE, related_name='profilo_docente')
    codice_docente = models.CharField(max_length=20, unique=True)
    dipartimento = models.CharField(max_length=100)
    ambito_ricerca = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Docente"
        verbose_name_plural = "Docenti"

    def __str__(self):
        return f"Docente {self.codice_docente}"


class Autore(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    biografia = models.TextField(blank=True)

    class Meta:
        verbose_name = "Autore"
        verbose_name_plural = "Autori"

    def __str__(self):
        return f"{self.nome} {self.cognome}"


class Libro(models.Model):
    titolo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    anno_pubblicazione = models.IntegerField()
    categoria = models.CharField(max_length=100)
    autori = models.ManyToManyField(Autore, related_name='libri')

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libri"

    def __str__(self):
        return self.titolo


class Copia(models.Model):
    STATO_CHOICES = [
        ('disponibile', 'Disponibile'),
        ('prestata', 'Prestata'),
        ('non_accessibile', 'Non accessibile'),
    ]
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='copie')
    numero_inventario = models.CharField(max_length=30, unique=True)
    stato = models.CharField(max_length=20, choices=STATO_CHOICES, default='disponibile')

    class Meta:
        verbose_name = "Copia"
        verbose_name_plural = "Copie"

    def __str__(self):
        return f"{self.libro.titolo} - {self.numero_inventario}"


class Prestito(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='prestiti')
    copia = models.ForeignKey(Copia, on_delete=models.CASCADE, related_name='prestiti')
    data_richiesta = models.DateField(auto_now_add=True)
    data_restituzione_prevista = models.DateField()
    data_restituzione_effettiva = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Prestito"
        verbose_name_plural = "Prestiti"

    def __str__(self):
        return f"Prestito {self.copia} a {self.utente}"


class Recensione(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='recensioni')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='recensioni')
    voto = models.IntegerField()
    commento = models.TextField(blank=True)
    data = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Recensione"
        verbose_name_plural = "Recensioni"

    def __str__(self):
        return f"Recensione di {self.utente} su {self.libro}"


class Evento(models.Model):
    titolo = models.CharField(max_length=200)
    descrizione = models.TextField()
    data = models.DateTimeField()
    luogo = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventi"

    def __str__(self):
        return self.titolo


class Iscrizione(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='iscrizioni')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='iscrizioni')
    presente = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Iscrizione"
        verbose_name_plural = "Iscrizioni"

    def __str__(self):
        return f"{self.utente} -> {self.evento}"


class Personale(models.Model):
    nome = models.CharField(max_length=100)
    ruolo = models.CharField(max_length=100)
    responsabile = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinati')

    class Meta:
        verbose_name = "Membro dello staff"
        verbose_name_plural = "Personale"

    def __str__(self):
        return f"{self.nome} ({self.ruolo})"