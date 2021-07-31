from django.urls import path
from leads import views

app_name = "leads"
urlpatterns = [
    # name parameter makes the path reference so we can use it in the template easily.
    path('', views.LeadListView.as_view(), name = 'home'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name = 'lead-detail'),
    path('<int:pk>/update', views.LeadUpdateView.as_view(), name = 'lead-update'),
    path('<int:pk>/delete', views.LeadDeleteView.as_view(), name = 'lead-delete'),
    path('<int:pk>/assign-agent/', views.AssignAgentView.as_view(), name = 'lead-assign'),
    path('<int:pk>/category/', views.LeadCategoryUpdateView.as_view(), name = 'lead-category-update'),
    path('create/', views.LeadCreateView.as_view(), name = 'lead-create'),
    path('categories/', views.CategoryListView.as_view(), name = 'category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name = 'category-detail'),
      
]
