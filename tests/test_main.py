import os
from time import sleep

import pl_worker.porch_light as pl
import pl_worker.webserver as web
import pytest
import requests
from dotenv import load_dotenv

load_dotenv("../prod.env")


# FIXME no way of currently testing this
@pytest.mark.skip
def test_start_test_server():
    from dotenv import load_dotenv

    load_dotenv("../prod.env")
    web.Server.start_server()


class TestPL:
    def test_check_hub(self):
        assert pl.check_hub().devices is not None

    def test_dl(self):
        p = pl.ColorPalate()
        path = p._download_photo_from_month_()
        assert os.path.exists(path)

    # FIXME Need to figure out how to run this in a subprocess
    # @pytest.mark.skip
    def test_change_color(self):
        p = pl.LightWorker.change_light_color()


class Test_API_full:
    from multiprocessing import Process

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
