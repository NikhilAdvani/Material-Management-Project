import requests

def SendMessage(msg, mobilenumber):
    url = "http://167.114.117.218/GatewayAPI/rest"
    headers = {"Cache-Control": "no-cache",'Content-Type': 'application/x-www-form-urlencoded','Accept': 'application/json'}
    data = {"loginid": 'VIKSDIWS', "password": 'vikram123@@', "msg":msg, "send_to":mobilenumber,"senderId": 'VIKSDIWS',"routeId": '8',"smsContentType": 'english'}
    response = requests.post(url=url, headers=headers, data=data)
    return response
