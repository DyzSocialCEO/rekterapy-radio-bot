import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped

# Bot configuration
API_ID = int(os.environ.get("API_ID", "6"))
API_HASH = os.environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID"))
STREAM_URL = os.environ.get("STREAM_URL")

# Initialize bot
app = Client(
    "radio_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Initialize PyTgCalls
pytgcalls = PyTgCalls(app)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "🎵 **RekTerapy Radio Bot**\n\n"
        "Commands:\n"
        "• `/play` - Start radio stream\n"
        "• `/stop` - Stop radio stream\n"
        "• `/status` - Check stream status"
    )

@app.on_message(filters.command("play"))
async def play_radio(client, message):
    try:
        await pytgcalls.join_group_call(
            CHAT_ID,
            AudioPiped(STREAM_URL)
        )
        await message.reply_text("🎵 **Radio started!** Now streaming RekTerapy Radio")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command("stop"))
async def stop_radio(client, message):
    try:
        await pytgcalls.leave_group_call(CHAT_ID)
        await message.reply_text("⏹️ **Radio stopped**")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command("status"))
async def radio_status(client, message):
    try:
        is_playing = pytgcalls.is_connected(CHAT_ID)
        status = "🟢 **Playing**" if is_playing else "🔴 **Stopped**"
        await message.reply_text(f"📻 **Radio Status:** {status}")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}")

async def main():
    await app.start()
    await pytgcalls.start()
    print("🎵 Radio bot started successfully!")
    await pytgcalls.idle()

if __name__ == "__main__":
    asyncio.run(main())
