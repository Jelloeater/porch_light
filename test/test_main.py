from dotenv import load_dotenv
import os

load_dotenv()
host_env = os.getenv("HUBITAT_HOST")
token_env = os.getenv("HUBITAT_API_TOKEN")
app_id_env = os.getenv("HUBITAT_API_APP_ID")


import pl_worker.porch_light

test_device_name = "Porch"


def test_device_bulb():
    pl_worker.porch_light.test_hub_get()
