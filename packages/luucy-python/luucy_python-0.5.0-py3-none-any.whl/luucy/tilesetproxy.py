"""
luucy.tilesetproxy service
"""

from typing import Optional

from luucy.base import BaseClient


class Attribute:
    """an attribute on a 3D tileset layer

    Parameters:
      client: the client object to handle all https calls
      attribute_id: the id of the attribute
    """

    def __init__(self, client: BaseClient, attribute_id: Optional[int] = None):
        self.client = client
        self.attribute_id = attribute_id

    def update_value(self, uuid: str, value: str) -> Optional[dict]:
        """update the value for the attribute

        Parameters:
          uuid: UUID of the object to be updated
          value: new value to be set
        """
        return self.client.call(
            "PUT",
            f"value/{uuid}-{self.attribute_id}",
            base="tileset-proxy",
            data={"attributeId": 103, "uuid": uuid, "value": value},
        )
