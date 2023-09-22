FROM python:3.11.2-slim

ENV TZ=Europe/Istanbul

WORKDIR /app

COPY . /app/

RUN apt-get update && apt-get install -y nginx

COPY requirements.txt .

RUN pip3 install -r requirements.txt


COPY . .




#Expose the port on which Gunicorn will run
EXPOSE 8000

#CMD [ "python3", "main.py" ]
#Command to start Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]
