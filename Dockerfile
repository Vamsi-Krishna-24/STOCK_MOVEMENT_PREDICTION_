# Use an official Python runtime as a parent image
FROM python:3.8

# Copy the requirements file into the container at /app
COPY . /app

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt


# Expose port 8501 to the outside world
EXPOSE 8501

# Command to run the application
CMD streamlit run --server.host 0.0.0.0 app.py

