from os import supports_bytes_environ
from typing import ContextManager
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django import forms
from django.forms.formsets import formset_factory
from django.views import generic
from agents.mixin import OrganizorAndLoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic.edit import CreateView
from .models import Agent, Lead, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LeadModelForm, LeadForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm


# CRUD + L = Create, Retrieve, Update, Delete and List

# Signup form
class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self, *args):
        return reverse('login')


class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'

# Create your views here.
def landing_page(request):
    return render(request, 'landing.html')

# List view , it automatically assign object_list as key
class LeadListView(LoginRequiredMixin,generic.ListView):
    template_name = 'leads/home.html'
    
    def get_queryset(self):
        user = self.request.user

        # initial queryset of leads for the entire organization 
        if user.is_organizer:
            queryset = Lead.objects.filter(organization = user.userprofile, agent__isnull = False)
            agent_isnull = False
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization, agent__isnull = False)
            # filter for agent that is logged in 
            queryset = queryset.filter(agent__user = user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization = user.userprofile, agent__isnull = True)
        context.update({
            "unassigned_leads": queryset
        })
        return context
    # We can change the default key name as follows
    # context_object_name = "leads"

# def lead_list(request):
#     leads = Lead.objects.all()
#     context = {
#         'leads':leads
#     }
#     return render(request, "home.html", context)


class LeadDetailView(LoginRequiredMixin,generic.DetailView):
    template_name = "leads/list_details.html"
    

    def get_queryset(self):
        user = self.request.user

        # initial queryset of leads for the entire organization 
        if user.is_organizer:
            queryset = Lead.objects.filter(organization = user.userprofile)
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization)
            # filter for agent that is logged in 
            queryset = queryset.filter(agent__user = user)
        return queryset


# def lead_detail(request, pk):
   
#     lead = Lead.objects.get(id=pk)
#     context = {
#         'lead': lead
#     }
    
#     return render(request, "list_details.html", context)

class LeadCreateView(OrganizorAndLoginRequiredMixin,generic.CreateView):
    template_name = 'leads/lead_create.html'
    # We don't need to pass the queryset, only need to pass form class
    form_class = LeadModelForm

    def get_success_url(self):
        return '/leads'
        # return reverse('leads: home')

    def form_valid(self, form):
        lead = form.save(commit = False)
        lead.organization = self.request.user.userprofile
        lead.save()
        # Todo send mail
        send_mail(
            subject= "A lead has been created",
            message="Go to the site to see the new lead",
            from_email = 'test@gmail.com', 
            recipient_list= ["test2@gmail.com"]
        )
        return super(LeadCreateView, self).form_valid(form)

    # In replace of redirect if for is successfully submitted

# def lead_create(request):
#     form = LeadModelForm()
#     if request.method == 'POST':
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             form.save() # Same as the below method. save as the new instance.
#             # to fetch the data.
#             # first_name = form.cleaned_data['first_name']
#             # last_name = form.cleaned_data['last_name']
#             # age = form.cleaned_data['age']
#             # #Returns the first object matched by the queryset, or None if there is no matching object. 
#             # agent = form.cleaned_data['agent']
#             # # Creating Leads using data
#             # Lead.objects.create (
#             #     first_name = first_name,
#             #     last_name = last_name,
#             #     age = age,
#             #     agent = agent
#             # )
#             return redirect('/leads')
#     context = {
#         'form': form
        
#     }
#     return render(request, "lead_create.html", context)


class LeadUpdateView(OrganizorAndLoginRequiredMixin,generic.UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
         # initial queryset of leads for the entire organization 
        return Lead.objects.filter(organization = user.userprofile)     
   
    def get_success_url(self):
        return '/leads'



# def lead_update(request, pk):
#     lead = Lead.objects.get(id = pk)
#     # Grab a particular lead and update the data
#     form = LeadModelForm(instance=lead)
#     if request.method == 'POST':
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             # to fetch the data.
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             #Returns the first object matched by the queryset, or None if there is no matching object. 
#             #Lead.object.first
            
#             return redirect('/leads')
#     context = {
#         'lead': lead,
#         'form': form
#     }
#     return render(request, "lead_update.html", context)


class LeadDeleteView(OrganizorAndLoginRequiredMixin,generic.DetailView):
    template_name = 'leads/lead_delete.html'
    
    def get_success_url(self):
        return '/leads'

    def get_queryset(self):
        user = self.request.user
    # initial queryset of leads for the entire organization 
        if user.is_organizer:
            queryset = Lead.objects.filter(organization = user.userprofile)
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization)
            # filter for agent that is logged in 
            queryset = queryset.filter(agent__user = user)
        return queryset
    

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(*kwargs)
        user = self.request.user
        
        if user.is_organizer:
            queryset = Category.objects.filter(organization = user.userprofile)
        else:
            queryset = Category.objects.filter(organization = user.agent.organization)
    
        context.update({
            "unassigned_lead_count": queryset.filter(organization__isnull = True).count()
        })

        return context

    def get_queryset(self):
        user = self.request.user 
        if user.is_organizer:
            queryset = Category.objects.filter(organization = user.userprofile)
        else:
            queryset = Category.objects.filter(organization = user.agent.organization)
        return queryset
    

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'category_detail.html'
    context_object_name = 'category'


    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(*kwargs)
    #     user = self.request.user

    #     leads = self.get_object().leads.all()
    #     context.update({
    #         "leads": leads
    #     })

    #     return context

    def get_queryset(self):
        user = self.request.user

        # initial queryset of leads for the entire organization 
        if user.is_organizer:
            queryset = Category.objects.filter(organization = user.userprofile)
        else:
            queryset = Category.objects.filter(organization = user.agent.organization)
        return queryset


class AssignAgentView(OrganizorAndLoginRequiredMixin, generic.FormView):
    template_name = 'assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return '/leads'

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id = self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)
# def lead_delete(request, pk):
#     lead = Lead.objects.get(id = pk)
#     lead.delete()
#     return redirect("/leads")
# #    
# #     context = {
# #         'form': form
        
# #     }
# #     return render(request, "lead_create.html", context)


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_category_update.html'
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user

        # initial queryset of leads for the entire organization 
        if user.is_organizer:
            queryset = Lead.objects.filter(organization = user.userprofile)
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization)
            # filter for agent that is logged in 
            queryset = queryset.filter(agent__user = user)
        return queryset
   
    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs = {"pk": self.get_object().id})
