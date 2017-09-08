#!/usr/bin/env python3
import discord
import asyncio
import sqlite3
import os
from datetime import datetime, timedelta

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!jar'):
        if len(message.mentions) > 0: 
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            report = (message.author.id,
                      message.mentions[0].id,
                      message.timestamp)
            c.execute("INSERT INTO jar_reports ('author_id', 'report_id', 'reported_at') VALUES (?,?,?)", report)
            conn.commit()
            conn.close()
            name = message.mentions[0].nick
            if name is None:
                name = message.mentions[0].name
            await client.send_message(message.channel, "You've been naughty {}!".format(name))
            await asyncio.sleep(2)
            await client.delete_message(message)
        else:
            # Helpful error message    
            err = await client.send_message(message.channel, 'You need to mention someone for this to work!: @Someone.')
            await asyncio.sleep(11)
            await client.delete_message(err)    

client.run(os.environ['DISCORD_KEY'])