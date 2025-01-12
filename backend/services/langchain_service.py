import json
import pytesseract 
from PIL import Image
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from backend.config.config import Config


# #api key handling
# base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # go one level up
# dotenv_path = os.path.join(base_dir, 'resources', '.env')
# load_dotenv(dotenv_path=dotenv_path)
# openai_api_key = os.getenv('OPENAI_API_KEY')


def extract_text_from_img(image_path):
    image = Image.open(image_path)  # open the image using PIL
    text = pytesseract.image_to_string(image) # extract text using tesseract OCR
    analyse_text(text)



def analyse_text(text):
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=Config.OPENAI_API_KEY)
    prompt = PromptTemplate(
        input_variables=["text"], 
        template="Analyze the following text or image of list of songs and search on internet to get title, artist name and release year of each song. You should extract text and analyse if image is entered. Output the information you got in 2D array in json form without any other response. Please don't make up informations and DO NOT put anything in the array if you don't know title, artistname, or release year.: {text}"
    )
    chain = prompt | llm
    response = chain.invoke(text) # getting response form ai
    
    # parsing response to get 2d array
    content = response.content
    print(response)
    try:
        parsed_content = content.strip('```json\n').strip('```')
        array = json.loads(parsed_content)
        print(array)
    except (json.JSONDecodeError, AttributeError) as e:
        array = []
        return "error parsing response: {e}"