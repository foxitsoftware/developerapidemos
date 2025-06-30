import fs from 'fs';
import { Readable } from 'stream';
import { finished } from 'stream/promises';
import path from 'node:path';

const CLIENT_ID = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;
const HOST = process.env.HOST;

async function uploadDoc(filepath, id, secret) {
	let filename = path.basename(filepath);
	let data = new FormData();
	let blob = await fs.openAsBlob(filepath);
	data.append('file', blob, filename);

	let req = await fetch(`${HOST}/pdf-services/api/documents/upload`, {
		method:'POST',
		headers: {
			client_id: id, 
			client_secret: secret
		},
		body: data
	});

	return await req.json();

}

async function manipulatePDF(doc, operations, id, secret) {

	let headers = {
		"client_id":id,
		"client_secret":secret,
		"Content-Type":"application/json"
	};

	let body = {
		"documentId":doc,
		"config": {
			"operations": operations
		}
	};

	let resp = await fetch(`${HOST}/pdf-services/api/documents/modify/pdf-manipulate`, {
		method:"POST",
		headers, 
		body:JSON.stringify(body)
	});

	return await resp.json();

}

async function checkTask(task, id, secret) {

	while(true) {
		let req = await fetch(`${HOST}/pdf-services/api/tasks/${task}`, {
			method:'GET',		
			headers: {
				client_id: id, 
				client_secret: secret,
				'Content-Type':'application/json'
			}
		});

		let result = await req.json();

		if(result['status'] === 'COMPLETED') {
			return result;
		} else if(result['status'] === 'FAILED') {
			console.log('Failure. Here is the last status:');
			console.log(result);
			process.exit(1);
		} else {
			console.log(`Current status, ${result['status']}, percentage: ${result['progress']}`);
			await delay(5);
		}

	}
}

// Lame function to add a delay to my polling calls
async function delay(x) {
	return new Promise(resolve => {
		setTimeout(() => resolve(), x * 1000);
	});
}

async function downloadResult(doc, filePath, id, secret) {
	let headers = {
		"client_id":id,
		"client_secret":secret
	}

	let res = await fetch(`${HOST}/pdf-services/api/documents/${doc}/download`, {
		headers
	});

	const body = Readable.fromWeb(res.body);
	const download_write_stream = fs.createWriteStream(filePath);
	return await finished(body.pipe(download_write_stream));

}

// This defines the operations we want to perform
let operations = [
	{ 
		"type":"MOVE_PAGES", 
		"pages": [ 1, 2],
		"targetPosition": 3
	}, 
	{ 
		"type":"ROTATE_PAGES", 
		"pages": [ 2 ], 
		"rotation": "ROTATE_CLOCKWISE_90"
	}, 
	{
		"type":"ADD_PAGES", 
		"pageCount": 5
	}
];

let doc = await uploadDoc('../../inputfiles/input.pdf', CLIENT_ID, CLIENT_SECRET);
console.log(`Uploaded doc to Foxit, id is ${doc['documentId']}`);

let task = await manipulatePDF(doc.documentId, operations, CLIENT_ID, CLIENT_SECRET, "HIGH");
console.log(`Created task, id is ${task['taskId']}`);

let result = await checkTask(task.taskId, CLIENT_ID, CLIENT_SECRET);
console.log(`Final result: ${JSON.stringify(result)}`);

await downloadResult(result.resultDocumentId, "../../output/node_manipulated_pdf.pdf", CLIENT_ID, CLIENT_SECRET);
console.log("Done and saved to: ../../output/node_manipulated_pdf.pdf");