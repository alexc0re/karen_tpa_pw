import os
from dataclasses import dataclass

from dotenv import load_dotenv




@dataclass
class Credentials:
    load_dotenv()
    APP_USERNAME: str = os.getenv("NAME")
    APP_PASSWORD: str = os.getenv("ASS")
    DB_PASS = str = os.getenv("DB_PASS")
    TELEGRAM_TOKEN = str = os.getenv("TELEGRAM_TOKEN")

    @classmethod
    def get_env_variables(cls):
        if not Credentials.APP_USERNAME or not Credentials.APP_PASSWORD:
            raise

        return cls(Credentials.APP_USERNAME, Credentials.APP_PASSWORD)

