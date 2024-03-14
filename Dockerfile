# Use the official Python image with Uvicorn and Gunicorn
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Set the working directory inside the container
WORKDIR /app

ENV PYTHONPATH=/app

# Copy the application code into the container
COPY ./src /app

# Install dependencies (if you have a requirements.txt file)
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose port 8000 (the default port used by FastAPI)
EXPOSE 8000

# Command to start the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
