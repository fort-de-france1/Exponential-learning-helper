import requests


class TelegramClient:
    def __init__(self, token: str, base_url: str):
        self.token = token
        self.base_url = base_url

    def prepare_url(self, method: str):
        result_url = f"{self.base_url}/bot{self.token}/"
        if method is not None:
            result_url += method
        return result_url

    def post(self, method: str = None, params: dict = None, body: dict = None):
        url = self.prepare_url(method)
        resp = requests.post(url=url, params=params, data=body)
        return resp.json()
