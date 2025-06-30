import os
import requests
import sys 
from time import sleep 
import base64 
from datetime import datetime

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
HOST = os.environ.get('HOST')

def docGen(doc, data, id, secret):
	
	headers = {
		"client_id":id,
		"client_secret":secret
	}

	body = {
		"outputFormat":"pdf",
		"documentValues": data,  
		"base64FileString":doc
	}

	request = requests.post(f"{HOST}/document-generation/api/GenerateDocumentBase64", json=body, headers=headers)

	return request.json()

with open('../../inputfiles/docgen_sample.docx', 'rb') as file:
	bd = file.read()
	b64 = base64.b64encode(bd).decode('utf-8')

data = {
	"name":"Raymond Camden", 
	"food": "sushi",
	"favoriteMovie": "Star Wars",
	"cats": [
		{"name":"Elise", "gender":"female", "age":14 },
		{"name":"Luna", "gender":"female", "age":13 },
		{"name":"Crackers", "gender":"male", "age":13 },
		{"name":"Gracie", "gender":"female", "age":12 },
		{"name":"Pig", "gender":"female", "age":10 },
		{"name":"Zelda", "gender":"female", "age":2 },
		{"name":"Wednesday", "gender":"female", "age":1 },
	],
}

result = docGen(b64, data, CLIENT_ID, CLIENT_SECRET)

if result["base64FileString"] == None:
	print("Something went wrong.")
	print(result)
	sys.exit()

b64_bytes = result["base64FileString"].encode('ascii')
binary_data = base64.b64decode(b64_bytes)

with open('../../output/docgen_sample.pdf', 'wb') as file:
	file.write(binary_data)
	print('Done and stored to ../../output/docgen_sample.pdf')