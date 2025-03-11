# Renesas Bot Electronics Design Support Agent  
Create RAG based electronic design assistant for Renesas Electronics that can consume all information in the Renesas KnowledgeBase here: https://en-support.renesas.com/knowledgeBase  
This bot should be able to answer any questions related to information available in the knowledge base.  
Image present in the knowledge base should be included in the answer wherever relevant.  
Add reference to the pages based on which the answers were given.  
User may send hand drawn sketches or images to the bot along with their query and bot should be able to answer that.  
In case the information cannot be found in the knowledgebase with goog enough confidence, the bot should be able to invoke another agent to search across all of renesas.com for possible answers.  
This bot needs to be deployed on the cloud with a streamlit interface.  

# Find the detailed report in report.pdf  

# Commands  
python -m venv venv  
Set -ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser  
venv\Scripts\activate  

------------------------
