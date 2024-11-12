# telesun-tel-bot

آموزش نصب و راه‌اندازی ربات تلگرام با Docker
1. نصب Docker و Docker Compose
نصب Docker
برای نصب Docker دستورهای زیر را وارد کنید:

bash
Copy code
sudo apt update
sudo apt install docker.io
برای اطمینان از اینکه Docker به درستی نصب شده است:

bash
Copy code
sudo docker --version
نصب Docker Compose
برای نصب Docker Compose:

bash
Copy code
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
برای اطمینان از نصب صحیح:

bash
Copy code
docker-compose --version
2. کلون کردن پروژه از GitHub
برای دانلود پروژه از GitHub، ابتدا آن را کلون کنید:

bash
Copy code
git clone https://github.com/Mahtiw/telesun-tel-bot.git
cd telesun-tel-bot
3. تنظیمات ربات تلگرام
تنظیم توکن ربات تلگرام
برای تنظیم توکن ربات تلگرام، به جای 'YOUR_BOT_TOKEN_HERE'، توکن واقعی ربات خود را وارد کنید. به این صورت:

python
Copy code
# توکن ربات
TOKEN = 'YOUR_BOT_TOKEN_HERE'
تنظیم اطلاعات پنل‌ها
برای تنظیم اطلاعات پنل‌ها، آدرس URL و اطلاعات ورودی پنل‌ها را به شکل زیر وارد کنید:

python
Copy code
# اطلاعات پنل‌ها
panels = [
    {"url": "http://s1.example.com:1111/", "username": "user1", "password": "admin1"},
    {"url": "http://s1.example.com:2222/", "username": "user2", "password": "admin2"},
    {"url": "http://s1.example.com:3333/", "username": "user3", "password": "admin3"},
]
در اینجا:

url: آدرس پنل‌ها
username: نام کاربری پنل
password: رمز عبور پنل
این اطلاعات را در فایل login.py تنظیم کنید.

4. اجرای Docker Compose
برای راه‌اندازی ربات از طریق Docker Compose، دستور زیر را اجرا کنید:

bash
Copy code
docker-compose up -d
این دستور تمامی سرویس‌های لازم را راه‌اندازی کرده و ربات را در پس‌زمینه اجرا می‌کند.

5. بررسی وضعیت کانتینرها
برای مشاهده وضعیت کانتینرهای در حال اجرا، از دستور زیر استفاده کنید:

bash
Copy code
docker ps
این دستور لیستی از کانتینرهای در حال اجرا را نمایش می‌دهد.

6. توقف یا ریستارت کانتینرها
برای توقف کانتینرهای در حال اجرا:

bash
Copy code
docker-compose down
برای راه‌اندازی مجدد کانتینرها:

bash
Copy code
docker-compose up -d
نکات تکمیلی
در صورتی که سرور شما ریستارت شود، ربات به صورت خودکار با استفاده از docker-compose راه‌اندازی خواهد شد.
مطمئن شوید که اطلاعات توکن و پنل‌ها را به درستی وارد کرده‌اید تا ربات به درستی کار کند.
