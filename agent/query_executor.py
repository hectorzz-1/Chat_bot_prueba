from db.models_db import TableAgent

# Le hace la query al cerebro de OpenAI
class QueryExecutor:

    def __init__(self,brain : str, agent: TableAgent):
        self.brain = brain
        self.agent = agent
    
    def make_query(self, conversation: list[dict]):
        try:
            # Coloca los parametros y configuraciones
            response = self.brain.chat.completions.create(
                model=self.agent.model,
                messages=conversation,
                temperature=self.agent.temperature,
                max_tokens=self.agent.max_tokens,
                presence_penalty=self.agent.presence_penalty,
                frequency_penalty=self.agent.frequency_penalty,
            )

            # Retorna la respuesta del bot
            return response.choices[0].message.content
    
        except Exception as e:
            return f"Error: {str(e)}"