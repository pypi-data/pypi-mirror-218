from pytest_bdd import scenario, given, when, then


@scenario("client/login.feature", "Log in successfully")
def test_client_can_log_in():
    pass


@given("that I have a valid username and password for a given environment")
@when("the client is created")
@then("it logs in successfully")
def log_in_successfully(client):
    assert client.api_token is not None
