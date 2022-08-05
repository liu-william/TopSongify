import requests
from auth import get_access_token

def main():
    make_playlist = True
    newPlaylist = CreatePlaylist()
    user_id = newPlaylist.get_user_id()

    while make_playlist:
        newPlaylist.get_top_songs()
        playlist_id = newPlaylist.create_playlist(user_id)
        newPlaylist.add_to_playlist(playlist_id)
        make_playlist = True if input("Make another playlist? Y/N: ").strip().upper() == "Y" else False

class CreatePlaylist:
    def __init__(self):
        """
            Initialize CreatePlaylist.
        """

        self.access_token = get_access_token()
        self.tracks = ""
        self.time = 0
        self.time_range = {
            1: "short_term",
            2: "medium_term",
            3: "long_term"
        }
        self.limit = 0


    def get_user_id(self) -> str:
        """
            Get's Spotify user ID.

            Returns:
                (str): Spotify user's ID.
        """

        query = "https://api.spotify.com/v1/me"

        request_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.access_token)
        }

        response = requests.get(query, headers=request_headers)

        response_json = response.json()

        return response_json["id"]

    def get_top_songs(self):
        """
            Gets user's top songs.
        """

        self.tracks = ""

        correct_time = False
        correct_limit = False

        while not correct_time: 
            print("\nSelect from the following time ranges.")
            self.time = int(input(" 1. 4 weeks \n 2. 6 weeks \n 3. All Time \n\nTime Range? "))
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

    def create_playlist(self, user_id: str) -> str:
        """
            Creates empty playlist.

            Args: 
                user_id (str): Spotify user ID.
            Returns: 
                (str): New playlist ID.
        """
        
        query = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)

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

    def add_to_playlist(self, playlist_id: str):
        """
            Populates top songs to playlist.
            
            Args: 
                playlist_id (str): New playlist ID
        """

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(playlist_id, self.tracks)

        request_headers = {
            "Accept": "application/json", 
            "Content-Type": "aaplication/json",
            "Authorization": "Bearer {}".format(self.access_token)
        }

        response = requests.post(
            query,
            headers=request_headers
        )

        response_json = response.json()

        try: 
            response_json["snapshot_id"]
            print("Playlist created successfully!\n")
        except Exception:
            print("Error creating playlist, try again.")

if __name__ == "__main__":
    main()