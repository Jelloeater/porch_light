import datetime
import logging.handlers
import os

from hubitatcontrol import Hub

console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(funcName)s():%(lineno)s)")
)
logging.basicConfig(level=logging.DEBUG, handlers=[console_handler])


def check_hub():
    host_env = os.getenv("HUBITAT_HOST")
    token_env = os.getenv("HUBITAT_API_TOKEN")
    app_id_env = os.getenv("HUBITAT_API_APP_ID")
    h = Hub(host=host_env, token=token_env, app_id=app_id_env)
    if h.devices is None:
        raise Exception("Cannot access Hubitat")
    return h


class MainLogic:
    def __init__(self):
        self.download_photo_from_month()

    def download_photo_from_month(self):
        now = datetime.datetime.now()
        m = now.strftime("%B")
        pass


# TODO Get Photo from month name
# TODO Get colors from photo
# TODO Set light to colors from photo ONLY if on
# TODO Listen for hook indicating time to change color
# TODO At end of run, check if light is still on
# TODO If light is off, go back to waiting for hook


if __name__ == "__main__":
    logging.info("SoP")
    check_hub()
    m = MainLogic()
