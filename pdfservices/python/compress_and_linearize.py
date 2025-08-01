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

def compressPDF(doc, level, id, secret):
	
	headers = {
		"client_id":id,
		"client_secret":secret,
		"Content-Type":"application/json"
	}

	body = {
		"documentId":doc,
		"compressionLevel":level	
	}

	request = requests.post(f"{HOST}/pdf-services/api/documents/modify/pdf-compress", json=body, headers=headers)
	return request.json()

def linearizePDF(doc, id, secret):

	headers = {
		"client_id":id,
		"client_secret":secret,
		"Content-Type":"application/json"
	}

	body = {
		"documentId":doc
	}

	request = requests.post(f"{HOST}/pdf-services/api/documents/optimize/pdf-linearize", json=body, headers=headers)
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

input = "../../inputfiles/input.pdf"
print(f"File size of input: {os.path.getsize(input)}")
doc = uploadDoc(input, CLIENT_ID, CLIENT_SECRET)
print(f"Uploaded doc to Foxit, id is {doc['documentId']}")

task = compressPDF(doc["documentId"], "HIGH", CLIENT_ID, CLIENT_SECRET)
print(f"Created task, id is {task['taskId']}")

result = checkTask(task["taskId"], CLIENT_ID, CLIENT_SECRET)
print("Done converting to PDF. Now doing linearize.")

task = linearizePDF(result["resultDocumentId"], CLIENT_ID, CLIENT_SECRET)
print(f"Created task, id is {task['taskId']}")

result = checkTask(task["taskId"], CLIENT_ID, CLIENT_SECRET)
print("Done with linearize task.")

output = "../../output/really_optimized.pdf"
downloadResult(result["resultDocumentId"], output , CLIENT_ID, CLIENT_SECRET)
print(f"Done and saved to: {output}.")
print(f"File size of output: {os.path.getsize(output)}") 