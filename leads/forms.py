from django import forms
from django.db.models import fields
from django.contrib.auth import get_user_model
from django.http import request
from .models import Lead, Agent
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model()

# Using model form
class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'

class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
        # field_classes = {'username': UsernameField}
    
class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        agents  = Agent.objects.filter(organization = request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents

class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )
