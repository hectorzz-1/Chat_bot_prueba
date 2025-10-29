from abc import ABC, abstractmethod
from typing import List, Dict


class History(ABC):

    @abstractmethod
    def to_dict(self) -> Dict[str, str]:
        # Devuelve el mensaje en formato dict listo para el historial
        pass


class HistoryMessage(History):
    # Clase genérica para representar un mensaje del historial.

    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


# Clases específicas
class HistoryOut(HistoryMessage):
    def __init__(self, out: str):
        super().__init__("assistant", out)


class HistoryUser(HistoryMessage):
    def __init__(self, prompt: str):
        super().__init__("user", prompt)


class HistoryInstructions(HistoryMessage):
    def __init__(self, role: str):
        super().__init__("system", role)


class HistoryManager:
    # Gestiona el historial de conversación del chat

    def __init__(self, history: List[Dict[str, str]] = None):
        self.history = history if history is not None else []

    def add(self, message: History) -> None:
        # Agrega un nuevo mensaje al historial
        self.history.append(message.to_dict())

    def get(self) -> List[Dict[str, str]]:
        # Devuelve el historial completo
        return self.history

    def clear(self) -> None:
        # Vacía el historial.
        self.history.clear()


if __name__ == "__main__" :

    h = HistoryManager([
    {"role": "user", "content": "hola, ¿que tal?"},
    {"role": "assistant", "content": "HOLA, como estás"}
        ])
    
    nu = HistoryUser("mi nombre es Hector")
    na = HistoryOut("un gusto Hector, ¿como estás?")

    h.add(nu)
    h.add(na)

    print(h.get())