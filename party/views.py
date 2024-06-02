from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from party.mixins import OwnerRequiredMixin
from party.models import Compo, Party, Entry 
from party.forms import EntryForm

class PartyList(ListView):
    model = Party
    template_name = 'party/party_list.html'

class PartyDetailView(DetailView):
    model = Party 
    template_name = 'party/party_detail.html'

class UpdateEntryView(OwnerRequiredMixin, UpdateView):
    model = Entry
    template_name = "party/entry_create.html"
    fields = [
        'title',
        'sub_file',
        'thumbnail',
        'team',
        'description',
    ]


class CreateEntryView(LoginRequiredMixin, CreateView):
    model = Entry
    template_name = 'party/entry_create.html'
    form_class = EntryForm

    def get_initial(self):
        initial = super().get_initial()
        initial["compo"] = get_object_or_404(Compo, pk=self.kwargs["compo_pk"])
        return initial

    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.owner = self.request.user 

        entry.save()
        return HttpResponseRedirect(reverse('party-detail', kwargs={'slug': entry.compo.party.slug }))
    