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


def extractPDF(doc, type, id, secret, pageRange):
	
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


def downloadResult(doc, path, id, secret):
	
	headers = {
		"client_id":id,
		"client_secret":secret
	}

	with open(path, "wb") as output:
		
		bits = requests.get(f"{HOST}/pdf-services/api/documents/{doc}/download", stream=True, headers=headers).content 
		output.write(bits)

doc = uploadDoc("../../inputfiles/input.pdf", CLIENT_ID, CLIENT_SECRET)
print(f"Uploaded pdf to Foxit, id is {doc['documentId']}")

task = extractPDF(doc["documentId"], "TEXT", CLIENT_ID, CLIENT_SECRET)
print(f"Created task, id is {task['taskId']}")
result = checkTask(task["taskId"], CLIENT_ID, CLIENT_SECRET)
print(f"Final result: {result}")

downloadResult(result["resultDocumentId"], "../../output/extract_text.txt", CLIENT_ID, CLIENT_SECRET)
print("Done and saved to: ../../output/extract_text.txt")

task = extractPDF(doc["documentId"], "IMAGE", CLIENT_ID, CLIENT_SECRET)
print(f"Created task, id is {task['taskId']}")
result = checkTask(task["taskId"], CLIENT_ID, CLIENT_SECRET)
print(f"Final result: {result}")

downloadResult(result["resultDocumentId"], "../../output/extract_images.zip", CLIENT_ID, CLIENT_SECRET)
print("Done and saved to: ../../output/extract_images.zip")

task = extractPDF(doc["documentId"], "PAGE", CLIENT_ID, CLIENT_SECRET, 2)
print(f"Created task, id is {task['taskId']}")
result = checkTask(task["taskId"], CLIENT_ID, CLIENT_SECRET)
print(f"Final result: {result}")

downloadResult(result["resultDocumentId"], "../../output/extract_page.pdf", CLIENT_ID, CLIENT_SECRET)
print("Done and saved to: ../../output/extract_page.pdf")
