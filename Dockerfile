# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Set the working directory to /feeder-bot
WORKDIR /feeder-bot

# Copy the current directory contents into the container at /feeder-bot
COPY . /feeder-bot

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

# Run arixv_twitter.py when the container launches
CMD ["-u", "arxiv_twitter.py"]
