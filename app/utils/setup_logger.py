import logging

logger = logging.getLogger('open-fec-graphql')
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    return logger.getChild(name)
