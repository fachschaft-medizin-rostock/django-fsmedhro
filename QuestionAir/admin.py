from django.contrib import admin
from .models import *


class KlausurAdmin(admin.ModelAdmin):
    model = Klausur


# Register your models here.
admin.site.register(Klausur, KlausurAdmin)
admin.site.register(Fach)
admin.site.register(Frage)
admin.site.register(Kommentar)