import asyncio

import discord
import feedparser

client = discord.Client()


async def update_checks():
    await client.wait_until_ready()
    episode_count = 0

    while not client.is_closed:
        episode_count = await new_episode_check(episode_count)

        await asyncio.sleep(900)


async def new_episode_check(current_count):
    episode_announcements = client.get_channel(id='369782637822345216')
    botpings = discord.utils.get(episode_announcements.server.roles, name='botpings')
    shoujo_shuumatsu_feed = "https://nyaa.si/?page=rss&q=shoujo+shuumatsu+1080p+horriblesubs&c=0_0&f=0"
    feed = feedparser.parse(shoujo_shuumatsu_feed)

    count = len(feed['items'])
    if current_count > 0 and count > current_count:
        link = feed['items'][0]['link']
        await client.send_message(episode_announcements, \
                "The new episode is here! {0} \n The link is here! {1}".format(botpings.mention, link))

    return count


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(update_checks())
token_file = open("token.txt", "r")
token = str(token_file.read())
client.run(token)
token_file.close()
