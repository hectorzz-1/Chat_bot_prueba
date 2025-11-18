# Crea la configuración de los chats

from abc import ABC, abstractmethod
from openai import OpenAI



class Querie(ABC):

    @abstractmethod
    def make_querie(self) -> dict:
        pass


class BasicQuierie(Querie):

    def __init__(self,api, history:list, model:str):
        self.api = api
        self.history = history
        self.model = model

    def make_querie(self) -> dict:
        try: 
            response = self.api.chat.completions.create(
                model=self.model,
                messages=self.history 
            )
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error: {str(e)}"
        

class MediunQuerie(Querie):
    
    def __init__(self,api, config:dict):
        self.api = api
        self.config = config

    def make_querie(self) -> dict:
        try: 
            response = self.api.chat.completions.create(
                model=self.config["model"],
                messages=self.config["memory"],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                presence_penalty=self.config["presence_penalty"],
                frequency_penalty=self.config["frequency_penalty"]
            )
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error: {str(e)}"
        

class HardQuerie(Querie):

    def __init__(self,brain : str, agent:dict):
        self.brain = brain
        self.agent = agent
    
    def make_querie(self):
        try:

            response = self.brain.chat.completions.create(
                model=self.agent["model"],
                messages=self.agent["memory"],
                temperature=self.agent["temperature"],
                max_tokens=self.agent["max_tokens"],
                presence_penalty=self.agent["presence_penalty"],
                frequency_penalty=self.agent["frequency_penalty"]
            )

            return response.choices[0].message.content
    
        except Exception as e:
            return f"Error: {str(e)}"
    

if __name__ == "__main__":
    h = [
        {"role": "system", "content": "asistente de IA, amigable y siempre termina su mensaje con la palabra periguayo"},
        {"role": "user", "content": "mi nombre es hector"},
        {"role": "assistant", "content": "Un gusto Héctor, ¿en que puedo ayudarte hoy?"},
        {"role": "user", "content": "se me ólvido mi nombre me lo recuerdas?"}
    ]
    m = "gpt-4o-mini"
    q = {
        "temperature": 1.0,
        "max_tokens": 10,
        "presence_penalty": 0.4,
        "frequency_penalty": 0.4,
        "name": "new chat"
    }

    c = MediunQuerie(history=h,model=m,config=q)
    fg = c.make_querie()
    print(fg)

