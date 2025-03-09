import os 
import asyncio
import streamlit as st 
from langchain_community.vectorstores import Chroma 
from langchain_openai import ChatOpenAI 
from langchain.chains import create_history_aware_retriever 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain 
from langchain.chains import create_retrieval_chain 
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain.chains import RetrievalQA
from langchain_core.messages import HumanMessage, AIMessage 
import urllib.parse
import base64
from dotenv import load_doadenv 



DB_PATH = "renesas_knowledge_db"

# ✅ Load Embeddings
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en", encode_kwargs={'normalize_embeddings': True})
st.sidebar.success("Embeddings loaded successfully")

# ✅ Load Chroma Vector Store
vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={'k': 2})
st.sidebar.success("Chroma retrieval ready!")

# ✅ Load LLM (ChatGPT)
llm = ChatOpenAI(
    model_name="gpt-4o",
    api_key=""
)
st.title("LLM with PDF and Image Retrieval gPT 4 vision")
user_input = st.text_area("Ask a question:", key="user_query")
uploaded_file = st.file_uploader("Upload an image (optional):", type=["png","jpg","jpeg"])

def encode_image(image_file):
    if image_file is not None:
        image_bytes = image_file.read()
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        return base64_image 
    return None 



if st.button("Submit"):
    if user_input:
        with st.spinner("Fetching docs.."):

            retrieved_docs = retriever.invoke(user_input)
            st.write(f"retrieved_docs = {retrieved_docs}")
            if retrieved_docs:
                references = []
                image_paths_str= retrieved_docs[0].metadata.get("images",[])
                image_paths = image_paths_str.split(", ") if image_paths_str else []
                for doc in retrieved_docs:
                    category = doc.metadata.get("category","Unknown Category")
                    subcategory = doc.metadata.get("subcategory","Unknown Category")
                    filename = doc.metadata.get("source","unknown source")
                    references.append (f"Refeences: {category}/{subcategory}/{filename}")
                
                custom_prompt = f"""
                Answer the following question based on the document provided.
                
                If any image is related to the answer, explicitly say:
                'Here is the image related to your query:'
                Describe the image as you understand it from context.
                
                Do not apologize for not displaying images. If images exist, refer to them confidently.

                
                --------------------
                Question: {user_input}
                """
                
                # response_text=""
                # st.write(f"image_paths = {image_paths}")
                # if image_paths:
                #     for image_path in image_paths:
                #         if os.path.exists(image_path):
                #             st.image(image_path, caption="Image from document", use_container_width=True)
                #             response_text = f"Here is the image from the doc: {image_path}"

                qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")
                answer = qa_chain.run(custom_prompt)
                st.subheader("LLM Answer:")
                st.markdown(answer)

                if references:
                    st.subheader("References")
                    for reference in references:
                        st.write(reference)

                if image_paths:
                    st.subheader("🖼 Relevant Image from Document:")
                    for image_path in image_paths:
                        if os.path.exists(image_path):
                            st.image(image_path, caption="🖼 Image from Document", use_container_width=True)

                #st.write(response_text)
            else:
                st.write("No relevant content found.")


