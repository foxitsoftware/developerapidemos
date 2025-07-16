# Foxit PDF Services SDK

This SDK lets developers more easily use the Foxit APIs, including [PDF Services](https://developer-api.foxit.com/pdf-services/) and [Document Generation](https://developer-api.foxit.com/document-generation/). You will need a [free set of credentials](https://app.developer-api.foxit.com/pricing) in order to call the APIs.

## Usage

Copy your credentials to the environment and then instantiate the SDK. Here's a sample:

```python
import pdf_service_sdk
import os 

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

sdk = pdf_service_sdk.PDFServiceSDK( client_id=CLIENT_ID,
                                     client_secret=CLIENT_SECRET)
```

## Methods Supported

* conversion(input_path, output_path) - general conversion method
* excel_to_pdf, html_to_pdf, image_to_pdf, pdf_to_excel, pdf_to_html, pdf_to_image, pdf_to_powerpoint, pdf_to_text, pdf_to_word, powerpoint_to_word, text_to_pdf, word_to_pdf - all take an input_path and output_path argument
* url_to_pdf(url, output_path) - convert a URL to pdf
* extract(input_path, output_path, type (one of TEXT, IMAGE, PAGE), page_range) - extracts either text, images (zip), or pages (new pdf)

## To Do: 

* remove-password, protect, linearize, combine, compress, flatten, manipulate, split, compare
* Make upload and download public... maybe?
* Make output path optional and just return the doc id
* Make checking a task public and a utility pollTask to handle repeating (this and the previous two methods would let devs chain calls)
