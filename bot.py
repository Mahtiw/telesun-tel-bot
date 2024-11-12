import json
from datetime import datetime
import jdatetime  # اضافه کردن کتابخانه jdatetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from Login import save_accounts_to_json

TOKEN = '7790482812:AAG9W_kVlZ13drEf911zoHmF6EmRZ9chCsE'

def bytes_to_human_readable(bytes_value):
    """تبدیل بایت به واحد مناسب (گیگابایت یا مگابایت)."""
    if bytes_value >= (1024 * 1024 * 1024):  # اگر بیشتر از 1 گیگابایت باشد
        return f"{bytes_value / (1024 * 1024 * 1024):.2f} GB"  # به گیگابایت
    elif bytes_value >= (1024 * 1024):  # اگر بیشتر از 1 مگابایت باشد
        return f"{bytes_value / (1024 * 1024):.2f} MB"  # به مگابایت
    else:  # اگر کمتر از 1 مگابایت باشد
        return f"{bytes_value / 1024:.2f} KB"  # به کیلوبایت

# فایل JSON که داده‌ها در آن قرار دارد
json_file = 'data.json'

# تابعی برای جستجوی کاربر بر اساس ایمیل
def get_user_info(email):
    with open(json_file, 'r') as f:
        data = json.load(f)

    for panel, users in data.items():
        for user in users:
            for client in user['clientStats']:
                if client['email'] == email:
                    up_size = client['up']
                    down_size = client['down']
                    total_size = client['total']  # حفظ مقدار به بایت
                    
                    # محاسبه مجموع دانلود و آپلود
                    total_download_upload_size = up_size + down_size  # مجموع

                    # تبدیل expiryTime به تاریخ شمسی یا نمایش "نامحدود" در صورت صفر یا منفی بودن
                    expiry_time_ms = client['expiryTime']  # میلی‌ثانیه
                    if expiry_time_ms <= 0:
                        expiry_time_str = "نامحدود"
                    else:
                        expiry_time = datetime.utcfromtimestamp(expiry_time_ms / 1000)  # تبدیل به ثانیه
                        expiry_time_jalali = jdatetime.datetime.fromgregorian(datetime=expiry_time)  # تبدیل به شمسی
                        expiry_time_str = expiry_time_jalali.strftime('%Y/%m/%d %H:%M:%S')  # فرمت تاریخ به شمسی

                    # تغییر وضعیت true/false به تیک سبز و قرمز
                    status_text = "✅ فعال" if client['enable'] else "❌ غیرفعال"

                    # ساخت دکمه‌ها برای نمایش در کادر
                    keyboard = [
                        [InlineKeyboardButton(f"✨ پنل: {panel}", callback_data='panel')],
                        [InlineKeyboardButton(f"👤 کاربر: {email}", callback_data='user')],
                        [InlineKeyboardButton(f"⬆️ آپلود: {bytes_to_human_readable(up_size)}", callback_data='upload')],
                        [InlineKeyboardButton(f"⬇️ دانلود: {bytes_to_human_readable(down_size)}", callback_data='download')],
                        [InlineKeyboardButton(f"📊 مجموع دانلود و آپلود: {bytes_to_human_readable(total_download_upload_size)}", callback_data='total')],
                        [InlineKeyboardButton(f"{status_text}", callback_data='status')],  # وضعیت با تیک سبز یا قرمز
                        [InlineKeyboardButton(f"⏳ تاریخ انقضا: {expiry_time_str}", callback_data='expiry')],
                        [InlineKeyboardButton(f"💾 مجموع: {bytes_to_human_readable(total_size)}", callback_data='total_size')]
                    ]

                    reply_markup = InlineKeyboardMarkup(keyboard)

                    return reply_markup  # بازگرداندن کادر اطلاعاتی

    return None  # اگر کاربر یافت نشد

# هندلر دستور start
async def start(update: Update, context) -> None:
    await update.message.reply_text('👋 خوش آمدید! ایمیل خود را ارسال کنید تا اطلاعات کاربر را دریافت کنید.')

# هندلر پیام‌های کاربر
async def handle_message(update: Update, context) -> None:
    email = update.message.text

    # فراخوانی save_accounts_to_json برای به‌روزرسانی اطلاعات پنل‌ها
    save_accounts_to_json()

    # جستجوی کاربر بر اساس ایمیل
    user_info_markup = get_user_info(email)

    if user_info_markup:
        # نمایش نتیجه به کاربر
        await update.message.reply_text('🔍 اطلاعات کاربر:', reply_markup=user_info_markup)
    else:
        await update.message.reply_text("❌ *کاربر یافت نشد*")

# تنظیمات اصلی ربات
def main():
    # ساخت اپلیکیشن ربات با استفاده از Application.builder()
    application = Application.builder().token(TOKEN).build()

    # اضافه کردن هندلرها
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # اجرای ربات
    application.run_polling()

if __name__ == '__main__':
    main()
