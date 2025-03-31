# Use an official lightweight Python image as base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only necessary files
COPY requirements.txt .
COPY app.py .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose the port for Chainlit
EXPOSE 8000

# Run the Chainlit app
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]
