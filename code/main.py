import sys
import asyncio
import telepot
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open
from telegram_interface import *


token = "token"
bot = telepot.aio.DelegatorBot(token, [
    pave_event_space()(
        per_chat_id(), create_open, telegram_interface, timeout=10),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')

loop.run_forever()


