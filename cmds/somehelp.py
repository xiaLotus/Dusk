from discord.ext import commands
import discord


class SomeHelp(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def sh(self, ctx):
        embed = discord.Embed(title = '指令', description = '指令大全', color = 0x8e2929)
        embed.add_field(name = 'wave', value = '打招呼', inline = True)
        embed.add_field(name = 'avr', value = '顯示大頭照', inline = True)
        embed.add_field(name = 'purge', value = '刪除留言，僅管理員可使用', inline = True)
        # 顯示機器人大頭照
        embed.set_image(url = self.bot.user.avatar.url)
        embed.set_footer(text = '目前整理到此結束')
        await ctx.send(embed = embed)



async def setup(bot: commands.Bot):
    await bot.add_cog(SomeHelp(bot))