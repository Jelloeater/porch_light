from dotenv import load_dotenv
import pl_worker.porch_light
load_dotenv()


def test_check_hub():
    assert pl_worker.porch_light.check_hub().devices is not None

