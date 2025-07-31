import logging
from .connection import __DiscordService, __DiscordBridge

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s:%(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("bridge.log", mode='w'),
        logging.StreamHandler()
    ]
)
