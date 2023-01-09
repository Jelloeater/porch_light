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
    p = h.get_device('Porch')
    assert p is not None


def test_init_device():
    h = pl.Hub()
    d = h.get_device('Porch')
    device = pl.Device(d)
    assert device is not None


def test_send_device_command():
    h = pl.Hub()
    d = h.get_device('Porch')
    test_bulb = pl.Bulb(d)

    # x=  test_bulb.get_switch()
    test_bulb.turn_on()
    # test_bulb.get_switch()
    y = test_bulb.get_switch()
    assert test_bulb.switch == 'on'

    test_bulb.turn_off()
    # test_bulb.get_switch()
    z = test_bulb.get_switch()
    assert test_bulb.switch == 'off'

    test_bulb.turn_on()
    # test_bulb.get_switch()
    a = test_bulb.get_switch()
    assert test_bulb.switch == 'on'

    test_bulb.turn_off()
    # test_bulb.get_switch()
    assert test_bulb.switch == 'off'
