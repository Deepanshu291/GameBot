import requests
import os

API_KEY = 'vYfvAY2ydmrv'
# API_KEY = os.environ['RSAKEY']

url = "https://random-stuff-api.p.rapidapi.com/ai"



def Bot(msg):
    querystring = {"msg": msg, "bot_name": "DogeBot", "bot_gender": "male (OPTIONAL)", "bot_master": "DevDt",
               "bot_age": "BAAP Bara bar", "bot_location": "India (OPTIONAL)"}

    headers = {
    'authorization': API_KEY,
    'x-rapidapi-host': "random-stuff-api.p.rapidapi.com",
    'x-rapidapi-key': "bb5d2d508fmsh2df345d6ad087c9p1612bfjsn88a03730773d"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    r = response.text
    r = r.split('"AIResponse":"')
    r = r[1]
    r = r.replace('"}','')
    return r
    print(r)

