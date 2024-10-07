import re
import discord
from discord import Message
from colorama import Fore, Style, init  # For pretty console colors
import discord
import asyncio
from config_handler import load_config, load_sent_codes, save_sent_codes

# Initialize colorama for colored console output
init()

# Create a self-bot instance with the token of a user (NOT a bot token!)
client = discord.Client()

# The regex pattern to match codes like the example: YTUBK-H3UUE-XW926-D524X
code_pattern = re.compile(r'\b[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}\b')

# Load configuration from config.json
config = load_config()
if not config:
    print("❌ Failed to load configuration. Exiting...")
    exit(1)

# Extract configurations from the config file
SERVERS_TO_MONITOR = config['servers']
BOT_MENTION_ID = config['bot_mention_id']
TARGET_SERVER_ID = config['target_server_id']
BOT_TOKEN = config['bot_token']
CODES_FILE = config['codes_file']

# Load sent codes from sent_codes.json
sent_codes = load_sent_codes()

# Message counter to print a progress message every 10 messages
message_counter = 0

# Event triggered when the bot is ready and connected
@client.event
async def on_ready():
    print(f"\n{Fore.GREEN}✅ Logged in as {client.user}! Monitoring servers and channels...{Style.RESET_ALL}")
    for server in SERVERS_TO_MONITOR:
        print(f"{Fore.CYAN}🔍 Monitoring server {server['guild_id']} and channels: {server['channels']}{Style.RESET_ALL}")

# Function to check messages for codes and send a normal message
@client.event
async def on_message(message: Message):
    global message_counter
    message_counter += 1

    if message_counter % 15 == 0:
        print(f"{Fore.CYAN}🔄 Still working... Received {message_counter} messages so far!{Style.RESET_ALL}")

    if message.guild is not None:
        for server in SERVERS_TO_MONITOR:
            if message.guild.id == server['guild_id'] and message.channel.id in server['channels']:
                found_codes = code_pattern.findall(message.content)

                for code in found_codes:
                    if code not in sent_codes:
                        print(f"\n{Fore.YELLOW}🔍 Code Detected! {Style.RESET_ALL}")
                        print(f"{Fore.MAGENTA}{'='*50}{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}🌐 Server: {message.guild.name} (ID: {message.guild.id}){Style.RESET_ALL}")
                        print(f"{Fore.BLUE}📣 Channel: {message.channel.name} (ID: {message.channel.id}){Style.RESET_ALL}")
                        print(f"{Fore.CYAN}👤 Author: {message.author} (ID: {message.author.id}){Style.RESET_ALL}")
                        print(f"{Fore.RED}🔑 Code found: {code}{Style.RESET_ALL}")
                        print(f"{Fore.MAGENTA}{'='*50}{Style.RESET_ALL}\n")

                        guild_b = client.get_guild(TARGET_SERVER_ID)
                        channel_b = guild_b.get_channel(message.channel.id)

                        if channel_b is not None:
                            await channel_b.send(f"<@{BOT_MENTION_ID}> redeemcode {code}")
                            sent_codes.add(code)
                            save_sent_codes(sent_codes)
                            print(f"{Fore.GREEN}✅ Message sent to bot with code {code}!{Style.RESET_ALL}")

                            response = await wait_for_bot_response(channel_b, BOT_MENTION_ID)
                            if response:
                                print(f"{Fore.LIGHTGREEN_EX}📝 Response from bot: {response}{Style.RESET_ALL}")
                            else:
                                print(f"{Fore.RED}❌ No response from bot within the time limit.{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}❌ Error: Could not find channel {message.channel.id} in Server {message.guild.id}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.LIGHTBLACK_EX}⚠️ Code {code} has already been sent. Skipping...{Style.RESET_ALL}")

# Function to wait for the bot's response message (with embed) in the same channel
async def wait_for_bot_response(channel, bot_mention_id, timeout=30):
    def check_response(message):
        return message.author.id == bot_mention_id and message.channel == channel and len(message.embeds) > 0

    try:
        message = await client.wait_for('message', timeout=timeout, check=check_response)
        embed = message.embeds[0]

        if "THERE WAS AN ERROR" in embed.title:
            return f"Error: {embed.description}"
        elif "Code redeemed" in embed.title:
            return f"Success: {embed.description}"
        else:
            return "Unknown response received."
    except asyncio.TimeoutError:
        return None

# Run the client using the bot token from the config
client.run(BOT_TOKEN)
