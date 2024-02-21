import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
import os

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(**kwargs):
    url = "http://localhost:3000/dealerships/get"
    results = []
    # Check if dealer_id is in kwargs
    if 'dealer_id' in kwargs:
        dealer_id = kwargs['dealer_id']
        # Call get_request with a URL parameter
        json_result = get_request(url, id=dealer_id)
    else:
        json_result = get_request(url)

    if json_result:
        dealers = json_result
        for dealer in dealers:
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

def analyze_review_sentiments(text):
    nlu_api_key = os.environ.get('NLU_API_KEY')
    url = os.environ.get('NLU_URL')
    if not nlu_api_key or not url:
        print('No NLU service credentials')
        return None
    authenticator = IAMAuthenticator(nlu_api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(text=text, 
        features=Features(sentiment=SentimentOptions(targets=[text])),
        language='en').get_result()
    label = json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    return label


def get_dealer_reviews_from_cf(dealer_id):
    results = []
    # Call get_request with a URL parameter
    url = "http://localhost:5000/api/get_reviews"
    json_result = get_request(url, id=dealer_id)
    if json_result:
        reviews = json_result
        for review in reviews:
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review["dealership"], username=review["username"], name=review["name"], purchase=review["purchase"],
                                   review=review["review"], purchase_date=review["purchase_date"], car_make=review["car_make"],
                                   car_model=review["car_model"],
                                   car_year=review["car_year"], sentiment="None")

            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(json_payload, **kwargs):
    #microservice enpoint to post review
    url = "http://localhost:5000/api/post_review"
    print("POST from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
