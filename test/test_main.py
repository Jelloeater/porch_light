import os
from time import sleep

import requests
from dotenv import load_dotenv
from fastapi.testclient import TestClient

import pl_worker.porch_light as pl
import pl_worker.webserver as web

load_dotenv()
# Webserver test client
client = TestClient(web.web_app().app)


def test_check_hub():
    assert pl.check_hub().devices is not None


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_hub_api():
    response = client.get("/check-hub")
    assert response.status_code == 200
    assert response.json()[0]["token"] == os.environ.get("HUBITAT_API_TOKEN")


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
