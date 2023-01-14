from dotenv import load_dotenv
import os

load_dotenv()
host_env = os.getenv("HUBITAT_HOST")
token_env = os.getenv("HUBITAT_API_TOKEN")
app_id_env = os.getenv("HUBITAT_API_APP_ID")

import hubitatcontrol as Hubitat

test_device_name = "Porch"


def test_device_bulb():
    h = Hubitat.Hub(host=host_env, token=token_env, app_id=app_id_env)
    d = h.get_device(test_device_name)
    test_bulb = Hubitat.Advanced_Zigbee_RGBW_Bulb(h, d)

    test_bulb.turn_on()
    assert test_bulb.switch == "on"
    test_bulb.turn_off()
    assert test_bulb.switch == "off"
    test_bulb.turn_on()
    assert test_bulb.switch == "on"
