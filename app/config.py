import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key_if_not_set'
    MONGO_URI = os.environ.get('MONGO_URI')