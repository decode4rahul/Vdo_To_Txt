from pyrogram import Client, filters
import os
import asyncio

# Bot Configuration
API_ID = "23303701"
API_HASH = "17ee05da4127078430e807b73865d1e2"
BOT_TOKEN = "7773494703:AAEiEZIP9nuuJokaNnxzpYc_j6NXgvu8PIA"
CHANNEL_ID = "@combobyfamous"  # Channel where videos will be backed up

# Initialize Bot
bot = Client("video_to_audio_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

print("Bot is running...")

# Send welcome message when bot starts
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("👋 Hello! Send me a video, and I'll extract the audio for you. 🎵")

# Function to Convert Video to Audio
def convert_video_to_audio(video_path, output_path):
    print("Converting video to audio...")
    os.system(f"ffmpeg -i {video_path} -q:a 0 -map a {output_path} -y")
    print("Conversion complete.")
    return output_path

# Handler for Video Messages
@bot.on_message(filters.video)
async def video_handler(client, message):
    print("Video received.")
    video = message.video
    file_id = video.file_id
    video_size = round(video.file_size / (1024 * 1024), 2)  # Convert size to MB
    
    # Notify user
    msg = await message.reply("📥 Video received! Downloading... ⏳")
    
    # Forward video to backup channel
    await message.forward(CHANNEL_ID)
    print("Video forwarded to backup channel.")
    
    # Download video file
    print("Downloading video...")
    video_path = await client.download_media(file_id)
    print("Video downloaded.")
    
    # Extract original filename if available, otherwise use downloaded filename
    # video_name = video.file_name if video.file_name else os.path.basename(video_path)  # Commented out
    
    audio_path = "Weather.mp3"  # Set extracted audio name to Weather.mp3
    
    # Update message to extraction step
    await msg.edit("🎛 Extracting audio from video... ⏳")
    convert_video_to_audio(video_path, audio_path)
    
    # Get extracted audio size
    audio_size = round(os.path.getsize(audio_path) / (1024 * 1024), 2)  # Convert to MB
    
    # Send the extracted audio to the user
    print("Sending audio to user...")
    audio_msg = await message.reply_audio(audio_path, caption=f"🎥 Video Size: {video_size} MB\n💾 Audio Size: {audio_size} MB")
    print("Audio sent.")
    
    # Update message to success
    await msg.delete()
    
    # Delete the files to save storage
    print("Deleting temporary files...")
    os.remove(video_path)
    os.remove(audio_path)
    print("Temporary files deleted.")
    
    # Send thank-you message
    thank_you_msg = await message.reply("🙏 Thank you for using this bot! 😊✨ Enjoy your extracted audio! 🎧")
    
    # Wait for 3-4 seconds before sending sticker
    await asyncio.sleep(3)
    
    # Send sticker after thank-you message
    sticker_msg = await message.reply_sticker("CAACAgUAAxkBAAIB02erXfP4pyRWV8NiAwJ8pBbk4LfsAAIQAQACtAEULTZXx-tOGZnuHgQ")
    
    # Delete sticker and thank-you message after 1-2 minutes
    await asyncio.sleep(90)  # 90 seconds (1.5 minutes)
    await sticker_msg.delete()
    await thank_you_msg.delete()
    print("Sticker and thank-you message deleted.")

# Handler for Non-Video Messages
@bot.on_message(filters.text)
async def text_handler(client, message):
    await message.reply("❌ I only process videos! Please send me a video to extract audio. 🎥")

# Handler for Stickers (to get sticker file_id)
@bot.on_message(filters.sticker)
async def sticker_handler(client, message):
    await message.reply(f"🆔 Sticker ID: `{message.sticker.file_id}`")

bot.run()
