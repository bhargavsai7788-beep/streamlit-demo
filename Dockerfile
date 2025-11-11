# Start from a slim Python base image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy your app's code into the container
COPY app.py .

# Expose the port Streamlit runs on
EXPOSE 8501

# The command to run your app
# This uses the standard command to run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]