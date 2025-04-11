from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
IMAGE_FOLDER = "images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

@app.route('/extract-images', methods=['POST'])
def extract_images():
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file part in the request"}), 400

    file = request.files['pdf']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    pdf_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.pdf")
    file.save(pdf_path)

    image_paths = []
    doc = fitz.open(pdf_path)
    for page_index in range(len(doc)):
        for img_index, img in enumerate(doc.get_page_images(page_index)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"{uuid.uuid4()}.{image_ext}"
            image_path = os.path.join(IMAGE_FOLDER, image_filename)

            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
                image_paths.append(image_filename)

    doc.close()
    os.remove(pdf_path)

    return jsonify({"extracted_images": image_paths})


if __name__ == '__main__':
    app.run(debug=True)
