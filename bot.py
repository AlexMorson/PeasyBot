import threading
import asyncio
import discord
client = discord.Client()

class Message:
    def __init__(self, channel, content):
        """Create a new Message

        Args:
            channel (discord.Channel / str): the channel to send the message in
            content (str)                  : the contents of the message
        """
        self.channel = channel
        self.content = content

class Channel:
    def __init__(self, server, name):
        """Create a new channel

        Args:
            server (discord.Server): the server to create the channel in
            name   (str)           : the name of the new channel
        """
        self.server = server
        self.name = name

class Condition:
    """A condition is a requirement for a command to be performed by the bot"""
    def __init__(self, start=None, author=None, channel=None):
        """Create a condition

        Args:
            start   (str)            : test if the message starts with this string
            author  (discord.User)   : test if the author of the message matches this
            channel (discord.Channel): test if the message was sent in this channel
        """
        self.start = start
        self.author = author
        self.channel = channel

    def holds(self, message):
        """Test whether the condition holds for a given message"""
        return (self.start   is None or message.content.split()[0] == self.start  ) and\
               (self.author  is None or message.author             == self.author ) and\
               (self.channel is None or message.channel            == self.channel)

class Action:
    """An action the bot will perform"""
    def __init__(self, sendMessage=None, createChannel=None, deleteChannel=None):
        """Create an action

        Args:
            sendMessage   (Message)        : a message the bot should send
            createChannel (Channel)        : a new channel the bot should make
            deleteChannel (discord.Channel): a channel the bot should delete
        """
        self.sendMessage = sendMessage
        self.createChannel = createChannel
        self.deleteChannel = deleteChannel

    async def execute(self):
        """Make the bot perform the action"""
        if self.sendMessage is not None:
            if type(self.sendMessage.channel) == discord.Channel:
                await client.send_message(self.sendMessage.channel, self.sendMessage.content)
            else:
                for channel in client.get_all_channels():
                    if channel.name == self.sendMessage.channel:
                        await client.send_message(channel, self.sendMessage.content)
        if self.createChannel is not None:
            await client.create_channel(self.createChannel.server, self.createChannel.name)
        if self.deleteChannel is not None:
            await client.delete_channel(self.deleteChannel)

class Command:
    """A command is run if a message meets it's condition"""
    def __init__(self, func, condition):
        """Create a command

        Args:
            func      ((discord.Message)->(Action)): the function to run if the condition holds
            condition (Condition)                  : the condition to test for
        """
        self.func = func
        self.condition = condition
        
    async def apply(self, message):
        """Call the function if the condition holds

        Args:
            message (discord.Message): the message that has been sent
        """
        if self.condition.holds(message):
            action = self.func(message)
            if action is not None:
                actions.append(action)

# All the commands the bot has
commands = []
# All the actions the bot has yet to perform
actions = []

def command(condition):
    """Decorator to add a command to the bot

    Args:
        condition (Condition): the condition for the command
    """
    def decorator(func):
        """Add the command to the bot

        Args:
            func ((discord.Message)->(Action)): the function to run if the condition holds
        """
        commands.append(Command(func, condition))
    return decorator

def execute(action):
    """Allows the user to make the bot perform actions in their own event loop

    Args:
        action (Action): the action to perform
    """
    actions.append(action)

def run(token):
    """Start the bot (non-blocking)

    Args:
        token (str): the bot's login token
    """
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=botLoop, args=(asyncio.get_event_loop(), token))
    t.start()

def botLoop(loop, token):
    """Start the bot and action loop

    Args:
        loop  (AbstractEventLoop): the main asyncio event loop
        token (str)              : the bot's login token
    """
    asyncio.set_event_loop(loop)
    try:
        asyncio.ensure_future(actionLoop())
        asyncio.ensure_future(client.run(token))
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(client.logout())
    finally:
        loop.close()

async def actionLoop():
    """Check for and perform any outstanding actions"""
    # Make sure the bot is logged in before trying to perform actions
    while not client.is_logged_in:
        await asyncio.sleep(1)
    await asyncio.sleep(3)
    
    while True:
        if actions != []:
            await actions.pop(0).execute()
        await asyncio.sleep(0)

@client.event
async def on_ready():
    """Called when the bot has logged in"""
    print("Logged in as", client.user.name)

@client.event
async def on_message(message):
    """Called whenever the bot sees a new message
    Try to apply the message to each command

    Args:
        message (discord.Message): the message the bot sees
    """
    for command in commands:
        await command.apply(message)
