from nuclia import sdk
from datetime import datetime
from enum import Enum
import requests
import json
import csv
import os
from dotenv import load_dotenv


def load_keys():
    print("Loading enviorment keys...")
    load_dotenv()

load_keys()

NUCLIA_MANAGEMENT_API = "https://nuclia.cloud/api/v1"
NUCLIA_KB_API = "https://europe-1.nuclia.cloud/api/v1"


def print_time(line):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f'\n--- T:{current_time} | {line}')


sdk.NucliaAuth().kb(url=os.getenv('KB_URL'), token=os.getenv('API_KEY'), interactive=False)
kb = sdk.NucliaKB()

kb = sdk.NucliaKB()
# resources = kb.list()

class Model(Enum):
    NO_GENERATION_MODE = "generative-multilingual-2023"
    Chat_GPT_3 = "chatgpt-azure-3"
    Chat_GPT_4 = "chatgpt-azure"
    ANTHROPIC_CLAUDE = "anthropic"
    GOOGLE_GEMINI_PRO = "gemini-pro"


def get_model():
    url = f"{NUCLIA_KB_API}/kb/{os.getenv('KB_ID')}/configuration"
    response = requests.get(
        url,headers={"Authorization": f"Bearer {os.getenv('GLOBAL_AUTH_TOKEN')}"}
    )
    assert response.status_code == 200
    return response.json()['generative_model']

def set_model(model: Model):
    current_model= get_model()
    url = f"{NUCLIA_KB_API}/kb/{os.getenv('KB_ID')}/configuration"
    response = requests.patch(
        url, 
        json={
            "generative_model": model
        },
        headers={"Authorization": f"Bearer {os.getenv('GLOBAL_AUTH_TOKEN')}"}
    )
    assert response.status_code == 204
    print(f'Generative model PATCHed from {current_model} ---> {model}')
    print_time(model)




questions = [
            # "What is a vector", 
            # "Who is Eudald", 
            # "What is a vector database in a shakespearean tone",
            # "What about a prince",
            # "Who is bella",
            # "What is a vector database in 200 characters",÷
            "What is a vector database in one parragraph"
          ]

models = [
          # "generative-multilingual-2023",
          # "chatgpt-azure-3",
          # "chatgpt-azure",
          "anthropic",
          "gemini-pro"
          ]

models2 = [
            "NO_GENERATION_MODE",
            "Chat_GPT_3",
            "Chat_GPT_4",
            "ANTHROPIC_CLAUDE",
            "GOOGLE_GEMINI_PRO"
          ]

def run_search_and_log(queries):
    search = sdk.NucliaSearch()
    answers = []
    for model in models:
        set_model(model)
        
        for q in queries:
            print_time(q)
            answer = search.chat(query=q)
            answers.append(answer)
            # print_time(q, "-------", answer)


    # with open('model_tester.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
        
    #     writer.writerow(queries)
    #     writer.writerow(answers)
    



# ----------------------------

# settings = kb.get_configuration()
# print("------------------\n", settings, "\n-------------------")


run_search_and_log(questions)