from flask import Flask, render_template, request, globals
import requests
from rivescript import RiveScript
import json
import os
import datetime

date = datetime.date.today() + datetime.timedelta(days=1)
tmr = date.strftime('%m/%d/%Y')

bot = RiveScript() 
bot.load_directory(os.getcwd()+'/brain')
bot.sort_replies()

app = Flask(__name__,static_folder='')
app.secret_key = 'secret_key'

name_flag = False

@app.route('/')
def index():
    global name_flag
    name_flag = False
    return render_template('index.html')

def ConfirmBooking(dentist_name, client_name, time):
    time = int(time.split(":")[0])
    body = {"dentist_name": dentist_name, "time": time, "client_name" : client_name}
    url = 'http://127.0.0.1:5555/v1/timeslots/dental/reserve'
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, data=json.dumps(body), headers=headers)
    data = r.json()
    if r.status_code == 201:
        reply = f"Thank you {data['client_name']}, your appointment with <b>{data['dentist_name']}</b> for {tmr} at {data['time']}:00 has been confirmed.\
                Your booking id is: <b> {data['booking_id']} </b>, to cancel this appointment, type <em>cancel booking {data['booking_id']}</em>"
    elif r.status_code == 400:
        reply = f"This timeslot is already booked by another appointment, please select another timeslot or check {dentist_name} available timeslot\
                    by typing: <em> check {dentist_name} timetable.</em> etc."
    else:
        reply = "The timeslot or doctor you want to book is not exist, please select another timeslot"
    return reply

def ConfirmCancel(booking_id):
    url = f'http://127.0.0.1:5555/v1/timeslots/dental/cancel?booking_Id={booking_id}'
    r = requests.put(url)
    data = r.json()
    if r.status_code == 201:
        reply = f"Thank you {data['client_name']}, your appointment with <b>{data['dentist_name']}</b> for {tmr} at {data['time']}:00 has been canceled."
    elif r.status_code == 400:
        reply = 'The appointment has already been canceled before'
    else:
        reply = 'The appointment you want to cancel is not exist, please enter another booking id'
    return reply


def ask_wit(msg):

    Token = 'ORBW3DUSZ65HZ4HCEWXELY73HSRFWSGQ'
    headers = {'Authorization': 'Bearer '+ Token}
    url = f'https://api.wit.ai/message?v=20201115&q={msg}'

    reply = requests.get(url, headers = headers)
    data = reply.json()
    try:
        intent = data['intents'][0]['name']
        if intent == 'ListAllDentist':
            # list all available doctors in the clinic and the client can choose
            url = f"http://127.0.0.1:8888/v1/dentists"
            reply = requests.get(url)
            if reply.status_code == 200:
                data = reply.json()
                reply = 'All the dentists in our clinic are listed below: <br>\
                        <table> <tr> <th>Dentist name</th>\
                            <th>Location</th>\
                            <th>Specialization</th></tr>'
                for i in data:
                    reply += '<tr>'
                    reply += '<td>' + i['name'] + '</td>'
                    reply += '<td>' + i['location'] + '</td>'
                    reply += '<td>' + i['specialization'] + '</td>'
                    reply += '</tr>'
                reply += '</table>To know more information about the Doctor, please type: <em>Information about dr.sharon </em>' 
            elif reply.status_code == 500:
                reply = 'Server has some problem, please wait'
            else:
                reply = 'url not correct'
        elif intent == 'GetTheDentist':
            # ask the client for the preferred doctor and provide information about the doctor
            dentist_name = data['entities']['dentist_name:dentist_name'][0]['body']
            url = f"http://127.0.0.1:8888/v1/dentists/{dentist_name}"
            reply = requests.get(url)
            if reply.status_code == 200:
                data = reply.json()
                reply = f"<table><tr><th>Dentist name</th><td>{data['name']}</td></tr>\
                                <tr><th>Location</th><td>{data['location']}</td></tr>\
                                <tr><th>Specialization</th><td>{data['specialization']}</td></tr>\
                                <tr><th>Phone number</th><td>{data['phone']}</td></tr>\
                                </table>"
                reply += f"To know the available timeslot of {data['name']}, please type:<em>'Get timetable of {data['name']}'</em> etc."
            elif reply.status_code == 404:
                reply = "The dentist you want to know doesn't work at our clinic, please choose another one"
        elif intent == 'GetDentistTimeslot':
            dentist_name = data['entities']['dentist_name:dentist_name'][0]['body']
            globals.session['dentist_name'] = dentist_name
            url = f'http://127.0.0.1:5555/v1/timeslots/dental?dentist_name={dentist_name}'
            reply = requests.get(url)
            data = reply.json()
            reply = f"The available timeslot of {dentist_name} is shown below:</br>"
            for i in data:
                reply += f"{i['time']}:00<br>"
            reply += f"To make an appointment with {dentist_name}, please type: 'book 9:00' etc."
        elif intent == 'MakeAppointment':
            # if not available, suggest other timeslot
            # if available, confirm booking and summarize at the end
            # Attempt to make appointment, can store value in session
            if 'timeslot:timeslot' not in data['entities'] and 'dentist_name:dentist_name' in data['entities']:
                dentist_name  = data['entities']['dentist_name:dentist_name'][0]['body']
                reply = f"Please tell me the timeslot you want to book with {dentist_name}, \
                    to check his/her timetable, you can type: <em>Check {dentist_name} timetable </em>"
            else:
                time = data['entities']['timeslot:timeslot'][0]['body']
                dentist_name = ''
                if 'dentist_name:dentist_name' in data['entities']: # direct booking
                    dentist_name  = data['entities']['dentist_name:dentist_name'][0]['body']
                    globals.session['dentist_name'] = dentist_name
                elif 'dentist_name' in globals.session:
                    dentist_name = globals.session['dentist_name']
                globals.session['time'] = time
                globals.session['action'] = 'book'
                if dentist_name:
                    reply = f"Please confirm your booking for appointment for {dentist_name} at {time} for tomorrow, type: 'yes', if you change your mind please type: 'no'"
                else:
                    reply = "Please tell me the dentist you want to book with"
        elif intent == 'CancelAppointment':
            if 'booking_id:booking_id' in data['entities']:
                globals.session['booking_id'] = int(data['entities']['booking_id:booking_id'][0]['body'])
                globals.session['action'] = 'cancel'
                reply = f"Please confirm your cancel for appointment with booking id {globals.session['booking_id']}, type: 'yes', if you change your mind please type: 'no'"
            else:
                reply = f"Please provide the booking id of the appointment you want to cancel, please type: 'cancel booking xxx'"
    except Exception as e:
        print(f"wit error:{e}")
        reply = "Sorry, i don't understand:("
    return reply

@app.route('/message', methods=['POST'])
def message():
    global name_flag
    user_input = request.json['dataId']
    answer = "Sorry, i don't understand:("
    try:
        globals.session["username"]
        user_name = globals.session["username"]
        # provide basic greetings
        answer = bot.reply(user_name, user_input)
        if 'ERR' in answer:
            answer = ask_wit(user_input)
        elif answer == "check username":
            answer = f'Your name is {user_name}'
        # confirm action
        elif answer == 'yes':
            action = globals.session['action']
            if action == 'book':
                answer = ConfirmBooking(globals.session['dentist_name'], globals.session['username'], globals.session['time'])
            else:
                answer = ConfirmCancel(globals.session['booking_id'])
        # confirm action 
        elif answer == 'no':
            if globals.session['action'] == 'book':
                answer = 'To choose another timeslot with the dentist you choose, type: <em>"Book 10:00" </em>etc, \
                    to get timetable for another doctor type: <em>"Check xx timetable"</em>'
                globals.session.pop('action', None)
            else:
                answer = 'No cancel has been made! Enjoy your time!:)'
                globals.session.pop('action', None)
        elif answer ==  "end":
            answer = 'Thank you for talking with bot, your session is end now, have a nice day:D'
            name_flag = False
            globals.session.pop('username', None)
        return answer
    except Exception as e:
        print(e)
        if "username" in globals.session:
            reply = "Sorry, I don't understand:("
        else:
            # no name 
            if name_flag:
                    globals.session["username"] = user_input
                    reply = f'Hello {globals.session["username"]}, welcome to use Dental Booking Chatbot Service!<br>\
                        You can talk with me or make appointment with dentist for <b>Tomorrow</b>.<br>\
                        To get the list of all available dentists, please type <em><b>"List all available dentists"</b></em> etc.<br>\
                        To check the timetable of a specific dentists, please type <em><b>"Check xx timetable"</b></em> etc.\
                        To make an appointment directly, please type <em><b>"Book me with xx at xx:00"</b></em> etc.'
            # ask for name 
            else:
                reply = 'Please enter your name to start the conversation'
                name_flag = True
        return reply

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port=8000, debug = True)


    