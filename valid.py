
from typing import List, Dict
from pympler import asizeof
from abc import ABC, abstractmethod


# Esta clase valida si puso menos de los tokens maximos permitidos
# Si hay menos tokens que el maximo permitido --> True
# Si hay más tokens que el maximo permitido --> False
class TokensValid:


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
    


class Meter(ABC):
     
    @abstractmethod
    def size_m(self):
        pass


class MeterKB(Meter):
    def size_m(self, size_bytes):
        # Devuelve el tamaño en kilobytes
        return size_bytes / 1024
    

class MeterMB(Meter):
    def size_m(self, size_bytes):
        # Devuelve el tamaño en megabytes
        return size_bytes / (1024 ** 2)



class HistoryValid:
    def __init__(self, history: List[Dict[str, str]], max_bytes: int, meter: Meter):
        self.history = history
        self.max_bytes = max_bytes
        self.meter = meter

    def size_bytes(self) -> int:
        # Devuelve el tamaño total del objeto en bytes
        return asizeof.asizeof(self.history)

    def meter_bytes(self) -> float:
        # Devuelve el tamaño convertido según el medidor (KB o MB)
        s_bytes = self.size_bytes()
        return self.meter.size_m(s_bytes)

    def count_max_bytes(self) -> bool:
        # Devuelve True si está dentro del límite de memoria
        size = self.size_bytes()
        return size <= self.max_bytes
    

if __name__ == "__main__":
    
    history = [{"role": "user", "content": "x" * 5000}]

    max_bytes = 5 * 1024  # 10 KB

    validator = HistoryValid(history, max_bytes, meter=MeterKB())

    print(f"Tamaño actual: {validator.meter_bytes():.2f} KB")
    print(f"Límite máximo: {max_bytes / 1024} KB")

    print(validator.count_max_bytes())
 