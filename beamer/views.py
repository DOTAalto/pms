from django.shortcuts import render
from django.views.generic.detail import DetailView

from party.models import Compo, Entry
from party.mixins import StaffRequiredMixin, OwnerRequiredMixin

class CompoSlideshow(StaffRequiredMixin, DetailView):
    model = Compo
    template_name = 'beamer/slideshow.html'

class PreviewEntry(OwnerRequiredMixin, DetailView):
    model = Entry
    template_name = 'beamer/preview.html'