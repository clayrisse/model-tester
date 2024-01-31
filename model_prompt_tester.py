# from nuclia import sdk
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


# sdk.NucliaAuth().kb(url=os.getenv('KB_URL'), token=os.getenv('API_KEY'), interactive=False)
# kb = sdk.NucliaKB()

# kb = sdk.NucliaKB()
# # resources = kb.list()
context = ''
question = ''
chat_history = ''

class Model(Enum):
    NO_GENERATION_MODE = ["generative-multilingual-2023", ""]
    Chat_GPT_3 = ["chatgpt-azure-3", f'Input here your prompt with the words {context} and {question} in brackets where you want those fields to be placed, in case you want them in your prompt. For this generative model {chat_history} is not available to modify in the prompt']
    Chat_GPT_4 = ["chatgpt-azure", f'Input here your prompt with the words {context} and {question} in brackets where you want those fields to be placed, in case you want them in your prompt. For this generative model {chat_history} is not available to modify in the prompt']
    ANTHROPIC_CLAUDE = ["anthropic",f'Input here your prompt with the words{chat_history}, {context} and {question} in brackets where you want those fields to be placed, in case you want them in your prompt.']
    GOOGLE_GEMINI_PRO = ["gemini-pro", f'Input here your prompt with the words {context} and {question} in brackets where you want those fields to be placed, in case you want them in your prompt. For this generative model {chat_history} is not available to modify in the prompt']


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
    print_time(f'answering...')
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
    print_time(f'answering......')
    return response.json()["answer"]
   

questions = [
            "What is a vector", 
            "Who is Eudald", 
            "What is a vector database in a shakespearean tone",
            # "What about a prince",
            # "Who is bella",
            "What is a vector database in 200 characters",
            "What is a vector database in 2 paragraphs"
            ]

models =    [
            # "generative-multilingual-2023",
            "chatgpt-azure-3",
            "chatgpt-azure",
            "anthropic",
            "gemini-pro"
            ]

# prompts = None
prompts =   [
            "Give a detailed answer to this question in a list format. ",
            "Answer this question always in French"
            "Answer in bulletpoints",
            # "Give a detailed answer to this \{question\} in a list format.  If you do not find an answer in this context: \{context\}, say that you don't have enough data.",
            # "Answer this \{question\} in a concise way",
            # "Answer this \{question\} always in French"
            ]

# models2 = [
#             "NO_GENERATION_MODE",
#             "Chat_GPT_3",
#             "Chat_GPT_4",
#             "ANTHROPIC_CLAUDE",
#             "GOOGLE_GEMINI_PRO"
#           ]


headers = ["Questions"]


# if prompts in globals():
if prompts is not None:
    headers_promps = ["Propmts"]
    for question in questions:
        print(question)
        for prompt in prompts:
            headers.append(question)
            headers_promps.append(prompt)
    models_answers = [headers, headers_promps]
else:    
    headers.extend(questions)
    models_answers = [headers]



def run_search_for_all_models(queries, prompts, logs = True, ):
    logger(logs)
    print_time(f'\n-------------- Started searching for {len(queries)} diferent queries ----------------')


    if prompts is not None:
        headers_promps = ["Prompts"]
        for model in models:
            set_model(model)       
            answers = [model]
            for query in questions:
                for prompt in prompts:
                    print_time(f'{model} | Q: {query[:40]} | P: {prompt[:60]}')
                    # ans = f'Question: {query}\nPrompt: {prompt}'
                    ans = search(query, prompt)
                    answers.append(ans)

            models_answers.append(answers)

    else:   
        for model in models:
            set_model(model)       
            answers = [model]
            for query in queries:
                print_time(f'{model} Q: {query[:50]} P: {prompt[:60]}')
                # ans = f'Question: {query}\nPrompt: {prompt}'
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


# models_answers = run_search_for_all_models(questions, prompts, False)
# print(search("what is a vector database"))
models_answers = run_search_for_all_models(questions, prompts)
export_to_csv(models_answers)

# -------------------- exploring prompting


