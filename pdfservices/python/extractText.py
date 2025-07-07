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
		files = {'file': (path, f)}

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

	return requests.get(f"{HOST}/pdf-services/api/documents/{doc}/download", headers=headers).content 

doc = uploadDoc("../../inputfiles/input.pdf", CLIENT_ID, CLIENT_SECRET)
print(f"Uploaded pdf to Foxit, id is {doc['documentId']}")

task = extractPDF(doc["documentId"], "TEXT", CLIENT_ID, CLIENT_SECRET)
print(f"Created task, id is {task['taskId']}")

result = checkTask(task["taskId"], CLIENT_ID, CLIENT_SECRET)
print(f"Final result: {result}")

text = getResult(result["resultDocumentId"], CLIENT_ID, CLIENT_SECRET)
print(text)

