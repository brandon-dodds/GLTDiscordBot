import discord
import asyncio
import time

client = discord.Client()


async def my_background_task():
    await client.wait_until_ready()
    day = time.strftime("%a")
    hour = time.strftime("%H")
    channel = discord.Object(id='369587962603896834')
    if day == "Fri" and hour == "15":
        await client.send_message(channel, "The new episode is here! @botpings")
        await asyncio.sleep(60)  # task runs every 60 seconds


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(my_background_task())
client.run('MzY5NTg1NTE3MzYyMTUxNDM2.DMawKA.wTHjFgny7JZx6Y1uAsJAFbEX5F4')
