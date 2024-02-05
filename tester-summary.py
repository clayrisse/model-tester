from datetime import datetime
import csv
from models import API

# Remember to set KB_ID, KB_URL, API_KEY and GLOBAL_AUTH_TOKEN keys in your .env file

show_log = True
def logger(logger = True):
    global show_log
    show_log = logger

def print_time(line):
    if show_log is True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'.{current_time} | {line}')


models =    [
            # "generative-multilingual-2023",
            "chatgpt-azure-3",
            "chatgpt-azure",
            "anthropic"
            ]

prompts =   [
            "Make a bullet point summary of the following content: text",
            "Make a thorough summary of the following news article: text"
            # "Make a bullet point summary of the following content: \{text\}",
            # "Make a thorough summary of the following news article: \{text\}"
            ]

resources = [
            "4df19a1be2a28f11dca2910fa60b3e00", 
            "03faa53a4fa1b7c84cef3499018ae084"
            ]


headers = ["Models"]
if len(prompts) > 0:
    head_model_prompt = ["Model/Prompt"]
    for model in models:
        for prompt in prompts:
            head_model_prompt.append(f'Model:{model}\n\nP:{prompt}')
    models_summaries = [head_model_prompt]
else:    
    headers.extend(models)
    models_summaries = [headers]



def run_summarize_with_prompting(models, resources, prompts, logs = True,):
    logger(logs)
    print_time(f'\n-------------- Started summarizing {len(models)} diferent models ----------------')


    if len(prompts) > 0:
        for model in models:
            API.set_model(model)       
            summaries = [model]
            for model in models:
                for prompt in prompts:
                    print_time(f'{model} P: {summaries[:40]}')
                    # sum = f'model: {query}\nPrompt: {prompt}'
                    sum = API.summarize(resources, prompt)   
                    summaries.append(sum)

            models_summaries.append(summaries)

    else:   
        for model in models:
            API.set_model(model)   
            summaries = [model]
            for model in models:
                print_time(f'{model} Sumary ')
                sum = f'Model for sumary: {model}\nResources: {resources}'
                sum = API.summarize(resources)   
               
                summaries.append(sum)
                
            models_summaries.append(summaries)

    return models_summaries


def export_to_csv(models_summaries):
    with open('Table_Summary_With_Prompt.csv', 'w', newline='') as file:
    # with open('Table_Summary_No_Prompt.csv', 'w', newline='') as file:
        print_time(f'\n-------------- Started writing process for {len(models_summaries)} models ----------------')
        writer = csv.writer(file)
        
        for answer_row in models_summaries:
            print_time(f'Writing {answer_row[0]} row')
            writer.writerow(answer_row)
    

# ----------------------------

run_summarize_with_prompting(models, resources, prompts)
# run_summarize_with_prompting(models, resources, [])
export_to_csv(models_summaries)

# -------------------- exploring prompting


