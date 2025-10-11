# Aquí estarán las clases que harán las queries y las configurarán

# Librerias
import tiktoken


# obtiene la querie
class HandlingQueries:

    def __init__(self, input_user: str):
        self.input_user = {"rol" : "user", "content" : input_user}


# Esta clase dirá la cantidad de tokens de las quieres
# o los mostrará 
class tokens_querie:

    def __init__(self, model:str , querie:str):
        self.querie = querie
        self.encoding = tiktoken.encoding_for_model(model)

    # función que obtiene los tokes
    def tokens(self):
        tokens = self.encoding.encode(self.querie)
        return tokens
    
    # dirá la cantidad de tokens
    def count_tokens(self):
        return len(self.tokens())
    
    # retornará los id de tokens
    def get_tokens_id(self):
        return self.tokens()
    
    # retornará un diccionario
    # con keys=id del token : value=token
    def get_tokens(self):
        tokens_id = self.tokens()
        token_list = [self.encoding.decode([t]) for t in tokens_id]
        return dict(zip(tokens_id, token_list))
    

if __name__ == "__main__":
    
    f = tokens_querie(querie="Claro, tu nombre es Héctor. ¿Hay", model="gpt-4o-mini")
    print(f.count_tokens())