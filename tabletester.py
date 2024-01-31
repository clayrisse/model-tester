from nuclia import sdk
from datetime import datetime
from enum import Enum
import requests
import csv
import os
from dotenv import load_dotenv


def load_keys():
    print("Loading enviorment keys...")
    load_dotenv()

load_keys()

NUCLIA_MANAGEMENT_API = "https://nuclia.cloud/api/v1"
NUCLIA_KB_API = "https://europe-1.nuclia.cloud/api/v1"

def logger(logger = True):
    global show_log
    show_log = logger

def print_time(line):
    if show_log is True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'.{current_time} | {line}')


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
    print_time(f'| | | | | | | | | | Generative model PATCHed from {current_model} ---> {model}')

def search(query, prompt = ""):
    url = f"{NUCLIA_KB_API}/kb/{os.getenv('KB_ID')}/chat"
    response = requests.post(
        url, 
        json={
            "query": query, 
            "prompt": prompt
        },
        headers={
            "Authorization": f"Bearer {os.getenv('GLOBAL_AUTH_TOKEN')}",
            "x-synchronous": "true"
            }
    )

    assert response.status_code == 200
    print_time(f'answering...')
    return response.json()["answer"]
   

questions = [
            "What is a vector", 
            "Who is Eudald", 
            "What is a vector database in a shakespearean tone",
            "What about a prince",
            "Who is bella",
            "What is a vector database in 200 characters",
            "What is a vector databasein 2 paragraphs"
          ]

models = [
        #   "generative-multilingual-2023",
          "chatgpt-azure-3",
          "chatgpt-azure",
          "anthropic",
          "gemini-pro"
          ]

# models2 = [
#             "NO_GENERATION_MODE",
#             "Chat_GPT_3",
#             "Chat_GPT_4",
#             "ANTHROPIC_CLAUDE",
#             "GOOGLE_GEMINI_PRO"
#           ]


headers = ["Models"]
headers.extend(questions)
models_answers = [headers]


def run_search_for_all_models(queries, prompt = "", logs = True, ):
    logger(logs)
    print_time(f'\n-------------- Started searching for {len(queries)} diferent queries ----------------')
    # Switching from SDK to ditect /chat call
    # search = sdk.NucliaSearch()

    for model in models:
        set_model(model)       
        answers = [model]
        for query in queries:
            print_time(f'{model} Q: {query}')
            # ans = f'Question: {q}'
            # ans = search.chat(query=query)
            ans = search(query, prompt)
            answers.append(ans)
            
        models_answers.append(answers)

    return models_answers


def export_to_csv(models_answers):
    with open('model_tester.csv', 'w', newline='') as file:
        print_time(f'\n-------------- Started writing process for {len(models_answers)} models ----------------')
        writer = csv.writer(file)
        
        for answer_row in models_answers:
            print_time(f'Writing {answer_row[0]} row')
            writer.writerow(answer_row)
    

# ----------------------------


# models_answers = run_search_for_all_models(questions, "", False)
models_answers = run_search_for_all_models(questions)
export_to_csv(models_answers)

# -------------------- exploring prompting


