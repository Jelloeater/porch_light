import os
from time import sleep

import requests
from dotenv import load_dotenv
from fastapi.testclient import TestClient

import pl_worker.porch_light
import pl_worker.porch_light as pl
import pl_worker.webserver as web

load_dotenv()


class TestPL:
    def test_check_hub():
        assert pl.check_hub().devices is not None

    def test_dl(self):
        p = pl_worker.porch_light.MainLogic()


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
