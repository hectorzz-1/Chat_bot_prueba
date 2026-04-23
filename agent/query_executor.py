# Le hace la query al cerebro de OpenAI
class QueryExecutor:

    def __init__(self,brain : str, agent:dict):
        self.brain = brain
        self.agent = agent
    
    def make_query(self):
        try:
            # Coloca los parametros y configuraciones
            response = self.brain.chat.completions.create(
                model=self.agent["model"],
                messages=self.agent["memory"],
                temperature=self.agent["temperature"],
                max_tokens=self.agent["max_tokens"],
                presence_penalty=self.agent["presence_penalty"],
                frequency_penalty=self.agent["frequency_penalty"]
            )

            # Retorna la respuesta del bot
            return response.choices[0].message.content
    
        except Exception as e:
            return f"Error: {str(e)}"