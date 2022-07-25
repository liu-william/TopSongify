import requests
from secrets import client_id, client_secret, REDIRECT_URI, access_token, user_id

CLIENT_ID = client_id
CLIENT_SECRET = client_secret
REDIRECT_URI = REDIRECT_URI
USER_ID = user_id

class CreatePlaylist:
    def __init__(self):
        self.access_token = access_token
        self.tracks = ""
        self.time = 0
        self.time_range = {
            1: "short_term",
            2: "medium_term",
            3: "long_term"
        }
        self.limit = 0

    def get_top_songs(self):
        correct_time = False
        correct_limit = False

        while not correct_time: 
            self.time = int(input(" 1. 4 weeks \n 2. 6 weeks \n 3. All Time \nTime Range? "))
            correct_time = True if (self.time in self.time_range) else False
            if not correct_time:
                print("Invalid answer\n")            

        while not correct_limit:
            self.limit = int(input("Song limit? Enter an integer between 10 - 50: "))
            correct_limit = False if self.limit < 10 or self.limit > 50 else True
            if not correct_limit:
                print("Invalid answer\n")        

        query = "https://api.spotify.com/v1/me/top/tracks"

        request_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.access_token)
        }

        request_params = {
            "time_range": self.time_range[self.time],
            "limit": self.limit,
            "offset": "0"
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
        
        query = "https://api.spotify.com/v1/users/{}/playlists".format(USER_ID)

        request_data = {
            "name": "On Repeat {}".format(" ".join(self.time_range[self.time].split("_")).title()),
            "description": "{} Songs that you love {}".format(self.limit, " ".join(self.time_range[self.time].split("_")).title()), 
            "public": False
        }

        request_headers = {
            "Accept": "application/json", 
            "Authorization": "Bearer {}".format(self.access_token)
        }

        response = requests.post(
            query, 
            headers=request_headers, 
            json=request_data
        )
        
        response_json = response.json()

        return response_json["id"]    # Created playlist ID

    def add_to_playlist(self):
        
        self.new_playlist_id = self.create_playlist()

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id, self.tracks)

        request_headers = {
            "Accept": "application/json", 
            "Content-Type": "aaplication/json",
            "Authorization": "Bearer {}".format(self.access_token)
        }
        response = requests.post(
            query,
            headers=request_headers
        )

def main():
    a = CreatePlaylist()
    a.get_top_songs()
    a.add_to_playlist()

if __name__ == "__main__":
    main()