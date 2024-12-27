import requests
import json
from . models import Subscription

def get_access_token():
    url = 'https://api-m.sandbox.paypal.com/v1/oauth2/token'
    data = {'grant_type': 'client_credentials'}
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US'
    }

    client_id = 'Af2NgzrsNBpZWrq9DFCxQX7LtY7w3uuGzHaHk9dVKEwUUbK2eKCrZJTq0WErhu9RYXFAE5e6Be4m8Vzj'
    secret_id = 'EKXe6xK6J_cf5Q02T1TjkV_xlhSuZe3G3-ye0QJTtHrWOUCaOsrCcOHvobN0BE7WufXi7X00_6XrxGyE'

    try:
        # Make the request to PayPal's API
        response = requests.post(url, auth=(client_id, secret_id), data=data, headers=headers)

        # Check for HTTP errors
        response.raise_for_status()

        # Parse JSON response
        response_json = response.json()
        access_token = response_json.get('access_token')

        if not access_token:
            print("Error: Access token not found in response:", response_json)
            return None

        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def cancel_subscription_paypal(access_token, subID):
    # Validate access_token
    if not access_token:
        print("Access token is missing. Cannot proceed with subscription cancellation.")
        return

    url = f'https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{subID}/cancel'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        print("Subscription canceled successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to cancel subscription: {e}")