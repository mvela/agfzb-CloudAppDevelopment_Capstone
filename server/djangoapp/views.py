"""
This module provides views for the dealership application.

It includes views to render the index page, about page, contact page, 
and handle user authentication including login, logout, and registration.
"""
import logging
import json
from django.http import HttpResponseNotAllowed, HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import CarDealer, CarMake, CarModel, DealerReview
import datetime
from datetime import date

# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_dealerships(request):
    """
    Get the list of dealerships from a remote server and render them in the index.html template.
    """
    state = request.GET.get("state", None)
    context = {}
    if state:
        dealerships = get_dealers_from_cf(state=state)
        context["state"] = state
    else:
        dealerships = get_dealers_from_cf()
    context["dealerships"] = dealerships
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
        return render(request, 'djangoapp/user_login.html', context)
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

def get_dealer_details(request, dealer_id):
    """
    Get the details of a specific dealer.
    """
    reviews = get_dealer_reviews_from_cf(dealer_id)
    dealership = get_dealers_from_cf(dealer_id=dealer_id)[0]
    context = {"dealership": dealership, "reviews": reviews}
    if request.method == "GET":
        return render(request, 'djangoapp/dealer_details.html', context)
    return HttpResponseNotAllowed("GET")


@login_required(login_url='/djangoapp/login')
def add_review(request, dealer_id):
    """
    Add a review for a specific dealer.
    """
    dealership = get_dealers_from_cf(dealer_id=dealer_id)[0]
    cars = CarModel.objects.filter(dealerId=dealer_id)
    context = {"dealership": dealership , "cars": cars}
    if request.method == "GET":
        return render(request, 'djangoapp/add_review.html', context)
        
    if request.method == "POST":
        review = {}
        review["purchase"] = request.POST.get("purchase")
        review["review"] = request.POST.get("review")
        review["dealership"] = dealer_id
        review["username"] = request.user.username
        review["name"] = request.user.first_name + " " + request.user.last_name
        review["review_date"] = datetime.datetime.now().isoformat()
        if request.POST.get("purchase"):
            review["purchase_date"] = request.POST.get("purchaseDate")
            if "purchaseDate" not in request.POST or "carOptions" not in request.POST:
                return HttpResponse("Missing required fields", status=400)
            review["purchase_date"] = request.POST.get("purchaseDate")
            car_model_id = request.POST.get("carOptions")
            car = CarModel.objects.get(id=car_model_id)
            review["car_model"] = car.name
            review["car_make"] = car.make.name
            review["car_year"] = car.year
        payload = review
        post_request(payload, dealer_id=dealer_id)
        return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
    return HttpResponseNotAllowed(["GET", "POST"])
