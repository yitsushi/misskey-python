import requests
from .admin import Admin
from .app import App


class Client():
    api_key: str
    domain: str

    def __init__(self, domain, api_key):
        self.domain = domain
        self.api_key = api_key

    def admin(self):
        return Admin(self)

    def notes(self, local=False, reply=False, renote=False,
              withFiles=False, poll=False, limit=10,
              sinceId=None, untilId=None):
        payload = {
            "local": local,
            "reply": reply,
            "renote": renote,
            "withFiles": withFiles,
            "poll": poll,
            "limit": limit
        }

        if sinceId is not None:
            payload['sinceId'] = sinceId
        if untilId is not None:
            payload['untilId'] = untilId

        return self.send("/notes", payload)

    def app(self):
        return App(self)

    def send(self, path, payload):
        payload['i'] = self.api_key
        response = requests.post(
            f'https://{self.domain}/api{path}',
            json=payload
        )
        return response.json()
