import openai
from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env
openai.api_key = os.getenv('OPENAI_KEY')  # Set the API key
client = OpenAI()

def send_openai(context: list[str]):
    msgs = [{"role": "developer", "content": "You are my smartest assistant that can help me with any type of tasks asked to you"}]
    i_to_role = lambda i: "assistant" if i%2 else "user"
    for i, msg in enumerate(context):
        msgs.append({"role": i_to_role(i), "content":msg})
    
    
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=msgs,
        stream=True,
    )
    for chunk in stream:
        yield chunk  # Yield each chunk as it comes in