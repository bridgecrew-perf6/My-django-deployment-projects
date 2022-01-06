from django.db import models

#Here we are importing the user from the auth models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):

    #This is basically a model class (UserProfileInfo) is to add an additional information that the default user(User which we are importing) it doesn't have.
    #The default user already has things like Username,email,password,Fname and Lname
    #But if we want to add more attributes to your actual user, you can essentially almost like extending the class of this OneToOne relationship where you dont want to do is just directly inherit from the User class.
    #That may seem really tempting, but doing that may screw up your database and thinking that it has multiple instances of the same user. So instead we use a OneToOne field relaitonship.

    # Create relationship (don't inherit from User!)
    #From django 2.x onwards, on_delete is a required parameter. on_delete=models.CASCADE 
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add any additional attributes you want
    #If blank is True means there wont be any error if user didnt fill it up.
    portfolio_site = models.URLField(blank=True)

    # pip install pillow to use this!
    # Optional: pip install pillow --global-option=”build_ext” --global-option=”--disable-jpeg”
    #We need add a sub folder in the media folder nameing profile_pics. 
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username