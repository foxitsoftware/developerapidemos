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

def convertToPDF(doc, id, secret):
	
	headers = {
		"client_id":id,
		"client_secret":secret,
		"Content-Type":"application/json"
	}

	body = {
		"documentId":doc	
	}

	request = requests.post(f"{HOST}/pdf-services/api/documents/create/pdf-from-word", json=body, headers=headers)
	return request.json()

def protectPDF(doc, password, id, secret):

	headers = {
		"client_id":id,
		"client_secret":secret,
		"Content-Type":"application/json"
	}

	body = {
		"documentId":doc,
		"config": {
			"userPassword":password
		}
	}

	request = requests.post(f"{HOST}/pdf-services/api/documents/security/pdf-protect", json=body, headers=headers)
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

def downloadResult(doc, path, id, secret):
	
	headers = {
		"client_id":id,
		"client_secret":secret
	}

	with open(path, "wb") as output:
		
		bits = requests.get(f"{HOST}/pdf-services/api/documents/{doc}/download", stream=True, headers=headers).content 
		output.write(bits)

doc = uploadDoc("../../inputfiles/input.docx", CLIENT_ID, CLIENT_SECRET)
print(f"Uploaded doc to Foxit, id is {doc['documentId']}")

task = convertToPDF(doc["documentId"], CLIENT_ID, CLIENT_SECRET)
print(f"Created task, id is {task['taskId']}")

result = checkTask(task["taskId"], CLIENT_ID, CLIENT_SECRET)
print("Done converting to PDF. Now adding a password.")

task = protectPDF(result["resultDocumentId"], "password", CLIENT_ID, CLIENT_SECRET)
print(f"Created task, id is {task['taskId']}")

result = checkTask(task["taskId"], CLIENT_ID, CLIENT_SECRET)
print("Done with password task.")

downloadResult(result["resultDocumentId"], "../../output/input_multi.pdf", CLIENT_ID, CLIENT_SECRET)
print("Done and saved to: ../../output/input_multi.pdf. When opening, use password of 'password'")