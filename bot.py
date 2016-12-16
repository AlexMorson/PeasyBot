import asyncio
import discord
client = discord.Client()

class Message:
    def __init__(self, channel, content):
        self.channel = channel
        self.content = content

class Channel:
    def __init__(self, server, name):
        self.server = server
        self.name = name

commands = []
results = []

class Condition:
    def __init__(self, start=None, author=None, channel=None):
        self.start = start
        self.author = author
        self.channel = channel

    def holds(self, message):
        return (self.start   is None or message.content.split()[0] == self.start  ) and\
               (self.author  is None or message.author             == self.author ) and\
               (self.channel is None or message.channel            == self.channel)

class Result:
    def __init__(self, sendMessage=None, createChannel=None, deleteChannel=None):
        self.sendMessage = sendMessage
        self.createChannel = createChannel
        self.deleteChannel = deleteChannel

    async def doActions(self):
        if self.sendMessage is not None:
            await client.send_message(self.sendMessage.channel, self.sendMessage.content)
        if self.createChannel is not None:
            await client.create_channel(self.createChannel.server, self.createChannel.name)
        if self.deleteChannel is not None:
            await client.delete_channel(self.deleteChannel)

class Command:
    def __init__(self, func, condition):
        self.func = func
        self.condition = condition
        
    async def __call__(self, message):
        if self.condition.holds(message):
            result = self.func(message)
            if result is not None:
                results.append(result)

def command(condition):
    def decorator(func):
        commands.append(Command(func, condition))
    return decorator

def run(token):
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(resultLoop())
        asyncio.ensure_future(client.start(token))
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(client.logout())
    finally:
        loop.close()

async def resultLoop():
    while True:
        if results != []:
            print(results[0].createChannel.server.name,results[0].createChannel.name)
            await results.pop(0).doActions()
        await asyncio.sleep(0)

@client.event
async def on_ready():
    print("Logged in as", client.user.name)

@client.event
async def on_message(message):
    for command in commands:
        await command(message)
