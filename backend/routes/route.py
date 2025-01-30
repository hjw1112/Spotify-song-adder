from ..services.langchain_service import analyse_text, extract_text_from_img
from ..services.spotify_service import search_track, add_song_to_playlist, create_playlist, get_spotify_oauth, create_spotify_instance, get_token, is_logged_in, get_logged_in_user_id
from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from werkzeug.utils import secure_filename
import os
from spotipy import Spotify

routes = Blueprint('routes', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



@routes.route('/login')
def login():
    #redirect the user to Spotify's authorization page.
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)


@routes.route('/callback')
def callback():
    #handle spotify's redirect, fetch the access token, and get user profile.
    sp_oauth = get_spotify_oauth()
    code = request.args.get("code")
    if not code:
        return "Authorization failed", 100

    #fetch token info
    token_info = sp_oauth.get_access_token(code, check_cache=False)
    session["token_info"] = token_info

    #fetch user profile
    sp = Spotify(auth=token_info["access_token"])
    user_profile = sp.me()
    session["username"] = user_profile.get("display_name", "Unknown User")  #store username in session

    #redirect to the index page
    return redirect(url_for("routes.index"))


@routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("landing"))



@routes.route('/index')
def index():
    if not is_logged_in():
        return redirect(url_for("routes.login"))

    username = session.get("username", "Unknown User")  #get username from session
    return render_template("index.html", username=username)


@routes.route('/process', methods=['POST'])
def analyse():
    try:
        song_array = None

        #handle text input
        if request.is_json:
            try:
                data = request.get_json()
                if 'text' in data:
                    text = data['text']

                text = request.json['text']
                if not text.strip():
                    return jsonify({"error": "Text input cannot be empty"}), 200

                song_array = analyse_text(text)  # analyse the text
                if not song_array or len(song_array) == 0:
                    return jsonify({"error": "No valid songs found in the text"}), 300
            except Exception as e:
                return jsonify({"error": f"Failed to parse JSON: {str(e)}"}), 400
            
        #handle image input
        elif 'image' in request.files:
            image = request.files['image']
            if image.filename == '':
                return jsonify({"error": "No image file provided"}), 500

            #save and process the uploaded image
            filename = secure_filename(image.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(file_path)

            #extract text and analyse it
            extracted_text = extract_text_from_img(file_path)
            song_array = analyse_text(extracted_text)
            if not song_array or len(song_array) == 0:
                return jsonify({"error": "No valid songs found in the image"}), 600

        #invalid input
        else:
            return jsonify({"error": "Invalid input. Provide either 'text' or an image."}), 700

        #create spotify playlist and add songs
        user_id = get_logged_in_user_id()
        if not user_id:
            return jsonify({"error": "User not logged in"}), 800

        playlist_id = create_playlist(user_id)
        if not playlist_id:
            return jsonify({"error": "Failed to create playlist"}), 900

        uri_list = search_track(song_array)
        if not uri_list or len(uri_list) == 0:
            return jsonify({"error": "No tracks found for the given songs"}), 1000

        add_song_to_playlist(uri_list, playlist_id)

        #return JSON response with playlist_id
        return jsonify({"playlist_id": playlist_id})

    except Exception as e:
        print(f"Error in /process route: {e}")
        return jsonify({"error": "Internal Server Error"}), 110


