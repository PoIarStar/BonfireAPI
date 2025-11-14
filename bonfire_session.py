from configparser import ConfigParser

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from tools.queries import Query, get_me, login


class RequestError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class BonfireSession(Session):
    def __init__(self, token: str = ""):
        super().__init__()
        retry_strategy: Retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter: HTTPAdapter = HTTPAdapter(max_retries=retry_strategy)
        self.mount("http://", adapter)
        self.mount("https://", adapter)

        config: ConfigParser = ConfigParser()
        config.read("config.ini")

        self.requests_url: str = config["URL"]["requests"]  # у меня есть подозрение, что она всё-таки нужна
        # ну или я не понял, как работает J_API_ACCESS_TOKEN. потому что мне говорят, что я не авторизован

        self.login_url: str = config["URL"]["login"]

        self.token: str = token

    def is_auth(self) -> bool:
        return bool(self.post(get_me())["data"])  # переделать проверку через обработку ошибки

    def login(self, email: str, password: str):
        res = super().post(url=self.login_url, json=login(email, password).to_dict())
        res.raise_for_status()
        res_data = res.json()
        if "errors" in res_data:
            raise RequestError(res_data["errors"])
        self.token = res_data["data"]["loginEmail"]["accessToken"]

    def post(self, json: Query, **kwargs) -> dict:
        print(self.token)
        json.data["J_API_ACCESS_TOKEN"] = self.token
        json.data["J_REQUEST_NAME"] = ""
        res = super().post(url=self.login_url, json=json.to_dict(), **kwargs)
        res.raise_for_status()
        res_data = res.json()
        if "errors" in res_data:  # Потом надо нормально сделать классы ошибок
            raise RequestError(res_data["errors"])
        return res_data
