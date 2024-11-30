from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

# Initialize your bot with the token
bot = TeleBot("7207023522:AAHhYRF4EKT8ZcaX2IdmUmy2X7kzZ5D8OUc")

# Function to approve all pending chat join requests
def approve_all_pending_requests(chat_id):
    try:
        # Fetch all pending join requests
        response = requests.get(
            f"https://api.telegram.org/bot{bot.token}/getChatJoinRequests",
            params={"chat_id": chat_id},
            timeout=10
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            
            if data.get("ok") and data.get("result"):
                for request in data["result"]:
                    user_id = request["user"]["id"]
                    try:
                        # Approve the request
                        approve_response = requests.post(
                            f"https://api.telegram.org/bot{bot.token}/approveChatJoinRequest",
                            json={"chat_id": chat_id, "user_id": user_id},
                            timeout=10
                        )
                        
                        if approve_response.status_code == 200:
                            # Create and send a welcome photo to the user
                            markup = InlineKeyboardMarkup()
                            markup.add(
                                InlineKeyboardButton(text="Tᴇᴀᴍ sᴀᴛ 🤍✨", url="https://t.me/Team_SAT_25")
                            )
                            
                            bot.send_photo(
                                chat_id=user_id,
                                photo='https://graph.org/file/4b30ed0d57465b79c1033.jpg',
                                caption='''Your Channel Joining Request Accepted\n\nThanks For Joining Our Channel ❤️''',
                                reply_markup=markup,
                                parse_mode='HTML'
                            )
                        else:
                            print(f"Failed to approve user {user_id}: {approve_response.json().get('description', 'Unknown error')}")
                    
                    except requests.exceptions.RequestException as e:
                        print(f"Error approving user {user_id}: {e}")
            else:
                print("No pending join requests found or insufficient permissions.")
        else:
            print(f"Failed to fetch join requests: {response.json().get('description', 'Unknown error')}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching join requests: {e}")

# Command to handle approving all join requests (triggered manually)
@bot.message_handler(commands=['approve_all'])
def handle_approve_all(message):
    try:
        chat_id = message.chat.id  # Replace this with your target chat ID if required
        approve_all_pending_requests(chat_id)
        bot.reply_to(message, "Approved all pending join requests!")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

# Start the bot
try:
    bot.polling()
except Exception as e:
    print(f"Bot polling failed: {e}")
