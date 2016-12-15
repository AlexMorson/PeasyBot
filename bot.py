from enum import Enum
from discord import Client
client = Client()

class CommandType(Enum):
    NoResult = 0
    SendMessage = 1
    CreateRoom = 2

class Command:
    def __init__(self, func, commandTypes, start, channel, server): #commandTypes is a list
        self.func = func
        self.commandTypes = commandTypes
        self.start = start
        self.channel = channel
        self.server = server
        
    async def __call__(self, message):
        if (self.start   is None or message.content.startswith(self.start)) and\
           (self.channel is None or message.channel == self.channel       ) and\
           (self.server  is None or message.server  == self.server        ):
            output = self.func(message)
            for commandType in self.commandTypes:
                if commandType is CommandType.NoResult:
                    break
                if commandType is CommandType.SendMessage:
                    await client.send_message(message.channel, output.pop(0))
                if commandType is CommandType.CreateRoom:
                    await client.create_channel(message.server, output.pop(0))

@client.event
async def on_ready():
    print("Logged in as", client.user.name)

commands = []
@client.event
async def on_message(message):
    for command in commands:
        await command(message)

def command(commandType, start=None, channel=None, server=None):
    def decorator(func):
        commands.append(Command(func, commandType, start, channel, server))
    return decorator

def run(token):
    client.run(token)
