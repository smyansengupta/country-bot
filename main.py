"""
Country Bot
Created by Smyan Sengupta using REST Countries API
"""

import discord
import requests
import json
from discord.ext import commands
import locale

locale.setlocale(locale.LC_ALL, 'en_US')

client = commands.Bot(command_prefix="cb!", help_command=None)


@client.event
async def on_ready():
    print("Country Bot is ready!")
    await client.change_presence(activity=discord.Game("cb!help"))


@client.command()
async def help(ctx):
    h_info = discord.Embed(title="Help Menu", author="Country Bot", description="All commands",
                           color=discord.Color.blurple())
    h_info.add_field(name="cb!country [country]", value="Gives info on the country", inline=False)
    h_info.add_field(name="cb!help", value="Shows help menu", inline=False)

    await ctx.send(embed=h_info)


@client.command()
async def country(ctx, *, name):
    region = None
    subregion = None
    area = None
    capital = None
    population = None
    language = None
    languages = []
    native_languages = []
    currency = None
    currency_symbol = None
    code = None
    flag = None

    if name.lower() == "united states" or name.lower() == "us" or name.lower() == "america":
        name = "United States of America"
    elif name.lower() == "india":
        name = "Republic of India"
    elif name.lower() == "north korea":
        name = "Democratic People's Republic of Korea"
    elif name.lower() == "south korea":
        name = "Korea (Republic of)"
    elif name.lower() == "uk":
        name = "United Kingdom"

    r = requests.get(f'https://restcountries.com/v2/name/{name}')
    data = r.json()

    if data == {'status': 404, 'message': 'Not Found'}:
        error = discord.Embed(title="Error", color=discord.Color.blurple())
        error.add_field(name="Command not found", value="Please try again")
        await ctx.send(embed=error)
        return

    if 'name' in data[0]:
        name = data[0]['name']
    if 'region' in data[0]:
        region = data[0]['region']
    if 'subregion' in data[0]:
        subregion = data[0]['subregion']
    if 'area' in data[0]:
        area = data[0]['area']
    if 'capital' in data[0]:
        capital = data[0]['capital']
    if 'population' in data[0]:
        population = data[0]['population']
    if 'languages' in data[0]:
        for lang in data[0]['languages']:
            languages.append(lang['name'])
            try:
                native_languages.append(lang['nativeName'])
            except KeyError:
                continue
        language = ""
        for i in range(len(languages)):
            if i < len(native_languages) and native_languages[i] == languages[i]:
                if i == 0:
                    language += languages[i]
                else:
                    language += f'\n{languages[i]}'
            else:
                if i == 0:
                    language += f'{languages[i]} ({native_languages[i]})'
                else:
                    if i < len(native_languages):
                        language += f'\n{languages[i]} ({native_languages[i]})'
                    else:
                        language += f'\n{languages[i]}'
    if 'currencies' in data[0]:
        currency = data[0]['currencies'][0]['name']
        currency_symbol = data[0]['currencies'][0]['symbol']
    if 'alpha2Code' in data[0]:
        code = data[0]['alpha2Code']
    if 'flags' in data[0]:
        flag = data[0]['flags']['png']
    
    global c_info
    
    """
    req = urllib.request.urlopen(f'https://flagcdn.com/60x45/{code.lower()}.png')
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    image = cv2.imdecode(arr, -1)
    if image is not None:
        mean_color = np.mean(image[0:60, 0:45], axis=(0, 1))
        mean_color_hex = '%02x%02x%02x' % mean_color
        c_info = discord.Embed(title=name, color=mean_color_hex)
    else:
        c_info = discord.Embed(title=name, color=discord.Color.blurple())
    """
    
    c_info = discord.Embed(title=name, color=discord.Color.blurple())
    if code is not None:
        c_info.set_thumbnail(url=f'https://flagcdn.com/60x45/{code.lower()}.png')
    if region is not None:
        c_info.add_field(name="Region", value=region, inline=True)
    if subregion is not None:
        c_info.add_field(name="Subregion", value=subregion, inline=True)
    if capital is not None:
        c_info.add_field(name="Capital", value=capital, inline=True)
    if area is not None:
        area = locale.format_string("%d", area, grouping=True)
        c_info.add_field(name="Area", value=f'{area} sq km', inline=True)
    if population is not None:
        population = locale.format_string("%d", population, grouping=True)
        c_info.add_field(name="Population", value=population, inline=True)
    if currency is not None and currency_symbol is not None:
        c_info.add_field(name="Currency", value=f'{currency} ({currency_symbol})', inline=True)
    if language is not None:
        c_info.add_field(name="Languages", value=language, inline=False)

    await ctx.send(embed=c_info)


# client.run("")
