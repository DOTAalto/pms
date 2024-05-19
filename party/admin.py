from django.contrib import admin

from party.models import Entry, Party, Compo

# Register your models here.
admin.site.register(Party)
admin.site.register(Compo)
admin.site.register(Entry)