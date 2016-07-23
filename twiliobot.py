import os
from flask import Flask, request, Response
from slackclient import SlackClient
from twilio import twiml
from twilio.rest import TwilioRestClient
import twilio
import xlrd
import xlwt


class user(object):
	def __init__(self, user_type, phone_number, PIN):
		self.user_type = user_type
		self.phone_number = phone_number
		self.PIN = PIN
 
caller_list = []

SLACK_WEBHOOK_SECRET = "2nVn5Xp6AVTMF2TU9UU8AIzQ"
TWILIO_NUMBER ="+12516629139"
USER_NUMBER = "+972547772958"
 
app = Flask(__name__)
slack_client = SlackClient(os.environ.get('xoxp-62429019142-62382628995-62503851861-dc91e37657', None))
TWILIO_ACCOUNT_SID = "ACa007a50542306a3188fb2ec4aad37568"
TWILIO_AUTH_TOKEN = "5959988bf309757269e2fc2fd6b65add"
twilio_client = TwilioRestClient(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)

book = xlrd.open_workbook("example.xls")
sheet = book.sheet_by_name("DataBase")
sheet_auth = book.sheet_by_name("authentication_databse")
finalmessage =""
global name
name = ""
global finalphase
finalphase = False
	

@app.route('/twilio', methods=['POST'])
def twilio_post():
	
	print "got it"
	print(request.form['Body'])
	curr_PIN = 0
	curr_user_type = ""
	response = twiml.Response()
	if request.form['From'] == USER_NUMBER:
		
		caller_number = request.form['From']
		message = request.form['Body']	
		if(caller_number not in caller_list):
			#for i in range(sheet_auth.nrows):
			#	if(sheet_auth.cell_value(rowx = i, colx = 1) == caller_number):
			curr_PIN = sheet_auth.cell_value(rowx = 1, colx = 0) 
			curr_user_type = sheet_auth.cell_value(rowx = 1, colx = 2)
			caller_list.append(caller_number)
			print(str(int(curr_PIN)), str(int(request.form['Body'])))
			if(str(int(curr_PIN)) != str(int(request.form['Body']))):
				message = "PIN is invalid for this user, please insert a valid PIN"
				twilio_client.messages.create(to=USER_NUMBER, from_=TWILIO_NUMBER,
										body=message)
				return Response(response.toxml(), mimetype="text/xml"), 200
			else:
				message = "PIN is OK, welcome "+ curr_user_type
				twilio_client.messages.create(to=USER_NUMBER, from_=TWILIO_NUMBER,
										body=message)
				return Response(response.toxml(), mimetype="text/xml"), 200
			
		elif  finalphase:
			global finalphase
			global name
			for i in range(1,sheet.nrows):
				if sheet.cell(i,0).value.lower() == name.lower():
					for j in (2,sheet.ncols):
						if sheet.cell(0,j).value.lower() == message.lower():
							sheet.write(i,j,"yes")
							twilio_client.messages.create(to=USER_NUMBER, from_=TWILIO_NUMBER,
										body="Done.")
							finalphase = False
							return Response(response.toxml(), mimetype="text/xml"), 200
		
		else:
			name = message
			for i in range(1,sheet.nrows):
				if sheet.cell(i,0).value.lower() == message.lower():
					for j in range(1,sheet.ncols):
						global finalmessage
						if(str(sheet.cell(i,j).value) == "no"):
							continue
						finalmessage += str(sheet.cell(0,j).value) + ": " + str(sheet.cell(i,j).value) + " "
			if(finalmessage == ""):
				finalmessage = "not found"
				twilio_client.messages.create(to=USER_NUMBER, from_=TWILIO_NUMBER,
										  body=finalmessage)
				return Response(response.toxml(), mimetype="text/xml"), 200
			finalmessage += "\n" + "please write the name of the updated vaccination:"
			twilio_client.messages.create(to=USER_NUMBER, from_=TWILIO_NUMBER,
										  body=finalmessage)
			finalphase = True
			return Response(response.toxml(), mimetype="text/xml"), 200

			
			
		
@app.route('/slack', methods=['POST'])
def slack_post():
    if request.form['token'] == SLACK_WEBHOOK_SECRET:
        channel = request.form['channel_name']
        username = request.form['user_name']
        text = request.form['text']
        response_message = username +  " in " +  channel +  " says: " +  text
        twilio_client.messages.create(to=USER_NUMBER, from_=TWILIO_NUMBER,
                                      body=response_message)
    return Response(), 200

@app.route('/', methods=['GET'])
def test():
   return Response('It works!')
 

if __name__ == '__main__':
	app.run(debug=True)