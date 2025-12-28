# Use Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy required files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Command to run the app
CMD ["python", "main.py"]