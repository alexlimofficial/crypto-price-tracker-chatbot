"""
Author: Alex Lim

Module for setting up the required webhooks. There are two webhooks that are utilized:
    1) Webhooks for notifying application of new membership (new member in space or bot added to new space)
    2) Webhooks for notifying application that a new message is posted
"""
import requests 
import sys

def set_webhooks(bearer, ngrok_url):
    url = "https://api.ciscospark.com/v1/webhooks"  # Cisco API endpoint - webhooks

    headers = {                                     # Headers
        "Authorization": "Bearer " + bearer, 
        "Content-Type": "application/json"
    }   

    payload1 = {                    # Request parameters for webhook 1: memberships/created
        "name": "Webhook 1",
        "targetUrl": ngrok_url,
        "resource": "memberships",
        "event": "created"
    }

    payload2 = {                    # Request parameters for webhook 2: messages/created
        "name": "Webhook 2",
        "targetUrl": ngrok_url,
        "resource": "messages",
        "event": "created"
    }

    # Setup webhook 1
    webhook1 = requests.post(url=url, json=payload1, headers=headers)
    if webhook1.status_code != 200:
        print("Status Code", webhook1.status_code, ": Unable to setup webhook 1.")
        sys.exit()
    else:
        print("SUCCESS: Webhook 1 created.")

    # Setup webhook 2
    webhook2 = requests.post(url=url, json=payload2, headers=headers)
    if webhook2.status_code != 200:
        print("Status Code", webhook1.status_code, ": Unable to setup webhook 2.")
        sys.exit()
    else:
        print("SUCCESS: Webhook 2 created")