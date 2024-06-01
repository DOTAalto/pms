from django.forms import ModelForm, HiddenInput

from party.models import Entry


class EntryForm(ModelForm):
    class Meta:
        model = Entry
        exclude = [
            'created_at',
            'updated_at',
            'order',
            'owner',
        ]