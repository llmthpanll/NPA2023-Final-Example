import requests
import json
import time
from sentMessage import sentMessage


accessToken = "Bearer NjAyY2M0YzYtZmQxZS00MzhjLWI2MWEtZTc4MzJjZDA5M2NhOTI3NzRmMGQtNzM5_P0A1_6a2cc597-4b00-40e5-8b6c-999a42f528a5"

# roomIdToGetMessages = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vODFmMDk4MjAtYjY4OC0xMWVlLTgzMDItZWZhNWNiYmRkNjg0"
roomIdToGetMessages = "Y2lzY29zcGFyazovL3VzL1JPT00vZjBkZjY0NDAtYWU5Yi0xMWVlLTg5MGMtMGQzNjUwOTJlMmUy"

while True:
    time.sleep(1)
    GetParameters = {
        "roomId": roomIdToGetMessages,
        "max": 1
    }
    r = requests.get("https://webexapis.com/v1/messages",
                     params=GetParameters,
                     headers={"Authorization": accessToken}
                     )
    if not r.status_code == 200:
        raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(
            r.status_code, r.text))

    json_data = r.json()
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)

    # check if the text of the message starts with the magic character "/" and yourname followed by a location name
    # e.g.  "/chotipat San Jose"
    if message.find("/") == 0:
        # extract name of a location (city) where we check for GPS coordinates using the OpenWeather Geocoding API
        # Enter code below to hold city name in location variable.
        # For example location should be "San Jose" if the message is "/chotipat San Jose".
        Name = message[1:message.find(" ")]
        location = message[message.find(" ")+1::]

#######################################################################################
# 5. Prepare openweather Geocoding APIGetParameters..
        # Openweather Geocoding API GET parameters:
        # - "q" is the the location to lookup
        # - "limit" is always 1
        # - "key" is the openweather API key, https://home.openweathermap.org/api_keys
        openweatherGeoAPIGetParameters = {
            "q": location,
            "limit": 1,
            "appid": "6177ca9eef14f2deffea572993c92873",
        }

#######################################################################################
# 6. Provide the URL to the OpenWeather Geocoding address API.
        # Get location information using the OpenWeather Geocoding API geocode service using the HTTP GET method
        r = requests.get("http://api.openweathermap.org/geo/1.0/direct",
                         params=openweatherGeoAPIGetParameters
                         )
        # Verify if the returned JSON data from the OpenWeather Geocoding API service are OK
        json_data = r.json()
        # check if the status key in the returned JSON data is "0"
        if not r.status_code == 200:
            responseMessage = "Dear {}\nI am sorry, I cannot found {}. Please type location in List of ISO 3166 country codes".format(Name, location)
            
            sentMessage(accessToken, roomIdToGetMessages, responseMessage)
            
            print("Dear {}\nI am sorry, I cannot found {}. Please type location in List of ISO 3166 country codes".format(Name, location))
            continue
            raise Exception(
                "Incorrect reply from OpenWeather Geocoding API. Status code: {}".format(r.status_code))

#######################################################################################
# 7. Provide the OpenWeather Geocoding key values for latitude and longitude.
        # Set the lat and lng key as retuned by the OpenWeather Geocoding API in variables
        try:
            locationLat = json_data[0].get("lat")
            locationLng = json_data[0].get("lon")
        except:
            responseMessage = "Dear {}\nI am sorry, I cannot found {}. Please type /yourname location. For example, /methasit San Jose.".format(Name, location)
            
            sentMessage(accessToken, roomIdToGetMessages, responseMessage)
            
            print("I am sorry, I cannot found {}. Please type /yourname location. For example, /methasit San Jose.".format(location))
            continue

#######################################################################################
# 8. Prepare openweatherAPIGetParameters for OpenWeather API, https://openweathermap.org/api; current weather data for one location by geographic coordinates.
        # Use current weather data for one location by geographic coordinates API service in Openweathermap
        openweatherAPIGetParameters = {
            "lat": locationLat,
            "lon": locationLng,
            "appid": "6177ca9eef14f2deffea572993c92873"
        }

#######################################################################################
# 9. Provide the URL to the OpenWeather API; current weather data for one location.
        rw = requests.get("https://api.openweathermap.org/data/2.5/weather",
                          params=openweatherAPIGetParameters
                          )
        json_data_weather = rw.json()

        if not "weather" in json_data_weather:
            raise Exception("Incorrect reply from openweathermap API. Status code: {}. Text: {}".format(
                rw.status_code, rw.text))

#######################################################################################
# 10. Complete the code to get weather description and weather temperature
        weather_desc = json_data_weather["weather"][0]["description"]
        weather_temp = json_data_weather["main"]["temp"]

#######################################################################################
# 11. Complete the code to format the response message.
        # Example responseMessage result: In Austin, Texas (latitude: 30.264979, longitute: -97.746598), the current weather is clear sky and the temperature is 12.61 degree celsius.
        responseMessage = "Dear {}\nIn {} (latitude: {}, longitute: {}), the current weather is {} and the temperature is {:.2f} degree celsius.\n".format(
            Name, location, locationLat, locationLng, weather_desc, weather_temp - 273.15)
        # print("Sending to Webex Teams: " + responseMessage)

#######################################################################################
# 12. Complete the code to post the message to the Webex Teams room.
        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        sentMessage(accessToken, roomIdToGetMessages, responseMessage)
        
        
        
        
        
    # elif message.find("/") == 0:
    #     Name = message[1:message.find(" ")]
    #     location = message[message.find(" ")+1::]
    #     responseMessage = "Dear {}\nI am sorry, I cannot found {}. Please type /yourname location. For example, /methasit San Jose.".format(Name, location)
    #     sentMessage(accessToken, roomIdToGetMessages, responseMessage)
        
