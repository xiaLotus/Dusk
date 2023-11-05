from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta
import asyncio
from pathlib import Path
import os
import discord
import pytz
import datetime

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, ctx):
        if (ctx.content == '早') and (ctx.author != self.bot.user) and (ctx.author.id == 1049270937314406470):
            await ctx.channel.send('米線老爺早❤️')
        if (ctx.content == '早') and (ctx.author != self.bot.user):
            await ctx.channel.send(f'<@{ctx.author.id}> 早 ~')
    

async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))