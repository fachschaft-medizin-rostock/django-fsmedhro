from django.contrib import admin
from .models import *


class TestatAdmin(admin.ModelAdmin):
    model = Testat
    filter_horizontal = ('studiengang', 'studienabschnitt', )


# Register your models here.
admin.site.register(Testat, TestatAdmin)
admin.site.register(Pruefer)
admin.site.register(Frage)
admin.site.register(Kommentar)
admin.site.register(Meldung)
