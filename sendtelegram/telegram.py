import requests
import json

from env_setup import Credentials


def send_telegram(text: str):
    token = Credentials.TELEGRAM_TOKEN
    url = "https://api.telegram.org/bot"
    channel_id = "-889877330"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text errnor")

if __name__ == '__main__':
  send_telegram("test msg")



