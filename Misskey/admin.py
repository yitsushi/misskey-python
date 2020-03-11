from .admin_queue import Queue


class Admin:
    client = None

    def __init__(self, client):
        self.__client = client

    def queue(self):
        return Queue(self.__client)
