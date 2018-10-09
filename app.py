# Initial setup

import json
import pyrebase
import random
import requests

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from pyfcm import FCMNotification

# Firebase configuration
config = {
    "apiKey": "AIzaSyBbGWcyla5IKW8s6M7IRhne2d02QzGOYmw",
    "authDomain": "blight-c675c.firebaseapp.com",
    "databaseURL": "https://blight-c675c.firebaseio.com",
    "storageBucket": "blight-c675c.appspot.com",
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Keep sample_data = 1 if you want to check alerts with sample data
global sample_data
sample_data = 1

# Flask object creation
app = Flask(__name__)

# Check disaster page
@app.route("/check_disaster")

# Function for checking any disaster
def check_disaster():
	# Defining the server key
	push_service = FCMNotification(api_key="AAAAQphrR20:APA91bEUrVu2ErYDuUPYcBdwBoBTAAICi6BTT9mRQXFwacQRJJznB2ma9gXgeVKJa4esADzrIDgGwX4wOdG5ZRwhCzdevPCJuxoPcoM8VVn59km1lvpKJfCQKFWke95A3K1abuIX-_o_")

	if(sample_data == 1):
		fcm_ids = []
	
		# Selection of Vellore as the location in this sample case
		selected_city = 'Vellore'
		all_users = db.child("locations").child(selected_city).get()
		
		# Extraction of FCM ids for the particular area
		for user in all_users.each():
			fcm_ids.append(user.val())
			
		# Sending the message to multiple devices
		message_title = random.choice(["ETH: Earthquake Alert", "FLD: Flood Alert", "FOT: Forest Fire Alert", "TND: Thunderstorm Alert"])
		message_body = "Alert has been issued in your area. Stay careful!"
	
		push_service.notify_multiple_devices(registration_ids=fcm_ids, message_title=message_title, message_body=message_body)
		
		return 'The alert has been sent.'
	
	elif(sample_data == 0):
		api_key = 'wCZcX0UM9VQCyDHz1neUkcOdv5g5IyX0'
		#api_key = 'WUDCNIeqK4DxaaWl1ekL9zwP4Cn0ZElI'
		#api_key = '3rRLEdKYJZYfSA0nvMftbmf4wJSUzL8J'
		
		selected_city = 'Vellore'
		location_lookup_url = 'http://dataservice.accuweather.com/locations/v1/cities/search?apikey=' + api_key + '&q=' + location_name

		# Coverting the response text to JSON format and finding the location key
		lookup_response = requests.get(location_lookup_url).text
		lookup_response = json.loads(lookup_response)
		location_key = lookup_response[0]["Key"]
	
		disaster_url = 'http://dataservice.accuweather.com/alarms/v1/1day/' + location_key + '?apikey=' + api_key
		disaster_response = requests.get(disaster_url)
	
		all_users = db.child("locations").child(selected_city).get()
		
		fcm_ids = []
		for user in all_users.each():
			fcm_ids.append(user.val())
	
		if (disaster_response != '[]'):
			message_title = "EMA: Earthquake Alert"
			message_body = "Alert has been issued in your area. Stay careful!"
			push_service.notify_multiple_devices(registration_ids=fcm_ids, message_title=message_title, message_body=message_body)
			
		return 'The alert has been sent.'
# Function for retrieving the details from Firebase
def retrieve_data():
	users = db.child("users").get()
	locations = {}
	
	for value in users.each():
		temp_array = []
		key_value = value.val()['location']
		try:
			temp_array = locations[key_value]
			temp_array.append(value.val()['device_token'])
		except:
			temp_array = [value.val()['device_token']]
		locations[key_value] = temp_array
		
	db.child("locations").set(locations)

# Index page
@app.route("/")

def index():
	return_value = {"message":"Welcome to the Blight back-end!"}
	json_string = json.dumps(return_value)
	return json_string

# Query page
@app.route("/query", methods = ["GET"])

def query():
	location = request.args.get('location').lower()
	
	temperature_url = 'https://www.wolframcloud.com/objects/b68ac476-0ef9-4721-952e-a853e6c5ebdf?a=' + location
	pressure_url = 'https://www.wolframcloud.com/objects/bd7c282b-ad1e-48a9-8688-fafdd6e946cf?b=' + location
	humidity_url = 'https://www.wolframcloud.com/objects/541161bf-270a-4680-b9e3-fa04bef25e6c?c=' + location
	visibility_url = 'https://www.wolframcloud.com/objects/45cb3295-9423-479c-8d1a-273023107c55?d=' + location
	windspeed_url = 'https://www.wolframcloud.com/objects/cabfa8b0-0213-45eb-ae1d-d29f5c8358d9?e=' + location

	temp_response = requests.get(temperature_url)
	pressure_response = requests.get(pressure_url)
	humidity_response = requests.get(humidity_url)
	visibility_response = requests.get(visibility_url)
	wind_response = requests.get(windspeed_url)
	
	temp_response = float(temp_response.text.split(" ")[0])
	pressure_response = float(pressure_response.text.split(" ")[0])
	humidity_response = float(humidity_response.text.split(" ")[0])
	visibility_response = float(visibility_response.text.split(" ")[0])
	wind_response = float(wind_response.text.split(" ")[0])
	
	# Extracing info from 
	forecast_temp_url = 'https://www.wolframcloud.com/objects/aa96736b-8971-4d37-9be7-2305a9e0a347?f=' + location
	forecast_pressure_url = 'https://www.wolframcloud.com/objects/6fc18c5d-b4b6-42e8-9b55-6cbff043be7b?g=' + location
	
	forecast_temp_response = requests.get(forecast_temp_url).text[111:].split("}")[0]
	forecast_temp_response = forecast_temp_response.split(",")
	
	for index in range(0, len(forecast_temp_response)):
		forecast_temp_response[index] = float(forecast_temp_response[index])
	
	forecast_pressure_response = requests.get(forecast_pressure_url).text[111:].split("}")[0]
	forecast_pressure_response = forecast_pressure_response.split(",")
	
	for index in range(0, len(forecast_pressure_response)):
		forecast_pressure_response[index] = float(forecast_pressure_response[index])
	
	return_value = {"temperature": "%.2f" % temp_response, "pressure": "%.2f" % pressure_response, 
					"humidity": "%.2f" % humidity_response, "visibility": "%.2f" % visibility_response, "wind": "%.2f" % wind_response, 
					"forecast_t_d1": "%.2f" % forecast_temp_response[0], "forecast_t_d2": "%.2f" % forecast_temp_response[1], 
					"forecast_t_d3": "%.2f" % forecast_temp_response[2], "forecast_t_d4": "%.2f" % forecast_temp_response[3], 
					"forecast_t_d5": "%.2f" % forecast_temp_response[4], "forecast_t_d6": "%.2f" % forecast_temp_response[5],
					"forecast_p_d1": "%.2f" % forecast_pressure_response[0], "forecast_p_d2": "%.2f" % forecast_pressure_response[1], 
					"forecast_p_d3": "%.2f" % forecast_pressure_response[2], "forecast_p_d4": "%.2f" % forecast_pressure_response[3], 
					"forecast_p_d5": "%.2f" % forecast_pressure_response[4], "forecast_p_d6": "%.2f" % forecast_pressure_response[5]}
	
	json_string = json.dumps(return_value)
	
	return json_string

# Error page
@app.errorhandler(404)

def page_not_found(e):
	return json.dumps({"message":"The required page was not found."}), 404

if __name__ == "__main__":
	app.debug = True
	app.run()

# Starting the scheduler with the required job
task_scheduler = BackgroundScheduler(daemon=True)
task_scheduler.add_job(retrieve_data, 'interval', seconds=10000)
task_scheduler.start()
