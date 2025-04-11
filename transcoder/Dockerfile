# 🐍 Use Python 3.11 slim base image
FROM python:3.11-slim

# 🎵 Install ffmpeg for audio processing
# Update apt and install ffmpeg, then clean up to reduce image size
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean && rm -rf /var/lib/apt/lists/*

# 📂 Set working directory
WORKDIR /app

# 📄 Copy requirements file
COPY requirements.txt .

# 📦 Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 📂 Copy application code
COPY . .

# 🚀 Run the application
CMD ["python", "main.py"]
