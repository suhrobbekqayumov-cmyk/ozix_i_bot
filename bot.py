import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import google.generativeai as genai
from aiohttp import web

# --- KONFIGURATSIYA ---
API_TOKEN = "8784506881:AAE9KLEePUzstvg4RG8I6ibslbJ16QqTdnM"
GOOGLE_API_KEY = "AIzaSyB_qVuPSw9c0Mo4P6oE00dDxoGpL1F03-4"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def handle(request):
    return web.Response(text="Bot is Live!")

@dp.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer("Salom! Yangi botingiz muvaffaqiyatli ishga tushdi! 🚀")

@dp.message()
async def ai_msg(msg: types.Message):
    try:
        res = model.generate_content(msg.text)
        await msg.answer(res.text)
    except:
        await msg.answer("Xatolik bo'ldi, qayta urinib ko'ring.")

async def main():
    logging.basicConfig(level=logging.INFO)
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
