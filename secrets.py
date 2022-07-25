import random
import string
import urllib.parse
import requests
import base64

REDIRECT_URI = "https://topsongify.com"
CHARACTERS = string.ascii_letters + string.digits + string.punctuation
QUERY = "https://accounts.spotify.com/api/token"

client_id = input("Enter Client ID: ").strip()
client_secret = input("Enter Client Secret: ").strip()
user_id = input("Enter user ID").strip()
state = "".join(random.choice(CHARACTERS) for i in range(16))
scope = "user-top-read playlist-modify-public playlist-modify-private"

auth_url = "https://accounts.spotify.com/authorize"
auth_url += "?client_id=" + urllib.parse.quote(client_id)
auth_url += "&response_type=code"
auth_url += "&redirect_uri=" + urllib.parse.quote(REDIRECT_URI)
# auth_url += "&state=" + urllib.parse.quote(state)
auth_url += "&scope=" + urllib.parse.quote(scope)

print("Please authenticate using this URL: " + auth_url, "\n")

redirected_url = input("Please enter the full redirected_url: ")
a = REDIRECT_URI + "/?code="
b = "&state=" + state
code = redirected_url[len(a):]
# code = code[:len(b)]
# print(code)

request_data = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": REDIRECT_URI
}

request_header = {
    "Authorization": "Basic " + str(base64.b64encode(bytes(client_id + ":" + client_secret, "utf-8")))[2:-1], 
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(
    url=QUERY, 
    data=request_data, 
    headers=request_header
)

response_json = response.json()

access_token = response_json["access_token"]