import datetime
import logging.handlers
import os
import pathlib

from bing_image_downloader import bing
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

    @property
    def keywords(self):  # pragma: no cover
        # No need to check for coverage
        match datetime.datetime.now().month:
            case 1:
                return "snow winter cold"
            case 2:
                return "valentine heart love"
            case 3:
                return "st patricks irish lucky"
            case 4:
                return "easter bunny spring"
            case 5:
                return "Cinco de mayo"
            case 6:
                return "summer beach fun water"
            case 7:
                return "Independence USA flag"
            case 8:
                return "summer sky"
            case 9:
                return "labor day"
            case 10:
                return "halloween spooky"
            case 11:
                return "thanksgiving fall family"
            case 12:
                return "christmas tree presents"

    def download_photo_from_month(self):
        output_path = pathlib.Path(__file__).parent.resolve()
        b = bing.Bing(
            query=self.keywords,
            limit=1,
            output_dir=output_path,
            adult="None",
            timeout=5,
            filter="photo",
            verbose=True,
        )
        b.run()
        image_path = os.path.join(output_path, "Image_1.jpg")
        if not os.path.exists(image_path):
            raise ValueError("File not downloaded")
        return image_path

    def get_colors(self):
        # TODO Get colors from photo
        pass

    def change_light_color(self):
        # TODO Set light to colors from photo ONLY if on
        # TODO At end of run, check if light is still on, If light is off, exit loop
        # TODO
        pass
