from django.forms import ModelForm, HiddenInput

from party.models import Entry


class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = [
            'title',
            'sub_file',
            'thumbnail',
            'team',
            'description',
            'compo',
        ]
        widgets = {
            'compo': HiddenInput
        }