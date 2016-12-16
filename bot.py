from discord import Client
client = Client()

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

    async def doActions(self, message):
        if self.sendMessage is not None:
            await client.send_message(message.channel, self.sendMessage)
        if self.createChannel is not None:
            await client.create_channel(message.server, self.createChannel)
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
                await result.doActions(message)

@client.event
async def on_ready():
    print("Logged in as", client.user.name)

commands = []
@client.event
async def on_message(message):
    for command in commands:
        await command(message)

def command(condition):
    def decorator(func):
        commands.append(Command(func, condition))
    return decorator

def run(token):
    client.run(token)
