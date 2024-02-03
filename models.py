
from datetime import datetime
from enum import Enum
import requests
import os
from dotenv import load_dotenv

# Remember to set KB_ID, KB_URL, API_KEY and GLOBAL_AUTH_TOKEN keys in your .env file

def load_keys():
    print("Loading enviorment keys...")
    load_dotenv()

load_keys()

NUCLIA_MANAGEMENT_API = "https://nuclia.cloud/api/v1"
NUCLIA_KB_API = f'https://{os.getenv("KB_ZONE")}.nuclia.cloud/api/v1'

show_log = True
def logger(logger = True):
    global show_log
    show_log = logger

def print_time(line):
    if show_log is True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'.{current_time} | {line}')


# class Model(Enum):
#     NO_GENERATION_MODE = ["generative-multilingual-2023", ""]
#     Chat_GPT_3 = ["chatgpt-azure-3", f'Input here your prompt with the words {context} and {question} in brackets where you want those fields to be placed, in case you want them in your prompt. For this generative model {chat_history} is not available to modify in the prompt']
#     Chat_GPT_4 = ["chatgpt-azure", f'Input here your prompt with the words {context} and {question} in brackets where you want those fields to be placed, in case you want them in your prompt. For this generative model {chat_history} is not available to modify in the prompt']
#     ANTHROPIC_CLAUDE = ["anthropic",f'Input here your prompt with the words{chat_history}, {context} and {question} in brackets where you want those fields to be placed, in case you want them in your prompt.']
#     GOOGLE_GEMINI_PRO = ["gemini-pro", f'Input here your prompt with the words {context} and {question} in brackets where you want those fields to be placed, in case you want them in your prompt. For this generative model {chat_history} is not available to modify in the prompt']

class API:
    def get_model():
        url = f'{NUCLIA_KB_API}/kb/{os.getenv("KB_ID")}/configuration'
        response = requests.get(
            url,headers={"Authorization": f"Bearer {os.getenv('GLOBAL_AUTH_TOKEN')}"}
        )
        assert response.status_code == 200
        return response.json()['generative_model']


    def set_model(model):
        current_model= API.get_model()
        url = f'{NUCLIA_KB_API}/kb/{os.getenv("KB_ID")}/configuration'
        response = requests.patch(
            url, 
            json={
                "generative_model": model
            },
            headers={"Authorization": f"Bearer {os.getenv('GLOBAL_AUTH_TOKEN')}"}
        )
        assert response.status_code == 204
        print_time(f'| | | | | | | | | | Generative model PATCHed from {current_model} ---> {model}')


    def search(query, prompt = ""):
        print_time(f'answering in...')
        url = f'{NUCLIA_KB_API}/kb/{os.getenv("KB_ID")}/chat'
        response = requests.post(
            url, 
            json={
                "query": query, 
                "prompt": prompt
            },
            headers={
                "Authorization": f'Bearer {os.getenv("GLOBAL_AUTH_TOKEN")}',
                "x-synchronous": "true"
                }
        )

        print_time(f'answering out......')
        assert response.status_code == 200
        return response.json()["answer"]

    def summarize(resources=["4df19a1be2a28f11dca2910fa60b3e00"], prompt = ""):
        print_time(f'summarizing...')
        url = f'{NUCLIA_KB_API}/kb/{os.getenv("KB_ID")}/summarize'
        response = requests.post(
            url, 
            json={
                "resources": resources,
                "user_prompt": prompt
            },
            headers={
                "Authorization": f'Bearer {os.getenv("GLOBAL_AUTH_TOKEN")}',
                # "x-synchronous": "true"
                }
        )
        # print(response.json())
        assert response.status_code == 200
        print_time(f'summarized......')
        return response.json()["summary"]



