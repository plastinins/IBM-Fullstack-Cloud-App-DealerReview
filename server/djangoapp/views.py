from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import post_request, get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf
from .local_settings import FAAS_API_DEALERSHIP_URL, FAAS_API_REVIEW_URL
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    # Redirect user back to index view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        user_exist = False
        try:
            # Check if user already exists
            username = request.POST['username']
            password = request.POST['password']
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Renders the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = FAAS_API_DEALERSHIP_URL
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context['dealer_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Renders the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = FAAS_API_REVIEW_URL
        # Get reviews from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context['review_list'] = reviews
        context['dealer_id'] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)


# View to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            context["error_message"] = "Please, login at first"
            context["dealer_id"] = dealer_id
            return render(request, 'djangoapp/add_review.html', context)
        
        review = {}
        review["id"] = 0 # wtf?
        review["name"] = request.POST["newreview_name"]
        review["dealership"] = dealer_id
        review["review"] = request.POST["newreview_review"]
        review["purchase"] = request.POST["newreview_purchase"]
        review["purchase_date"] = request.POST["newreview_purchase_date"]
        review["car_make"] = request.POST["newreview_car_make"]
        review["car_model"] = request.POST["newreview_car_model"]
        review["car_year"] = request.POST["newreview_car_year"]
        json_payload = {}
        json_payload["review"] = review
        json_result = post_request(FAAS_API_REVIEW_URL, json_payload, dealerId=dealer_id)
        print("POST request result: ", json_result)
        if json_result["status"] == 200:
            context["success_message"] = "Thank you for your review!"
        else:
            context["error_message"] = "Error: review was not saved."
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/add_review.html', context)
