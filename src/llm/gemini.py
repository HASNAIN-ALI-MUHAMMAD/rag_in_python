from src.envs import Env
from google import genai

class LLMGemini:
    client: genai.Client

    def __init__(self):
        # self.model = model
        # self.temperature = temperature
        self.client = genai.Client(api_key=Env.get('GOOGLE_API_KEY'))

    # def generate_text(self, prompt: str) -> str:
    #     response = self.client.models.generate_content(
    #         model="gemini-2.5-flash",
    #         contents = f"{prompt}",
    #         # config=types.TextConfig(temperature=self.temperature, max_output_tokens=1024)
    #     )
    #     return response.text
    
    def embed_text(self, text: str):
        response = self.client.models.embed_content(
            model= "gemini-embedding-001",
            contents=[text],
            config=genai.types.EmbedContentConfig(output_dimensionality=1536)
        )
        return response.embeddings[0].values