from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetAdminLogRequest
from telethon.tl.types import ChannelAdminLogEventsFilter

# Replace these with your own values
api_id = '22012880'
api_hash = '8034191591:AAFi9GqD6TpgS-d5DvX22Vh2DGgXB4SUZfg'
phone = '+917367017930'  # e.g., '+123456789'

client = TelegramClient('session_name', api_id, api_hash)

async def accept_all_join_requests(channel_id):
    try:
        async for event in client.iter_admin_log(
            entity=channel_id,
            filter=ChannelAdminLogEventsFilter(participants=True),
        ):
            if event.join_request:
                try:
                    await client.edit_admin(channel_id, event.user_id, invite=True)
                    print(f"Accepted join request from {event.user_id}")
                except Exception as e:
                    print(f"Failed to accept join request from {event.user_id}: {e}")
        print("All join requests accepted.")
    except Exception as e:
        print(f"Error: {e}")

@client.on(events.NewMessage(pattern='/accept_all'))
async def handler(event):
    # Check if the command is sent from a channel
    if event.is_channel and event.is_group:
        channel_id = event.chat_id
        await accept_all_join_requests(channel_id)
        await event.reply("Accepted all pending join requests in this channel.")
    else:
        await event.reply("This command can only be used in a channel where you are an admin.")

with client:
    print("Userbot is running...")
    client.run_until_disconnected()
