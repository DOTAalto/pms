from party.mixins import StaffRequiredMixin
from party.models import Compo
from vote.forms import VoteLoginForm
from vote.models import VoteKey
from vote.utils import votekey_valid
from vote.mixins import VoteKeyRequiredMixin

from django.shortcuts import render, reverse
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

# Create your views here.
class LoginVoteView(FormView):
    form_class = VoteLoginForm
    template_name = "vote/login.html"

    def get_success_url(self):
        return reverse('vote') 

    def form_valid(self, form):
        response = super().form_valid(form)
        votekey = form.cleaned_data["votekey"]
        if votekey_valid(votekey):
            response.set_cookie('votekey', votekey, httponly=True)
            return response
        else:
            context = self.get_context_data()
            context["error"] = "Invalid key, please go to the info desk to sort this issue out"
            
            return TemplateResponse(self.request, self.template_name, context)


class VoteView(VoteKeyRequiredMixin, DetailView):
    model = Compo
    template_name = "vote/vote.html"


class VoteListView(VoteKeyRequiredMixin, ListView):
    model = Compo
    template_name = "vote/list.html"


class VoteManagementView(StaffRequiredMixin, TemplateView):
    template_name = "vote/management.html"