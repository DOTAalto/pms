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


class InlineEntryAdmin(SortableStackedInline):
    model = Entry
    exclude = [
        'sub_file',
        'title',
        'thumbnail',
        'owner',
        'team',
        'description',
        'technology',
        'instructions',
        'contact_phone',
        'contact_telegram',
    ]
    can_delete = False
    extra = 0

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    model = Entry
    actions = [export_entries]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # remove extra buttons from compo and owner
        remove_extras(form.base_fields['compo'])
        remove_extras(form.base_fields['owner'])
        return form



@admin.register(Compo)
class CompoAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ['__str__', 'voting_status']
    inlines = [InlineEntryAdmin]
    list_filter = ['party__title']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # remove extra buttons next to party selection
        field = form.base_fields['party']
        remove_extras(field)
        return form


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}

        # Remove save and add another and save and continue editing buttons from the UI
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)


def remove_extras(field):
    field.widget.can_add_related = False
    field.widget.can_change_related = False
    field.widget.can_view_related = False