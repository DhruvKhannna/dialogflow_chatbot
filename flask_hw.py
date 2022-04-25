# import flask dependencies 
from flask import Flask, request, make_response, jsonify 
from webexteamssdk import WebexTeamsAPI
from google.cloud import dialogflow
import requests
import webbrowser
import psycopg2
import pandas as pd
from datetime import datetime
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


# initialize the flask app 
app = Flask(__name__)
api = WebexTeamsAPI()
room_id="Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vODNhYzQ5ZTAtYmIxMC0xMWVjLTljMWQtNzUzMDI1MjAyMDg1"
ACCESS_TOKEN='YTllYjc1ZTktZGMzNi00NDllLTlkOWYtZGU4ZjFhYjI5MWNiOTllMGY3MWEtMjc0_P0A1_b6609cee-56d7-44a5-9f67-2e1759d7cfaf'
conn=psycopg2.connect(
			database="Goals101",
			user="postgres",
			password="123456",
			host="127.0.0.1",
			port=5433)

# default route 
@app.route('/') 
def index(): 
	return 'Hello World!' 

# function for responses 

"""
def results(): 
	print("********************** we are in results start************************")
	# build a request object 
	req = request.get_json(force=True) 
	print('req {}'.format(req))
	# fetch action from json 
	action = req.get('queryResult').get('fulfillmentText') 
	#fulfillmentText=req.query_result.fulfillment_text
	text_response={'fulfillmentText': '{}'.format(action)}
	send_msg_to_webex(text_response['fulfillmentText'])
	print("********************** we are in results end************************")
	return text_response
	#api.messages.create(room_id, text=text_response['fulfillmentText'])
"""

def send_msg_to_webex(msg):
	URL='https://api.ciscospark.com/v1/messages'
	headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,
		   'Content-type': 'application/json;charset=utf-8'}
	post_data = {'roomId': room_id,'text': msg}
	response = requests.post(URL, json=post_data, headers=headers)
	
	return 'OK'


def generate_file(intent,df):
	filename=intent+str(datetime.now().strftime('%Y%m%d%H%M%S'))+'.csv'
	#writer=pd.ExcelWriter(filename)
	df.to_csv(filename,index=False)
	return filename

def send_excel_to_webex(filename):
	file_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
	m = MultipartEncoder({'roomId': room_id,'text': 'Query Executed!','files': (f'{filename}', open(f'{filename}', 'rb'),file_type)})
	headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,'Content-type': m.content_type}
	r = requests.post('https://webexapis.com/v1/messages', data=m,headers=headers)
	return "Done"

	# return a fulfillment response 
	return text_response
def results2(txt):
	print("********************** we are in results2 start************************")
	project_id='chatbot-dflow'
	session_id='abcd'
	print('#1')
	session_client=dialogflow.SessionsClient()
	print('#2')
	session=session_client.session_path(project_id,session_id)
	print('#3')
	text_input=dialogflow.TextInput(text=txt,language_code='en')
	print('#4')
	query=dialogflow.QueryInput(text=text_input)
	print('#5')
	print('query input: {}'.format(query))
	print('#6')
	response=session_client.detect_intent(request={"session":session,"query_input":query})
	print('#7')
	fulfillmentText=response.query_result.fulfillment_text
	intent=response.query_result.intent.display_name
	print('this is intent ::::::{}'.format(intent))
	if intent=='SQL_Query1':
		print('your SQLQuery1 executing!')
		fulfillmentText='your SQLQuery1 executing!'
		send_msg_to_webex(fulfillmentText)
		# new addition
		data=pd.read_sql('SELECT bank,count(*) FROM data1 group by bank ;',conn)
		print(data.head(3))
		filename=generate_file(intent,data)
		send_excel_to_webex(filename)
		return {'fulfillmentText':fulfillmentText}
	if intent=='SQL_Query2':
		data=pd.read_sql('SELECT gender,debit_card_or_credit_card,avg(cast(amount as integer)) FROM data1 group by debit_card_or_credit_card,gender ;',conn)
		data2=data.set_index(['gender','debit_card_or_credit_card'])
		value=data2.loc[[('F', 'C')],'avg'].values[0]
		fulfillmentText="Average Credit Card Transaction spending by Female : {}".format(value)
		send_msg_to_webex(fulfillmentText)
		return {'fulfillmentText':fulfillmentText}
	else:
		print('#8')
		#status=send_msg_to_webex(fulfillmentText) # this is doubt? 
		print('#9')
		#print(status)
		send_msg_to_webex(fulfillmentText)
		print("********************** we are in results2 end************************")
		return {'fulfillmentText':fulfillmentText}



# create a route for webhook 
"""
@app.route('/webhook', methods=['GET', 'POST']) 
def webhook(): 
	# return response 
	return make_response(jsonify(results())) 
"""

@app.route('/webhook',methods=['GET','POST'])
def webex():
	print("********************** we are in webex start************************")
	if request.method=="GET":
		URL = 'https://webexapis.com/v1/messages'
		ACCESS_TOKEN='YTllYjc1ZTktZGMzNi00NDllLTlkOWYtZGU4ZjFhYjI5MWNiOTllMGY3MWEtMjc0_P0A1_b6609cee-56d7-44a5-9f67-2e1759d7cfaf'
		room_id="Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vODNhYzQ5ZTAtYmIxMC0xMWVjLTljMWQtNzUzMDI1MjAyMDg1"

		headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,
					'Content-type': 'application/json;charset=utf-8'}
		
		#MDZlNGI1NjMtYmUyOC00MDg1LWFiYTMtY2MyMzkyZjc0N2JhN2YxZDk5NWMtZmUy_P0A1_b6609cee-56d7-44a5-9f67-2e1759d7cfaf
		params={'email':'dhruv6992.khanna@gmail.com','roomId':room_id}
		response = requests.get(URL,headers=headers,params=params)
		print(response)
		if response.status_code == 200:
			print('req {}'.format(response.json()['items'][0]['text']))
			txt=response.json()['items'][0]['text']
			print("********************** we are in webex end************************")
			#return_val=results2(txt)
			print("********************** we are in webex end after results2************************")
		#return txt
		return make_response(jsonify(results2(txt)))

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