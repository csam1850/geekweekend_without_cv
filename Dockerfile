FROM python:3.7.5

WORKDIR /application

LABEL maintainer="geekweekend" 

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /application

ENV FLASK_APP app.py

EXPOSE 5000

CMD [ "python", "app.py" ]


# run following commands in command prompt
# docker build -t classifier .
# docker run -d -p 5000:5000 classifier
