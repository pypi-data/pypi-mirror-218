"""
luucy.base
"""

from typing import Optional

import os
import json
import requests

from luucy.error import LuucyInavlidCredentials


class BaseClient:
    """base client

    Parameter:
      username: login username
      password: login password
      environment: luucy environment, default: app.luucy.ch

    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_base: str = "app.luucy.ch",
        api_key: Optional[str] = None,
    ):
        self.username = username
        self.password = password

        self.username = os.environ.get("LUUCY_USERNAME", self.username)
        self.password = os.environ.get("LUUCY_PASSWORD", self.password)

        self.api_base = api_base
        self.api_token = api_key

        if self.api_token:
            return None

        if self.username and self.password:
            res = self.call(
                "POST",
                "login",
                data={"login": self.username, "password": self.password},
            )

            if res:
                self.api_token = res["apiKey"]
                return None

        raise LuucyInavlidCredentials

    def call(
        self,
        http_method: str,
        path: str,
        parameters: Optional[dict] = None,
        data: Optional[dict] = None,
        base: str = "api",
    ) -> Optional[dict]:
        """make an api call"""

        return_data = None

        res = requests.request(
            http_method,
            url=f"https://{self.api_base}/{base}/{path}",
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            params=parameters,
            cookies={"apiKey2": self.api_token} if self.api_token else None,
            data=json.dumps(data),
            timeout=10,
        )

        if res.status_code == 200:
            return_data = res.json()

        return return_data
