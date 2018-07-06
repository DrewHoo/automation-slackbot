import os
from dotenv import load_dotenv

load_dotenv()
SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK')
BASE_URL = os.getenv('BASE_URL')