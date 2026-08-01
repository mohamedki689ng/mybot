import asyncio
import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# توكن بوتك الشخصي المربوط وجاهز
BOT_TOKEN = "8798887487:AAFvcvD9Q18Aq_0v8pcRcapJQkeNRHP2-F8"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "أهلاً بيك يا لو. البوت شغال وجاهز لاستقبال الرابط لتنفيذ الاختبار."
    )


async def frontend_interaction_test(target_url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            ),
        )

        page = await context.new_page()

        try:
            await page.goto(target_url, wait_until="networkidle", timeout=60000)

            share_selectors = [
                "button[data-e2e='share-button']",
                "[aria-label='Share']",
                "button:has-text('Share')",
            ]

            share_clicked = False

            for selector in share_selectors:
                locator = page.locator(selector).first
                try:
                    await locator.wait_for(state="visible", timeout=3000)
                    await locator.click()
                    share_clicked = True
                    break
                except Exception:
                    pass

            if not share_clicked:
                await browser.close()
                return "Share button was not found."

            await page.wait_for_timeout(1500)

            modal_selectors = [
                "[role='dialog']",
                ".modal",
                "[data-testid='modal']",
            ]

            modal_opened = False

            for selector in modal_selectors:
                try:
                    await page.locator(selector).first.wait_for(
                        state="visible",
                        timeout=3000,
                    )
                    modal_opened = True
                    break
                except Exception:
                    pass

            await browser.close()

            if modal_opened:
                return "Frontend interaction test passed and modal opened successfully."
            return "Share button clicked, but no modal detected."

        except PlaywrightTimeoutError:
            await browser.close()
            return "Navigation timed out."

        except Exception as e:
            await browser.close()
            return f"Error: {e}"


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    target_url = update.message.text.strip()

    if not (
        target_url.startswith("http://")
        or target_url.startswith("https://")
    ):
        await update.message.reply_text("يا حب ابعت رابط صحيح يبدأ بـ http:// أو https://")
        return

    await update.message.reply_text("[*] جاري تشغيل الأتمتة وفحص الهدف...")

    result = await frontend_interaction_test(target_url)

    await update.message.reply_text(result)


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("[*] بوت تيليجرام يعمل الآن وجاهز للاستقبال...")
    app.run_polling()


if __name__ == "__main__":
    main()
