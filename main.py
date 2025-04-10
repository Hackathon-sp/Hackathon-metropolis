import time
from emailReader import check_email
from utils import configure_gemini
import os

### To remove API key from env cache, since gemini api key expires after a day
if 'GENAI_API_KEY' in os.environ:
    del os.environ['GENAI_API_KEY']

from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    configure_gemini()
    while True:
        print("Reading Email Data")
        check_email()
        time.sleep(5)
