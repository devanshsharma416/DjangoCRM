from django.contrib import admin
from .models import Lead, Agent, User, UserProfile, Category

# Register your models here.
# class UserAdmin(admin.ModelAdmin):
#     list_display= ('first_name', 'last_name', 'email')

admin.site.register(Category)  
admin.site.register(UserProfile)
admin.site.register(Lead)
admin.site.register(Agent)
admin.site.register(User)
