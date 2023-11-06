from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta
import asyncio
from pathlib import Path
import os
import discord
import pytz
import datetime

class Join(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(1170908747527356427)
        embed = discord.Embed(
            title = f"歡迎！",
            description = f"{member.mention}"
        )
        embed.set_image(
            url = self.member.avatar_url
        )

        await channel.send(embed = embed)

    

async def setup(bot: commands.Bot):
    await bot.add_cog(Join(bot))