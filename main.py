import asyncio
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import GetParticipantsRequest, ApproveChannelJoinRequest
from telethon.tl.types import ChannelParticipantsRequests

# Your API ID and Hash, replace with your values
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

# Initialize the client
client = TelegramClient('userbot_session', api_id, api_hash)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Responds to the /start command."""
    await event.reply("Hello! I am here to help approve all pending join requests in this channel. Use /approveall to approve all requests.")

@client.on(events.NewMessage(pattern='/approveall'))
async def approve_all_requests(event):
    # Check if the command is issued in a channel
    if event.is_channel and event.is_group:
        channel_id = event.chat_id  # Get the channel ID dynamically
        try:
            # Fetch pending join requests for the detected channel
            offset = 0
            limit = 100
            requests_approved = 0

            # Process requests in batches until there are no more
            while True:
                requests = await client(GetParticipantsRequest(
                    channel=channel_id,
                    filter=ChannelParticipantsRequests(),
                    offset=offset,
                    limit=limit,
                    hash=0
                ))

                # If there are no pending requests, exit the loop
                if not requests.users:
                    break

                # Approve each pending join request
                for user in requests.users:
                    try:
                        await client(ApproveChannelJoinRequest(channel=channel_id, user_id=user.id))
                        print(f'Approved join request from {user.username or user.id}')
                        requests_approved += 1
                        await asyncio.sleep(1)  # Short delay to reduce the risk of hitting the flood limit
                    except FloodWaitError as e:
                        print(f"Flood wait error encountered. Waiting for {e.seconds} seconds.")
                        await asyncio.sleep(e.seconds)  # Wait for the specified time before continuing

                # Update offset for the next batch of requests
                offset += limit

            await event.reply(f"All pending join requests ({requests_approved}) have been approved for this channel.")
        except Exception as e:
            await event.reply(f"Error: {str(e)}")
    else:
        await event.reply("Please use the /approveall command in a channel or group.")

# Start the client
with client:
    print("Userbot is running and listening for commands...")
    client.run_until_disconnected()
