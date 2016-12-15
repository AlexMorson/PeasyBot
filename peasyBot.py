import bot

@bot.command(bot.Condition(start="!create"))
def createRoom(message):
    channelName = "".join(message.content[len("!create"):].split()).lower()
    return bot.Result(sendMessage="Creating channel called {}.".format(channelName), createChannel=channelName)

@bot.command(bot.Condition(start="!echo"))
def echo(message):
    return bot.Result(sendMessage=message.content[len("!echo"):].lstrip())

bot.run("MjUyMTk1MjYxMTM5Mzg2MzY5.Cxur_Q.QDEkWgWeEHyTHNVlog0hCVwDmM0")
