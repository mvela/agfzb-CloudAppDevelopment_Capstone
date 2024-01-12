"""
This module provides views for the dealership application.

It includes views to render the index page, about page, contact page, 
and handle user authentication including login, logout, and registration.
"""
import logging
from django.http import HttpResponseNotAllowed, HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def get_dealerships(request):
    """
    Get the list of dealerships from a remote server and render them in the index.html template.
    """

    url = "http://localhost:3000/dealerships/get"
    dealerships = get_dealers_from_cf(url)
    context = {"dealerships": dealerships}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)
    return HttpResponseNotAllowed("GET")

def about(request):
    """
    Renders the about page.
    """
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)
    return HttpResponseNotAllowed("GET")

def contact(request):
    """
    Renders the contact page.
    """
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)
    return HttpResponseNotAllowed("GET")

def login_request(request):
    """
    Handles the login request from the user.

    This function checks the request method and performs the necessary actions based on it.
    If the method is GET, it renders the login page.
    If the method is POST, it authenticates the user's credentials and redirects to the dealership page if successful.
    If the authentication fails, it displays an error message.
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
    Logs out the user and redirects to the dealership page.
    """
    logout(request)
    return redirect('djangoapp:get_dealerships')

def registration_request(request):
    """
    Handles the registration request from the user.
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
def get_dealer_details(request, dealer_id):
    """
    Get the details of a specific dealer.
    """
    url = "http://localhost:5000/api/get_reviews"
    reviews = get_dealer_reviews_from_cf(url, dealer_id)
    context = {"reviews": reviews}
    if request.method == "GET":
        return render(request, 'djangoapp/dealer_details.html', context)
    return HttpResponseNotAllowed("GET")


# Create a `add_review` view to submit a review