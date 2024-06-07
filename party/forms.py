from django.core.exceptions import ValidationError
from django import forms
from django.utils import timezone

from party.models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = [
            'created_at',
            'updated_at',
            'order',
            'owner',
        ]
        labels = {
            'team': 'Author',
            'sub_file': 'File'
        }
        widgets = {
            'has_audio': forms.CheckboxInput(),
            'exits_automatically': forms.CheckboxInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        compo = cleaned_data['compo'] 
        now = timezone.now()
        
        # check for submission_deadline and metadata_deadline
        initial_sub_file = self.initial.get('sub_file')
        cleaned_sub_file = self.cleaned_data.get('sub_file')

        changed_data = self.changed_data
        if 'sub_file' in self.changed_data and now > compo.submission_deadline:
            raise ValidationError("The deadline for submitting a file has passed. You can still edit the other information of your entry. If your issue is critical, please contact the organizers")

        
        if now > compo.metadata_deadline:
            raise ValidationError("The deadline for the compo has passed, you can't edit or submit a new entry. If your issue is critical, please contact the organizers")
        
        return cleaned_data
