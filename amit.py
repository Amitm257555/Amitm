from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Bot ka Token jo aapko BotFather se mila
TOKEN = '7660912209:AAEDIP4-zQJXvomFwqSby5MFAOHZtG8KkD0'

# Admin user ID ko define karein
ADMIN_USER_ID = 5239817533  # Isse apne Telegram user ID se replace karein

# User data structure
user_data = {}

# Command for /start
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_data:
        update.message.reply_text("Please authenticate with admin to use this bot.")
    else:
        reply_text = (
            "Welcome! Choose an option:\n"
            "1. Save Attack\n"
            "2. Start Attack\n"
            "3. Stop Attack"
        )
        update.message.reply_text(reply_text)

# Command for adding user by admin
def add_user(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_USER_ID:
        if len(context.args) == 1:
            user_id = int(context.args[0])
            user_data[user_id] = {'ip': None, 'port': None}
            update.message.reply_text(f'User with ID {user_id} added successfully!')
        else:
            update.message.reply_text('Usage: /add6023 <user_id>')
    else:
        update.message.reply_text('You are not authorized to add users!')

# Command for saving attack details
def save_attack(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in user_data:
        update.message.reply_text("Please enter the target IP and port in this format: `IP PORT`")
    else:
        update.message.reply_text("You need to authenticate first.")

# Save IP and Port
def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in user_data:
        # Split the message into IP and PORT
        try:
            ip, port = update.message.text.split()
            user_data[user_id]['ip'] = ip
            user_data[user_id]['port'] = port
            update.message.reply_text(f'Target IP and Port saved as: {ip} {port}')
        except ValueError:
            update.message.reply_text("Invalid format! Please enter in `IP PORT` format.")
    else:
        update.message.reply_text("You need to authenticate first.")

# Start Attack Command
def start_attack(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in user_data:
        ip = user_data[user_id]['ip']
        port = user_data[user_id]['port']
        if ip and port:
            update.message.reply_text(f'Attack started on {ip}:{port}')
            # Yahan aap apna attack start karne ka code likh sakte hain
        else:
            update.message.reply_text("You need to save target IP and port first.")
    else:
        update.message.reply_text("You need to authenticate first.")

# Stop Attack Command
def stop_attack(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in user_data:
        ip = user_data[user_id]['ip']
        port = user_data[user_id]['port']
        if ip and port:
            update.message.reply_text(f'Attack stopped on {ip}:{port}')
            # Yahan aap apna attack stop karne ka code likh sakte hain
        else:
            update.message.reply_text("No attack is running. Save IP and port first.")
    else:
        update.message.reply_text("You need to authenticate first.")

def main():
    # Bot ke liye Updater ka setup
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('add6023', add_user))
    dp.add_handler(CommandHandler('save_attack', save_attack))
    dp.add_handler(CommandHandler('start_attack', start_attack))
    dp.add_handler(CommandHandler('stop_attack', stop_attack))

    # Message handler for saving IP and port
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Bot ko polling mode me start karna
    updater.start_polling()

    # Bot ko chalu rakhna
    updater.idle()

if __name__ == '__main__':
    main()