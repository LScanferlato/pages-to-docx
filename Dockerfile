FROM python:3.11-slim

# Install LibreOffice
RUN apt-get update && \
    apt-get install -y libreoffice && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Create upload folder
RUN mkdir -p /tmp/uploads

# Expose port
EXPOSE 5000

CMD ["python", "app.py"]

