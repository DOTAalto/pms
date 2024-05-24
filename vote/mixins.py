from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from vote.utils import votekey_valid

class VoteKeyRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        votekey = request.COOKIES.get('votekey')
        if not votekey or not votekey_valid(votekey):
            return HttpResponseRedirect(reverse('vote-login'))
        return super().dispatch(request, *args, **kwargs)