# Use lightweight Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose ports
EXPOSE 5000
EXPOSE 7860

# Start both services
CMD ["sh", "-c", "python backend/auth/auth_server.py & python backend/dashboard.py"]