
# Use Python 3.9 as the base image
FROM python:3.9-slim

# Make scripts available on PATH
ENV PATH="/scripts:${PATH}"

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python -m pip install --upgrade pip

# Copy and install Python dependencies
COPY ./requirements.txt /requirements.txt
RUN python -m pip install --no-cache-dir -r /requirements.txt

# Create application directory
RUN mkdir -p /app

# Copy application files
COPY ./SyntheticData /app
WORKDIR /app

# Copy scripts
COPY ./scripts /scripts
RUN chmod +x /scripts/*

# Create a non-root user
RUN groupadd -r user && \
    useradd -r -g user user && \
    chown -R user:user /app

# Run as non-root user
USER user

# Expose application port
EXPOSE 8000

# Start the application
ENTRYPOINT ["entrypoint.sh"]
