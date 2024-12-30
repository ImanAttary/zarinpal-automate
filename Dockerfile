FROM selenium/standalone-chrome:131.0-chromedriver-131.0


USER root
WORKDIR /app

# اطمینان از نصب pip
RUN apt-get update && apt-get install -y python3-pip


# کپی و نصب وابستگی‌ها
COPY ./requirements.txt /app/requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt --break-system-packages

# کپی کد به داکر
COPY . .
RUN chmod +x /app/betaPanel/

# اضافه کردن مجوز اجرا به اسکریپت
RUN chmod +x /app/run_tests.sh


# دستور پیش‌فرض برای اجرای تست‌ها
CMD [ "/bin/bash", "-c", "./run_tests.sh" ]