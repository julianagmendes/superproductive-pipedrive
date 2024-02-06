from django import forms
from user_management.models import Company

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['schema_name', 'is_active']

# class EmailTemplateForm(forms.ModelForm):
#     class Meta:
#         model = EmailTemplates
#         fields = ['body', 'subject']  # Add other fields as needed