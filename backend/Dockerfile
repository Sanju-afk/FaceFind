# 1. Use Python 3.10 slim as the base
FROM python:3.10-slim

# 2. Set the working directory
WORKDIR /app

# 3. Install system dependencies
# Added 'g++' and 'build-essential' in case any AI libraries need to compile C++ extensions
# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
# 4. Create the professional temp directory
# This ensures the folder exists and has the right permissions before the app starts [cite: 199, 227]
RUN mkdir -p /tmp/facefind && chmod 777 /tmp/facefind

# 5. Copy requirements and install them
# Keeping this separate from 'COPY . .' leverages Docker's cache for faster builds
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application [cite: 10]
COPY . .

# 7. Expose the port FastAPI runs on
EXPOSE 8000

# 8. Optimized Command to run the application
# Added '--proxy-headers' for when you eventually use NGINX in Phase 5 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]