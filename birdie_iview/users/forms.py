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
    CLUB_NAME_CHOICES = [
        ('Driver', 'Driver'),
        ('2 Wood', '2 Wood'),
        ('3 Wood', '3 Wood'),
        ('4 Wood', '4 Wood'),
        ('5 Wood', '5 Wood'),
        ('6 Wood', '6 Wood'),
        ('7 Wood', '7 Wood'),
        ('8 Wood', '8 Wood'),
        ('9 Wood', '9 Wood'),
        ('1 Iron', '1 Iron'),
        ('2 Iron', '2 Iron'),
        ('3 Iron', '3 Iron'),
        ('4 Iron', '4 Iron'),
        ('5 Iron', '5 Iron'),
        ('6 Iron', '6 Iron'),
        ('7 Iron', '7 Iron'),
        ('8 Iron', '8 Iron'),
        ('9 Iron', '9 Iron'),
        ('Pitching Wedge', 'Pitching Wedge'),
        ('Sand Wedge', 'Sand Wedge'),
        ('Lob Wedge', 'Lob Wedge'),
        ('Gap Wedge', 'Gap Wedge'),
        ('Fairway Wood', 'Fairway Wood'),
        ('Hybrid', 'Hybrid'),
        ('Putter', 'Putter'),
        
    ]

    club_name = forms.ChoiceField(choices=CLUB_NAME_CHOICES, label='Club Type')

    class Meta:
        model = Clubs
        fields = ['club_name', 'club_manufacturer', 'club_model', 'club_loft']
        labels = {
            'club_name': 'Club Type',
            'club_manufacturer': 'Manufacturer',
            'club_model': 'Model',
            'club_loft': 'Loft (degrees)',
        }