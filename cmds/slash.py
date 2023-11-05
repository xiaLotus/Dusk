import discord
from typing import Optional
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
import json

class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # name指令名稱，description指令敘述
    @app_commands.command(name = "hello", description = "Hello, world!")
    async def hello(self, interaction: discord.Interaction):
        # 回覆使用者的訊息
        await interaction.response.send_message("Hello, world!")

    # @app_commands.describe(參數名稱 = 參數敘述)
    # 參數: 資料型態，可以限制使用者輸入的內容
    @app_commands.command(name = "add", description = "計算相加值")
    @app_commands.describe(a = "輸入數字", b = "輸入數字")
    async def add(self, interaction: discord.Interaction, a: int, b: int):
        await interaction.response.send_message(f"Total: {a + b}")

    # 參數: Optional[資料型態]，參數變成可選，可以限制使用者輸入的內容
    @app_commands.command(name = "say", description = "大聲說出來")
    @app_commands.describe(name = "輸入人名", text = "輸入要說的話")
    async def say(self, interaction: discord.Interaction, name: str, text: Optional[str] = None):
        if text == None:
            text = "。。。"
        await interaction.response.send_message(f"{name} 說 「{text}」")

    # @app_commands.choices(參數 = [Choice(name = 顯示名稱, value = 隨意)])
    @app_commands.command(name = "order", description = "點餐機")
    @app_commands.describe(meal = "選擇餐點", size = "選擇份量")
    @app_commands.choices(
        meal = [
            Choice(name = "漢堡", value = "hamburger"),
            Choice(name = "薯條", value = "fries"),
            Choice(name = "雞塊", value = "chicken_nuggets"),
        ],
        size = [
            Choice(name = "大", value = 0),
            Choice(name = "中", value = 1),
            Choice(name = "小", value = 2),
        ]
    )
    async def order(self, interaction: discord.Interaction, meal: Choice[str], size: Choice[int]):
        # 獲取使用指令的使用者名稱
        customer = interaction.user.name
        # 使用者選擇的選項資料，可以使用name或value取值
        meal = meal.value
        size = size.value
        await interaction.response.send_message(f"{customer} 點了 {size} 號 {meal} 餐")

class Daily(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = 'daily', description = '每日 星座')
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
        with open('all_horoscope_data.json', 'r', encoding = 'utf-8') as json_file:
            star_urls = json.load(json_file)
        
        # print(self.bot.user.name)
        star = star.value
        # 引述
        short_review = star_urls[star]['今日短評']
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

        embed = discord.Embed(title = f"{star}", color = '#7796F0')
        # embed.set_author(
        #     name = f'{self.bot.user.name}',
        #     icon_url = self.bot.user.avatar.url
        # )
        # 短評到幸運星座 
        embed.add_field(name = '今日短評', value = f'{short_review}', inline = True)
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
        await interaction.response.send_message(embed = embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))
    await bot.add_cog(Daily(bot))