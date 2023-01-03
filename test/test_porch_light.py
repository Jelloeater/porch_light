import porch_light.porch_light


def test_creds():
    from dotenv import load_dotenv
    import os

    load_dotenv()
    assert os.getenv("hubitat_api_app_id") is not None
    assert os.getenv("hubitat_api_token") is not None


def test_hub_get():
    h = porch_light.porch_light.Main().get_hub()
    if h.devices is not None:
        assert True
    else:
        assert False
