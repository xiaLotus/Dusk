from discord.ext import commands
from discord.ext.commands import Context
import discord
import datetime


class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label = "普通指令", emoji = "🈷️", description = "快速導覽一般指令!"),
            discord.SelectOption(
                label = "爬蟲指令", emoji = "🈲",description = "爬蟲指令導覽!"),
            discord.SelectOption(
                label = "?指令", emoji = "❓", description = "還沒想好!")
            ]
        super().__init__(
            placeholder = "快速導覽",
            max_values = 1,
            min_values = 1,
            options = options
        )
    
    async def callback(self, interaction: discord.Interaction):
        help_embed = discord.Embed(color = 0xBEBEFE)
        help_embed.set_author(
            name = f"嗨！ {interaction.user.name}"
        )

        select_value = self.values[0]
        if select_value == '普通指令':
            help_embed.description = f"這裡是普通指令，沒有甚麼特殊功能"
            help_embed.colour = 0xF59E42
            help_embed.add_field(
                name = '`!wave`',
                value = '向某人打招呼',
                inline = True 
            )
            help_embed.add_field(
                name = '`!avr`',
                value = '查看頭像',
                inline = True 
            )
            help_embed.add_field(
                name = '`!pruge`',
                value = '刪除留言，僅管理員可以使用',
                inline = True 
            )
            help_embed.add_field(
                name = '`!sh`',
                value = '可以看見選單呦',
                inline = True 
            )
            help_embed.add_field(
                name = '`!pm`',
                value = '!pm @people message',
                inline = True 
            )

        if select_value == '爬蟲指令':
            help_embed.description = f"這裡是爬蟲指令，目前只開放我可不想室友都成精啊此伺服器使用"
            help_embed.colour = 0xF59E42
            help_embed.add_field(
                name = '`!download` `69` `書號`',
                value = '輸入書號，如 31585',
                inline = True 
            )
        if select_value == '?指令':
            help_embed.description = f"可以期待 ~"
            help_embed.colour = 0xF59E42
        
        await interaction.response.edit_message(
            embed = help_embed, content = None, view = None
        )
class SelectView(discord.ui.View):
    def __init__(self, embed: discord.Embed):
        super().__init__()
        self.embed = embed
        self.add_item(Select())


class Embed(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name = "avr", description = "平常的Embed")
    async def avr(self, ctx):
        embed = discord.Embed()
        embed.set_author(name = ctx.author.display_name,
                         url = '',
                         icon_url = ctx.author.display_avatar.url
                         )
        embed.set_image(url = ctx.author.display_avatar.url)
        await ctx.send(embed = embed)



class SomeHelp(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def sh(self, ctx):
        # 創建一個預設嵌入
        help_embed = discord.Embed(
            # title = "Dusk ",
            # description = "Dusk 插件指令",
            color = 0xBEBEFE
        )
        help_embed.set_author(
            name = f'{self.bot.user.name}插件指令',
            url = '',
            icon_url = self.bot.user.avatar.url
        )
        help_embed.add_field(
            name = '普通指令',
            value = '`選擇普通指令查詢`', 
            inline = True
        )
        help_embed.add_field(
            name = '爬蟲指令',
            value = '`選擇爬蟲指令查詢`', 
            inline = True
        )
        help_embed.add_field(
            name = '?指令',
            value = '可以期待一下',
            inline = True
        )
        help_embed.set_image(url = self.bot.user.avatar.url)
        help_embed.set_footer(text = '目前整理到此結束')
        view = SelectView(help_embed)
        await ctx.send(embed = help_embed, view = view)
        # await ctx.send(view = SelectView())
    



async def setup(bot: commands.Bot):
    await bot.add_cog(SomeHelp(bot))
    await bot.add_cog(Embed(bot))