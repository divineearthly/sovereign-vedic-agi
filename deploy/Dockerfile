FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN pip install torch numpy fastapi uvicorn

# Copy Vedic AGI
COPY vedic_agi /app/vedic_agi
COPY setup.py /app/

# Install package
RUN pip install -e .

# Expose API port
EXPOSE 8000

# Start server
CMD ["python", "-m", "vedic_agi.applications.api"]
