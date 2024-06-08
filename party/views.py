from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from party.mixins import OwnerRequiredMixin
from party.models import Compo, Party, Entry 
from party.forms import EntryForm


class PartyDetailView(DetailView):
    model = Party 
    template_name = 'party/party_detail.html'

    def get_object(self, queryset=None):
        return self.model.objects.get(is_active=True)


class UpdateEntryView(OwnerRequiredMixin, UpdateView):
    model = Entry
    template_name = "party/entry_create.html"
    form_class = EntryForm
    success_url = reverse_lazy('entries')

    def get_success_url(self):
        return self.success_url

class EntryList(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'party/entry_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.user)
        return qs
    

class InfoView(TemplateView):
    template_name = 'party/info.html'


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
        return HttpResponseRedirect(reverse_lazy('entries'))
    