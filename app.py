import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)
ocr_model = "mistral-ocr-latest"

def _perform_ocr(url: str) -> str:
    try:   # Apply OCR to the PDF URL
        response = client.ocr.process(
            model=ocr_model,
            document={
                "type": "document_url",
                "document_url": url
                }
            )
    except Exception:
        try:  # IF PDF OCR fails, try Image OCR
            response = client.ocr.process(
                model=ocr_model,
                document={
                    "type": "image_url",
                    "image_url": url
                    }
                )
        except Exception as e:
            return e  # Return the error to the model if it fails, otherwise return the contents
    return "\n\n".join([f"### Page {i+1}\n{response.pages[i].markdown}" for i in range(len(response.pages))])


def main():
    url = input("Enter url:")
    print(_perform_ocr(url))   

if __name__ == "__main__":
    main()