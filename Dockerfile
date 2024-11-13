FROM python:3.9-slim

EXPOSE 8000

# Set working directory
WORKDIR /app

# Installing dependencies
COPY app/packages.txt .
RUN pip install --no-cache-dir -r packages.txt

# Copy the application code
COPY app .

# Run the application with Gunicorn
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]