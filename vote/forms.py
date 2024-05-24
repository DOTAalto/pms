from django import forms


class VoteLoginForm(forms.Form):
    votekey = forms.CharField()
