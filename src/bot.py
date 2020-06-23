import os
from dotenv import load_dotenv
from discord.ext import commands

# Load environment variable(s) from .env file to shell's environment variables
load_dotenv()

# Get the value of the 'DISCORD_TOKEN' env variable
TOKEN = os.getenv('DISCORD_TOKEN')

# Create instance of Bot
bot = commands.Bot(command_prefix='!')

# List of global variables w/ default values
wrg = None
book = None
# Called when 'client is done preparing the data received from discord
# Usually after login is successful and the Client.guilds are filled up'
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

# Exception Handling for the bot
@bot.event
async def on_command_error(ctx, err):
    # Ignore any errors that originate in on_command_error
    if hasattr(ctx.command, 'on_error'):
        return

    if isinstance(err, commands.MissingRequiredArgument):
        return await ctx.send('Cannot grant your request. Missing a parameter for \'{}\'.'.format(ctx.command.name))
    elif isinstance(err, commands.ArgumentParsingError):
        return await ctx.send('Cannot grant your request. Unable to parse your input for {}.'.format(ctx.command.name))
    elif isinstance(err, commands.BadArgument):
        return await ctx.send('Cannot grant your request. Parsing or conversion failure on command argument(s) for {}.'.format(ctx.command.name))
    elif isinstance(err, commands.NoPrivateMessage):
        return await ctx.send('Cannot grant your request. \'{}\' does not work in private messages.'.format(ctx.command.name))
    elif isinstance(err, commands.CommandNotFound):
        return await ctx.send('Cannot grant your request. The command, \'{}\', does not exist.'.format(ctx.command.name))
    elif isinstance(err, commands.DisabledCommand):
        return await ctx.send('Cannot grant your request. The command, \'{}\', has been disabled.'.format(ctx.command.name))
    elif isinstance(err, commands.CommandInvokeError):
        err = getattr(err, 'original', err)
        return await ctx.send('Cannot grant your request. \'{}\' raised an exception: {}.'.format(ctx.command.name, err))
    elif isinstance(err, commands.MissingPermissions):
        return await ctx.send('Cannot grant your request. You lack the permissions to run \'{}\'.'.format(ctx.command.name))
    elif isinstance(err, commands.MissingRole):
        return await ctx.send('Cannot grant your request. You lack the correct Role to run \'{}\'.'.format(ctx.command.name))
    elif isinstance(err, commands.ExtensionError):
        return await ctx.send('Cannot grant your request. An ExtensionError has occurred.')
    elif isinstance(err, commands.CheckFailure):
        return await ctx.send('Cannot grant your request. CheckFailure with \'{}\'. Do not have correct permissions.'.format(ctx.command.name))
    elif isinstance(err, commands.UserInputError):
        return await ctx.send('Cannot grant your request. There has been an error in your input.')
    elif isinstance(err, commands.CommandError):
        return await ctx.send('Cannot grant your request. A CommandError has occurred when running the \'{}\' command.'.format(ctx.command.name))
    else:
        return await ctx.send('Cannot grant your request. The following exception has been raised: \'{}\'.'.format(ctx.command.name))


# '!test' command
@bot.command(name='test', help='Repeats given arguments')
async def test(ctx, *args):
    await ctx.send('{0} arguments: {1}'.format(len(args), ', '.join(args)))


# '!shutdown' command
@bot.command(name='shutdown', help='Turns the bot off')
async def shutdown(ctx, *args):
    await ctx.send('Shutting down Discord Book Bot')
    exit()


# '!setWRG' command
@bot.command(name='setWRG', help='SET Weekly Reading Goal')
async def setWRG(ctx, goal: str):
    # Overwrite 'wrg' global variable
    global wrg
    wrg = goal

    # Send confirmation message to discord
    await ctx.send('Weekly Reading Goal set to \'{}\''.format(goal))


# '!getWRG' command
@bot.command(name='getWRG', help='GET Weekly Reading Goal')
async def getWRG(ctx):
    if wrg is None:
        await ctx.send('Weekly Reading Goal has not been set')
    else:
        await ctx.send('Weekly Reading Goal: \'{}\''.format(wrg))


# '!deleteWRG' command
@bot.command(name='deleteWRG', help='DELETE Weekly Reading Goal')
async def deleteWRG(ctx):
    # Overwrite 'wrg' global variable
    global wrg
    wrg = None

    await ctx.send('Removed Weekly Reading Goal')

# '!setBook' command
@bot.command(name='setBook', help='SET Book that will be read')
async def setBook(ctx, currBook: str):
    # Overwrite 'book' global variable
    global book
    book = currBook

    # Send confirmation message to discord
    await ctx.send('Book set to \'{}\''.format(currBook))


# '!getBook' command
@bot.command(name='getBook', help='GET Book that is currently being read')
async def getBook(ctx):
    if book is None:
        await ctx.send('Book has not been set')
    else:
        await ctx.send('Book Club is currently reading: \'{}\''.format(book))


# '!deleteBook' command
@bot.command(name='deleteBook', help='DELETE Book')
async def deleteBook(ctx):
    # Overwrite 'book' global variable
    global book
    book = None

    await ctx.send('Removed Book')

# Run the Client
bot.run(TOKEN)
