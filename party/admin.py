import tempfile
import zipfile
import os
from io import BytesIO
from adminsortable2.admin import SortableStackedInline, SortableAdminBase

from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import reverse, redirect
from django.urls import path
from django.utils.html import format_html

from party.models import Entry, Party, Compo, CompoVotingStatus


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
    fields = ['compo']
    can_delete = False
    max_num = 0

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    model = Entry
    list_display = ['__str__', 'entry_total_points']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # remove extra buttons from compo and owner
        remove_extras(form.base_fields['compo'])
        remove_extras(form.base_fields['owner'])
        return form



@admin.register(Compo)
class CompoAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ['__str__', 'submission_deadline_simple', 'metadata_deadline_simple', 'voting_status', 'go_to_live_button', 'export_entries_button']
    inlines = [InlineEntryAdmin]
    list_filter = ['party__title']

    def get_readonly_fields(self, request, obj=None):
        # set voting_status and current_entry_pos to readonly when creating a new compo
        if not obj:
            return ['voting_status', 'current_entry_pos']
        else:
            return []

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # remove extra buttons next to party selection
        field = form.base_fields['party']
        remove_extras(field)

        return form
    
    def get_urls(self):
        urls = super().get_urls()
        additional_urls = [
            path('go-to-live/<int:compo_pk>', self.admin_site.admin_view(self.go_to_live), name='compo_go_to_live'),
            path('export-entries/<int:compo_pk>', self.admin_site.admin_view(self.export_entries), name='export_entries')
        ]
        return additional_urls + urls

    def go_to_live_button(self, compo):
        return format_html(
            '<a class="button" href="{}">Start</a>',
            reverse('admin:compo_go_to_live', args=[compo.pk])
        )
    
    go_to_live_button.short_description = 'Go to Live'

    def go_to_live(self, request, compo_pk):
        compo = self.get_object(request, compo_pk)
        compo.voting_status = CompoVotingStatus.LIVE
        compo.save()
        return redirect(reverse('control-beamer', args=[compo.pk]))

    def export_entries_button(self, compo):
        return format_html(
            '<a class="button" href="{}">Export entries</a>', 
            reverse('admin:export_entries', args=[compo.pk])
        )
    
    def export_entries(self, request, compo_pk):
        buffer = BytesIO()
        compo = self.get_object(request, compo_pk)


        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as export:
            for entry in compo.entries.all():
                if entry.sub_file:
                    export.write(entry.sub_file.path, entry.entry_filename)

        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='application/x-zip-compressed')
        response['Content-Disposition'] = f'attachment; filename={compo.title.lower()}_entries.zip'
        return response 
    
    export_entries_button.short_description = 'Export entries'


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