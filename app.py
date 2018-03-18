# Initial setup

import json
import requests

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from pyfcm import FCMNotification

# Defining the server key
push_service = FCMNotification(api_key="AAAAI6Yezgk:APA91bHTgkp5RKolA8Fb2VzYZjCt5z8iadT6dmRUzAVhzqWngXiFtHLu__spT82XXXy9vstzBixnzuG0Rgtuyf6hsCBywd6fpYXpsI5Gma6t9vfdyIkEA9b4UtBc4SRg1w6IBmKmwBFk")

# Function for checking any disaster
def check_disaster():
	api_key = '3rRLEdKYJZYfSA0nvMftbmf4wJSUzL8J'
	disaster_url = 'http://dataservice.accuweather.com/alarms/v1/1day/190975?apikey=' + api_key

	disaster_response = requests.get(disaster_url)
	
	if (disaster_response.text != '[]'):
		print('There is an emergency.')
		
	return len(disaster_response.text)
	
# Starting the scheduler with the required job
task_scheduler = BackgroundScheduler(daemon=True)
task_scheduler.add_job(check_disaster, 'interval', minutes=10)
task_scheduler.start()

# Flask object creation
app = Flask(__name__)

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
	
	temperature_url = 'https://www.wolframcloud.com/objects/2fd9ef4c-bad7-4a1e-911b-1612268870a2?a=' + location
	pressure_url = 'https://www.wolframcloud.com/objects/b06e46ec-6771-419c-9131-a95aa4da6bf1?b=' + location
	humidity_url = 'https://www.wolframcloud.com/objects/118560e8-ed93-4dcc-8ae5-4ebef9e92269?c=' + location
	visibility_url = 'https://www.wolframcloud.com/objects/23efd16a-2010-476e-ae56-6a756f6d1a73?d=' + location
	windspeed_url = 'https://www.wolframcloud.com/objects/adb4d8d1-c5d4-4ace-adb9-9379e25ed252?e=' + location

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
	forecast_temp_url = 'https://www.wolframcloud.com/objects/2383eee0-e0b4-4eb5-b349-af0eda7ca348?f=' + location
	forecast_pressure_url = 'https://www.wolframcloud.com/objects/bdf58b84-08bf-4cb5-9c78-6e647a8eac8f?g=' + location
	
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
