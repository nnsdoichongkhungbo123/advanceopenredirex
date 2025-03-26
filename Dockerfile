# Use Python 3.12 slim as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies: git, nano, and system updates
RUN apt update && apt install -y git nano && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && pip install aiohttp tqdm && pip install aiofiles

# Clone the OpenRedireX repository
RUN git clone https://github.com/nnsdoichongkhungbo123/advanceopenredirex.git /app

# Give execution permission to the setup script
RUN chmod +x /app/setup.sh

# Remove "sudo" from setup.sh since Docker runs as root
RUN sed -i 's/sudo //g' /app/setup.sh

# Run the setup script to install dependencies
RUN /app/setup.sh

# Create the directory for live_subdomains.txt
RUN mkdir -p /home/jamesvn

# Create a sample live_subdomains.txt file
RUN touch /home/jamesvn/live_subdomains.txt

# Move live_subdomains.txt to the OpenRedireX directory
RUN mv /home/jamesvn/live_subdomains.txt /app/

# Set the default command to run OpenRedireX
CMD ["python3", "/app/openredirex.py"]









