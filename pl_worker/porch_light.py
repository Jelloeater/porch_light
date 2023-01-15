import logging.handlers

console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(funcName)s():%(lineno)s)"
    )
)
logging.basicConfig(level=logging.DEBUG, handlers=[console_handler])
import os
import hubitatcontrol as Hubitat


def test_hub_get():
    host_env = os.getenv("HUBITAT_HOST")
    token_env = os.getenv("HUBITAT_API_TOKEN")
    app_id_env = os.getenv("HUBITAT_API_APP_ID")
    h = Hubitat.Hub(host=host_env, token=token_env, app_id=app_id_env)
    if h.devices is not None:
        assert True
    else:
        assert False


if __name__ == "__main__":
    logging.info("SoP")
    test_hub_get()
