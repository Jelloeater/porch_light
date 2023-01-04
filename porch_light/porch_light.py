import logging
import os
import requests
from dotenv import load_dotenv

# syslog_handler = logging.handlers.SysLogHandler(address=(settings.syslog_server, settings.syslog_port))
console_handler = logging.StreamHandler()
# syslog_handler.setFormatter(logging.Formatter("APP_NAME \n[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(funcName)s():%(lineno)s)"))
console_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(funcName)s():%(lineno)s)"
    )
)

# logging.basicConfig(level=logging.WARN, handlers=[console_handler, syslog_handler])
logging.basicConfig(level=logging.DEBUG, handlers=[console_handler])


class hub:
    def __init__(self, host, app_id, token):
        self.host = host
        self.app_id = app_id
        self.token = token
        self.base_url_prefix = self.host + "/api/" + self.app_id + "/apps/101/devices/"
        self.devices = self.get_devices()

    def get_devices(self):
        r = requests.get(
            url=self.base_url_prefix + "all", params={"access_token": self.token}
        )
        return r.json()


class Main:
    @staticmethod
    def get_hub():
        load_dotenv()  # Load Env file if dev locally, if remote, env vars must be loaded externally
        host = "https://cloud.hubitat.com"
        app_id = os.getenv("HUBITAT_API_APP_ID")
        token = os.getenv("HUBITAT_API_TOKEN")
        return hub(host=host, app_id=app_id, token=token)

    def start(self):
        logging.debug("SoP")
        h = self.get_hub()
        assert h is not None
        logging.debug("")


if __name__ == "__main__":
    print(os.environ)
    Main().start()
