from discord.ext import commands
from datetime import datetime
from discord import app_commands
import discord
import asyncio


class Delete(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.has_permissions(manage_messages = True)
    @commands.command()
    async def purge(self, ctx, amount: int):

        now = datetime.now()

        # 檢查執行指令的成員是否具有管理員權限
        if ctx.author.guild_permissions.administrator:
            await ctx.channel.purge(limit = amount + 1)
            embed = discord.Embed(
                title = '刪除留言',
            )
            embed.add_field(
                name = f'管理員 - {ctx.author.display_name}', 
                value = f'''
                    刪除{amount}條訊息，時間是
                    {now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}
                    ''',
                inline = True
            )
            embed.set_image(url = ctx.author.display_avatar.url)
            # 頻道id
            channel_id = 1167396097501708299
            # get 頻道id
            send_ctx_to_channel = self.bot.get_channel(channel_id)
            if send_ctx_to_channel:
                await send_ctx_to_channel.send(embed = embed)
            else:
                await ctx.send('無法找到該頻道。')
        else:
            await ctx.send('不是管理員無法使用該指令。')



async def setup(bot: commands.Bot):
    await bot.add_cog(Delete(bot))