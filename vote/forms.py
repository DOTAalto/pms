from django import forms
from vote.models import Vote


class VoteLoginForm(forms.Form):
    votekey = forms.CharField()

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['points', 'entry']
        widgets = {
            'points': forms.RadioSelect,
            'entry': forms.HiddenInput
        }