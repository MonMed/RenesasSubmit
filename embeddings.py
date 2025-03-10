import os 
import json
from langchain.schema import Document 
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings 

OUTPUT_JSON_DIR = "Extracted_JSONS"
DB_PATH = "renesas_knowledge_db"

def load_json_docs(folder):
    json_docs = []
    for category in os.listdir(folder):
        category_path = os.path.join(folder, category)
        if not os.path.isdir(category_path):
            continue

        for subcategory in os.listdir(category_path):
            subcategory_path = os.path.join(category_path, subcategory)
            if not os.path.isdir(subcategory_path):
                continue 

            for filename in os.listdir(subcategory_path):
                if filename.endswith(".json"):
                    file_path = os.path.join(subcategory_path, filename)
                    with open(file_path, "r",encoding="utf-8") as file:
                        data=json.load(file)
                        text_content = f"Category:{category}\nSubCategory:{subcategory}\n{data.get('content',"")}"

                        image_list = data.get("images", [])
                        image_str = ", ".join(image_list) if image_list else "No Images"

                        json_docs.append(Document(
                            page_content=text_content,
                            metadata={
                                "source":filename,
                                "category":category, 
                                "subcategory":subcategory, 
                                "images": image_str
                                }
                        ))
    return json_docs

print("Loading json files...")
documents = load_json_docs(OUTPUT_JSON_DIR)
print(documents)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2", encode_kwargs={'normalize_embeddings':True})

vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=DB_PATH)
print(f"ChromDB Succesfully saved in {DB_PATH}")


