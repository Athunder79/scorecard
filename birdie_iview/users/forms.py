from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper,Layout
from crispy_forms.layout import Submit
from .models import Profile, Clubs

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'  
        self.fields['email'].widget.attrs['placeholder'] = 'Email'  
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'  
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password' 

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Sign Up'))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address1', 'address2', 'city', 'country']


class ClubsForm(forms.ModelForm):
    class Meta:
        model = Clubs
        fields = ['club_name', 'club_type']