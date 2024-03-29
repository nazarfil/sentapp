# Use an official Python runtime as an image
FROM python:3.9

# The EXPOSE instruction indicates the ports on which a container 
# will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it
EXPOSE 5000

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this instruction 
# creates a directory with this name if it doesn’t exist
WORKDIR /sentapp

# Install any needed packages specified in requirements.txt
COPY app /sentapp/app
COPY requirements.txt /sentapp
COPY wsgi.py /sentapp
COPY static /sentapp
RUN pip3 install -r requirements.txt

# Run app.py when the container launches
CMD gunicorn --worker-connections=1000 --workers=1 wsgi:app --threads 2 -b 0.0.0.0:5000