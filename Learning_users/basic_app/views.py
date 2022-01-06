from django.shortcuts import render

from basic_app.forms import UserForm, UserProfileInfoForm

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

#Django 2.0 removes the django.core.urlresolvers module, which was moved to django.urls
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

#This @login_required decorator is a inbuilt function which makes sure that user is logged in.
#This is just additional method where we send that the user is logged in. we can give additional functionality also after login. 
@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in. Nice!")

#This @login_required decorator is a inbuilt function which makes sure that user is logged in.
@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # We are saving the user form directly to the database.
            user = user_form.save()
            
            # This is essentially hashing the password using set_password() method.
            user.set_password(user.password)

            #We are saving to the database
            user.save()

            # commit = false because we dont want to get errros with collisions where it tries to overwrite the User 
            profile = profile_form.save(commit=False)
            
            # This sets up the one to one relationship, In models.py in UserProfileInfo that user is equal to one to one relationship with the user which is imported.
            profile.user = user

            # Check if they provided a profile picture
            # request.FILES is used because its actually a file(images,pdf,files,png, etc).
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                #profile_pic is the key which we defined in the models.py
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            #.errors will fetch the error occured.
            print(user_form.errors,profile_form.errors)
    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'basic_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        # Here we are getting username form the login.html the input tag name="username"
        username = request.POST.get('username')
        
        # Here we are getting username form the login.html the input tag name="password"
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                # Basically we are doing the user login successful and provide access to the homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'basic_app/login.html', {})




    