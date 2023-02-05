import os

from dotenv import load_dotenv
import pl_worker.porch_light
import pl_worker.webserver
from fastapi.testclient import TestClient

load_dotenv()
# Webserver test client
client = TestClient(pl_worker.webserver.web_app().app)


def test_check_hub():
    assert pl_worker.porch_light.check_hub().devices is not None


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_hub_api():
    response = client.get("/check-hub")
    assert response.status_code == 200
    assert response.json()[0]['token'] == os.environ.get('HUBITAT_API_TOKEN')
