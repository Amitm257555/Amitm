import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your token and admin ID
TOKEN = '7660912209:AAEDIP4-zQJXvomFwqSby5MFAOHZtG8KkD0'  # Add your bot token here
ADMIN_USER_ID = 5239817533  # Add your admin user ID here

# States for ConversationHandler
IP_PORT, CONFIRM_ATTACK = range(2)

# Dictionary to store user attack details
user_attack_details = {}

# Start command
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id == ADMIN_USER_ID:
        reply_keyboard = [['😎 Save Attack', '🚀 Start Attack', '🛑 Stop Attack']]
        update.message.reply_text(
            'Welcome, Admin! Choose an option:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
    else:
        update.message.reply_text('You are not authorized to use this bot.')

# Save Attack command
def save_attack(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please enter the target IP and port in this format: `IP PORT`')
    return IP_PORT

# Function to save IP and Port
def receive_ip_port(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    text = update.message.text
    try:
        ip, port = text.split()
        user_attack_details[user_id] = {'ip': ip, 'port': port}
        update.message.reply_text(f'Target IP and Port saved as: {ip} {port}')
        return CONFIRM_ATTACK
    except ValueError:
        update.message.reply_text('Invalid format. Please enter the IP and port again.')
        return IP_PORT

# Start Attack command
def start_attack(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in user_attack_details:
        ip = user_attack_details[user_id]['ip']
        port = user_attack_details[user_id]['port']
        update.message.reply_text(f'Attack started on {ip}:{port}!')
        # Add your attack-starting logic here
    else:
        update.message.reply_text('No IP and port saved. Use the "😎 Save Attack" option first.')

# Stop Attack command
def stop_attack(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in user_attack_details:
        ip = user_attack_details[user_id]['ip']
        port = user_attack_details[user_id]['port']
        update.message.reply_text(f'Attack stopped on {ip}:{port}!')
        # Add your attack-stopping logic here
    else:
        update.message.reply_text('No attack in progress to stop.')

# Cancel command to stop the conversation
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

# Main function to run the bot
def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Conversation handler to handle saving IP and port
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('😎 Save Attack'), save_attack)],
        states={
            IP_PORT: [MessageHandler(Filters.text & ~Filters.command, receive_ip_port)],
            CONFIRM_ATTACK: [MessageHandler(Filters.regex('🚀 Start Attack'), start_attack)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)

    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.regex('🚀 Start Attack'), start_attack))
    dispatcher.add_handler(MessageHandler(Filters.regex('🛑 Stop Attack'), stop_attack))

    # Start polling for updates
    updater.start_polling()
    
    # Idle to keep the bot running
    updater.idle()

if __name__ == '__main__':
    main()
