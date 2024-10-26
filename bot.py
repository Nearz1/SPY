import discord
from discord.ext import commands
import aiohttp
import io  # Importação necessária para manipulação de dados em bytes

client = commands.Bot(command_prefix="!", self_bot=True)

SOURCE_GUILD_ID = 1132111315553497208
SOURCE_CHANNEL_ID = 1139014684553523320
TARGET_GUILD_ID = 1299751076974563419
TARGET_CHANNEL_ID = 1299751076974563422

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    # Verifica se a mensagem é do canal de origem e do servidor de origem
    if message.guild and message.guild.id == SOURCE_GUILD_ID and message.channel.id == SOURCE_CHANNEL_ID:
        # Enviar mensagem de texto
        content = f'{message.author}: {message.content}'
        target_guild = client.get_guild(TARGET_GUILD_ID)
        if target_guild:
            target_channel = target_guild.get_channel(TARGET_CHANNEL_ID)
            if target_channel:
                await target_channel.send(content)
                print(f"Sent message to target channel: {message.content}")
                
                # Enviar anexos (imagens e vídeos)
                if message.attachments:
                    for attachment in message.attachments:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(attachment.url) as response:
                                if response.status == 200:
                                    data = await response.read()
                                    file = discord.File(io.BytesIO(data), filename=attachment.filename)
                                    await target_channel.send(file=file)
                                    print(f"Sent attachment to target channel: {attachment.url}")
                                else:
                                    print(f"Failed to download attachment: {attachment.url}")
            else:
                print("Target channel not found.")
        else:
            print("Target guild not found.")

client.run('MTI2NDI5MjU1MTY3OTAxNzA3MA.Gk0sGX.3-7r8hDbljM4FUV0BlsbIR0W78NG5OOo9vyom8')
