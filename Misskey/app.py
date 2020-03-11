class App:
    client = None

    def __init__(self, client):
        self.__client = client

    def create(self, name, description, permission, callback_url=""):
        payload = {
            'name': name,
            'description': description,
            'permission': permission,
            'callbackUrl': callback_url
        }

        return self.__client.send('/app/create', payload)
