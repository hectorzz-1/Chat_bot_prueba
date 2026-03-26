# Librerias
import json
from pathlib import Path
from dataclasses import dataclass, fields, field

from config import BASE_DIR

# Clase base
class JsonTools:

    def to_dict(self):
        # Convierte atributos de dataclass a diccionario, excluyendo los con metadata exclude=True
        result = {}
        for f in fields(self):
            if not f.metadata.get("exclude", False):
                result[f.name] = getattr(self, f.name)
        return result

    # Cargamos el json
    # si no existe o está vacio retornamos None
    def load_json(self, file: Path):
        try:
            # Si no existe retornamos None
            if not file.exists():
                return None

            # Si está vacío retornamos None
            if file.stat().st_size == 0:
                return None

            # Cargamos el json y lo retoramos
            with file.open("r") as f:
                return json.load(f)
            
        # Si el json no es valido
        except json.JSONDecodeError:
            raise ValueError(f"{file} is not valid JSON")
        # Si el json no existe
        except FileNotFoundError:
            raise FileNotFoundError(f"{self.file} does not exist")


@dataclass
class JsonAddConfig(JsonTools):
    file: Path = field(metadata={"exclude": True})

    temperature: float = 1.0
    max_tokens: int = 350
    max_input_tokens: int = 400
    presence_penalty: float = 0.4
    frequency_penalty: float = 0.4
    model: str = "gpt-4o-mini"
    tokens: int = 0
    name: str = "new chat"
    role: str = "system"
    content: str = "Un asistente amigable que busca ayudar al resto"
    

    # Hacemos la estructura
    def _build_structure(self):
        # Diccionario con todos los atributos 
        base = self.to_dict()

        # Colocamos role y content en memory
        return {
            **base,
            "memory": [{
                "role": self.role,
                "content": self.content
            }]
        }

    def Add_config(self):
        # Inicializa un JSON con las configuraciones
        data = self.load_json(self.file)

        # Si está vacío
        # le añadimos una [{}] con las configuraciones base
        if not data:
            # Obtenemos la estructura en una lista
            structure = [self._build_structure()]
            # Añadimos el json
            with open(self.file, "w") as json_file:
                json.dump(structure, json_file, indent=4)
                return True

        # Si no está vacio
        # Añadimos un {} con las configuraciones a la []
        else:
            # Obtemos la estructura
            structure = self._build_structure()
            # Añadimos las configuraciones del nuevo bot
            data.append(structure)

            # Lo añadimos al json
            with open(self.file, "w") as json_file:
                json.dump(data, json_file, indent=4)
                return True


if __name__ == "__main__":

    FILE = BASE_DIR / "config" / "agents.json"
    jac = JsonAddConfig(file=FILE)

    jac.Add_config()
