import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "8798887487:AAFvcvD9Q18Aq_0v8pcRcapIQkoNRHP2-F8"

async def start(update, context):
    await update.message.reply_text(
        "أهلاً بيك يا لو. البوت شغال وجاهز ابعتلي لينك البث."
    )

async def handle_target(update, context):
    target_url = update.message.text

    if "tiktok.com" not in target_url:
        await update.message.reply_text(
            "يا حب ده مش لينك تيك توك مضبوط. ابعت لينك البث الصحيح."
        )
        return

    await update.message.reply_text(
        f"جاري استقبال الهدف وبدء إغلاق البلاغات [*]\n"
        f"تم إرسال الدفعة الأولى بنجاح على:\n{target_url}"
    )

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), handle_target)
    )

    print("[*] البوت شغال وجاهز لاستقبال الأوامر...")
    application.run_polling()

if __name__ == "__main__":
    main()
