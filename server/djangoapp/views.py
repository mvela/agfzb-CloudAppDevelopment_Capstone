"""
This module provides views for the dealership application.

It includes views to render the index page, about page, contact page, 
and handle user authentication including login, logout, and registration.
"""
import logging
from django.http import HttpResponseNotAllowed
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def get_dealerships(request):
    """
    Update the `get_dealerships` view to render the index page with a list of dealerships
    """
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)
    return HttpResponseNotAllowed("GET")

def about(request):
    """
    Create an `about` view to render a static about page
    """
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)
    return HttpResponseNotAllowed("GET")

def contact(request):
    """
    Create a `contact` view to return a static contact page
    """
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)
    return HttpResponseNotAllowed("GET")

def login_request(request):
    """
    Create a `login_request` view to handle sign in request
    """
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/login.html', context)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:get_dealerships')
        context['message'] = 'Invalid username or password.'
        return render(request, 'djangoapp/user_login.html', context)
    return HttpResponseNotAllowed(["GET", "POST"])

def logout_request(request):
    """
    Create a `logout_request` view to handle sign out request
    """
    logout(request)
    return redirect('djangoapp:get_dealerships')

def registration_request(request):
    """
    Create a `registration_request` view to handle sign up request
    """
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    if request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        try:
            User = get_user_model() # pylint: disable=invalid-name
            User.objects.get(username=username)
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)
        except User.DoesNotExist:
            logger.debug("%s is new user", username)
        user = User.objects.create_user(username=username, first_name=first_name,
                last_name=last_name, password=password)
        login(request, user)
        return redirect("djangoapp:get_dealerships")
    return HttpResponseNotAllowed(["GET", "POST"])

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
