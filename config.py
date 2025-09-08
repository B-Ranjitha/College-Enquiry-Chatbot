import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'bbc-college-secret-key-2023')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DATABASE = 'college_chatbot.db'
