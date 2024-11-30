from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

# Initialize the bot with the token
bot = TeleBot("7207023522:AAHhYRF4EKT8ZcaX2IdmUmy2X7kzZ5D8OUc")

# Handle the /start command to show the bot is alive
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "✅ Bot is up and running!")

# Handle chat join requests
@bot.message_handler(func=lambda message: hasattr(message, 'chat_join_request'))
def handle_join_requests(message):
    # Extract chat ID and user ID from the join request
    chatid = message.chat_join_request.chat.id
    userid = message.chat_join_request.from_user.id
    
    # Approve the join request using Telegram's API
    response = requests.post(
        f"https://api.telegram.org/bot{bot.token}/approveChatJoinRequest", 
        json={"chat_id": chatid, "user_id": userid}
    )

    # Check if the request was successful
    if response.status_code == 200:
        # Create an inline keyboard markup with a button for the developer
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="⚙️Tᴇᴀᴍ sᴀᴛ ✨🤍", url="https://t.me/Team_SAT_25"))
        
        # Send a welcome photo with the message to the user
        bot.send_photo(
            chat_id=userid,
            photo='https://envs.sh/wVy.jpg',
            caption='''Your Channel Joining Request Accepted\n\nThanks For Joining Our Channel ❤️''',
            reply_markup=markup,
            parse_mode='HTML'
        )
    else:
        print(f"Failed to approve join request: {response.text}")

# Start the bot
bot.polling()
