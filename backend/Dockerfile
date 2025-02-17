# Use official Python image as base
FROM python:3.12

RUN apt update && apt install -y ffmpeg && rm -rf /var/lib/apt/lists/*
ENV FFMPEG_BINARY="/usr/bin/ffmpeg"
ENV FFPROBE_BINARY="/usr/bin/ffprobe"

# Set working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose port 5000 for Flask
EXPOSE 5005

# Set the entrypoint to run the Flask app
CMD ["python", "app.py"]
