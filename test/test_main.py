import pytest
from dotenv import load_dotenv

import pl_worker.main as pl

load_dotenv()


def test_creds():
    import os
    assert os.getenv("HUBITAT_API_APP_ID") is not None
    assert os.getenv("HUBITAT_API_TOKEN") is not None


def test_hub_get():
    h = pl.Main().get_hub()
    if h.devices is not None:
        pytest.hub = h
        assert True
    else:
        pytest.hub = None
        assert False


def test_lookup_device():
    h = pl.Main().get_hub()
    p = h.get_device_id('Porch')
    assert p is not None

def test_init_device():
    h = pl.Main().get_hub()
    device = pl.Device(h, h.get_device_id('Porch'))
    assert device is not None


def test_send_device_command():
    h = pl.Main().get_hub()
    status = h.get_device_attributes('Porch')['switch']

    print(status)
