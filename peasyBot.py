from datetime import datetime
import bot

@bot.command(bot.Condition(start="!echo"))
def echo(message):
    return bot.Action(sendMessage=bot.Message(channel=message.channel, content=message.content[len("!echo"):].lstrip()))

@bot.command(bot.Condition(start="!create"))
def create(message):
    return bot.Action(createChannel=bot.Channel(server=message.server, name=message.content[len("!create"):].lstrip()))

@bot.command(bot.Condition(start="!antidisestablishmentarianism"))
def anti(message):
    return bot.Action(sendMessage=bot.Message(channel=message.channel, content="Yup"))

bot.run("MjUyMTk1MjYxMTM5Mzg2MzY5.Cxur_Q.QDEkWgWeEHyTHNVlog0hCVwDmM0")
"""
curHour = datetime.now().hour
curMinute = datetime.now().minute
update = False
while True:
    if datetime.now().hour != curHour:
        curHour = datetime.now().hour
        update = True
    if datetime.now().minute != curMinute:
        curMinute = datetime.now().minute
        if curMinute in (0, 15, 30, 45):
            update = True
        
    if update:
        message = ""
        if curMinute == 0:
            message = "{} o'clock".format(curHour)
        if curMinute == 15:
            message = "quarter past {}".format(curHour)
        if curMinute == 30:
            message = "half past {}".format(curHour)
        if curMinute == 45:
            message = "quarter to {}".format((curHour+1)%24)
        
        bot.execute(bot.Result(sendMessage=bot.Message(channel="general", content="It is {}!".format(message))))
        update = False
"""
