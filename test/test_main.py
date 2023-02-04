from dotenv import load_dotenv
import pl_worker.porch_light
import pl_worker.webserver
from fastapi.testclient import TestClient

load_dotenv()
# Webserver test client
client = TestClient(pl_worker.webserver.app)


def test_check_hub():
    assert pl_worker.porch_light.check_hub().devices is not None


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
