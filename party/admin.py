import tempfile
import zipfile
import os
from io import BytesIO
from adminsortable2.admin import SortableStackedInline, SortableAdminBase

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


class EntryAdmin(SortableStackedInline):
    model = Entry
    actions = [export_entries]
    list_filter = ['compo__title']
    exclude = [
        'sub_file',
        'title',
        'thumbnail',
        'owner',
        'team',
        'description'
    ]
    can_delete = False
    extra = 0


@admin.register(Compo)
class CompoAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [EntryAdmin]


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']

admin.site.register(Entry)