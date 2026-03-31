# Use Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run API
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]