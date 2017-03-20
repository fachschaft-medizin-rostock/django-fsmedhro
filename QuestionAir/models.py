from django.db import models
from django.contrib.auth.models import User
from fsmedhrocore.models import Dozent, BasicHistory, Studienabschnitt, Studiengang
from django.utils import timezone


# TODO: bitte Dokument überprüfen


class QuestionAirUser(models.Model):
    """
    Extends django.contrib.auth.models.User
    """
    user = models.OneToOneField(User)

    def __str__(self):
        # Vorname + Nachname
        return self.user.get_full_name()


class Fach(models.Model):
    name = models.CharField(max_length=500)
    Studienabschnitt = models.ManyToManyField(Studienabschnitt)
    Studiengang = models.ManyToManyField(Studiengang)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Fach"
        verbose_name_plural = "Fächer"


class Klausur(models.Model):
    name = models.CharField(max_length=120)
    Fach = models.ForeignKey(Fach, verbose_name="Fach")
    datum = models.DateField(default=timezone.datetime.today, verbose_name="Klausurdatum")

    class Meta:
        verbose_name = "Klausur"
        verbose_name_plural = "Klausuren"

    def __str__(self):
        return self.name


class Frage(models.Model):
    # TODO: change relationship to ManytoOne
    Klausur = models.ForeignKey(Klausur, verbose_name="Klausur")
    # TODO: bearbeitbare Texte erstellen
    Fragentext = models.TextField(null=False, blank=True, verbose_name="Frage")
    option1 = models.TextField(null=True, blank=True, verbose_name="Option 1")
    option2 = models.TextField(null=True, blank=True, verbose_name="Option 2")
    option3 = models.TextField(null=True, blank=True, verbose_name="Option 3")
    option4 = models.TextField(null=True, blank=True, verbose_name="Option 4")
    option5 = models.TextField(null=True, blank=True, verbose_name="Option 5")
    answerA = models.TextField(null=True, blank=False, verbose_name="A")
    answerB = models.TextField(null=True, blank=False, verbose_name="B")
    answerC = models.TextField(null=True, blank=False, verbose_name="C")
    answerD = models.TextField(null=True, blank=False, verbose_name="D")
    answerE = models.TextField(null=True, blank=False, verbose_name="E")
    submitter = models.ManyToManyField(User)
    correctAnswer = models.PositiveIntegerField(default=1)
    scoreA = models.PositiveIntegerField(default=0)
    scoreB = models.PositiveIntegerField(default=0)
    scoreC = models.PositiveIntegerField(default=0)
    scoreD = models.PositiveIntegerField(default=0)
    scoreE = models.PositiveIntegerField(default=0)

    # TODO: correctAnswer als aufwahlfeld von answerA-E
    # TODO: option1-5 als optional Field --> nur angezeigt wenn Inhalt vorhanden

    class Meta:
        verbose_name = "Frage"
        verbose_name_plural = "Fragen"

    # TODO: Score up AnswerA-E wenn beantworten geklickt

    def score_upa(self,):
        self.scoreA = models.F('scoreA') + 1
        self.save()

    def score_upb(self,):
        self.scoreB = models.F('scoreB') + 1
        self.save()

    def __str__(self):
        return self.Fragentext


class Kommentar(BasicHistory):
    text = models.TextField()
    visible = models.BooleanField(default=False, verbose_name="Sichtbarkeit")
    frage = models.ForeignKey(Frage)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Kommentar"
        verbose_name_plural = "Kommentare"

#TODO: Antworten der User speichern --> für spätere Auswertung