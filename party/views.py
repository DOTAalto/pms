from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse

from party.models import Compo, Party, Entry 
from party.forms import EntryForm


class PartyDetailView(DetailView):
    model = Party 
    template_name = 'party/party_detail.html'

"""
class PartyListView(ListView):
    template_name = 'party/party_list.html'

"""

class SubmitToCompoView(CreateView):
    model = Entry
    template_name = 'party/submission_create.html'
    form_class = EntryForm

    def get_initial(self):
        initial = super().get_initial()
        initial["compo"] = get_object_or_404(Compo, pk=self.kwargs["compo_pk"])
        return initial

    def form_valid(self, form):
        submission = form.save(commit=False)

        submission.save()
        return HttpResponseRedirect(reverse('party-detail', kwargs={'slug': submission.compo.party.slug }))
    