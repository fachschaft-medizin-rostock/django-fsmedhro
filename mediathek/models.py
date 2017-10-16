from django.db import models
from django.contrib.auth.models import User
from fsmedhrocore.models import BasicHistory
from django.utils import timezone


class Kunde(models.Model):
    """
    Extends django.contrib.auth.models.User
    """
    user = models.OneToOneField(User)

    anschrift = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=16, blank=True, null=True)
    bemerkung = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        returns "[Vorname] [Nachname]"
        """
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Kundin/Kunde"
        verbose_name_plural = "Kundinnen/Kunden"
        ordering = ("user__last_name",)


class Sammelbestellung(models.Model):
    bezeichnung = models.CharField(max_length=30)
    start = models.DateTimeField()
    ende = models.DateTimeField()
    abgeschlossen = models.BooleanField(default=False, verbose_name="abgeschlossen")

    def __str__(self):
        return self.bezeichnung

    class Meta:
        verbose_name = "Sammelbestellung"
        verbose_name_plural = "Sammelbestellungen"
        ordering = ("abgeschlossen", "-ende")


class Ware(models.Model):
    bezeichnung = models.CharField(max_length=30)
    marke = models.CharField(max_length=30, null=True, blank=True)
    variation = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        s = self.bezeichnung
        if self.marke:
            s = "{}: {}".format(self.marke, s)
        if self.variation:
            s = "{} ({})".format(s, self.variation)
        return s  # "marke: bezeichnung (variation)"

    class Meta:
        verbose_name = "Ware"
        verbose_name_plural = "Waren"
        ordering = ("marke", "bezeichnung", "variation")


class Angebot(models.Model):
    preis = models.DecimalField(max_digits=8, decimal_places=2)  # max. 999999.99
    ware = models.ForeignKey(Ware, on_delete=models.CASCADE)
    sammelbestellung = models.ForeignKey(Sammelbestellung, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {} - {} €".format(self.sammelbestellung, self.ware, self.preis)

    class Meta:
        verbose_name = "Angebot"
        verbose_name_plural = "Angebote"
        ordering = ("ware__marke", "ware__bezeichnung", "ware__variation")


class Auftrag(models.Model):

    ERSTELLT, BEARBEITET, ABGESCHLOSSEN = range(0, 3)

    STATUS = (
        (ERSTELLT, 'erstellt'),
        (BEARBEITET, 'bearbeitet'),
        (ABGESCHLOSSEN, 'abgeschlossen'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datum = models.DateField(default=timezone.datetime.today, verbose_name="Auftrags-Datum")
    status = models.IntegerField(choices=STATUS, default=ERSTELLT)

    # override Model API method, STATUS can be overridden in subclasses
    def get_status_display(self):
        return self.STATUS[self.status][1]

    def __str__(self):
        return "{} {} ({}), {}".format(
            self._meta.verbose_name_raw, self.pk, self.datum, self.get_status_display())

    class Meta:
        verbose_name = "Auftrag"
        verbose_name_plural = "Aufträge"
        ordering = ('-datum', 'status',)


class Bestellung(Auftrag):

    Auftrag.STATUS = (
        (Auftrag.ERSTELLT, 'bestellt'),
        (Auftrag.BEARBEITET, 'abholbereit'),
        (Auftrag.ABGESCHLOSSEN, 'abgeschlossen'),
    )

    anzahl = models.IntegerField(default=1)
    angebot = models.ForeignKey(Angebot, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Sammelbestellung(Auftrag)"
        verbose_name_plural = "Sammelbestellungen(Aufträge)"


class Einstellungen(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    oeffnungszeiten = models.TextField(null=True, blank=True, verbose_name="Öffnungszeiten")
    konto_inhaber = models.CharField(max_length=30, default='KontoinhaberIn', verbose_name="KontoinhaberIn")
    konto_iban = models.CharField(max_length=22, default='DE00000000000000000000', verbose_name="Konto IBAN")

    class Meta:
        verbose_name = "Einstellungen"
        verbose_name_plural = "Einstellungen"