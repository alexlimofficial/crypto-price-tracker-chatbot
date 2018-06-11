"""
Author: Alex Lim

Cisco Webex Teams Bot: Cryptocurrency Price Tracker Bot.

Pulls cryptocurrency data from CryptoCompare
Documentation/Source: https://min-api.cryptocompare.com/

Endpoint: https://min-api.cryptocompare.com/data/price

Parameters: ?fsym=BTC&tsyms=USD,JPY,EUR
    - fsym = From Symbol (Crytocurrency Ticker/Symbol)
    - tsyms = To Symbols (Converts Cryptocurrency Price to XX Currency)

@commands
--help me
--hello
--price <crypto symbol>  

References:
https://developer.webex.com/getting-started.html
http://ciscosparkapi.readthedocs.io/en/latest/index.html
https://developer.webex.com/webhooks-explained.html?utm_source=Llab3&utm_medium=step3&utm_campaign=spark
"""
from pprint import pprint
from webhooks import set_webhooks
import HTTPmethods
import requests
import json
import sys
import os
try:
    from flask import Flask
    from flask import request
except ImportError as e:
    print(e)
    print("Looks like 'flask' library is missing.\n"
          "Type 'pip3 install flask' command to install the missing library.")
    sys.exit()

### API endpoint URL ###
api_endpoint = "https://api.ciscospark.com/v1"

### Prompt for bot access token and ngrok URL ###
# bearer = os.environ.get("BOT_ACCESS_TOKEN", "") # BOT'S ACCESS TOKEN
bearer = str(input("Your Cisco Webex Teams Bot Access Token? "))
ngrok_url = str(input("ngrok URL? "))

### API Headers ###
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Bearer " + bearer
}

def help_me():

    return "Sure! I can help. Below are the commands that I understand:<br/>" \
           "`Help me` - I will display what I can do.<br/>" \
           "`Hello` - I will display my greeting message.<br/>" \
           "`Price` - I will display the current price of the cryptocurrency (in USD).<br/>" \
           "***Please provide the symbol and not the full name of the coin.<br/>"

def greetings():

    return "Hi, my name is **%s**.<br/>" \
           "Type `Help me` to see what I can do.<br/>" % bot_name

def get_crypto_price(symbol):
    conversion = 'USD'
    url = "https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}".format(symbol, conversion)
    resp = requests.get(url)
    
    # Check for API error codes
    if resp.status_code != 200:
        print("Error calling API, please try again")
        sys.exit()
    
    result = resp.json()
    price = "Current price of " + str(symbol) + ": $" + str(result[conversion])
    return price

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def spark_webhook():
    ### POST Request ###
    if request.method == 'POST':
        webhook = request.get_json(silent=True)
        # if webhook['data']['personEmail']!= bot_email:
            # pprint(webhook)
        if webhook['resource'] == "memberships" and webhook['data']['personEmail'] == bot_email:
            HTTPmethods.send_post(url="https://api.ciscospark.com/v1/messages", headers=headers,
                                  data=
                                  {
                                        "roomId": webhook['data']['roomId'],
                                        "markdown": (greetings() +
                                            "**Note This is a group room and you have to call "
                                            "me specifically with `@%s` for me to respond**" % bot_name)
                                  }
                                 )
        msg = None
        if "@webex.bot" not in webhook['data']['personEmail']:
            result = HTTPmethods.send_get(
                url='https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']),
                headers=headers)
            in_message = result.get('text', '').lower()
            in_message = in_message.replace(bot_name.lower() + " ", '')
            if in_message.startswith('help me'):
                msg = help_me()
            elif in_message.startswith('hello'):
                msg = greetings()
            elif in_message.startswith('price'):
                msg = get_crypto_price(in_message.split(' ')[1].upper())
            else:
                msg = "Sorry, but I did not understand your request. Type `Help me` to see what I can do"
            if msg != None:
                HTTPmethods.send_post(url="https://api.ciscospark.com/v1/messages", headers=headers,
                                      data={"roomId": webhook['data']['roomId'], "markdown": msg})
        return "true"
        
    ### GET Request ###
    elif request.method == 'GET':
        """ Static HTML to display on http://localhost:8080 """
        message = "<center><img src=\"https://cdn-images-1.medium.com/max/800/1*wrYQF1qZ3GePyrVn-Sp0UQ.png\" alt=\"Spark Bot\" style=\"width:256; height:256;\"</center>" \
                  "<center><h2><b>Congratulations! Your <i style=\"color:#ff8000;\">%s</i> bot is up and running.</b></h2></center>" \
                  "<center><b><i>Don't forget to create Webhooks to start receiving events from Cisco Webex Teams!</i></b></center>" % bot_name
        return message

def main():
    global bot_email, bot_name
    set_webhooks(bearer, ngrok_url)     # Create the required webhooks for new memberships and new messages
    if len(bearer) != 0:
        test_auth = HTTPmethods.send_get("https://api.ciscospark.com/v1/people/me", headers=headers, js=False)
        if test_auth.status_code == 401:
            print("Looks like the provided access token is not correct.\n"
                  "Please review it and make sure it belongs to your bot account.\n"
                  "Do not worry if you have lost the access token. "
                  "You can always go to https://developer.ciscospark.com/apps.html "
                  "URL and generate a new access token.")
            sys.exit()
        if test_auth.status_code == 200:
            test_auth = test_auth.json()
            bot_name = test_auth.get("displayName","")
            bot_email = test_auth.get("emails","")[0]
    else:
        print("'bearer' variable is empty! \n"
              "Please populate it with bot's access token and run the script again.\n"
              "Do not worry if you have lost the access token. "
              "You can always go to https://developer.ciscospark.com/apps.html "
              "URL and generate a new access token.")
        sys.exit()

    if "@webex.bot" not in bot_email:
        print("You have provided an access token which does not relate to a Bot Account.\n"
              "Please change for a Bot Account access toekneview it and make sure it belongs to your bot account.\n"
              "Do not worry if you have lost the access token. "
              "You can always go to https://developer.ciscospark.com/apps.html "
              "URL and generate a new access token for your Bot.")
        sys.exit()
    else:
        app.run(host='localhost', port=8080)

if __name__ == "__main__":
    main()
