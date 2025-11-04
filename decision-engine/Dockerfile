# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Run Flask app
CMD ["python", "main.py"]
