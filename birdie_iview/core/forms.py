from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from django.core.exceptions import ValidationError
from django import forms
from .models import Shot, Round, Course, Hole ,Clubs


class ShotForm(forms.ModelForm):
    class Meta:
        model = Shot
        fields = ['latitude', 'longitude', 'club']
    
    def __init__(self, user, *args, **kwargs):
        super(ShotForm, self).__init__(*args, **kwargs)
        self.fields['club'].queryset = Clubs.objects.filter(user=user)
        self.fields['club'].empty_label = 'Select a club'
        self.fields['club'].label = ''  
        self.helper = FormHelper()
        self.helper.form_show_labels = False 
        self.helper.layout = Layout(
            Field('latitude', id='latitude', css_class='hide-input'),
            Field('longitude', id='longitude', css_class='hide-input'),
            Field('club', id='club', css_class='custom-select', label=''),  
        )


class HideInput(forms.widgets.Input):
    input_type = 'hidden'

ShotForm.base_fields['latitude'].widget = HideInput()
ShotForm.base_fields['longitude'].widget = HideInput()

class RoundForm(forms.ModelForm):
    course = forms.ModelChoiceField(label='Course', queryset=Course.objects.all(), required=True)

    class Meta:
        model = Round
        fields = ['course']

    def __init__(self, *args, **kwargs):
        super(RoundForm, self).__init__(*args, **kwargs)
        self.fields['course'].widget = forms.Select()  
        self.fields['course'].choices = self.get_course_choices()  

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('course', id='course'),
        )

    def get_course_choices(self):
        existing_courses = Course.objects.all().values_list('id', 'name')
        course_choices = [(str(course[0]), course[1]) for course in existing_courses]
        course_choices.insert(0, ('', 'Select or type course name...'))
        return course_choices

class HoleForm(forms.ModelForm):
    class Meta:
        model = Hole
        fields = ['hole_num', 'hole_par', 'hole_distance']
        widgets = {'hole_num': forms.HiddenInput()}
        labels = {'hole_par': 'Select Par'}

    PAR_CHOICES = (
        ('', 'Select Par'),  
        (3, 'Par 3'),
        (4, 'Par 4'),
        (5, 'Par 5'),
    )

    hole_par = forms.ChoiceField(choices=PAR_CHOICES, required=True)

    def __init__(self, *args, **kwargs):
        super(HoleForm, self).__init__(*args, **kwargs)
        self.fields['hole_distance'].required = True  
        self.fields['hole_distance'].widget.attrs['placeholder'] = 'Enter the distance for the hole' 
        self.fields['hole_distance'].label = ""
        self.fields['hole_par'].label = ""
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('hole_num', id='hole_num'),
            Field('hole_par', id='hole_par'),
            Field('hole_distance', id='hole_distance'),
        )

    def clean_hole_distance(self):
        hole_distance = self.cleaned_data.get('hole_distance')
        try:
            hole_distance = float(hole_distance)
            if hole_distance < 0:
                raise ValidationError('Distance cannot be negative')
        except (TypeError, ValueError):
            raise ValidationError('Invalid distance entered, please enter a number')
        return hole_distance