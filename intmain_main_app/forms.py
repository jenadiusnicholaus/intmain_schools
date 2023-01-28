import imp
from django import forms
from .models import Activity


class ContentActivityForm(forms.ModelForm):
    content_status_choices = (
        ('draft', 'Draft'),
        ('send_for_approval', 'Send For Approval'),
    )
    status = forms.ChoiceField()

    class Meta:
        model = Activity
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = self.content_status_choices


class SupervisorActivityForm(forms.ModelForm):
    supervisor_status_choices = (
        ('return_for_amendment', 'Return For Amendment'),
        ('approved', 'Approve'),
    )
    status = forms.ChoiceField()

    class Meta:
        model = Activity
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = self.supervisor_status_choices


class DefaultActivityForm(forms.ModelForm):
    status_choices = (
        ('invalid_status', 'Invalid Status'),
    )
    status = forms.ChoiceField()

    class Meta:
        model = Activity
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = self.status_choices

