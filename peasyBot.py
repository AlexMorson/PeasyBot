import bot

@bot.command([bot.CommandType.SendMessage, bot.CommandType.CreateRoom], "!create")
def createRoom(message):
    channelName = "".join(message.content[len("!create"):].split()).lower()
    return ["Creating channel called {}.".format(channelName), channelName]

bot.run("MjUyMTk1MjYxMTM5Mzg2MzY5.Cxur_Q.QDEkWgWeEHyTHNVlog0hCVwDmM0")
