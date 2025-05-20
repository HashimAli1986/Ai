import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# إعداد المفاتيح
openai.api_key = "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"
BOT_TOKEN = "7560392852:AAGNoxFGThp04qMKTGEiIJN2eY_cahTv3E8"

# إعداد اللوغات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# دالة التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.effective_user.id

    if len(user_message) > 500:
        await update.message.reply_text("❗ الرجاء إرسال رسالة لا تتجاوز 500 حرف.")
        return

    logger.info(f"المستخدم {user_id} سأل: {user_message[:100]}...")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "أنت مساعد مالي خبير في تحليل الأسهم وتوصيات التداول."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message["content"]
    except Exception as e:
        logger.error(f"خطأ أثناء استدعاء OpenAI: {e}")
        reply = "حدث خطأ تقني. يرجى المحاولة مرة أخرى لاحقًا."

    await update.message.reply_text(reply)

# الدالة الرئيسية لتشغيل البوت
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("البوت شغال يا ذيبان...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
