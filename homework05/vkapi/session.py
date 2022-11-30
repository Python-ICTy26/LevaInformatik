import typing as tp

import requests
from requests.adapters import HTTPAdapter, Retry

from vkapi.config import VK_CONFIG


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.retries = Retry(total=max_retries, backoff_factor=backoff_factor, status_forcelist=[500])

        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=self.retries))
        self.session.mount('http://', HTTPAdapter(max_retries=self.retries))

        self.base_url = base_url
        self.timeout = timeout

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        payload = dict(kwargs)
        payload['access_token'] = VK_CONFIG['access_token']

        return self.session.get(
            f'{self.base_url}/{url}',
            params=payload,
            timeout=self.timeout
        )

    def post(self, url: str, *args: tp.Any, data: tp.Any = None, json: tp.Any = None, **kwargs: tp.Any) -> requests.Response:
        payload = dict(kwargs)
        payload['access_token'] = VK_CONFIG['access_token']

        return self.session.post(
            f'{self.base_url}/{url}',
            params=payload,
            data=data,
            json=json,
            timeout=self.timeout
        )
