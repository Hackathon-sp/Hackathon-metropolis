import time
from emailReader import check_email
from utils import configure_gemini

if __name__ == "__main__":
    configure_gemini()
    while True:
        print("Reading Email Data")
        check_email()
        time.sleep(5)
