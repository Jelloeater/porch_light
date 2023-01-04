import porch_light.porch_light


def test_print_envs():
    import os

    print(os.environ)


def test_creds():
    from dotenv import load_dotenv
    import os

    load_dotenv()
    assert os.getenv("HUBITAT_API_APP_ID") is not None
    assert os.getenv("HUBITAT_API_TOKEN") is not None


def test_hub_get():
    h = porch_light.porch_light.Main().get_hub()
    if h.devices is not None:
        assert True
    else:
        assert False
