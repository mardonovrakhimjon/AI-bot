import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    TOKEN = os.getenv("TOKEN")


Settings = Settings()