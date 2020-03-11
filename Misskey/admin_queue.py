class Queue:
    client = None

    def __init__(self, client):
        self.__client = client

    def jobs(self, domain, state, limit=50):
        payload = {"domain": domain, "state": state, "limit": limit}
        return self.__client.send("/admin/queue/jobs", payload)
