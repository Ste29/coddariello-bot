import asyncio
import telepot
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open
from codApi import *
import os

class telegram_interface(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(telegram_interface, self).__init__(*args, **kwargs)
        self._count = 0
        self.codapi = codApi()

    async def printer(self, output):
        if len(output) == 1:
            print(output[0])
            await self.sender.sendMessage(output[0])
        else:
            # for _output in output:
            #     print(_output)
            _output = '\n'.join(output)
            print(output)
            print(_output)
            await self.sender.sendMessage(_output)

    def getName(self, command):
        if len(command) == 1:
            player_name = command[0]
        elif len(command) == 2:
            player_name = f"{command[0]} {command[1]}"
        return player_name

    async def on_chat_message(self, msg):
        self._count += 1
        if self._count == 1:
            await self.codapi.logger()

        print(msg["text"])
        command = [m.lower() for m in msg["text"].split()]
        if command[0] == "!stats":
            player_name = self.getName(command[1:])
            try:
                output, _ = await self.codapi.statsPlayer(player_name)
            except ValueError:
                output = await self.codapi.statsPlayer(player_name)
            await self.printer(output)

        elif command[0] == "!weekly":
            player_name = self.getName(command[1:])
            try:
                output, _ = await self.codapi.weeklyPlayer(player_name)
            except ValueError:
                output = await self.codapi.weeklyPlayer(player_name)
            await self.printer(output)


        elif command[0] == "!match":
            player_name = self.getName(command[1:])
            output = await self.codapi.lastMatch(player_name, 1)

            await self.printer(output)

        elif command[0] == "!credits":
            output = ["Questo bot è stato creato da Stefano Villata: @ste29ebasta"]
            await self.printer(output)

        elif command[0] == "!help":
            output = ["Bot creato per vedere le stats su cod warzone:\n\n"
                      "!stats iltuonick -> Le tue statistiche\n"
                      "!weekly iltuonick -> Le tue statistiche settimanali\n"
                      "!match iltuonick -> Il tuo ultimo game\n"
                      "!graph iltuonick N -> Grafico del rateo sui tuoi ultimi game, puoi decidere quanti game "
                      "visualizzare nel grafico scegliendo N compreso tra 10 e 20\n"
                      "!credits -> Il creatore del bot\n\n"
                      "Se ci sono problemi controlla il nick e il tag activision oppure contattami"]
            await self.printer(output)

        elif command[0] == "!graph":
            try:
                limit = int(command[-1])
                player_name = self.getName(command[1:-1])
            except ValueError:
                player_name = self.getName(command[1:])

            try:
                output = await self.codapi.graph(player_name, limit)
            except UnboundLocalError:
                output = await self.codapi.graph(player_name)
            currentDirectory = os.getcwd()
            dirphoto = os.path.join(currentDirectory, "kd.png")
            try:
                await self.sender.sendPhoto(photo=open(dirphoto, "rb"))
                os.remove(dirphoto)
            except FileNotFoundError:
                await self.printer(output)
