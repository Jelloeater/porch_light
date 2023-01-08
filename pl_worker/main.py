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
        self.devices = self.load_devices()

    def load_devices(self) -> dict:
        r = requests.get(
            url=self.base_url_prefix + "all", params={"access_token": self.token}
        )
        return r.json()

    def get_device_id(self, name: str) -> int:
        self.devices = self.load_devices()
        for i in self.devices:
            if i['label'] == name:
                return i['id']

    def update_devices(self):
        self.devices = self.load_devices()


class Device(Hub):
    def __init__(self, id: str):
        super().__init__()
        for i in self.devices:
            if i['id'] == id:
                self.name = i['name']
                self.label = i['label']
                self.type = i['type']
                self.id = i['id']
                self.commands = i['commands']
                self.capabilities = i['capabilities']
                self.attributes = i['attributes']
                self.history = self.update_device_history()

    def update_attributes(self):
        pass
        # FIXME Update attributes on command send

    def update_device_history(self):
        r = requests.get(
            url=self.base_url_prefix + str(self.id) + "/events", params={"access_token": self.token}
        )
        return r.json()

    def send_device_command(self, command: str, secondary_command: str = None):
        if secondary_command is None:
            r = requests.get(
                url=self.base_url_prefix + str(self.id) + "/" + command, params={"access_token": self.token}
            )
            return r.json()
        else:
            r = requests.get(
                url=self.base_url_prefix + str(self.id) + "/" + command + '/' + secondary_command,
                params={"access_token": self.token}
            )
            return r.json()


class Bulb(Device):
    def __init__(self, id: str):
        super().__init__(id)

    def turn_on(self):
        self.send_device_command(command='on')

    def turn_off(self):
        self.send_device_command(command='off')


class Main:
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
