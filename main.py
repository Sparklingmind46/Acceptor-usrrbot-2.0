import os
from pyrogram import Client, filters
from pyrogram.types import Message

# Replace with your actual values
api_id = '22012880'  # Replace with your API ID
api_hash = '8034191591:AAFi9GqD6TpgS-d5DvX22Vh2DGgXB4SUZfg'  # Replace with your API Hash
string_session = os.getenv("STRING_SESSION")  # Assuming you store the string session in an environment variable

# Initialize the client with the string session
app = Client("my_account", api_id=api_id, api_hash=api_hash, session_string=string_session)

async def accept_all_join_requests(channel_id):
    try:
        # Fetching the admin logs for join requests
        async for event in app.get_chat_administrators(channel_id):
            if event.user_id in channel_id:
                await app.promote_chat_member(channel_id, event.user_id, can_invite_users=True)
                print(f"Accepted join request from {event.user_id}")
        print("All join requests accepted.")
    except Exception as e:
        print(f"Error: {e}")

@app.on_message(filters.command('ping'))
async def ping(client, message: Message):
    await message.reply("Bot is alive!")

@app.on_message(filters.command('accept_all'))
async def accept_all(client, message: Message):
    if message.chat.type in ['group', 'supergroup', 'channel']:
        channel_id = message.chat.id
        await accept_all_join_requests(channel_id)
        await message.reply("Accepted all pending join requests in this channel.")
    else:
        await message.reply("This command can only be used in a channel where you are an admin.")

print("Userbot is running...")
app.run()
