from discord.ext import commands
import discord


class hello(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # @commands.command()
    # async def hello(self, ctx):
    #     await ctx.send(f"Hi! <@{ctx.author.id}>")
    #     # await ctx.send(ctx.guild.id)
    
    @commands.command()
    async def wave(self, ctx, to: discord.User = commands.parameter(
        default = lambda ctx: ctx.author
        )):
        await ctx.send(f'Hello {to.mention} :wave:')
    
    # @commands.command(pass_context = True)
    # async def serverid(self, ctx):
    #     server_id = ctx.guild.id
    #     await ctx.send(server_id)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(hello(bot))