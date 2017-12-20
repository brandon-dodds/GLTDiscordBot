import asyncio

import discord
import feedparser

client = discord.Client()


async def update_checks():
    await client.wait_until_ready()
    episode_count = None
    tkmiz_last_published = None

    while not client.is_closed:
        [episode_count, tkmiz_last_published] = await asyncio.gather(new_episode_check(episode_count),
                                                                     tkmiz_media_check(tkmiz_last_published))
        await asyncio.sleep(900)


async def new_episode_check(current_count):
    episode_announcements = client.get_channel(id='369782637822345216')
    botpings = discord.utils.get(episode_announcements.server.roles, name='botpings')
    shoujo_shuumatsu_feed = "https://nyaa.si/?page=rss&q=shoujo+shuumatsu+1080p+horriblesubs&c=0_0&f=0"
    feed = feedparser.parse(shoujo_shuumatsu_feed)

    count = len(feed['items'])
    if current_count is not None and count > current_count:
        link = feed['items'][0]['link']
        await client.send_message(episode_announcements,
                                  "The new episode is here! {0} \n The link is here! {1}".format(botpings.mention,
                                                                                                 link))

    return count


async def tkmiz_media_check(last_published):
    art_media = client.get_channel(id='351101813212184577')
    tkmiz_media_feed = "https://twitrss.me/twitter_user_to_rss/?user=tkmiz%2Fmedia"
    feed = feedparser.parse(tkmiz_media_feed)

    published = feed['items'][0].published_parsed
    if last_published is not None and published > last_published:
        link = feed['items'][0]['link']
        await client.send_message(art_media, "Fresh potato from tsukumizu! \n {0}".format(link))

    return published


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
