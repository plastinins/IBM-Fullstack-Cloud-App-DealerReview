import requests
import json
import urllib
import datetime
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from .local_settings import NLU_API_KEY, NLU_API_URL


def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)

        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")

    return ""



def post_request(url, json_payload, **kwargs):
    print("Payload: ", json_payload, ". Params: ", kwargs)
    print("POST TO {} ".format(url))
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                json=json_payload, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Method to get dealers from a cloud function
def get_dealers_from_cf(url, state=""):
    results = []
    # Call get_request with a URL parameter
    if state == "":
        json_result = get_request(url)
    else:
        json_result = get_request(url, state=state)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],state=dealer["state"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results


# Method to get dealer by id from a cloud function
def get_dealer_by_id_from_cf(url, dealer_id):
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealer_id)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # Just to take the first entry if it exists
        for dealer in dealers:
            # Create a CarDealer object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],state=dealer["state"],
                                   st=dealer["st"], zip=dealer["zip"])
            return dealer_obj

    return None


# Method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["entries"]
        # For each dealer object
        for review in reviews:
            # Create a DealerReview object
            if review["purchase"]:
                review_obj = DealerReview(make=review["car_make"], model=review["car_model"], 
                                    year=review["car_year"], dealer_id=review["dealership"], 
                                    id=review["id"], name=review["name"], purchase=review["purchase"], 
                                    purchase_date=review["purchase_date"], review=review["review"])
            else:
                review_obj = DealerReview(dealer_id=review["dealership"], 
                                    id=review["id"], name=review["name"], purchase=review["purchase"], 
                                    review=review["review"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results

# Method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    result = "Not checked"
    try:
        json_result = get_request(url=NLU_API_URL, 
                        api_key=NLU_API_KEY, 
                        version="2021-03-25",
                        features="sentiment",
                        text=urllib.parse.quote_plus(text))
        result = json_result["sentiment"]["document"]["label"]
    
    finally:
        return result

