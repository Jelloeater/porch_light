import logging

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


class Main:
    def start(self):
        logging.debug("SoP")


if __name__ == "__main__":
    Main().start()
