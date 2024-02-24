from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,SetPasswordForm
from django.contrib.auth.models import User
from .models import InfoLivrason

# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'my-input', 'placeholder': 'Entrer username'}),
#             'email': forms.EmailInput(attrs={'class': 'my-input', 'placeholder': 'Entrer email'}),
#             'password1': forms.PasswordInput(attrs={'class': 'my-input', 'placeholder': 'Entre le mot de passe'}),
#             'password2': forms.PasswordInput(attrs={'class': 'my-input', 'placeholder': 'Répéter le mot de passe'}),
#         }
class Modifier_mdpForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(Modifier_mdpForm, self).__init__(*args, **kwargs)

		self.fields['new_password1'].widget.attrs['class'] = 'my-input'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Mot de passe'
		self.fields['new_password1'].label = 'Mot de passe'
		self.fields['new_password1'].help_text = '<span class="form-text text-muted"><small>Password can\'t be too similar to your other personal information,contain at least 8 characters, can\'t be a commonly used password, can\'t be entirely numeric.</small></span>'

		self.fields['new_password2'].widget.attrs['class'] = 'my-input'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirmer le mot de passe'
		self.fields['new_password2'].label = 'Mot de passe'
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class ProfilForm(UserChangeForm):
	# Hide Password stuff
	password = None
	# Get other fields
	email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'my-input', 'placeholder':'Email Address'}), required=False)
	username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class':'my-input', 'placeholder':'Username'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'email')


class SinscrireForm(UserCreationForm):
	email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'my-input', 'placeholder':'Enter email'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SinscrireForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'my-input'
		self.fields['username'].widget.attrs['placeholder'] = 'Entrer username'
		self.fields['username'].label = 'Username'
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'my-input'
		self.fields['password1'].widget.attrs['placeholder'] = 'Entrer le mot de passe'
		self.fields['password1'].label = 'Mot de passe'
		self.fields['password1'].help_text = '<span class="form-text text-muted"><small>Password can\'t be too similar to your other personal information,contain at least 8 characters, can\'t be a commonly used password, can\'t be entirely numeric.</small></span>'

		self.fields['password2'].widget.attrs['class'] = 'my-input'
		self.fields['password2'].widget.attrs['placeholder'] = 'Répeter le mot de passe'
		self.fields['password2'].label = 'Mot de passe'
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
		

class InfoLivrasonForm(forms.ModelForm):
    VILLE_CHOICES = (
        ('tanger', 'Tanger'),
        ('tetouan', 'Tetouan'),
    )

    PAYS_CHOICES = (
        ('marocco', 'Marocco'),
        ('belgium', 'Belgium'),
    )

    address = forms.CharField(label="Addresse", widget=forms.TextInput(attrs={'class': 'my-input', 'placeholder': 'Address'}), required=True)
    ville = forms.ChoiceField(choices=VILLE_CHOICES, widget=forms.Select(attrs={'class':'my-input'}))
    pays = forms.ChoiceField(choices=PAYS_CHOICES, widget=forms.Select(attrs={'class':'my-input'}))
    codePostal = forms.CharField(label="Code Postal", widget=forms.TextInput(attrs={'class': 'my-input', 'placeholder': 'Postal Code'}), required=False)
    numTele = forms.CharField(label="Numero telephone ", widget=forms.TextInput(attrs={'class': 'my-input', 'placeholder': 'Telephone Number'}), required=False)

    class Meta:
        model = InfoLivrason
        fields = ('address', 'ville', 'pays', 'codePostal', 'numTele')



		