# import flask dependencies 
from flask import Flask, request, make_response, jsonify 
from webexteamssdk import WebexTeamsAPI
from google.cloud import dialogflow
import requests
import webbrowser

# initialize the flask app 
app = Flask(__name__) 

api = WebexTeamsAPI()
room_id="Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vODNhYzQ5ZTAtYmIxMC0xMWVjLTljMWQtNzUzMDI1MjAyMDg1"
ACCESS_TOKEN="YzFlNThjMGEtMmQ3NC00OTllLTlmNjMtZmYwNDZmNTBhMzJlZjk0NGUxYTItYmVm_P0A1_b6609cee-56d7-44a5-9f67-2e1759d7cfaf"
# default route 
@app.route('/') 
def index(): 
	return 'Hello World!' 

# function for responses 
def results(): 
	# build a request object 
	req = request.get_json(force=True) 
	print('req {}'.format(req))
	# fetch action from json 
	action = req.get('queryResult').get('queryText') 
	text_response={'fulfillmentText': 'This is a response from webhook. since you said {}'.format(action)} 
	api.messages.create(room_id, text=text_response['fulfillmentText'])

def send_msg_to_webex(msg):
	URL='https://api.ciscospark.com/v1/messages'
	headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,
		   'Content-type': 'application/json;charset=utf-8'}
	post_data = {'roomId': room_id,'text': msg}
	response = requests.post(URL, json=post_data, headers=headers)

	return 'OK'

	# return a fulfillment response 
	return text_response
def results2(txt):
	project_id='chatbot-dflow'
	session_id='abcd'
	session_client=dialogflow.SessionsClient()
	session=session_client.session_path(project_id,session_id)
	text_input=dialogflow.TextInput(text=txt,language_code='en')
	query=dialogflow.QueryInput(text=text_input)
	response=session_client.detect_intent(request={"session":session,"query_input":query})
	fulfillmentText=response.query_result.fulfillment_text
	status=send_msg_to_webex(fulfillmentText)
	print(status)
	return status



# create a route for webhook 
@app.route('/webhook', methods=['GET', 'POST']) 
def webhook(): 
	# return response 
	return make_response(jsonify(results())) 

@app.route('/webhook2',methods=['GET','POST'])
def webex():
	if request.method=="GET":
		URL = 'https://webexapis.com/v1/messages'
		ACCESS_TOKEN="YzFlNThjMGEtMmQ3NC00OTllLTlmNjMtZmYwNDZmNTBhMzJlZjk0NGUxYTItYmVm_P0A1_b6609cee-56d7-44a5-9f67-2e1759d7cfaf"
		room_id="Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vODNhYzQ5ZTAtYmIxMC0xMWVjLTljMWQtNzUzMDI1MjAyMDg1"
		headers = {'Authorization': 'Bearer ' + 'MDZlNGI1NjMtYmUyOC00MDg1LWFiYTMtY2MyMzkyZjc0N2JhN2YxZDk5NWMtZmUy_P0A1_b6609cee-56d7-44a5-9f67-2e1759d7cfaf',
					'Content-type': 'application/json;charset=utf-8'}
		params={'email':'dhruv6992.khanna@gmail.com','roomId':room_id}
		response = requests.get(URL,headers=headers,params=params)
		print(response)
		if response.status_code == 200:
			print('req {}'.format(response.json()['items'][0]['text']))
			txt=response.json()['items'][0]['text']
			return_val=results2(txt)
		return txt

	else:
		return "Empty"
		
	#webbrowser.open_new('http://127.0.0.1:5000/webhook2')
	
	#return txt
"""
@app.route('/webhook3',methods=['GET','Post'])
def web():
	if request.method=='POST'
	URL='https://api.ciscospark.com/v1/messages'
	headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,
		   'Content-type': 'application/json;charset=utf-8'}
	post_data = {'roomId': room_id,'text': msg}
	response = requests.post(URL, json=post_data, headers=headers)
	print('response_new {}'.format(response.json()))
	return make_response(jsonify(results())) 
"""

# run the app 
if __name__ == '__main__': 
	if True:
		app.run(use_reloader=True)
	else:
		print('Failed!')