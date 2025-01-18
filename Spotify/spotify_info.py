import time
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler

try:
    import http.server
except ImportError:
    print("http.server module is missing. Ensure you're using Python 3.x.")
    raise

client_id = '832b6169fcec41e39354f2f39bfc2dd2'
client_secret = 'b1d6ae94f59642d3ba2ec4b7fafb8118'
redirect_uri = 'http://localhost:5000/callback'
scope = 'user-read-currently-playing'

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=CacheFileHandler(),
    show_dialog=True
))

def get_current_song_data():
    """Fetch the currently playing track's data from Spotify."""
    try:
        song_data = sp.current_user_playing_track()
        if song_data and song_data.get('item'):
            return song_data
        return None
    except Exception as e:
        print(f"Error fetching current song: {e}")
        return None

def get_song_name(song_data):
    """Extract and return the song name."""
    if song_data:
        return song_data['item']['name']
    return "No song is currently playing."

def get_artist_name(song_data):
    """Extract and return the artist(s) name(s)."""
    if song_data:
        return ", ".join(artist['name'] for artist in song_data['item']['artists'])
    return "No artist is currently playing."

def update_currently_playing(interval=5):
    """Continuously fetch and display the currently playing track."""
    print("Fetching currently playing song... (Press Ctrl+C to stop)")
    try:
        while True:
            song_data = get_current_song_data()
            song_name = get_song_name(song_data)
            artist_name = get_artist_name(song_data)
            print(f"Currently playing: {song_name} by {artist_name}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped updating currently playing song.")

if __name__ == "__main__":
    update_currently_playing(interval=5)