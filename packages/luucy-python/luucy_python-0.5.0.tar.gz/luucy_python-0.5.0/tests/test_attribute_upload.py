import json
from unittest import mock

from luucy.tilesetproxy import Attribute
from luucy.base import BaseClient

TEST_UUID = "fa8e48e4-bed6-4215-ae01-18fe23155ce3"
TEST_TOKEN = "18b8c9a1234599b5043e654321e0c870956aga09"


@mock.patch("luucy.base.requests.request", autospec=True)
class TestAttribute:
    def test_update_attribute(self, mock_request):
        client = BaseClient(api_key=TEST_TOKEN)

        attribute = Attribute(client, attribute_id=103)
        attribute.update_value(uuid=TEST_UUID, value="1")

        mock_request.assert_called_once_with(
            "PUT",
            url="https://app.luucy.ch/tileset-proxy/value/fa8e48e4-bed6-4215-ae01-18fe23155ce3-103",
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            params=None,
            cookies={"apiKey2": f"{TEST_TOKEN}"},
            data=json.dumps({"attributeId": 103, "uuid": TEST_UUID, "value": "1"}),
            timeout=10,
        )
