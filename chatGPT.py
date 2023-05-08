#%%
import openai
import os

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
    context =  [ {'role':'system', 'content':''} ]
    model = 'gpt-3.5-turbo'
    def __init__(self, model = 3, system = '') -> None:
        self.set_system(system)
        if model == 4:
            self.model = 'gpt-4'
        else:
            self.model = 'gpt-3.5-turbo'

    def ask(self, prompt, temperature=0):
        self.context.append({'role':'user', 'content':f"{prompt}"})
        response = get_completion_from_messages(self.context, self.model, temperature) 
        self.context.append({'role':'assistant', 'content':f"{response}"})
        output(response)
        return response
    
    def set_system(self, content):
        self.context[0]['content'] = content



# %%
# d = Dialogue(4)
# d.ask("how to export all the packages I install in the current conda environment?")

