from dotenv import load_dotenv

import porch_light.porch_light

load_dotenv()


def test_creds():
    import os
    assert os.getenv("HUBITAT_API_APP_ID") is not None
    assert os.getenv("HUBITAT_API_TOKEN") is not None


def test_hub_get():
    h = porch_light.porch_light.Main().get_hub()
    if h.devices is not None:
        assert True
    else:
        assert False
