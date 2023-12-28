from django import forms
from user_management.models import YourModel

class YourModelForm(forms.ModelForm):
    class Meta:
        model = YourModel
        fields = '__all__'
