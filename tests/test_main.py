import os
from time import sleep

import requests
from dotenv import load_dotenv

import pl_worker.porch_light as pl
import pl_worker.webserver as web
from multiprocessing import Process

load_dotenv("../prod.env")
os.environ.setdefault("PL_TEST_MODE", str(True))  # To break out of color cycle loop


class TestPL:
    def test_check_hub(self):
        assert pl.check_hub().devices is not None

    def test_dl(self):
        p = pl.ColorPalate()
        path = p._download_photo_from_month_()
        assert os.path.exists(path)

    def test_change_color(self):
        import hubitatcontrol

        light = hubitatcontrol.lookup_device(hub_in=pl.get_hub(), device_lookup=os.getenv("HUBITAT_DEVICE_TO_CYCLE"))
        light.turn_on()
        p = pl.LightWorker.change_light_color()


class Test_API_full:
    background_server = Process(target=web.Server.start_server, daemon=True)

    @classmethod
    def setup_class(cls):
        cls.background_server.start()
        sleep(0.5)  # Wait for server to start

    @classmethod
    def teardown_class(cls):
        cls.background_server.terminate()

    def test_base_url(self):
        r = requests.get(url="http://" + web.Server.local_nic() + ":" + str(web.Server.port))
        assert r.status_code == 200

    def test_check_hub(self):
        r = requests.get(url="http://" + web.Server.local_nic() + ":" + str(web.Server.port) + "/check-hub")
        assert r.status_code == 200
        assert r.json()[0]["token"] == os.environ.get("HUBITAT_API_TOKEN")
