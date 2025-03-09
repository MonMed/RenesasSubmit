import os 
import json 
import fitz 

PDF_DIR = "KnowledgeBase"
OUTPUT_JSON_DIR = "Extracted_JSONS"
os.makedirs(OUTPUT_JSON_DIR, exist_ok=True)

def extract_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text=""
    images = []

    for page in doc:
        text += page.get_text("text") + "\n\n"
        
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            img_bytes = base_image["image"]
            img_filename = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_image_{img_index}.jpg"
            img_path = os.path.join(os.path.dirname(pdf_path), "images", img_filename)

            # Save the image to local folder
            os.makedirs(os.path.join(os.path.dirname(pdf_path), "images"), exist_ok=True)
            with open(img_path, "wb") as img_file:
                img_file.write(img_bytes)

            
            images.append(img_path)
    
    return text.strip(), images

def save_to_json(pdf_name, text, images, category, subcategory):
    json_folder = os.path.join(OUTPUT_JSON_DIR, category, subcategory)
    os.makedirs(json_folder, exist_ok = True)

    json_path = os.path.join(json_folder, f"{pdf_name}.json")

    data = {
        "filename":pdf_name,
        "category":category,
        "subcategory":subcategory,
        "content":text,
        "images": images
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    
    print(f"JSON saved: {json_path}")

def process_all_pdfs(pdf_root_dir):
    for category in os.listdir(pdf_root_dir):
        category_path = os.path.join(pdf_root_dir, category)
        if not os.path.isdir(category_path):
            continue 

        for subcategory in os.listdir(category_path):
            subcategory_path = os.path.join(category_path, subcategory)
            if not os.path.isdir(subcategory_path):
                continue

            for pdf_file in os.listdir(subcategory_path):
                if pdf_file.endswith(".pdf"):
                    pdf_path = os.path.join(subcategory_path, pdf_file)
                    pdf_name = os.path.splitext(pdf_file)[0]
                    print(f"Processing: {pdf_name}")

                    extracted_text, images = extract_pdf(pdf_path)
                    save_to_json(pdf_name, extracted_text, images, category, subcategory)

process_all_pdfs(PDF_DIR)
print("\n All PDFs have been process and stored as JSONs.")




