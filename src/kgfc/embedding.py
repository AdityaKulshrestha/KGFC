import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class CodeEmbedder():
    def __init__(self, client: str = "google"):
        if client == "google":
            self.client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
            self.model = "gemini-embedding-exp-03-07"

    def generate_embedding(self, text):
        result = self.client.models.embed_content(
            model=self.model,
            contents=text,
            config=types.EmbedContentConfig(task_type="CODE_RETRIEVAL_QUERY")
        )
        return result.embeddings[0].values

    
