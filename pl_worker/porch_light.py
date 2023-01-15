import logging.handlers

console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(funcName)s():%(lineno)s)"
    )
)
logging.basicConfig(level=logging.DEBUG, handlers=[console_handler])
import os

import hubitatcontrol.main as hubitat


def check_hub():
    host_env = os.getenv("HUBITAT_HOST")
    token_env = os.getenv("HUBITAT_API_TOKEN")
    app_id_env = os.getenv("HUBITAT_API_APP_ID")
    h = hubitat.Hub(host=host_env, token=token_env, app_id=app_id_env)
    if h.devices is None:
        raise Exception("Cannot access Hubitat")


if __name__ == "__main__":
    logging.info("SoP")
    check_hub()
