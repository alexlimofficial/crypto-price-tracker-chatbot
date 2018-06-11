# Cisco Webex Teams Bot: Crypto Price Tracker

This repository consists of a cryptocurrency price quote query chatbot designed for 
the Cisco Webex Teams application. 

## Requirements

1. Python 3.5+ 
2. ngrok 
3. Cisco Webex Teams (formerly Cisco Spark) 
4. Cisco Webex Teams Developer Account (with bot access token)

## How To Run

### Run Bot

Open a terminal and run the python file ```crypto-bot.py```. This will create the required webhooks and launch the application
on a test environment running on localhost port 8080. 

```
$ python crypto-bot.py
```

### ngrok 

A key requiremenet for a bot application is that it should be reachable via a publicly accessible internet address/port. 
The open source tool and service called **ngrok** was used to create a virtual tunnel between the PC running the application 
and the internet. This tunnel allows incoming HTTP requests sent to a special URL at the ngrok cloud service to be relayed 
through to the listening bot application. 

```
For Linux/macOS: ./ngrok http 5000
For Windows: ngrok http 8080
```

## Cisco Webex Teams 

Because this chatbot is designed specifically for the Cisco Webex Teams application, users must download Cisco Webex Teams in order to use it. Once downloaded, create a new space and add the chatbot to the space. 

### Interacting with the chatbot

**Commands**
```Help me```               : Shows all commands that bot is capable of interpreting.
```Hello```                 : Prompts a greeting from the bot. 
```Price <crypto symbol>``` : Returns current data on cryptocurrency. 