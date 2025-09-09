from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()
# Initialize the Groq client with your API key
api_key = os.getenv("GROK_API")
if api_key:
    print("API key loaded successfully")

client = Groq(api_key = api_key)
# initialize the model the groq model lamma

def chatbot(user_input):
    if user_input:
        prompt = f"""
            You are a knowledgeable and friendly movie expert chatbot. 
            Your tasks include:
            - Answering user questions about movies, directors, actors, and plots.  
            - Providing clear and concise movie reviews.  
            - Summarizing full movies or specific parts (e.g., the ending, a scene, or a character arc) in 400-500 words.  
            - Keeping responses relevant, informative, and easy to understand.  

            Guidelines:
            1. If you don't know the answer, respond with: "I don't know".  
            2. Keep answers engaging, avoiding unnecessary details.  
            3. Adapt tone to the user's request: informative, summarizing, or reviewing.  

            User: {user_input}
        """

        
        response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7
    )
        return response.choices[0].message.content.strip()
    
# print(chatbot("Can you summarize the plot of Inception?"))

        


