from django.db import models
from django.contrib.auth.models import User
from fsmedhrocore.models import Dozent, BasicHistory, Studienabschnitt, Studiengang, Fach
from django.utils import timezone


class Pruefer(Dozent):
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "PrüferIn"
        verbose_name_plural = "PrüferInnen"


class Testat(models.Model):
    bezeichnung = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    studienabschnitt = models.ManyToManyField(Studienabschnitt)
    studiengang = models.ManyToManyField(Studiengang)
    # pruefer = models.ManyToManyField(Pruefer)
    #fach = models.ForeignKey(Fach, on_delete=models.CASCADE, null=True, blank=True)
    fach = models.ManyToManyField(Fach)

    def __str__(self):
        return self.bezeichnung

    class Meta:
        verbose_name = "mündl. Testat"
        verbose_name_plural = "mündl. Testate"
        ordering = ("bezeichnung",)


class Textbeitrag(BasicHistory):
    text = models.TextField()
    sichtbar = models.BooleanField(default=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ("-created_date",)


class Meldung(Textbeitrag):
    beitrag = models.ForeignKey(Textbeitrag, related_name="meldungen")
    bearbeitet = models.BooleanField(default=False)  # Medlung abschließend bearbeitet

    class Meta:
        verbose_name = "Meldung"
        verbose_name_plural = "Meldungen"


class Frage(Textbeitrag):
    # Wann wurde die Frage gestellt? ( != BasicHistory.created_date )
    datum = models.DateField(default=timezone.datetime.today, verbose_name="Prüfungs-Datum")
    score = models.PositiveIntegerField(default=1)
    antwort = models.TextField(null=True, blank=True, verbose_name="Antwort")
    pruefer = models.ForeignKey(Pruefer, verbose_name="PrüferIn")
    testat = models.ForeignKey(Testat, verbose_name="Testat/Prüfung")

    def score_up(self, user):
        """
        erhöht den Score der Frage um 1 und speichert
        :param user: the logged in User, who clicked the "score up" button
        """
        self.score = models.F('score') + 1
        self.modified_by = user
        self.save()

    class Meta:
        verbose_name = "Frage"
        verbose_name_plural = "Fragen"


class Protokoll(Textbeitrag):
    datum = models.DateField(default=timezone.datetime.today, verbose_name="Prüfungs-Datum")
    pruefer = models.ForeignKey(Pruefer, verbose_name="PrüferIn")
    testat = models.ForeignKey(Testat, verbose_name="Testat/Prüfung")

    class Meta:
        verbose_name = "Protokoll"
        verbose_name_plural = "Protokolle"


class Kommentar(Textbeitrag):
    pruefer = models.ForeignKey(Pruefer)

    class Meta:
        verbose_name = "Kommentar"
        verbose_name_plural = "Kommentare"
