import requests
import json

with open("credentials.json", "r") as f:
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
