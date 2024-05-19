import tempfile
import zipfile
import os
from io import BytesIO

from django.contrib import admin
from django.http import HttpResponse

from party.models import Entry, Party, Compo


@admin.action(description="Export selected entries as zip")
def export_entries(modeladmin, request, queryset):
    """Exports selected entries from ModelAdmin"""
    buffer = BytesIO()

    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
        for entry in queryset.all():
            filename = os.path.basename(entry.sub_file.name)
            archive.write(entry.sub_file.path, filename)

    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename=entries.zip'
    return response


class EntryAdmin(admin.ModelAdmin):
    actions = [export_entries]
    list_filter = ['compo__title']


admin.site.register(Party)
admin.site.register(Compo)
admin.site.register(Entry, EntryAdmin)