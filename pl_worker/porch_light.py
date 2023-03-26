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

        for i in os.listdir(output_path):
            if "Image_1" in i:
                os.remove(os.path.join(output_path, i))

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
        dl_photo = None
        for i in os.listdir(output_path):
            if "Image_1" in i:
                dl_photo = i
        image_path = os.path.join(output_path, dl_photo)
        if not os.path.exists(image_path):
            raise ValueError("File not downloaded")
        return image_path

    def get_colors(self, tolerance: int, number_of_colors: int):
        import timeit

        start = timeit.default_timer()
        color = extcolors.extract_from_path(
            path=self._download_photo_from_month_(), tolerance=tolerance, limit=number_of_colors
        )
        logging.debug(f"Photo Compute time = {timeit.default_timer() - start}")
        return color


class LightWorker:
    @staticmethod
    def change_light_color():
        """Returns list of colors to cycle, and light device object"""
        colors_to_cycle = ColorPalate().get_colors(
            tolerance=int(os.getenv("COLOR_TOLERANCE")), number_of_colors=int(os.getenv("NUMBER_OF_COLORS"))
        )

        light = hubitatcontrol.lookup_device(hub_in=get_hub(), device_lookup=os.getenv("HUBITAT_DEVICE_TO_CYCLE"))
        while light.switch == "on":
            for i in colors_to_cycle[0]:
                r = i[0][0]
                g = i[0][1]
                b = i[0][2]

                hsl = colorsys.rgb_to_hls(r=r / 255, g=g / 255, b=b / 255)
                # Normalize RGB Values, as colorsys takes 0-1.0 for input

                # Scale values up to 0-100 for Hubitat
                hue = hsl[0] * 100
                level = 100  # Always full brightness
                sat = hsl[2] * 100
                logging.debug(f"HUE={hue}  SAT={sat}")
                light.set_color(hue=hue, saturation=sat, level=level)
                time.sleep(int(os.getenv("CYCLE_TIME")))
            if os.getenv("PL_TEST_MODE") == str(True):
                break
        return {"colors_to_cycle": colors_to_cycle, "light": light}
