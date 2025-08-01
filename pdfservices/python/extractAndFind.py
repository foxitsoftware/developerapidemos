import os
import requests
import sys 
from time import sleep 

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
HOST = os.environ.get('HOST')

def uploadDoc(path, id, secret):
	
	headers = {
		"client_id":id,
		"client_secret":secret
	}

	with open(path, 'rb') as f:
		files = {'file': f}

		request = requests.post(f"{HOST}/pdf-services/api/documents/upload", files=files, headers=headers)
		return request.json()


def extractPDF(doc, type, id, secret, pageRange=None):
	
	headers = {
		"client_id":id,
		"client_secret":secret,
		"Content-Type":"application/json"
	}

	body = {
		"documentId":doc,
		"extractType":type
	}

	if pageRange:
		body["pageRange"] = pageRange 

	request = requests.post(f"{HOST}/pdf-services/api/documents/modify/pdf-extract", json=body, headers=headers)
	return request.json()

def checkTask(task, id, secret):

	headers = {
		"client_id":id,
		"client_secret":secret,
		"Content-Type":"application/json"
	}

	done = False
	while done is False:

		request = requests.get(f"{HOST}/pdf-services/api/tasks/{task}", headers=headers)
		status = request.json()
		if status["status"] == "COMPLETED":
			done = True
			# really only need resultDocumentId, will address later
			return status
		elif status["status"] == "FAILED":
			print("Failure. Here is the last status:")
			print(status)
			sys.exit()
		else:
			print(f"Current status, {status['status']}, percentage: {status['progress']}")
			sleep(5)


def getResult(doc, id, secret):
	
	headers = {
		"client_id":id,
		"client_secret":secret
	}

	return requests.get(f"{HOST}/pdf-services/api/documents/{doc}/download", headers=headers).text

# Get PDFs from our input directory
inputFiles = list(filter(lambda x: x.endswith('.pdf'), os.listdir('../../inputfiles')))

# Keyword to match on: 
keyword = "Shakespeare"

for file in inputFiles:
	
	doc = uploadDoc(f"../../inputfiles/{file}", CLIENT_ID, CLIENT_SECRET)
	print(f"Uploaded pdf, {file}, to Foxit, id is {doc['documentId']}")

	task = extractPDF(doc["documentId"], "TEXT", CLIENT_ID, CLIENT_SECRET)
	result = checkTask(task["taskId"], CLIENT_ID, CLIENT_SECRET)

	text = getResult(result["resultDocumentId"], CLIENT_ID, CLIENT_SECRET)
	if keyword in text:
		print(f"\033[32mThe pdf, {file}, matched on our keyword: {keyword}\033[0m")
	else:
		print(f"The pdf, {file}, did not match on our keyword: {keyword}")
	
	print("")

