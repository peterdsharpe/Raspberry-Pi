import requests
import json
from pathlib import Path

this_dir = Path(__file__).parent.absolute()  # Get the current directory

with open(this_dir / "credentials.json", "r") as f:
    credentials = json.load(f)


def pushbullet_message(title, body):
    msg = {"type": "note", "title": title, "body": body}
    TOKEN = credentials["pushbullet_token"]
    resp = requests.post('https://api.pushbullet.com/v2/pushes',
                         data=json.dumps(msg),
                         headers={'Authorization': 'Bearer ' + TOKEN,
                                  'Content-Type' : 'application/json'})
    if resp.status_code != 200:
        raise Exception('Error', resp.status_code)
    else:
        print('Message sent')


if __name__ == '__main__':
    pushbullet_message(
        title="Peter's Title",
        body="Peter's Message"
    )
