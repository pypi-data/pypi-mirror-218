import pytest
from unittest import mock
import json
import os

from luucy.base import BaseClient
from luucy.error import LuucyInavlidCredentials

TEST_TOKEN = "18b8c9a1234599b5043e654321e0c870956aga09"


class TestClient:
    @mock.patch("luucy.base.requests.request", autospec=True)
    def test_client_can_make_login_request(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = json.load(
            open(f"tests/data/post_api_login.json")
        )

        client = BaseClient(username="luucy", password="lucerneCity")

        assert client.api_token == "18b8c9a1234599b5043e654321e0c870956aga09"

    @mock.patch("luucy.base.requests.request", autospec=True)
    def test_client_can_make_failing_login_request(self, mock_request):
        mock_request.return_value.status_code = 401
        mock_request.return_value.json.return_value = json.load(
            open(f"tests/data/post_api_login_fail.json")
        )

        with pytest.raises(LuucyInavlidCredentials):
            client = BaseClient(username="validUser", password="invalidPassword")

            assert client.api_token is None

    @mock.patch("luucy.base.requests.request", autospec=True)
    def test_client_can_make_login_request_with_environment(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = json.load(
            open(f"tests/data/post_api_login.json")
        )

        BaseClient(
            username="luucy", password="lucerneCity", api_base="app.staging.luucy.ch"
        )

        mock_request.assert_called_once_with(
            "POST",
            url="https://app.staging.luucy.ch/api/login",
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            params=None,
            cookies=None,
            data=json.dumps({"login": "luucy", "password": "lucerneCity"}),
            timeout=10,
        )

    @mock.patch.dict(os.environ, {"LUUCY_USERNAME": "luucy"})
    @mock.patch.dict(os.environ, {"LUUCY_PASSWORD": "lucerneCity"})
    @mock.patch("luucy.base.requests.request", autospec=True)
    def test_client_can_make_login_request_env_variables(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = json.load(
            open(f"tests/data/post_api_login.json")
        )

        client = BaseClient()

        assert client.api_token == "18b8c9a1234599b5043e654321e0c870956aga09"
