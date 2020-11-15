import callofduty
import asyncio
from callofduty import Mode, Platform, Title, Match
from matplotlib import pyplot as plt
import numpy as np


class codApi():
    def __init__(self):
        self.email = "your@email.it"
        self.psw = "yourpsw"

    async def logger(self):
        self.client = await callofduty.Login(self.email, self.psw)

    async def searchPlayer(self, nick):
        results = await self.client.SearchPlayers(Platform.Activision, nick, limit=3)
        for player in results:
            print(f"{player.username} ({player.platform.name})")

        nome = nick.split("#", 1)
        no_name = True
        if len(results) == 0:
            print("nessun risultato trovato, controlla il tuo nick")
        else:
            if len(nome) == 1:
                for player in results:
                    if player.username.split("#", 1)[0].lower() == nome[0]:
                        me = player
                        no_name = False
            else:
                me = results[0]
                no_name = False

        try:
            if len(nome) != 1 or no_name == True:
                me = results[1]
        except IndexError:
            try:
                me = results[0]
            except:
                print("nessun risultato trovato, controlla il tuo nick")
                no_name = True

        if no_name:
            output = ["nessun risultato trovato, controlla il tuo nick"]
        else:
            profile1 = await me.profile(Title.ModernWarfare, Mode.Warzone)

            try:
                level = profile1["level"]
                kd = '%.3f' % (profile1['lifetime']['mode']['br']["properties"]['kdRatio'])
                win = profile1['lifetime']['mode']['br']["properties"]['wins']
                top10 = profile1['lifetime']['mode']['br']["properties"]['topTen']

                print(f"\n{me.username} ({me.platform.name})")
                print(f"Level: {int(level)}, K/D Ratio: {kd}, # Win: {int(win)}, # top10: {int(top10)}")
                output = [f"{me.username}\nLevel: {level}, K/D Ratio: {kd}, # Win: {win}, # top10: {top10}\n\n " \
                         f"Se i risultati non sono quelli che ti aspettavi controlla il tag activion (il numero dopo #)"]
            except KeyError:
                output = [f"Il player {me.username} selezionato non ha mai giocato warzone, controlla nick e tag"]

        if no_name == True:
            return output
        else:
            return output, me.username

    async def lastMatch(self, nick, limit):
        output = []
        try:
            try:
                _, username = await self.searchPlayer(nick)
            except ValueError:
                username = False

            if username:
                match = await self.client.GetPlayerMatches(Platform.Activision, username, Title.ModernWarfare,
                                                           Mode.Warzone, limit=limit)
            else:
                match = await self.client.GetPlayerMatches(Platform.Activision, nick, Title.ModernWarfare,
                                                           Mode.Warzone, limit=limit)
            dettagli = await match[0].details()
            nome = nick.split("#", 1)[0]
            username1 = username.split("#", 1)[0]
            # print(nome)
            for player in dettagli["allPlayers"]:
                # print(player['player']['username'])
                if player['player']['username'].lower() == nome or player['player']['username'].lower() == username1:
                    team = player['player']['team']
                    placement = int(player['playerStats']['teamPlacement'])
                    print(f"last match placement: {placement}\n")
                    output.append(f"last match placement: {placement}\n")

            for player in dettagli["allPlayers"]:
                if player['player']['team'] == team:
                    print(
                        f"{player['player']['username']}, kills: {int(player['playerStats']['kills'])}, "
                        f"deaths: {int(player['playerStats']['deaths'])}")
                    output.append(f"{player['player']['username']}, kills: {int(player['playerStats']['kills'])}, "
                                  f"deaths: {int(player['playerStats']['deaths'])}")
            output.append("\nSe i risultati non sono quelli che ti aspettavi controlla "
                          "il tag activion (il numero dopo #)")

        except callofduty.errors.HTTPException:
            output.append("Nickname sbagliato, controlla anche il tag activion (il numero dopo #)")

        return output

    async def graph(self, nick):
        output = []
        kd = []
        try:
            try:
                _, username = await self.searchPlayer(nick)
            except ValueError:
                username = False

            if username:
                match = await self.client.GetPlayerMatches(Platform.Activision, username, Title.ModernWarfare,
                                                           Mode.Warzone, limit=10)
            else:
                match = await self.client.GetPlayerMatches(Platform.Activision, nick, Title.ModernWarfare,
                                                           Mode.Warzone, limit=10)

            nome = nick.split("#", 1)[0]
            username1 = username.split("#", 1)[0]
            for _match in match:
                dettagli = await _match.details()
                for player in dettagli["allPlayers"]:
                    # print(player['player']['username'])
                    if player['player']['username'].lower() == nome or\
                            player['player']['username'].lower() == username1:
                        kd.append(player['playerStats']['kdRatio'])

            kd_mean = [np.mean(kd)]*10
            kd.reverse()
            print(kd)
            plt.plot(kd, label="kd per game")
            plt.plot(kd_mean, label="average kd")
            plt.xlabel("games")
            plt.ylabel("rateo")
            plt.legend(["kd per game", "average kd"])
            plt.savefig('kd.png')
            plt.clf()
            plt.cla()
            plt.close()




        except callofduty.errors.HTTPException:
            output.append("Nickname sbagliato, controlla anche il tag activion (il numero dopo #)")
            print(5)