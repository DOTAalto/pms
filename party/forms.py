from django.forms import ModelForm, HiddenInput

from party.models import Entry


class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = [
            'title',
            'sub_file',
            'thumbnail',
            'author',
            'description',
            'compo',
        ]
        widgets = {
            'compo': HiddenInput
        }