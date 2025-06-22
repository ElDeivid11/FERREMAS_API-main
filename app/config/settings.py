from dotenv import load_dotenv
import os

load_dotenv()

BCCH_USER = os.getenv("BCCH_USER")
BCCH_PASS = os.getenv("BCCH_PASS")
