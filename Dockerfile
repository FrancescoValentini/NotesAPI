
FROM python:3.12-slim

# Prevent Python from writing bytecode and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and database directory
RUN groupadd --system appgroup \
    && useradd --system --gid appgroup --create-home appuser \
    && mkdir -p /app/data \
    && chown -R appuser:appgroup /app

# Copy application source with correct ownership
COPY --chown=appuser:appgroup . .

# Application port
EXPOSE 8000

# Switch to non-root user
USER appuser

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
