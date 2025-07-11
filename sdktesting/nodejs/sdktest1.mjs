import { PDFServiceSDK } from "./PDFServiceSDK.mjs";

const clientId = process.env.CLIENT_ID;
const clientSecret = process.env.CLIENT_SECRET;

const pdfService = new PDFServiceSDK(clientId, clientSecret);

await pdfService.wordToPDF('../../inputsfiles/input.docx', '../../output/output_from_nodesdk.pdf');
console.log("PDF conversion completed successfully.");