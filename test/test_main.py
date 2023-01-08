import time

import pytest
from dotenv import load_dotenv

import pl_worker.main as pl

load_dotenv()


def test_creds():
    import os
    assert os.getenv("HUBITAT_API_APP_ID") is not None
    assert os.getenv("HUBITAT_API_TOKEN") is not None


def test_hub_get():
    h = pl.Hub()
    if h.devices is not None:
        pytest.hub = h
        assert True
    else:
        pytest.hub = None
        assert False


def test_lookup_device():
    h = pl.Hub()
    p = h.get_device_id('Porch')
    assert p is not None

def test_init_device():
    h = pl.Hub()
    device = pl.Device(h.get_device_id('Porch'))
    assert device is not None


def test_send_device_command():
    h = pl.Hub()
    device = pl.Device(h.get_device_id('Porch'))

    test_bulb = pl.Bulb(id_in=device.id).turn_on()
    test_bulb.turn_on()
    assert test_bulb.switch == 'on'


    test_bulb.turn_off()
    test_bulb.update_bulb()
    assert test_bulb.switch == 'off'


    test_bulb.turn_on()
    test_bulb.update_bulb()
    assert test_bulb.switch == 'on'


    test_bulb.turn_off()
    test_bulb.update_bulb()
    assert test_bulb.switch == 'off'
