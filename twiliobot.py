import os
from flask import Flask, request, Response
from slackclient import SlackClient
from twilio import twiml
from twilio.rest import TwilioRestClient
import twilio

SLACK_WEBHOOK_SECRET = "2nVn5Xp6AVTMF2TU9UU8AIzQ"
TWILIO_NUMBER ="+12516629139"
USER_NUMBER = "+972547772958"
 
app = Flask(__name__)
slack_client = SlackClient(os.environ.get('xoxp-62429019142-62382628995-62431024326-9f056a928d', None))
TWILIO_ACCOUNT_SID = "ACa007a50542306a3188fb2ec4aad37568"
TWILIO_AUTH_TOKEN = "5959988bf309757269e2fc2fd6b65add"
twilio_client = TwilioRestClient(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)

@app.route('/twilio', methods=['POST'])
def twilio_post():
	print "got it"
	response = twiml.Response()
	if request.form['From'] == USER_NUMBER:
		message = request.form['Body']
		twilio_client.messages.create(to=USER_NUMBER, from_=TWILIO_NUMBER,
                                      body=message)
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