from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta
import asyncio
from pathlib import Path
import os
import discord
import pytz
import datetime



class Private_message(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def pm(self, ctx, user: discord.User, *, message):
        message = f"有人私訊你：{message}" or "不用理我"
        await user.send(message)
        await ctx.message.delete()
    

async def setup(bot: commands.Bot):
    await bot.add_cog(Private_message(bot))