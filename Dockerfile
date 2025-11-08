# Use Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set Python unbuffered mode
ENV PYTHONUNBUFFERED=1

# Copy requirements first for better caching
COPY requirements.txt .

# Install git (needed for FastMCP installation) and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y git && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Copy the server code
COPY karen_server.py .
COPY test_karen_server.py .

# Create non-root user
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app

# Switch to non-root user
USER mcpuser

# Run the server
CMD ["python", "karen_server.py"]