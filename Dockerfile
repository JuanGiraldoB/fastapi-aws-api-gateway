# Use the official Python image with Uvicorn and Gunicorn
FROM public.ecr.aws/lambda/python:3.12


# Set the working directory inside the container
WORKDIR /app

ENV PYTHONPATH=/app

# Copy the application code into the container
COPY ./src /app

# Install dependencies (if you have a requirements.txt file)
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# ENV HOST="0.0.0.0"
# ENV PORT=8000
# ENTRYPOINT uvicorn api.main:app --host ${HOST} --port ${PORT}
# Command to start the application
# CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["api.main.handler"]
