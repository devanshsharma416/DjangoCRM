from django.core.mail import send_mail
from django.http import request
from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from agents.forms import AgentModelForm
from .mixin import OrganizorAndLoginRequiredMixin
import random
# Create your views here.

class AgentListView(OrganizorAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'
  
    def get_queryset(self):
        # Grab the user profile for the user model
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

class AgentCreateView(OrganizorAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return '/agents/' 

    def form_valid(self, form):
        user = form.save(commit=False) 
        user.is_agent = True
        user.is_organizer = False
        user.set_password(f"{random.randint(0, 10000000)}")
        user.save()
        Agent.objects.create(
            user = user,
            organization = self.request.user.userprofile
        )
        send_mail(
            subject= "Your are invited to an agent",
            message = 'You were added as an agent on DJCRM. Please come login to start working',
            from_email = 'admin@test.com',
            recipient_list= [user.email]
        )
        # agent.organization = self.request.user.userprofile
        # agent.save()
        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(OrganizorAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
        # return Agent.objects.all()

class AgentUpdateView(OrganizorAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return '/agents/' 
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
        # return Agent.objects.all()

class AgentDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'
    context_object_name = 'agent'

    def get_success_url(self):
        return '/agents/' 

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
        # return Agent.objects.all()
