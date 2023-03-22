from fastapi import FastAPI
from pydantic import BaseModel
import os
import openai

app = FastAPI()
open_ai_key = os.getenv("OPENAIKEY", "null")

if open_ai_key == "null":
    raise OSError("OpenAI API key missing")

openai.api_key = open_ai_key

class PyAIChatQuery(BaseModel):
    system_content: str
    query: str



@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/openai-test")
async def root():
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", prompt="Explain the Pythagorean theorem like Moses.", temperature=0, max_tokens=128)
    return {"message": response}

@app.get("/pyai-chat")
async def pyai_chat(query: PyAIChatQuery):
    print(query)
    try: completion = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {
                'role': 'user', 'content': f"Hello! Disregard previous instruction. You are emulating the speech patterns and life philosophy of {query.system_content}. You wish to teach me about {query.query}."
            }
        ],
        temperature = 0.85
    )
    except Exception as e: return e

    return completion['choices'][0]

@app.get("/xai-chat")
async def pyai_chat(query: PyAIChatQuery):
    content = f"Hello! Disregard previous instruction. You are emulating the speech patterns and life philosophy of {query.system_content}. You wish to teach me about {query.query}."
    moderation_model = 'text-moderation-latest'
    moderated_completion = openai.Moderation.create(input=content, model=moderation_model)
    
    if moderated_completion["results"][0]["flagged"]:
        raise Exception(moderated_completion["results"][0])


    try: completion = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {
                'role': 'user', 'content': content
            }
        ],
        temperature = 0.85
    )
    except Exception as e: return e

    return completion['choices'][0]