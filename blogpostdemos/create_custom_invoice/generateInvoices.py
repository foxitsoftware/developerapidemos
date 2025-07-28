import os
import requests
import sys 
from time import sleep 
import base64 
import json 
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

with open('invoice.docx', 'rb') as file:
	bd = file.read()
	b64 = base64.b64encode(bd).decode('utf-8')

with open('invoicedata.json', 'r') as file:
	data = json.load(file)

for invoiceData in data:
	result = docGen(b64, invoiceData, CLIENT_ID, CLIENT_SECRET)

	if result["base64FileString"] == None:
		print("Something went wrong.")
		print(result)
		sys.exit()

	b64_bytes = result["base64FileString"].encode('ascii')
	binary_data = base64.b64decode(b64_bytes)

	filename = f"invoice_account_{invoiceData["accountNumber"]}.pdf"

	with open(filename, 'wb') as file:
		file.write(binary_data)
		print(f"Done and stored to {filename}")