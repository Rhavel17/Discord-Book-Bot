import os
import pycurl
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from discord.ext import commands
from io import BytesIO


# Load environment variable(s) from .env file to shell's environment variables
load_dotenv()

# Retreive the API keys stored in the .env file
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOODREADS_TOKEN = os.getenv('GOODREADS_TOKEN')

''' GoodReads API Setup'''
c = pycurl.Curl()
book_url = 'https://www.goodreads.com/book/title.xml?title={}&key={}'

c.setopt(c.SSL_VERIFYPEER, 0)

'''GoodReads Functions'''


# Get the author of a specified book
def author(book):
    if book is None:
        return None
    elif not book:
        return ""
    else:
        book_title = book.strip().replace(" ", "+")

    buffer = BytesIO()

    # Input the URL for the cURL request
    c.setopt(c.URL, book_url.format(book_title, GOODREADS_TOKEN))
    # Input the variable that will store the outputted data
    c.setopt(c.WRITEDATA, buffer)
    # Perform the cURL request
    c.perform()

    # Convert the BytesIO value into a string
    response = buffer.getvalue().decode('utf8')

    # Store the xml, in string format, as an ElementTree
    elem = ET.fromstring(response)

    # Retreive the author and title from the ElementTree
    auth = elem.find('book').find('authors').find('author').find('name').text
    title = elem.find('book').find('title').text

    c.reset()
    c.setopt(c.SSL_VERIFYPEER, 0)

    return (title, auth)


# Get the description of a specified book
def description(book):
    if book is None:
        return None
    elif not book:
        return ""
    else:
        book_title = book.strip().replace(" ", "+")

    buffer = BytesIO()

    # Input the URL for the cURL request
    c.setopt(c.URL, book_url.format(book_title, GOODREADS_TOKEN))
    # Input the variable that will store the outputted data
    c.setopt(c.WRITEDATA, buffer)
    # Perform the cURL request
    c.perform()

    # Convert the BytesIO value into a string
    response = buffer.getvalue().decode('utf8')

    # Store the xml, in string format, as an ElementTree
    elem = ET.fromstring(response)

    # Retrieve the description and the title from the ElementTree
    descript = elem.find('book').find('description').text
    title = elem.find('book').find('title').text

    # Remove any unwanted substrings in the description
    descript = descript.replace("<br />", "")
    descript = descript.replace("<i>", "")
    descript = descript.replace("</i>", "")
    descript = descript.replace("<p>", "")
    descript = descript.replace("</p>", "")
    descript = descript.replace("<b>", "")
    descript = descript.replace("</b>", "")
    descript = descript.replace("(back cover)", "")

    c.reset()
    c.setopt(c.SSL_VERIFYPEER, 0)

    return (title, descript)


# Get the book's page count
def page_count(book):
    if book is None:
        return None
    elif not book:
        return ""
    else:
        book_title = book.strip().replace(" ", "+")

    buffer = BytesIO()

    # Input the URL for the cURL request
    c.setopt(c.URL, book_url.format(book_title, GOODREADS_TOKEN))
    # Input the variable that will store the outputted data
    c.setopt(c.WRITEDATA, buffer)
    # Perform the cURL request
    c.perform()

    # Convert the BytesIO value to a string
    response = buffer.getvalue().decode('utf8')

    # Store the xml, in string format, as an ElementTree
    elem = ET.fromstring(response)

    # Retreive the author and title from the ElementTree
    pages = elem.find('book').find('num_pages').text
    title = elem.find('book').find('title').text

    c.reset()
    c.setopt(c.SSL_VERIFYPEER, 0)

    return (title, pages)


# Get the book's publication year
def pub_year(book):
    if book is None:
        return None
    elif not book:
        return ""
    else:
        book_title = book.strip().replace(" ", "+")

    buffer = BytesIO()

    # Input the URL for the cURL request
    c.setopt(c.URL, book_url.format(book_title, GOODREADS_TOKEN))
    # Input the variable that will store the outputted data
    c.setopt(c.WRITEDATA, buffer)
    # Perform the cURL request
    c.perform()

    # Convert the BytesIO value to a string
    response = buffer.getvalue().decode('utf8')

    # Store the xml, in string format, as an ElementTree
    elem = ET.fromstring(response)

    # Retreive the author and title from the ElementTree
    year = elem.find('book').find('work').find('original_publication_year').text
    title = elem.find('book').find('title').text

    c.reset()
    c.setopt(c.SSL_VERIFYPEER, 0)

    return (title, year)


# Get the book's user ratings
def ratings(book):
    if book is None:
        return None
    elif not book:
        return ""
    else:
        book_title = book.strip().replace(" ", "+")

    buffer = BytesIO()

    # Input the URL for the cURL request
    c.setopt(c.URL, book_url.format(book_title, GOODREADS_TOKEN))
    # Input the variable that will store the outputted data
    c.setopt(c.WRITEDATA, buffer)
    # Perform the cURL request
    c.perform()

    # Convert the BytesIO value to a string
    response = buffer.getvalue().decode('utf8')

    # Store the xml, in string format, as an ElementTree
    elem = ET.fromstring(response)

    # Retreive the author and title from the ElementTree
    num_ratings = elem.find('book').find('work').find('ratings_count').text
    rating = elem.find('book').find('average_rating').text
    title = elem.find('book').find('title').text

    c.reset()
    c.setopt(c.SSL_VERIFYPEER, 0)

    return (title, num_ratings, rating)


'''Discord Functionality'''

# Create instance of Bot
bot = commands.Bot(command_prefix='!')

# List of global variables w/ default values
wrg = None
book = None
meeting = None


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
        return await ctx.send('Cannot grant your request.\
         Unable to parse your input for {}.'.format(ctx.command.name))
    elif isinstance(err, commands.BadArgument):
        return await ctx.send('Cannot grant your request. Parsing or conversion failure on command argument(s) for {}.'.format(ctx.command.name))
    elif isinstance(err, commands.NoPrivateMessage):
        return await ctx.send('Cannot grant your request. \'{}\' does not work in private messages.'.format(ctx.command.name))
    elif isinstance(err, commands.CommandNotFound):
        return await ctx.send('Cannot grant your request. The command you entered does not exist.')
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
async def shutdown(ctx):
    await ctx.send('Shutting down Discord Book Bot')
    c.close()
    exit()


# '!setWRG' command
@bot.command(name='set_wrg', help='SET Weekly Reading Goal')
async def set_wrg(ctx, *args):
    # Overwrite 'wrg' global variable
    global wrg
    wrg = ' '.join(args)

    # Send confirmation message to discord
    await ctx.send('Weekly Reading Goal set to \'{}\''.format(wrg))


# '!getWRG' command
@bot.command(name='get_wrg', help='GET Weekly Reading Goal')
async def get_wrg(ctx):
    if wrg is None:
        await ctx.send('Weekly Reading Goal has not been set')
    else:
        await ctx.send('Weekly Reading Goal: \'{}\''.format(wrg))


# '!deleteWRG' command
@bot.command(name='delete_wrg', help='DELETE Weekly Reading Goal')
async def delete_wrg(ctx):
    # Overwrite 'wrg' global variable
    global wrg
    wrg = None

    await ctx.send('Removed Weekly Reading Goal')


# '!setBook' command
@bot.command(name='set_book', help='SET Book that will be read')
async def set_book(ctx, *args):
    # Overwrite 'book' global variable
    global book
    book = ' '.join(args)

    # Send confirmation message to discord
    await ctx.send('Book set to \'{}\''.format(book))


# '!getBook' command
@bot.command(name='get_book', help='GET Book that is currently being read')
async def get_book(ctx):
    if book is None:
        await ctx.send('Book has not been set')
    else:
        await ctx.send('Book Club is currently reading: \'{}\''.format(book))


# '!deleteBook' command
@bot.command(name='delete_book', help='DELETE Book')
async def delete_book(ctx):
    # Overwrite 'book' global variable
    global book
    book = None

    await ctx.send('Removed Book')


# '!getMeetTime' command
@bot.command(name="set_meeting", help='SET Meeting Time for book club')
async def set_meeting(ctx, *args):
    # Overwrite 'meeting' global variables
    global meeting
    meeting = ' '.join(args)

    await ctx.send('Meeting Time has been set to: \'{}\''.format(meeting))


# '!getMeetTime' command
@bot.command(name='get_meeting', help='GET Meeting Time for book club')
async def get_meeting(ctx):
    if meeting is None:
        await ctx.send('Meeting Time has not been set')
    else:
        await ctx.send('The Meeting Time for the book club is \'{}\''.format(meeting))


# '!deleteMeetTime' command
@bot.command(name='delete_meeting', help='DELETE Meeting Time for book club')
async def delete_meeting(ctx):
    # Overwrite 'meeting' global variable
    global meeting
    meeting = None

    await ctx.send('Removed Meeting Time')

# '!get_author' command
@bot.command(name='get_author', help='Get author from a specified book')
async def get_author(ctx, book):
    book_author = author(book)

    await ctx.send('The author of \"{}\" is {}'.format(book_author[0], book_author[1]))

# '!get_description' command
@bot.command(name='get_description', help='Get description of a specified book')
async def get_description(ctx, book):
    book_description = description(book)

    await ctx.send('Description of \"{}\":\n{}'.format(book_description[0], book_description[1]))


# '!get_page_count' command
@bot.command(name='get_page_count', help='Get the page count of a specified book')
async def get_page_count(ctx, book):
    pages = page_count(book)

    await ctx.send('\"{}\" has {} pages'.format(pages[0], pages[1]))


# '!get_pub_year' command
@bot.command(name='get_pub_year', help='Get the publication year of a specified book')
async def get_page_count(ctx, book):
    pub = pub_year(book)

    await ctx.send('\"{}\" was published in {}'.format(pub[0], pub[1]))


# '!get_rating' command
@bot.command(name='get_rating', help='Get the reader ratings of a specified book')
async def get_rating(ctx, book):
    book_ratings = ratings(book)

    await ctx.send('Out of {} people, \"{}\" received an average rating of {}'.format(book_ratings[1], book_ratings[0], book_ratings[2]))

# '!get_all' command
@bot.command(name='get_all', help='Get all data of a specified book')
async def get_all(ctx, book):
    book_author = author(book)
    book_description = description(book)
    pages = page_count(book)
    pub = pub_year(book)
    book_ratings = ratings(book)
    data_string = "Title: {}\nAuthor: {}\nDescription: {}\nPage Count: {}\nPublication Year: {}\nAverage Book Rating: {}\nNumber of Ratings: {}" \
        .format(book_author[0], book_author[1], book_description[1], pages[1], pub[1], book_ratings[2], book_ratings[1])

    await ctx.send(data_string)


# Run the Client
bot.run(DISCORD_TOKEN)
