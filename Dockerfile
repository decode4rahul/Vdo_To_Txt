# Use an official Python image as a base
FROM python:3.10

# Install FFmpeg
RUN apt update && apt install -y ffmpeg

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "bot.py"]
