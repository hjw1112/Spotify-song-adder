from ..services.langchain_service import analyse_text, extract_text_from_img
#from ..services.langchain_service import spotify stuff
from flask import Blueprint, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os

routes = Blueprint('routes', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@routes.route('/')
def home():
    return render_template('index.html')


@routes.route('/process', methods=['POST'])
def analyse():
    if request.json and 'text' in request.json:
        text = request.json['text']
        analysis = analyse_text(text) # analyse text
        # spotify_result = add_song_to_playlist(analysis)  # add to Spotify
        return jsonify({
            "type": "text", 
            "analysis": analysis, 
            # "spotify_result": spotify_result
        })

    elif 'image' in request.files:
        image = request.files['image']
        filename = secure_filename(image.filename)

        # save the file
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(file_path)

        # text extraction from the image
        extracted_text = extract_text_from_img(file_path)
        analysis = analyse_text(extracted_text)  # analyse the extracted text
        # spotify_result = add_song_to_playlist(analysis)  # add to Spotify
        return jsonify({
            "type": "image",
            "extracted_text": extracted_text,
            "analysis": analysis,
            # "spotify_result": spotify_result
        })

    # invalid input
    return jsonify({"error": "Invalid input. Provide either 'text' as JSON or an image as form-data."}), 400
    

