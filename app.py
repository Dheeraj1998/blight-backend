# Initial setup

import json
import requests

from flask import Flask, request
from pyfcm import FCMNotification

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
	
	return_value = {"temperature": temp_response, "pressure": pressure_response, "humidity": humidity_response, "visibility": visibility_response, "wind": wind_response}
	json_string = json.dumps(return_value)
	
	return json_string
	
	#temp_url = 'https://www.wolframcloud.com/objects/d50c639f-5ea7-495b-82ff-48ba3e53dd61?f=' + location

# Error page
@app.errorhandler(404)

def page_not_found(e):
	return json.dumps(data_repository["error"]), 404

if __name__ == "__main__":
	app.debug = True
	app.run()
