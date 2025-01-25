FROM selenium/standalone-chrome:latest

# Switch to root for package installation
USER root

# Install Python and pip
RUN sudo apt-get update && sudo apt-get install -y python3 python3-pip

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Copy application code
COPY . .

CMD ["python3", "-m", "src.driver"]