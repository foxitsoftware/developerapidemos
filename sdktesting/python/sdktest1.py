import pdf_service_sdk
import os 

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

sdk = pdf_service_sdk.PDFServiceSDK( client_id=CLIENT_ID,
                                     client_secret=CLIENT_SECRET)

#sdk.word_to_pdf(input_path="../../inputfiles/input.docx",output_path="../../output/output_from_sdk.pdf")
#print("Conversion completed successfully. Check the output file at ../../output/output_from_sdk.pdf")

#sdk.conversion(input_path="../../inputfiles/input.docx",output_path="../../output/output_from_sdk_v2.pdf")
#print("Conversion (second version) completed successfully. Check the output file at ../../output/output_from_sdk_v2.pdf")

#sdk.compress("../../inputfiles/input.pdf","../../output/compressed_from_sdk_low.pdf")
#sdk.compress("../../inputfiles/input.pdf","../../output/compressed_from_sdk_high.pdf", "HIGH")
#print("Compressed a PDF twice")

#sdk.linearize("../../inputfiles/input.pdf","../../output/linearized_from_sdk.pdf")
#print("Linearized a PDF")

sdk.flatten("../../inputfiles/input.pdf","../../output/flattened_from_sdk.pdf")
print("Flattened a PDF")
