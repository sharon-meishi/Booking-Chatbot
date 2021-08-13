# Booking-Chatbot
## A dental clinic system using a chatbot and dockerized services

# Introduction
This is an assignment for COMP9322 in UNSW. Following is the usage instruction of the dental chatbot service. The chatbot will help you to book a appointment with your selected dentist for tomorrow.\

**Chatbot implementation**: ML-based chatbot with wit\
**Frontend template references**: https://codepen.io/lilgreenland/pen/pyVvqB\
**Database**:SQLite

*'Frontend' and 'Backend' folder are under constrtuction, please ignore, a new interface built with React framework is coming*

# Start Chatbot Service
Open **dentalchatbot** and run the following command code inside the folder
```
python3 -m pip install -r requirements.txt
python3 chatbot.py
```
# Start Dental Service
Open **dentalservice** and run the following command code inside the folder
### Docker
```
# build the dentalservice image
docker build -t dentalservice .
# run dentalservice image
docker run -p 8888:8888 dentalservice
```
### Or
Open **dentalservice/demo** and run the following command code inside the folder
```
python3 __init__.py 
```

# Start Timeslot Service
Open **timeslotservice** and run the following command code inside the folder
### Docker
```
# build the timeslotservice image
docker build -t timeslotservice .
# run timeslotservice image
docker run -p 5555:5555 timeslotservice
```
### Or
Open **timeslotservice/demo** and run the following command code inside the folder
```
python3 __init__.py 
```

# Usage
Open your browser and go to http://127.0.0.1:8000/, you will see a page contains a chatbot. \
You can chat with bot for basic greeting eg. Hi/How are you, or type anything to start, the chatbot will ask for your name, and you can ask the bot **'what is my name'** if you firget the username you set.\
To see a detail user manual, please check **booking-chatbot-manual.pdf**

