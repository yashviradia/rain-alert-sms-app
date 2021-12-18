import requests
from dotenv import load_dotenv, find_dotenv
import os
from twilio.rest import Client

load_dotenv(find_dotenv())


OWM_Endpoint = os.environ.get("OWM_Endpoint")
owm_api_key = os.environ.get("OWM_API_KEY")

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

# lat and lon must be private
parameters = {
    "lat": 41.015137,
    "lon": 28.979530,
    "units": "metric",
    "exclude": "current,minutely,daily",
    "appid": owm_api_key,
}

response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()

weather_slice = weather_data["hourly"][:12]
will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]

    if int(condition_code) < 700:
        will_rain = True

# Natelnummer muss privat dargestellt werden
if will_rain:
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Take an Umbrella ;).",
        from_=os.environ.get("SENDER_NUMBER"),
        to=os.environ.get("RECEIVER_NUMBER")
    )
    print(message.status)
