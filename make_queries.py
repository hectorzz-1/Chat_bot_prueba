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
    
    def __init__(self,api, history:list, model:str, config:dict):
        self.api = api
        self.history = history
        self.model = model
        self.config = config

    def make_querie(self) -> dict:
        try: 
            response = self.api.chat.completions.create(
                model=self.model,
                messages=self.history,
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                presence_penalty=self.config["presence_penalty"],
                frequency_penalty=self.config["frequency_penalty"]
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
    a = OpenAI(api_key="")
    m = "gpt-4o-mini"
    q = {
        "temperature": 1.0,
        "max_tokens": 10,
        "presence_penalty": 0.4,
        "frequency_penalty": 0.4,
        "name": "new chat"
    }

    c = MediunQuerie(api=a, history=h,model=m,config=q)
    fg = c.make_querie()
    print(fg)



