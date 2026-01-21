from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Nome")
    last_name = forms.CharField(max_length=30, required=True, label="Sobrenome")
    email = forms.EmailField(required=True, label="E-mail")
    phone = forms.CharField(max_length=20, required=True, label="Telefone")
    zip_code = forms.CharField(max_length=10, required=True, label="CEP")
    street = forms.CharField(max_length=255, required=True, label="Rua")
    neighborhood = forms.CharField(max_length=100, required=True, label="Bairro")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data['phone']
            profile.zip_code = self.cleaned_data['zip_code']
            profile.street = self.cleaned_data['street']
            profile.neighborhood = self.cleaned_data['neighborhood']
            profile.save()
        return user
