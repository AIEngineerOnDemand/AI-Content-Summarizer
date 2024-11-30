import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os


# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=env_path)


def download_from_medium(url):
  
    # Create a session
    s = requests.Session()

    cookies = {
        'xsrf': os.getenv('XSRF_TOKEN'),
        'uid': os.getenv('UID'),
        'sid': os.getenv('SID'),
        'nonce': os.getenv('NONCE'),
        'g_state': os.getenv('G_STATE'),
        '_s': os.getenv('_S'),
        '_ga_7JY7T788PK': os.getenv('GA_7JY7T788PK'),
        '_ga': os.getenv('GA'),
        '_dd_s': os.getenv('DD_S'),
        '__stripe_mid': os.getenv('STRIPE_MID'),
    }
    # Use the session to get the page
    response = s.get(url, cookies=cookies)

    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find("article")
    paragraphs = article.find_all("p")
    text = ' '.join([para.text for para in paragraphs])
    return text

    # # Step 2: Text-to-Speech Conversion
    # tts = gTTS(text=text, lang='en')
    # tts.save("medium_article.mp3")   