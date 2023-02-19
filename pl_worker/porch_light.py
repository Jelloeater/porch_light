import colorsys
import datetime
import logging.handlers
import os
import pathlib
import time

import extcolors
import hubitatcontrol
from bing_image_downloader import bing

logging.basicConfig(level=logging.WARNING)


def get_hub():
    host_env = os.getenv("HUBITAT_HOST")
    token_env = os.getenv("HUBITAT_API_TOKEN")
    app_id_env = os.getenv("HUBITAT_API_APP_ID")
    return hubitatcontrol.get_hub(host=host_env, token=token_env, app_id=app_id_env)


def check_hub():
    h = get_hub()
    if h.devices is None:
        raise Exception("Cannot access Hubitat")
    return h


class ColorPalate:
    @property
    def __keywords__(self):  # pragma: no cover
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

    def _download_photo_from_month_(self):
        output_path = pathlib.Path(__file__).parent.resolve()
        b = bing.Bing(
            query=self.__keywords__,
            limit=1,
            output_dir=output_path,
            adult="",
            timeout=5,
            filter="clipart",
            verbose=False,
        )
        b.run()
        image_path = os.path.join(output_path, "Image_1.jpg")
        if not os.path.exists(image_path):
            raise ValueError("File not downloaded")
        return image_path

    def get_colors(self, tolerance: int, number_of_colors: int):
        return extcolors.extract_from_path(
            path=self._download_photo_from_month_(), tolerance=tolerance, limit=number_of_colors
        )


class LightWorker:
    @staticmethod
    def change_light_color():
        clr = ColorPalate().get_colors(
            tolerance=int(os.getenv("COLOR_TOLERANCE")), number_of_colors=int(os.getenv("NUMBER_OF_COLORS"))
        )

        porch = hubitatcontrol.lookup_device(hub_in=get_hub(), device_lookup=os.getenv("HUBITAT_DEVICE_TO_CYCLE"))
        while porch.switch == "on":
            for i in clr[0]:
                r = i[0][0]
                g = i[0][1]
                b = i[0][2]
                hsv = colorsys.rgb_to_hsv(r, g, b)
                logging.debug(hsv)
                # TODO Convert to HSL
                pass
                time.sleep(int(os.getenv("CYCLE_TIME")))
                # porch.set_hue()
                # porch.set_saturation()
                # porch.set_level()

        # TODO Set light to colors from photo ONLY if on
        # TODO At end of run, check if light is still on, If light is off, exit loop
