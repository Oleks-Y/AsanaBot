import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage import memory
from colorama import Fore

bot = Bot(token="1344620215:AAFEo5hC3D5Io-tua33KvfF5G28AtUJ0jhg")
# storege = redis.RedisStorage(host="redis-11331.c135.eu-central-1-1.ec2.cloud.redislabs.com:11331", port=11331, db=1, password="lSEPQlbMMdq3bkkTdncRf4Ev3NXkr6xd")
storage = memory.MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
print(Fore.CYAN + "Bot started")