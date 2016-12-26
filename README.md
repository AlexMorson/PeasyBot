# PeasyBot
Making discord bots easy! (ish)

## Command decorator
The main feature (so far) is a decorator that you can put in front of a function definition to make it into a bot command.

For example, a bot that says hello to anyone that types !command in the channel:

```Python
import bot

@bot.command(bot.Condition(start="!command"))
def command(message):
    messageString = "Hello {}!".format(message.author.name)
    newMessage = bot.Message(channel=message.channel, content=messageString)
    return bot.Action(sendMessage=newMessage)

bot.run(<token>)
```

## Execute Result
But as well as reacting to messages you can create your own event loop and make the bot do stuff on its own!

Here is a bot that tells you the time and date every 10 seconds

```Python
import time
import datetime
import bot

bot.run(<token>)

while True:
    messageString = "The time is {}".format(datetime.datetime.now().isoformat())
    newMessage = bot.Message(channel="general", content=messageString)
    bot.execute(bot.Action(sendMessage=newMessage))
    time.sleep(10)
```