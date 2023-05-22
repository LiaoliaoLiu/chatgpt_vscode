#%%
import openai
import os
import datetime
import json

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai.api_key  = os.getenv('OPENAI_API_KEY')

from IPython.core.display import display, Markdown
from redlines import Redlines

def output(string):
    return display(Markdown(string))

def output_diff(comp, main):
    return output(Redlines(comp, main))

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

class Dialogue:
    def __init__(self, model = 3, context_file = '', system = '') -> None:
        self.persistence = context_file if context_file else os.path.join(os.getcwd(), '.context.json')
        self.load_context()
        self.set_system(system)
        self.model = 'gpt-3.5-turbo' if model != 4 else 'gpt-4'

    def ask(self, prompt, temperature=0):
        self.context.append({'role':'user', 'content':f"{prompt}"})
        response = get_completion_from_messages(self.context, self.model, temperature) 
        self.context.append({'role':'assistant', 'content':f"{response}"})
        self.save_context()
        output(response)
        return response
    
    def set_system(self, content):
        """
        system is basically an initial prompt to do role-playing to have a rough context, see doc
        https://platform.openai.com/docs/guides/chat/chat-vs-completions
        """
        self.context[0]['content'] = content

    def load_context(self):
        try:
            with open(self.persistence, 'r') as f:
                self.context = json.load(f)
        except FileNotFoundError:
            self.context =  [ {'role':'system', 'content':''} ]
            with open(self.persistence, 'w') as f:
                json.dump(self.context, f)
    
    def save_context(self):
        with open(self.persistence, 'w') as f:
            json.dump(self.context, f)

    def backup_context(self):
        now = datetime.datetime.now().timestamp()
        backup_file = 'context-' + str(now) + '.json'
        with open(backup_file, 'w') as f:
            json.dump(self.context, f)

d = Dialogue(4)

# %%
