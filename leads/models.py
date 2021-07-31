# from django.contrib.auth.forms import UsernameField
from django.db import models
from django.db.models.base import Model
# # it is used to grab the user model that provided by the django. It is not recommended to use built-i user model
# from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    #it inherits all the fields of AbstractBaseUser. We can add more field
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20) 
    age = models.IntegerField(default=0)
    # models.CASCADE means, it will delete the leads if agent is deleted
    # foreign key allows the one agent to many leads
    organization = models.ForeignKey(UserProfile, on_delete= models.CASCADE)
    agent = models.ForeignKey("Agent", null = True, blank = True, on_delete = models.SET_NULL)
    category = models.ForeignKey("Category", related_name = "leads", on_delete=models.SET_NULL, null = True, blank = True)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()



    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(UserProfile, on_delete= models.CASCADE)
   

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=30) # New, Contacted, Converted, Unconverted
    organization = models.ForeignKey(UserProfile, blank = True, null = True, on_delete= models.CASCADE)

    def __str__(self):
        return self.name
    

    

# Create User Profile
# It will generate the event when we perform any changes in User Model
def post_user_created_signal(sender, instance, created, **kwarg):
    print(instance, created)
    # When user is created, we create the userprofile corresponding 
    if created:
        UserProfile.objects.create(user = instance)

post_save.connect(post_user_created_signal, sender = User)

   

