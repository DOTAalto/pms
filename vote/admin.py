from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django import forms 
from django.db import IntegrityError

from party.models import Party
from vote.models import VoteKey, Vote

class VoteKeyForm(forms.Form):
    party = forms.ModelChoiceField(required=True, queryset=Party.objects.all())
    keys = forms.CharField(required=True, widget=forms.Textarea)

class VoteKeyAdmin(admin.ModelAdmin):
    list_filter = ['party__title']
    change_list_template = 'admin/votekeys_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        additional_urls = [
            path('import-keys/', self.admin_site.admin_view(self.import_keys)),
        ]
        return additional_urls + urls 

    def import_keys(self, request):
        if  request.method == 'POST':
            form = VoteKeyForm(request.POST)
            if form.is_valid():
                keys = form.cleaned_data['keys'].splitlines()
                party = form.cleaned_data['party']
                import_failed = 0
                for key in keys:
                    try:
                        VoteKey.objects.create(
                            party=party,
                            key=key
                        )
                    except IntegrityError:
                        import_failed += 1

                import_total = len(keys)
                import_success = import_total - import_failed
                message = f"Imported {import_success} keys successfully, {import_failed} failed. (Total: {import_total})"
                self.message_user(request, message)
                return redirect('..')


        form = VoteKeyForm()
        context = {'form': form, 'opts': self.model._meta}
        return render(
            request, 'admin/import_keys.html', context
        )


admin.site.register(VoteKey, VoteKeyAdmin)
admin.site.register(Vote)