import pytest
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
        pytest.hub = h
        assert True
    else:
        pytest.hub = None
        assert False


def test_get_device_attributes():
    h = porch_light.porch_light.Main().get_hub()
    p = h.get_device_attributes('Porch')
    assert p is not None


def test_get_device_commands():
    h = porch_light.porch_light.Main().get_hub()
    for i in h.devices:
        dev = int(i['id'])
        out = h.get_device_commands(device_id=dev)
        assert out is not None


def test_get_device_history():
    h = porch_light.porch_light.Main().get_hub()
    for i in h.devices:
        dev = int(i['id'])
        out = h.get_device_history(device_id=dev)
        assert out is not None


def test_get_device_capabilities():
    h = porch_light.porch_light.Main().get_hub()
    for i in h.devices:
        dev = int(i['id'])
        out = h.get_device_capabilities(device_id=dev)
        assert out is not None

def test_send_device_command():
    h = porch_light.porch_light.Main().get_hub()
    p = h.get_device_attributes('Porch')
    print()
