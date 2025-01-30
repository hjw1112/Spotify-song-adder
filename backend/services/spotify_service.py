import os
import json
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
# from ..config.config import Config
from flask import session

load_dotenv()


sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
    scope="playlist-modify-public playlist-modify-private"
))


def search_track(track_array):
    error = False
    uri_list = []
    error_list = []
    for i, track_data in enumerate(track_array):
        try:
            song_title = track_data["title"]
            artist_name = track_data["artist"]
            query = f"track:{song_title} artist:{artist_name}"
            results = sp.search(q=query, type='track', limit=1)

            if results['tracks']['items']:
                track_uri = results['tracks']['items'][0]['uri']
                uri_list.append(track_uri)
            else:
                error = True
                error_list.append(f"No track found for '{song_title}' by '{artist_name}'")
        except KeyError as e:
            # handle missing keys in the dictionary
            error = True
            error_list.append(f"Missing key in track_array[{i}]: {e}")
        except Exception as e:
            # handle other unexpected errors
            error = True
            error_list.append(f"Error processing track_array[{i}]: {e}")


    if error == True:
        for i in range(len(uri_list)):
            if uri_list[i] == "error":
                error_list.append(i)
    
    return uri_list
                
    

def add_song_to_playlist(uri_list, playlist_id):
    success = []
    errors = []

    for track_uri in uri_list:
        try:
            sp.playlist_add_items(playlist_id, [track_uri])
            #for test
            #print(f"Track {track_uri} added to playlist {playlist_id}")
            success.append(track_uri)
        except Exception as e:
            print(f"Error adding track {track_uri}: {e}")
            errors.append({"track_uri": track_uri, "error": str(e)})

    # return the results
    return {"success": success, "errors": errors}
    

def create_playlist(user_id):
    playlist = sp.user_playlist_create(user_id, "Your songs", public=False)
    return playlist['id']










def get_spotify_oauth():
    cache_path = None
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="user-read-private user-read-email playlist-modify-public playlist-modify-private",
        cache_path=cache_path
    )


def create_spotify_instance():
    #create a spotify instance using user-specific tokens stored in session.
    token_info = session.get("token_info", None)
    if not token_info:
        raise Exception("User is not logged in")
    return Spotify(auth=token_info["access_token"])


def get_token():
    # handle spotify login and token exchange.
    sp_oauth = get_spotify_oauth()
    code = session.get("auth_code", None)
    if code:
        token_info = sp_oauth.get_access_token(code, check_cache=False)
        session["token_info"] = token_info
        return token_info
    return None


def is_logged_in():
    token_info = session.get("token_info", None)
    if not token_info:
        return False

    sp_oauth = get_spotify_oauth()
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
        session["token_info"] = token_info

    return True

def get_logged_in_user_id():
    try:
        token_info = session.get("token_info", None)

        # create a spotify instance with the user's token
        sp = Spotify(auth=token_info["access_token"])
        
        # fetch the user's profile
        user_profile = sp.me()
        
        # extract and return the user ID
        return user_profile["id"]
    except Exception as e:
        print(f"Error fetching user ID: {e}")
        return None