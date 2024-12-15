import os
import json
import discord
from discord.ext import commands
from tqdm import tqdm

LOG_FOLDER = "message_storage_log"
os.makedirs(LOG_FOLDER, exist_ok=True)

LOGGED_MESSAGES_FILE = os.path.join(LOG_FOLDER, "logged_messages.json")
if not os.path.exists(LOGGED_MESSAGES_FILE):
    with open(LOGGED_MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)
        
with open(LOGGED_MESSAGES_FILE, "r", encoding="utf-8") as f:
    logged_messages = json.load(f)

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def log_message(server_name, channel_name, message):
    server_folder = os.path.join(LOG_FOLDER, server_name)
    os.makedirs(server_folder, exist_ok=True)

    txt_file_path = os.path.join(server_folder, f"{server_name}.txt")
    json_file_path = os.path.join(server_folder, f"{server_name}.json")

    log_entry = f"[{message.created_at}] Channel: {channel_name}, Author: {message.author}, Message: {message.content}\n"
    json_entry = {
        "timestamp": str(message.created_at),
        "channel": channel_name,
        "author": str(message.author),
        "message": message.content,
    }

    # .txt file
    with open(txt_file_path, "a", encoding="utf-8") as txt_file:
        txt_file.write(log_entry)

    # .json file
    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    else:
        data = []

    data.append(json_entry)
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Fetching old messages...")

    for guild in bot.guilds:
        guild_id = str(guild.id)
        if guild_id not in logged_messages:
            logged_messages[guild_id] = set()

        print(f"Fetching messages for server: {guild.name}")
        for channel in guild.text_channels:
            try:
                total_messages = 0
                async for message in channel.history(limit=None):
                    total_messages += 1

                # progress bar
                with tqdm(
                    total=total_messages,
                    desc=f"Fetching {channel.name}",
                    unit="message",
                ) as pbar:
                    # Fetch & log messages
                    async for message in channel.history(limit=None):
                        if message.id not in logged_messages[guild_id]:
                            await log_message(guild.name, channel.name, message)
                            logged_messages[guild_id].add(message.id)
                            pbar.update(1)
            except discord.Forbidden:
                print(f"Cannot access channel: {channel.name} in {guild.name} (no permissions)")
            except discord.HTTPException as e:
                print(f"Failed to fetch messages for {channel.name} in {guild.name}: {e}")

    save_logged_messages()
    print("Old messages fetched successfully!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    guild_id = str(message.guild.id)
    if guild_id not in logged_messages:
        logged_messages[guild_id] = set()

    if message.id not in logged_messages[guild_id]:
        await log_message(message.guild.name, message.channel.name, message)
        logged_messages[guild_id].add(message.id)

        save_logged_messages()

def save_logged_messages():
    with open(LOGGED_MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {guild_id: list(msg_ids) for guild_id, msg_ids in logged_messages.items()}, f
        )

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run("Token")# replace with yoour actual token
