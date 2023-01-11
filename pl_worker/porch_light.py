import logging.handlers
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(funcName)s():%(lineno)s)"))
logging.basicConfig(level=logging.DEBUG, handlers=[console_handler])



if __name__ == '__main__':
    logging.info('SoP')
