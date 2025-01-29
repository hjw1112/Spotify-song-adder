import json
import pytesseract 
import os
from PIL import Image
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from ..config.config import Config

tesseract_path = os.getenv("PYTESSERACT_PATH", "/usr/bin/tesseract")

pytesseract.pytesseract.tesseract_cmd = tesseract_path


# #api key handling
# base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # go one level up
# dotenv_path = os.path.join(base_dir, 'resources', '.env')
# load_dotenv(dotenv_path=dotenv_path)
# openai_api_key = os.getenv('OPENAI_API_KEY')


def extract_text_from_img(image_path):
    image = Image.open(image_path)  # open the image using PIL
    text = pytesseract.image_to_string(image) # extract text using tesseract OCR
    #for test
    #print(text)
    return text



def analyse_text(text):
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=Config.OPENAI_API_KEY)
    prompt = PromptTemplate(
        input_variables=["text"], 
        template="Analyze the following text or image of list of songs and search on internet to get title and artist name of each song. Please ensure that the song name and artist name is valid(Check if the artist actually released the song.). Condiser the possibility of typo and text errors(if the song and artist exist). Output the information you got in 2D array in json form without any other response(example: {{'title': 'Shape of You', 'artist': 'Ed Sheeran'}}). Please don't make up informations or hallucinate and DO NOT put anything in the array if you don't know title or artist name. here is the text: {text}"
    )
    chain = prompt | llm
    response = chain.invoke(text) # getting response form ai
    
    # parsing response to get 2d array
    content = response.content

    try:
        parsed_content = content.strip('```json\n').strip('```')
        array = json.loads(parsed_content)
        # for test
        #print(array, "analysed")
        return array
    except (json.JSONDecodeError, AttributeError) as e:
        array = []
        return "error parsing response: {e}"

def reanalyse_text(text, response):
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=Config.OPENAI_API_KEY)
    prompt = PromptTemplate(
        input_variables=["text"], 
        template="This is your previous prompt and text input: [Analyze the following text of list of songs and search on internet to get title and artist name of each song. Please ensure that the song name and artist name is valid(Check if the artist actually released the song.). Condiser the possibility of typo and text errors(if the song and artist exist). Output the information you got in 2D array in json form without any other response. Please don't make up informations and DO NOT put anything in the array if you don't know title or artist name. here is the text: {text}] and this is your response:[{response}] your response was wrong so song and artist name wasn't correct. please retry analysing."
    )
    chain = prompt | llm
    response = chain.invoke(text, response) # getting response form ai
    
    # parsing response to get 2d array
    content = response.content

    try:
        parsed_content = content.strip('```json\n').strip('```')
        array = json.loads(parsed_content)
        # for test
        print(array, "reanalysed")
        return array
    except (json.JSONDecodeError, AttributeError) as e:
        array = []
        return "error parsing response: {e}"

