import os
import pytest

from luucy import BaseClient


@pytest.fixture()
def config():
    return {
        "username": os.environ["CI_LUUCY_USERNAME"],
        "password": os.environ["CI_LUUCY_PASSWORD"],
        "api_base": "app.integration.luucy.ch",
    }


@pytest.fixture()
def client(config):
    return BaseClient(**config)
