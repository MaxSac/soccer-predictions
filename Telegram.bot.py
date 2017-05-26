
# coding: utf-8

# In[ ]:

import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)

    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,99))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))

bot = telepot.Bot('364468925:AAHsPxwh6MUpg1MwsrqaL5IVNn7UTpA--2M')

MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')

while 1:
    time.sleep(10)

