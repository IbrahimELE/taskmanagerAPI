# Use the official Python base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file for dependency installation
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the application files (excluding requirements.txt)
COPY . .

# Expose the application port
EXPOSE 8000

# Set the default command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
