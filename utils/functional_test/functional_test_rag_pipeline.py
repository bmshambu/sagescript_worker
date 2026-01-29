
from langchain_core.vectorstores import InMemoryVectorStore
from utils.google_llm_handler import initialize_open_llm_embeddings
import json

class FunctionalTestCaseRAG:
    def __init__(self):
        self.embeddings = initialize_open_llm_embeddings()
        self.retriever = self.initialize_retriever()

    def load_field_metadata(self):
        with open("field_metadata.json", "r", encoding="utf-8") as f:
            return json.load(f)
        
    def field_metadata_to_text_chunks(self):
        field_metadata = self.load_field_metadata()
        if not field_metadata:
            raise ValueError("Field metadata is empty or not loaded correctly.")
        chunks = []
        for field_name, details in field_metadata.items():
            chunk = f"Field: {field_name}"
            for key, value in details.items():
                if value:
                    chunk += f"\n{key.replace('_', ' ').title()}: {value}"
            chunks.append(chunk)
        return chunks

    def initialize_retriever(self):
         # Step 1: Convert to text chunks
        text_chunks = self.field_metadata_to_text_chunks()

        # Step 2: Embed and index
        #embeddings = OpenAIEmbeddings()#
        vectorstore = InMemoryVectorStore.from_texts(text_chunks, embedding=self.embeddings)
        retriever = vectorstore.as_retriever()
        return retriever