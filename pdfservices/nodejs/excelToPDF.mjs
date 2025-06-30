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

async function excelToPDF(doc, id, secret) {

	let headers = {
		"client_id":id,
		"client_secret":secret,
		"Content-Type":"application/json"
	};

	let body = {
		"documentId":doc
	};

	let resp = await fetch(`${HOST}/pdf-services/api/documents/create/pdf-from-excel`, {
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

let doc = await uploadDoc('../../inputfiles/apples.xlsx', CLIENT_ID, CLIENT_SECRET);
console.log(`Uploaded doc to Foxit, id is ${doc['documentId']}`);

let task = await excelToPDF(doc.documentId, CLIENT_ID, CLIENT_SECRET, "HIGH");
console.log(`Created task, id is ${task['taskId']}`);

let result = await checkTask(task.taskId, CLIENT_ID, CLIENT_SECRET);
console.log(`Final result: ${JSON.stringify(result)}`);

await downloadResult(result.resultDocumentId, "../../output/node_fromexcel.pdf", CLIENT_ID, CLIENT_SECRET);
console.log("Done and saved to: ../../output/node_fromexcel.pdf");