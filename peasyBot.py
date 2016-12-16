import bot

channel = None

@bot.command(bot.Condition(start="/create"))
def createRoom(message):
    channelName = "".join(message.content[len("!create"):].split()).lower()
    return bot.Result(sendMessage="Creating channel called {}.".format(channelName), createChannel=channelName)

@bot.command(bot.Condition(start="!echo"))
def echo(message):
    return bot.Result(sendMessage=message.content[len("!echo"):].lstrip())
"""
@bot.command(bot.Condition(start="!delete"))
def deleteChannel(message):
    return bot.Result(deleteChannel=message.channel)
"""

@bot.command(bot.Condition(start="!lookhere"))
def lookHere(message):
    global channel
    channel = message.channel

@bot.command(bot.Condition(start="!delete"))
def say(message):
    global channel
    return bot.Result(deleteChannel=channel)

bot.run("MjUyMTk1MjYxMTM5Mzg2MzY5.Cxur_Q.QDEkWgWeEHyTHNVlog0hCVwDmM0")
