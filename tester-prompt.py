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


questions = [
            "What is a vector database?",
            "What is a vector", 
            "What is and emmbeding",
            "Who is Eudald",
            # "What is a vector database in a shakespearean tone",
            # "What about a prince",
            # "Who is bella",
            # "What is a vector database in 200 characters",
            ]

models =    [
            # "generative-multilingual-2023",
            "chatgpt-azure-3",
            "chatgpt-azure",
            "gemini-pro",
            "anthropic"
            ]

prompts =   [
            "Give a detailed answer to this question in a list format. "
            "Answer this question always in French",
            "Answer in bulletpoints"
            # "Give a detailed answer to this \{question\} in a list format.  If you do not find an answer in this context: \{context\}, say that you don't have enough data.",
            # "Answer this \{question\} in a concise way",
            # "Answer this \{question\} always in French"
            ]


headers = ["Questions"]
if len(prompts) > 0:
    head_query_prompt = ["Query/Prompt"]
    for question in questions:
        for prompt in prompts:
            head_query_prompt.append(f'Q:{question}\n\nP:{prompt}')
    models_answers = [head_query_prompt]
else:    
    headers.extend(questions)
    models_answers = [headers]



def run_search_for_all_models(queries, prompts = [], logs = True, ):
    logger(logs)
    print_time(f'\n-------------- Started searching for {len(queries)} diferent queries ----------------')


    if len(prompts) > 0:
        for model in models:
            API.set_model(model)       
            answers = [model]
            for query in questions:
                for prompt in prompts:
                    print_time(f'{model} | Q: {query[:40]} | P: {prompt[:60]}')
                    # ans = f'Question: {query}\nPrompt: {prompt}'
                    ans = API.search(query, prompt)
                    answers.append(ans)

            models_answers.append(answers)

    else:   
        for model in models:
            API.set_model(model)       
            answers = [model]
            for query in queries:
                print_time(f'{model} Q: {query[:50]} ')
                # ans = f'Question: {query}\nPrompt: {prompt}'
                ans = API.search(query)
                answers.append(ans)
                
            models_answers.append(answers)

    return models_answers


def export_to_csv(models_answers):
    # with open('Table_Models_No_Prompt.csv', 'w', newline='') as file:
    with open('Table_Models_With_Prompt.csv', 'w', newline='') as file:
        print_time(f'\n-------------- Started writing process for {len(models_answers)} models ----------------')
        writer = csv.writer(file)
        
        for answer_row in models_answers:
            print_time(f'Writing {answer_row[0]} row')
            writer.writerow(answer_row)
    

# ----------------------------


# models_answers = run_search_for_all_models(questions, [], False)
# models_answers = run_search_for_all_models(questions, [])
            
models_answers = run_search_for_all_models(questions, prompts)
export_to_csv(models_answers)

# -------------------- exploring prompting


