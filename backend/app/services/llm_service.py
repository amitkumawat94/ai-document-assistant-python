from groq import Groq

from app.config import settings


class LLMService:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = settings.groq_model

    def generate_answer(self, question: str, context: str) -> str:
        prompt = f"""
Answer the user's question using only the provided context.

If the answer cannot be found in the context, say:
"I couldn't find the answer in the provided documents."

Context:
{context}

Question:
{question}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful document assistant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content


llm_service = LLMService()