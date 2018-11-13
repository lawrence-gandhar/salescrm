from django.forms import ModelForm
from django.forms.widgets import TextInput
from crm.models.leads import Lead_status

class Lead_statusForm(ModelForm):
    class Meta:
        model = Lead_status
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }