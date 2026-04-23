import tiktoken

# Esta clase dirá la cantidad de tokens de las quieres
# o los mostrará 
class TokensQuery:

    def __init__(self, model:str , query:str):
        self.query = query
        self.encoding = tiktoken.encoding_for_model(model)

    # función que obtiene los tokes
    def tokens(self):
        tokens = self.encoding.encode(self.query)
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
    

# Sirve para controlar los limites de usos de tokens
class TokensValid:

    def __init__(self, tokens: int, max_tokens: int = 250):
        # Validaciones
        if not isinstance(tokens, int):
            raise TypeError("El valor de 'tokens' debe ser un número entero.")
        if not isinstance(max_tokens, int):
            raise TypeError("El valor de 'max_tokens' debe ser un número entero.")
        if tokens < 0:
            raise ValueError("El número de tokens no puede ser negativo.")
        if max_tokens <= 0:
            raise ValueError("El número máximo de tokens debe ser positivo.")

        self.tokens = tokens
        self.max_tokens = max_tokens

    #Retorna cuántos tokens quedan disponibles antes de alcanzar el límite.
    def remaining(self) -> int:
        return max(0, self.max_tokens - self.tokens)