import flickrapi as flickrapi
from dotenv import load_dotenv
import pl_worker.porch_light
load_dotenv()


def test_device_bulb():
    pl_worker.porch_light.check_hub()


