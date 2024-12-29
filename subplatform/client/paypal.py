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

def update_subscription_paypal(access_token, subID):
    
   bearer_token = f'Bearer {access_token}'

   headers = {
       'Content-Type': 'application/json',
       'Authorization': bearer_token,
   }

   subDetails = Subscription.objects.get(paypal_subscription_id=subID)

   # Obtain the current subscription plan for the user/client

   current_sub_plan = subDetails.subscription_plan

   if current_sub_plan == 'Standard':
       new_sub_plan_id = "P-9ST26449M6579211PM5YJRFI" # To Premium

   elif current_sub_plan == 'Premium':
       new_sub_plan_id = "P-5UT79485E39960225M5YJQEA" # To Standard

   url = f'https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{subID}/revise'

   revision_data = {
       "plan_id": new_sub_plan_id
   }

   # Make a POST request to PayPal's API for updating/revising the subscription

   response = requests.post(url, headers=headers, data=json.dumps(revision_data))

   # Output the response from PayPal

   response_data = response.json()

   print(response_data)


   approve_link = None

   for link in response_data.get('links', []):

        if link.get('rel') == 'approve':

            approve_link = link['href']

   if response.status_code == 200:

        print("Subscription updated successfully.")

        return approve_link

   else:

        print("Failed to update subscription. Status code:", response.status_code) 
        
   
def get_current_subscription(access_token, subID):
    
    bearer_token = f'Bearer {access_token}'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }

    url = f'https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{subID}'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        
        subscription_data = response.json()
        current_plan_id = subscription_data.get('plan_id')

        return current_plan_id
    
    else:

        print("Failed to get current subscription. Status code:", response.status_code)

        return None

def get_current_subscription(access_token, subID):
    
    bearer_token = f'Bearer {access_token}'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }

    url = f'https://api-m.sandbox.paypal.com/v1/billing/subscriptions/{subID}'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        
        subscription_data = response.json()
        current_plan_id = subscription_data.get('plan_id')

        return current_plan_id
    
    else:

        print("Failed to get current subscription. Status code:", response.status_code)

        return None






