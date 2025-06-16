FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY . .

# Expose default Chainlit port
EXPOSE 7860

# Start Chainlit
CMD ["chainlit", "run", "main.py", "--host", "0.0.0.0", "--port", "7860"]
