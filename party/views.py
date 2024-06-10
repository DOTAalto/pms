from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Sum

from party.mixins import OwnerRequiredMixin, StaffRequiredMixin
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
    

class YoutubeDescView(StaffRequiredMixin, DetailView):
    template_name = 'party/youtube.html'
    model = Compo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = self.calculate_positions(self.get_object().entries.all())
        return context
    
    @staticmethod
    def calculate_positions(entry_qs):
        entries = entry_qs.annotate(total_points=Sum('votes__points')).order_by('-total_points')
        positions = []
        position = 1

        for index, entry in enumerate(entries):
            if index > 0 and entry.total_points < entries[index - 1].total_points:
                position = index + 1
            positions.append((position, entry))

        return positions
