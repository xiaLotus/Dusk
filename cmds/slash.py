import discord
from typing import Optional
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
import json
import asyncio

class Daily(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = '每日星座', description = '選取你的星座')
    @app_commands.describe(star = '星座')
    @app_commands.choices(
        star = [
            Choice(name = "水瓶", value = "水瓶座今日運勢"),
            Choice(name = "處女", value = "處女座今日運勢"),
            Choice(name = "獅子", value = "獅子座今日運勢"),
            Choice(name = "巨蟹", value = "巨蟹座今日運勢"),
            Choice(name = "雙子", value = "雙子座今日運勢"),
            Choice(name = "金牛", value = "金牛座今日運勢"),
            Choice(name = "牡羊", value = "牡羊座今日運勢"),
            Choice(name = "天蠍", value = "天蠍座今日運勢"),
            Choice(name = "射手", value = "射手座今日運勢"),
            Choice(name = "雙魚", value = "雙魚座今日運勢"),
            Choice(name = "摩羯", value = "摩羯座今日運勢"),
            Choice(name = "天秤", value = "天秤座今日運勢"),
        ]
    )

    async def daily(self, interaction: discord.Interaction, star: Choice[str]):
        customer = interaction.user.display_name
        if interaction.channel_id != 1170618194801725480:
            await interaction.response.send_message("此指令僅能在指定頻道使用", ephemeral = True)
            return
        
        with open('all_horoscope_data.json', 'r', encoding = 'utf-8') as json_file:
            star_urls = json.load(json_file)
        
        # print(self.bot.user.name)
        star = star.value
        # 引述
        short_review = star_urls[star]['今日短評']
        # print(short_review)
        lucky_number = star_urls[star]['幸運數字']
        lucky_color = star_urls[star]['幸運顏色']
        auspicious_direction = star_urls[star]['開運方位']
        auspicious_time_today = star_urls[star]['今日吉時']
        lucky_zodiac_signs = star_urls[star]['幸運星座']

        # 整體運勢 星 與 沒點亮的星 與 text
        total_fortune_star = star_urls[star]['整體運勢']['star']
        total_fortune_unstar = star_urls[star]['整體運勢']['unstar']
        total_fortune_text = star_urls[star]['整體運勢']['text']

        # 愛情運勢 星 與 沒點亮的星 與 text
        love_star = star_urls[star]['愛情運勢']['star']
        love_unstar = star_urls[star]['愛情運勢']['unstar']
        love_text = star_urls[star]['愛情運勢']['text']

        # 事業運勢 星 與 沒點亮的星 與 text
        career_star = star_urls[star]['事業運勢']['star']
        career_unstar = star_urls[star]['事業運勢']['unstar']
        career_text = star_urls[star]['事業運勢']['text']


        # 財運運勢 星 與 沒點亮的星 與 text
        fortune_star = star_urls[star]['財運運勢']['star']
        fortune_unstar = star_urls[star]['財運運勢']['unstar']
        fortune_text = star_urls[star]['財運運勢']['text']

        # embed = discord.Embed(title = f"{star}", color = '#7796F0')
        embed = discord.Embed(title = f"{star}", color = discord.Color.orange())
        # embed.set_author(
        #     name = f'{self.bot.user.name}',
        #     icon_url = self.bot.user.avatar.url
        # )
        # 短評到幸運星座 
        embed.add_field(name = '今日短評', value = f"{short_review}", inline = True)
        embed.add_field(name = '幸運數字', value = f'{lucky_number}', inline = True)
        embed.add_field(name = '幸運顏色', value = f'{lucky_color}', inline = True)
        embed.add_field(name = '開運方位', value = f'{auspicious_direction}', inline = True)
        embed.add_field(name = '今日吉時', value = f'{auspicious_time_today}', inline = True)
        embed.add_field(name = '幸運星座', value = f'{lucky_zodiac_signs}', inline = True)

        embed.add_field(name = '整體運勢', 
                        value = f'星數: {total_fortune_star * "★"}{total_fortune_unstar * "☆"} \n 內文: {total_fortune_text}', 
                        inline = True
                        )
        
        embed.add_field(name = '愛情運勢', 
                        value = f'星數: {love_star*"★"}{love_unstar*"☆"} \n 內文:  {love_text}',                       
                        inline = True
                        )
        
        embed.add_field(name = '事業運勢', 
                        value = f'星數: {career_star*"★"}{career_unstar*"☆"} \n 內文: {career_text}',                        
                        inline = True
                        )
        embed.add_field(name = '財運運勢', 
                        value = f'星數: {fortune_star*"★"}{fortune_unstar*"☆"} \n 內文: {fortune_text}',                       
                        inline = True
                        )
        embed.set_footer(
            icon_url = self.bot.user.avatar.url,
            text = 'Dusk - 蕸製作'
        )
        await interaction.response.send_message(embed = embed)
            
    @app_commands.command(name="延遲",description="取得機器人的延遲")
    async def ping(self,interaction:discord.Interaction):
        past_ping = self.bot.latency
        new_ping1 = past_ping*1000
        await interaction.response.send_message(f"目前機器人的延遲是`{round(new_ping1,1)}ms`")

    @app_commands.command(name = "私訊", description = "Dusk幫你傳送訊囉...別吵，就在傳了")
    @app_commands.describe(member = "成員", message = "訊息")
    async def private_message(self, interaction: discord.Interaction, member: discord.User, message: str):
        text = f"{message}"
        await member.send(f"我是來幫忙傳話的： \n {text} \n 話傳完了，我走了")
        await interaction.response.send_message("傳送成功", ephemeral = True)

async def setup(bot: commands.Bot):

    await bot.add_cog(Daily(bot))