import bot

@bot.command(bot.Condition(start="!echo"))
def echo(message):
    return bot.Result(sendMessage=bot.Message(channel=message.channel, content=message.content[len("!echo"):].lstrip()))

@bot.command(bot.Condition(start="!create"))
def create(message):
    return bot.Result(createChannel=bot.Channel(server=message.server, name=message.content[len("!create"):].lstrip()))

bot.run("MjUyMTk1MjYxMTM5Mzg2MzY5.Cxur_Q.QDEkWgWeEHyTHNVlog0hCVwDmM0")
