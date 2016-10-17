from django import forms
from .models import Identity

class IdentityForm(forms.ModelForm):
	class Meta:
		model = Identity
		fields = '__all__'
