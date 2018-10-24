# settings.py
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()
DB = os.getenv('DB')
