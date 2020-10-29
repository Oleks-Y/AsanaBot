from aiogram import executor
from misc import dp
import handlers
import sched, time
import EventsScrapper
import asyncio

# async def start_checking_updates():
#     s = sched.scheduler(time.time, time.sleep)
#     s.enter(10, 1, EventsScrapper.getNewEventsComments())
#     s.run()
#
# async def main():
#     executor.start_polling(dp, skip_updates=True)
#     await start_checking_updates()
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
