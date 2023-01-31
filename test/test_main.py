from dotenv import load_dotenv
import pl_worker.porch_light
# import pl_worker.webserver

load_dotenv()


def test_check_hub():
    assert pl_worker.porch_light.check_hub().devices is not None


# def test_webserver():
#     pl_worker.webserver.start_server()
