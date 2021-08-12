FROM python:3.7-alpine
RUN python3.7 -m pip install --upgrade pip
#copy the package files to the container and then move into the direcotry

COPY . /timeslotservice
WORKDIR /timeslotservice

RUN python3.7 -m pip install -r requirements.txt

#open port 5000 for external communication
EXPOSE 5555

#run our service
WORKDIR /timeslotservice/demo
ENTRYPOINT ["python3.7"]
CMD ["__init__.py"]
