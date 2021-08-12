FROM python:3.7-alpine
RUN python3.7 -m pip install --upgrade pip
#copy the package files to the container and then move into the direcotry

COPY . /dentalservice
WORKDIR /dentalservice

RUN python3.7 -m pip install -r requirements.txt

#open port 5000 for external communication
EXPOSE 8888

#run our service
WORKDIR /dentalservice/demo
ENTRYPOINT ["python3.7"]
CMD ["__init__.py"]
