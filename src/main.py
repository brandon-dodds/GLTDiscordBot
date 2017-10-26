import discord
import asyncio
import feedparser

client = discord.Client()


async def my_background_task():
    await client.wait_until_ready()
    # Defining the feed, Parsing the feed and opening the text file.

    shoujo_shuumatsu_feed = "https://nyaa.si/?page=rss&q=shoujo+shuumatsu+1080p+horriblesubs&c=0_0&f=0"
    feed = feedparser.parse(shoujo_shuumatsu_feed)
    file = open("episode_count", "r+")
    x = len(feed["items"])
    current_amount = int(file.read())

    if x > current_amount:
        channel = discord.Object(id='369587962603896834')
        await client.send_message(channel, "{0}".format("The new episode is here! @botpings"))
        current_amount = current_amount + 1
        file.seek(0)
        file.write(str(current_amount))
        file.truncate()
        file.close()
        await asyncio.sleep(60)  # task runs every 60 seconds


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(my_background_task())
client.run('MzY5NTg1NTE3MzYyMTUxNDM2.DMawKA.wTHjFgny7JZx6Y1uAsJAFbEX5F4')
