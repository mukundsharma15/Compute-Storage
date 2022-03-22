import json, requests, time
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/begin', methods=['POST'])
def initiate():
	if request.method == 'POST':
		if ("banner") in request.json and "ip" in request.json:
			url = "http://localhost:5000/storedata"
			payload = json.dumps({"data": "a new string this time.  "})
			response = requests.request("POST", url, headers={'Content-Type': 'application/json'}, data=payload)
			return response.text

app.run(host='0.0.0.0', port=8000)