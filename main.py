import logging
import requests
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

import openai

# مفتاح OpenAI
openai.api_key = "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"

# توكن بوت تيليجرام
BOT_TOKEN = "7560392852:AAGNoxFGThp04qMKTGEiIJN2eY_cahTv3E8"

# إعداد اللوغ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# دالة توليد الرد باستخدام ChatGPT
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "أنت مساعد مالي ذكي متخصص في تحليل الأسهم وتقديم توصيات تداول بناءً على البيانات الفنية."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        reply = f"حدث خطأ أثناء الاتصال بـ GPT: {str(e)}"

    await update.message.reply_text(reply)

# تشغيل البوت
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("البوت شغال يا ذيبان...")
    await app.run_polling()

if __name__ == '__main__':
    import asyncio

    async def run_bot():
        app = Application.builder().token(BOT_TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        print("البوت شغال يا ذيبان...")
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        await app.updater.idle()

    asyncio.run(run_bot())
