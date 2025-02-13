import json
from datetime import datetime
import jdatetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from login import save_accounts_to_json, TOKEN

def bytes_to_human_readable(bytes_value):
    if bytes_value >= (1024 * 1024 * 1024):
        return f"{bytes_value / (1024 * 1024 * 1024):.2f} GB"
    elif bytes_value >= (1024 * 1024):
        return f"{bytes_value / (1024 * 1024):.2f} MB"
    else:
        return f"{bytes_value / 1024:.2f} KB"

json_file = 'data.json'

def get_user_info(email):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)

        for panel, users in data.items():
            for user in users:
                for client in user['clientStats']:
                    if client['email'] == email:
                        up_size = client['up']
                        down_size = client['down']
                        total_size = client['total']
                        
                        total_download_upload_size = up_size + down_size
                        remaining_size = total_size - total_download_upload_size if total_size > total_download_upload_size else 0

                        expiry_time_ms = client['expiryTime']
                        if expiry_time_ms <= 0:
                            expiry_time_str = "نامحدود"
                        else:
                            expiry_time = datetime.utcfromtimestamp(expiry_time_ms / 1000)
                            expiry_time_jalali = jdatetime.datetime.fromgregorian(datetime=expiry_time)
                            expiry_time_str = expiry_time_jalali.strftime('%Y/%m/%d %H:%M:%S')

                        status_text = "✅ فعال" if client['enable'] else "❌ غیرفعال"

                        keyboard = [
                            [InlineKeyboardButton(f"✨ پنل: {panel}", callback_data='panel')],
                            [InlineKeyboardButton(f"👤 کاربر: {email}", callback_data='user')],
                            [InlineKeyboardButton(f"⬆️ آپلود: {bytes_to_human_readable(up_size)}", callback_data='upload')],
                            [InlineKeyboardButton(f"⬇️ دانلود: {bytes_to_human_readable(down_size)}", callback_data='download')],
                            [InlineKeyboardButton(f"📊 مجموع دانلود و آپلود: {bytes_to_human_readable(total_download_upload_size)}", callback_data='total')],
                            [InlineKeyboardButton(f"📉 باقیمانده: {bytes_to_human_readable(remaining_size)}", callback_data='remaining')],
                            [InlineKeyboardButton(f"💾 حجم کل: {bytes_to_human_readable(total_size)}", callback_data='total_size')],
                            [InlineKeyboardButton(f"{status_text}", callback_data='status')],
                            [InlineKeyboardButton(f"⏳ تاریخ انقضا: {expiry_time_str}", callback_data='expiry')]
                        ]

                        reply_markup = InlineKeyboardMarkup(keyboard)

                        return reply_markup

        return None
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

async def start(update: Update, context) -> None:
    await update.message.reply_text('👋 خوش آمدید! ایمیل خود را ارسال کنید تا اطلاعات کاربر را دریافت کنید.')

async def handle_message(update: Update, context) -> None:
    email = update.message.text

    # Save accounts to JSON
    save_accounts_to_json()

    # Get user info
    user_info_markup = get_user_info(email)

    if user_info_markup:
        await update.message.reply_text('🔍 اطلاعات کاربر:', reply_markup=user_info_markup)
    else:
        await update.message.reply_text("❌ *کاربر یافت نشد*")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
