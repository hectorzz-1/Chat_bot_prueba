

# Esta clase valida si puso menos de los tokens maximos permitidos
# Si hay menos tokens que el maximo permitido --> True
# Si hay más tokens que el maximo permitido --> False
class Tokensvalid:


    def __init__(self, tokens: int, max_tokens: int = 25):
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

    #Retorna True si los tokens no superan el máximo permitido.
    def is_valid(self) -> bool:
        return self.tokens <= self.max_tokens

    #Retorna cuántos tokens quedan disponibles antes de alcanzar el límite.
    def remaining(self) -> int:
        return max(0, self.max_tokens - self.tokens)
    
