from django.shortcuts import render
from django.views.generic.detail import DetailView

from party.models import Compo
from party.mixins import StaffRequiredMixin

class ControlBeamerView(StaffRequiredMixin, DetailView):
    model = Compo
    template_name = 'beamer/control.html'