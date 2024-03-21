"""sent message to server"""
import requests
import json
def sentMessage(accessToken, roomId, Message):
    """sent message to server"""
    HTTPHeaders = {
            "Authorization": accessToken,
            "Content-Type": "application/json"
    }
    # The Webex Teams POST JSON data
    # - "roomId" is is ID of the selected room
    # - "text": is the responseMessage assembled above
    PostData = {
        "roomId": roomId,
        "text": Message
    }
    # Post the call to the Webex Teams message API.
    r = requests.post("https://webexapis.com/v1/messages",
                        data=json.dumps(PostData),
                        headers=HTTPHeaders
                        )
    if not r.status_code == 200:
        raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(
            r.status_code, r.text))

