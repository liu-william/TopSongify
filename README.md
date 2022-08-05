# <h1 style="text-align: center;">TopSongify</h1>
A simple Spotify playlist generator script based on user's listening activities.

## Inspiration
Just an avid music lover who loves to analyze their music activities and creating playlists.

## What it does
TopSongify will create playlists based on your Spotify listening activity! You have the option of choosing from the time frames: 4 weeks, 6 weeks, or all time. You can also choose the length of the playlist: 10-50 songs. 

## Future Improvements
Something that I would love to implement is to complete the Authorization Code Flow with PKCE with Flask. Currently, I am asking the user to paste the redirect URL.

In addition, there is so much more that you can do with the Spotify API. I want to be able to further analyze music activities and create more playlists with them. 

## Usage
Create an app on https://developer.spotify.com/dashboard/
Go to the app settings and add http://localhost/topsongify/callback/ to the Redirect URIs

```
git clone https://github.com/liu-william/TopSongsify
pip3 install -r requirements.txt
cd TopSongify
python3 main.py
```

Just follow the prompts and a playlist will be generated!