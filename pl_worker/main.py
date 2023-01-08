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


class Hub:
    def __init__(self):
        self.host = os.getenv("HUBITAT_HOST")
        self.app_id = os.getenv("HUBITAT_API_APP_ID")
        self.token = os.getenv("HUBITAT_API_TOKEN")
        self.base_url_prefix = self.host + "/api/" + self.app_id + "/apps/101/devices/"
        self.devices = self._update_devices_()

    def _update_devices_(self) -> dict:
        r = requests.get(
            url=self.base_url_prefix + "all", params={"access_token": self.token}
        )
        return r.json()

    def get_device_id(self, name: str) -> int:
        self._update_devices_()
        for i in self.devices:
            if i['label'] == name:
                return i['id']

    def get_device_attributes(self, name):
        self._update_devices_()
        for i in self.devices:
            if i['label'] == name:
                return i['attributes']

    def get_device_commands(self, device_id: int):
        r = requests.get(
            url=self.base_url_prefix + str(device_id) + "/commands", params={"access_token": self.token}
        )
        return r.json()

    def get_device_history(self, device_id: int):
        self._update_devices_()
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


class Bulb(Hub):
    def __init__(self, id):
        super().__init__()


class Main:
    @staticmethod
    def get_hub():
        return Hub()

    def start(self):
        logging.debug("SoP")
        h = self.get_hub()
        assert h is not None
        logging.debug(h)


if __name__ == "__main__":
    print(os.environ)
    while True:
        Main().start()
        time.sleep(1)
        break
