from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta
import asyncio
from pathlib import Path
import os
import discord
import pytz
import datetime

class TaskTime(commands.Cog):
  # 臺灣時區 UTC+8
  tz = datetime.timezone(datetime.timedelta(hours = 8))
  # 設定每日十二點執行一次函式
  everyday_time = datetime.time(hour = 0, minute = 0, tzinfo = tz)

  def __init__(self, bot: commands.Bot):
      self.bot = bot
      self.everyday.start()

  @tasks.loop(time = everyday_time)
  async def everyday(self):
      # 設定發送訊息的頻道ID
      channel_id = 1169176762438127656
      channel = self.bot.get_channel(channel_id)
      embed = discord.Embed(
          title = "睡覺時間",
          description = f"🕛 現在時間 {datetime.date.today()} 00:00",
          color = discord.Color.orange()
      )
      await channel.send(embed = embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(TaskTime(bot))