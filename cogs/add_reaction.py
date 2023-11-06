from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta
import asyncio
from pathlib import Path
import os
import discord
import pytz
import datetime

class add_reaction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot




    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        # 添加身分組的message_id
        role_message_id = 1170914712695885875
        # print(payload.emoji.id)
        if payload.message_id != role_message_id:
            return  
        if str(payload.emoji) == '\U0001F914':
            guild = await self.bot.fetch_guild(payload.guild_id)
            member = await guild.fetch_member(payload.user_id)
            role = guild.get_role(1049273963127255090)
            await member.add_roles(role)
            await member.send(f"獲得 【{role}】 身分組成功！", delete_after = 10)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        # 添加身分組的message_id
        role_message_id = 1170914712695885875
        # print(payload.emoji.id)
        if payload.message_id != role_message_id:
            return  
        if str(payload.emoji) == '\U0001F914':
            guild = await self.bot.fetch_guild(payload.guild_id)
            member = await guild.fetch_member(payload.user_id)
            role = guild.get_role(1049273963127255090)
            await member.remove_roles(role)
            await member.send(f"移除 【{role}】 身分組成功！", delete_after = 10)
    

async def setup(bot: commands.Bot):
    await bot.add_cog(add_reaction(bot))