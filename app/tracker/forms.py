from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

from . import models


User = get_user_model()

class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}

class TrackerForm(forms.ModelForm):

    class Meta:
        model = models.Tracker
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class CreatureForm(forms.ModelForm):

    class Meta:
        model = models.Creature
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'initiative': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


CreatureFormSet = forms.inlineformset_factory(
    models.Tracker, models.Creature, form=CreatureForm,
    extra=1, can_delete=False
)