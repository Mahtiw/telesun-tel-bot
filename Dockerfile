# انتخاب تصویر پایه
FROM python:3.9

# تنظیم پوشه کار
WORKDIR /app

# کپی کردن فایل‌های پروژه به کانتینر
COPY . .

# نصب وابستگی‌ها
RUN pip install --no-cache-dir -r requirements.txt

# اجرای فایل bot.py به عنوان برنامه اصلی
CMD ["python3", "bot.py"]
