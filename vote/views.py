import json

from party.mixins import StaffRequiredMixin
from party.models import Compo, Entry
from vote.forms import VoteLoginForm
from vote.models import VoteKey, Vote
from vote.utils import votekey_valid
from vote.mixins import VoteKeyRequiredMixin

from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, reverse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed

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

def get_votekey(request):
    found = False
    votekey = request.COOKIES.get('votekey')
    if not votekey_valid(votekey):
        return None, found
    found = True
    votekey = VoteKey.objects.get(key=votekey)
    return votekey, found

@csrf_exempt
def entries_to_vote_for(request, compo_pk):
    votekey, found = get_votekey(request)
    if not found:
        raise ValidationError
    compo = get_object_or_404(Compo, pk=compo_pk)
    entries = compo.entries.all()[:compo.current_entry_pos]
    return render(request, "vote/entries_formset.html", context={'entries': entries})


@csrf_exempt
def cast_vote_for_entry(request, entry_pk):
    votekey, found = get_votekey(request)
    if not found:
        raise ValidationError
    body = request.POST.dict()
    points = body['points']
    Vote.objects.update_or_create(
        entry=entry,
        votekey=votekey,
        defaults={
            'points': points
        }
    )
    return HttpResponse()


def is_superuser(user):
    return user.is_superuser

@csrf_exempt
@user_passes_test(is_superuser)
def record_current_entry(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    data = json.loads(request.body)
    current_entry = data.get('current_entry')
    compo_pk = data.get('compo_pk')
    print("CALLED")
    print(compo_pk)
    print(current_entry)

    if not compo_pk:
        return HttpResponseBadRequest('compo_pk missing')
    
    if current_entry:
        compo = Compo.objects.get(pk=compo_pk)
        compo.current_entry_pos = current_entry
        compo.save()

    return JsonResponse({'success': True})