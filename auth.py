import string
import urllib.parse
import requests
import base64
import sys
import random
import pkce

REDIRECT_URI = "http://localhost/topsongify/callback/"
TOKEN_QUERY = "https://accounts.spotify.com/api/token"
CHARACTERS = string.ascii_letters + string.digits

def retrieve_info() -> str: 
    """
        Retrieve user info.

        Returns:
            client_creds_b64 (str): Client Credentials in byte 64 format.
            state (str): State for prevention.
            client_id (str): App Client ID.
            code_verifier (str): Code Verifier for PKCE ext.
    """
    
    ######## REPLACE THESE 2 WITH OWN INFO... DO NOT COMMIT ########
    client_id = input("Enter Client ID: ").strip()
    client_secret = input("Enter Client Secret: ").strip()
    ################################################################

    scope = "user-top-read playlist-modify-public playlist-modify-private"
    client_creds_b64 = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds_b64.encode()).decode()
    state = "".join(random.choice(CHARACTERS) for i in range(16))    # Used to prevent forgery attacks.

    # PKCE (proof key for code exchange) for token verification.
    code_verifier = pkce.generate_code_verifier(length=random.choice([i for i in range(43, 129)]))
    code_challenge = pkce.get_code_challenge(code_verifier)

    auth_url = "https://accounts.spotify.com/authorize"
    auth_url += "?client_id=" + urllib.parse.quote(client_id)    # URL encode string
    auth_url += "&response_type=code"
    auth_url += "&redirect_uri=" + urllib.parse.quote(REDIRECT_URI)    
    auth_url += "&scope=" + urllib.parse.quote(scope)
    auth_url += "&state=" + urllib.parse.quote(state)    
    auth_url += "&show_dialog=true"    # To approve app each time
    auth_url += "&code_challenge_method=S256"
    auth_url += "&code_challenge=" + urllib.parse.quote(code_challenge)

    print("\nPlease authenticate using this URL: " + auth_url + "\n")

    return client_creds_b64, state, client_id, code_verifier

def authenticate_user(client_creds_b64: str, state: str, client_id: str, code_verifier: str) -> str:
    """
        Authenticate the user.

        Args:
            client_creds_b64 (str): Client Credentials in byte 64 format.
            state (str): State for prevention.
            client_id (str): App Client ID.
            code_verifier (str): Code Verifier for PKCE ext.

        Returns:
            (str): User's session access token.
    """

    redirected_url = input("Please paste the full redirected URL: ")

    # Extract access code
    code = redirected_url[len(REDIRECT_URI + "?code="):-len("&state=" + state)]
    returned_state = redirected_url[len(REDIRECT_URI + "?code=" + code + "&state=")]

    # Check for forgery attacks. 
    if returned_state != state:
        print("Returned state does match with state, Abort!")
        sys.exit()

    # Request Access token
    request_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": client_id,
        "code_verifier": urllib.parse.quote(code_verifier)
    }

    request_header = {
        "Authorization": "Basic " + client_creds_b64, 
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response_json = requests.post(
        url=TOKEN_QUERY, 
        data=request_data, 
        headers=request_header
    ).json()
    
    # Retrieve access token
    try:
        return response_json["access_token"]
    except KeyError as e:
        print("\nWrong redirected URL")
        return
    

def get_access_token():
    """
        Gives users 2 tries to get access token.

        Returns:
            access_token (str): User's session access token.
    """

    client_creds_b64, state, client_id, code_verifier = retrieve_info()
    access_token = None
    tries = 0

    # Authenticate (up to 2 tries)   
    while not access_token and tries < 2:
        access_token = authenticate_user(client_creds_b64, state, client_id, code_verifier)
        tries += 1
    
    if access_token:
        return access_token 
    
    print("Failed to authenticate after 2 tries. Program terminating")
    sys.exit()