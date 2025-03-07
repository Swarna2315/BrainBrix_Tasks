import os
import groq
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def ask_groq(question, context):
    """Sends a prompt to Groq's LLM API and returns the response."""
    if not GROQ_API_KEY:
        return "Error: Groq API Key not found!"

    client = groq.Client(api_key=GROQ_API_KEY)
    
    prompt = f"Here is some information from a PDF:\n\n{context}\n\nUser's question: {question}\n\nAnswer:"
    
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  
            messages=[
                {"role": "system", "content": "You are an AI assistant that answers based on the provided document."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error with Groq API: {e}")
        return "Sorry, I couldn't process your request."
