# Initial setup

import json
from flask import Flask
from pyfcm import FCMNotification

# Flask object creation
app = Flask(__name__)

# Index page
@app.route("/")

def index():
	return_value = {"message":"Welcome to the Blight back-end!"}
	json_string = json.dumps(return_value)
	return json_string

# Error page
@app.errorhandler(404)

def page_not_found(e):
	return json.dumps(data_repository["error"]), 404

if __name__ == "__main__":
	app.debug = True
	app.run()
