import requests
from secrets import client_id, client_secret, REDIRECT_URI, access_token, user_id

CLIENT_ID = client_id
CLIENT_SECRET = client_secret
REDIRECT_URI = REDIRECT_URI

class CreatePlaylist:
    def __init__(self):
        self.access_token = access_token
        self.tracks = ""
        self.user_id = user_id

    def get_top_songs(self):
        query = "https://api.spotify.com/v1/me/top/tracks"

        request_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.access_token),
        }

        request_params = {
            "time_range": "short_term",
            "limit": "50",
            "offset": "0",
        }

        response = requests.get(
            query, 
            params=request_params, 
            headers=request_headers
            )
        
        response_json = response.json()
        
        for item in response_json["items"]:
            self.tracks += (item["uri"] + ",")
   
        self.tracks = self.tracks[:-1]

    def create_playlist(self):
        # today = date.today()
        # todayFormatted = today.strftime("%dd/%mm/%Y")
        
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)

        request_body = {
            "name": "On Repeat",
            "description": "Songs you love", 
            "public": False
        }

        request_headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer {}".format(self.access_token)
        }

        response = requests.post(
            query, 
            data=request_body, 
            headers=request_headers
        )
        
        response_json = response.json()

        return response_json["id"]    # Created playlist ID

    def add_to_playlist(self):
        
        self.new_playlist_id = self.create_playlist()

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id, self.tracks)

        request_headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer {}".format(self.access_token)
        }
        response = requests.post(
            query,
            headers=request_headers
        )

        print(response)

def main():
    a = CreatePlaylist()
    a.get_top_songs()
    a.create_playlist()
    a.add_to_playlist()

if __name__ == "__main__":
    main()