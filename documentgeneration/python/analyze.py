import os
import requests
import sys 
import json
from time import sleep 
import base64 
from datetime import datetime

clientId = os.environ.get('CLIENT_ID')
clientSecret = os.environ.get('CLIENT_SECRET')
HOST = os.environ.get('HOST')

def analyzeDoc(doc,id, secret):
	
	headers = {
		"client_id":id,
		"client_secret":secret
	}

	body = {
		"base64FileString":doc
	}

	request = requests.post(f"{HOST}/document-generation/api/AnalyzeDocumentBase64", json=body, headers=headers)

	return request.json()


with open('../../inputfiles/docgen1.docx', 'rb') as file:
	bd = file.read()
	b64 = base64.b64encode(bd).decode('utf-8')

result = analyzeDoc(b64, clientId, clientSecret)
print(json.dumps(result, indent=4))

