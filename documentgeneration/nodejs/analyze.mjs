import fs from 'fs';

const CLIENT_ID = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;
const HOST = process.env.HOST;

async function analyzeDoc(doc, id, secret) {

	let headers = {
		"client_id":id, 
		"client_secret":secret, 
		"Content-Type":"application/json"
	};

	let body = {
		"base64FileString":doc
	};

	let req = await fetch(`${HOST}/document-generation/api/AnalyzeDocumentBase64`, {
		method:'POST', 
		headers, 
		body: JSON.stringify(body)
	});

	return await req.json();

}

let buffer = fs.readFileSync('../../inputfiles/docgen_sample.docx');
let b64 = buffer.toString('base64');

let result = await analyzeDoc(b64, CLIENT_ID, CLIENT_SECRET);
console.log(result);
