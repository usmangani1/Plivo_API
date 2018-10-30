FROM python:2.7-slim

WORKDIR /APP
ADD . /APP

# Copy the current directory contents into the container at /app
RUN pip install redis
RUN pip install gunicorn
RUN pip install mysql-connector
RUN pip install flask
RUN pip install requests
RUN pip install flask_restful

#Run app.py when the container launches

CMD ["gunicorn","-w","1","-b","0.0.0.0:5000","APIhandler:app"]

