import discord
import asyncio

client = discord.Client()

# Replace with your desired channel ID
DESIRED_CHANNEL_ID = 1234567890

# Replace with your bot owner ID
BOT_OWNER_ID = 1234567890

# Store the selected channel ID in a dictionary
selected_channels = {}

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    # Check if the message is from the desired channel
    if message.channel.id == selected_channels.get(message.guild.id, None):
        # Process the message
        # ...
        pass
    else:
        # Ignore messages from other channels
        return

@client.event
async def on_guild_join(guild):
    # Send a private message to the bot owner asking for channel selection
    user = await client.fetch_user(BOT_OWNER_ID)
    await user.send("Hi! I have joined a new server. Please select a channel where the results will be posted.")

    # Wait for user input and store the selected channel ID
    def check(m):
        return m.author == user and m.guild is None

    try:
        message = await client.wait_for('message', check=check, timeout=60)
        channel_id = int(message.content)
    except asyncio.TimeoutError:
        await user.send("Timeout. Please try again later.")
        return
    except ValueError:
        await user.send("Invalid channel ID. Please try again.")
        return

    # Store the selected channel ID in the dictionary
    selected_channels[guild.id] = channel_id

client.run('YOUR_BOT_TOKEN')
