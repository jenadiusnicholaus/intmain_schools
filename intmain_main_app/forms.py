import imp
from django import forms
from .models import Notes


class ContentNotesForm(forms.ModelForm):
    content_status_choices = (
        ('draft', 'Draft'),
        ('send_for_approval', 'Send For Approval'),
    )
    status = forms.ChoiceField()

    class Meta:
        model = Notes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = self.content_status_choices


class SupervisorNotesForm(forms.ModelForm):
    supervisor_status_choices = (
        ('return_for_amendment', 'Return For Amendment'),
        ('approved', 'Approve'),
    )
    status = forms.ChoiceField()

    class Meta:
        model = Notes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = self.supervisor_status_choices


class DefaultNotesForm(forms.ModelForm):
    status_choices = (
        ('invalid_status', 'Invalid Status'),
    )
    status = forms.ChoiceField()

    class Meta:
        model = Notes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = self.status_choices