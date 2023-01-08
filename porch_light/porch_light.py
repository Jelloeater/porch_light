import logging
import os
import time

import requests

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

    def get_devices(self) -> dict:
        r = requests.get(
            url=self.base_url_prefix + "all", params={"access_token": self.token}
        )
        return r.json()

    def get_device_attributes(self, name):
        self.get_devices()
        for i in self.devices:
            if i['label'] == name:
                return i['attributes']

    def get_device_commands(self, device_id: int):
        r = requests.get(
            url=self.base_url_prefix + str(device_id) + "/commands", params={"access_token": self.token}
        )
        return r.json()

    def get_device_history(self, device_id: int):
        r = requests.get(
            url=self.base_url_prefix + str(device_id) + "/events", params={"access_token": self.token}
        )
        return r.json()

    def get_device_capabilities(self, device_id: int):
        r = requests.get(
            url=self.base_url_prefix + str(device_id) + "/capabilities", params={"access_token": self.token}
        )
        return r.json()

    def send_device_command(self, device_id: int, command: str, secondary_command: str = None):
        if secondary_command is None:
            r = requests.get(
                url=self.base_url_prefix + str(device_id) + "/" + command, params={"access_token": self.token}
            )
            return r.json()
        else:
            r = requests.get(
                url=self.base_url_prefix + str(device_id) + "/" + command + '/' + secondary_command,
                params={"access_token": self.token}
            )
            return r.json()


class Main:
    @staticmethod
    def get_hub():
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
    while True:
        Main().start()
        time.sleep(1)
