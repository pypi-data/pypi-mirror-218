from pytest_bdd import scenario, given, when, then

from luucy import Attribute


@scenario("tileset-proxy/upload-attributes.feature", "Update existing attribute")
def test_can_upload_attribute():
    pass


@given("that I have a valid layer ID, building UUID and attribute name")
@when("updating the attribute")
@then("the data is saved")
def log_in_successfully(client):
    update = Attribute(client, attribute_id=27).update_value(
        uuid="fa8e48e4-bed6-4215-ae01-18fe23155ce3", value="1"
    )

    assert update
    assert update["value"] == 1
