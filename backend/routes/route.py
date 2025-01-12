from services.langchain_service import analyse_text
from backend.services.spotify_service import add_song_to_playlist

from flask import Blueprint, request, jsonify, render_template

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/analyze', methods=['POST'])
def analyse():
    text = request.json.get('text')
    analysis = analyse_text(text)  #process text with openai
    return jsonify({"analysis": analysis})

