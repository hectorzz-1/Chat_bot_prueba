from abc import ABC, abstractmethod
from uuid import UUID, uuid4
from datetime import datetime


class Compiler(ABC):
    
    @abstractmethod
    def get(self):
        pass


class TableMessenge:

    # Los roles que acepta la tabla
    VALID_ROLES = {"user", "assistant", "system"}

    def __init__(self, id_conversation:UUID, role:str, date:datetime, content:str):
        
        # Valida que el id sea UUID
        try: 
            if isinstance(UUID(id_conversation), UUID):
                pass
        except:
            raise TypeError("id must be a UUID")
        
        # Valida que role sea un str
        if not isinstance(role, str):
            raise TypeError("role must be a string")
        # Valida que el valor de role sea valido
        # user, assistant o system
        if role not in self.VALID_ROLES:
            raise ValueError(
                f"role must be one of {self.VALID_ROLES}"
            )

        # Valida que el valor de date sea de tipo datetime
        if not isinstance(date, datetime):
            raise TypeError("date must be datetime.datetime")
        
        # Valida que content sea un str
        if not isinstance(content, str):
            raise TypeError("content must be a string")
        # Valida que content no esté vacío
        if not content.strip():
            raise ValueError("content cannot be empty")
        
        # Id de la conversacion a la cual pertenece el mensaje
        self.id_conversation = str(id_conversation) # UUID
        # Rol de quien emite el mensaje
        self.role = role # user, assistant o system
        # Hora en la que se envió el mensaje
        self.date = date # datatime
        # Contenido del mensaje
        self.content = content # str, no empty


class MessageSQLMapper:

    # La columnas de la tabla
    COLUMNS = ("id_conversation", "role", "date", "content")

    # Se le tiene que pasar un objeto de tipo TableMessenge
    # y usara los datos para ordenar los datos en una tupla
    @staticmethod
    def to_row(message: TableMessenge):
        return (
            message.id_conversation,
            message.role,
            message.date,
            message.content
        )

    # Se llama así TMessengeCompiler.from_row(row)
    # Retorna un objeto valido
    @staticmethod 
    def from_row( row) -> TableMessenge:
        # Se crea un objeto valido y lo retorna
        return TableMessenge (
                id_conversation=row[0],
                role=row[1],
                date=row[2],
                content=row[3]
            )
    

class TableConversation:

    def __init__(
            self,
            id:UUID, title:str, time_start:datetime,
            id_agent:UUID, tokens: int
            ):
        
        # Valida que el id sea UUID
        try: 
            if isinstance(UUID(id), UUID):
                pass
        except:
            raise TypeError("id must be a UUID")
        
        # Valida que title sea un str
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        # Valida que el title no esté vacío
        if not title.strip():
            raise ValueError("title cannot be empty")
        
        # Valida que time_start sea de tipo datetime
        if not isinstance(time_start, datetime):
            raise TypeError("'time start' must be datetime.datetime")
        
        # Valida que el id sea UUID
        try: 
            if isinstance(UUID(id), UUID):
                pass
        except:
            raise TypeError("id must be a UUID")
        
        # Valida que tokens sea un int
        if not isinstance(tokens, int):
            raise TypeError("tokens must be a integer")
        # Valida que el tokens no sea menor que 0
        if tokens < 0:
            raise TypeError("tokens cannot be less than 0")

        # Id de la conversación
        self.id = str(id) # type: UUID
        # Título de la conversación
        self.title = title # type: str
        # Hora en la que se creo la conversación
        self.time_start = time_start # type: datetime
        # Agente a la cual está asociada la conversacion
        self.id_agent = str(id_agent) # type: UUID
        # Los tokens que uso la conversación
        self.tokens = tokens # type: int


class ConversationSQLMapper:

    # La columnas de la tabla
    COLUMNS = (
        "id", "title", "time_start",
        "id_agent", "tokens"
        )

    # Se le tiene que pasar un objeto de tipo TableConversation
    # y usará los datos para ordenar los datos en una tupla
    @staticmethod
    def to_row(message: TableConversation):
        return (
            message.id,
            message.title,
            message.time_start,
            message.id_agent,
            message.tokens
        )
    
    # Se llama así ConversationSQLMapper.from_row(row)
    # Retorna un objeto valido
    @staticmethod
    def from_row(row) -> TableConversation: 
        # Se crea un objeto valido y lo retorna
        return  TableConversation(
            id=row[0],
            title=row[1],
            time_start=row[2],
            id_agent=row[3],
            tokens=row[4],
        )


class TableAgent:
    
    ABLE_MODELS = ("gpt-4o", "gpt-4o-mini", "gpt-5.5", "o3")

    def __init__(
            self, id:UUID, name:str, model:str, behavior:str, temperature:float,
            presence_penalty:float, frequency_penalty:float,
            max_tokens:int, max_input_tokens:int
            ):
        
        # Valida que el id sea UUID
        try: 
            if isinstance(UUID(id), UUID):
                pass
        except:
            raise TypeError("id must be a UUID")

        # Valida que name sea un str
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        # Valida que el name no esté vacío
        if not name.strip():
            raise ValueError("name cannot be empty")
        
        # Valida que model sea un str
        if not isinstance(model, str):
            raise TypeError("model must be a string")
        # Valida que el model no esté vacío
        if not model.strip():
            raise ValueError("model cannot be empty")
        # Validar que sea un modelo usable
        if model not in self.ABLE_MODELS:
            raise ValueError(f"Please use one of these models: {self.ABLE_MODELS}")
        
        # Valida que behavior sea un str
        if not isinstance(behavior, str):
            raise TypeError("behavior must be a string")
        # Valida que el behavior no esté vacío
        if not behavior.strip():
            raise ValueError("behavior cannot be empty")
        
        # Valida que temperature sea un float
        if not isinstance(temperature, float):
            raise TypeError("temperature must be a float")
        # Validar que temperature sea mayor que 0
        if temperature <= 0:
            raise("temperature canno be less tham 0")
        # Validar que temperature sea menor que 2
        if temperature >= 2:
            raise("temperature canno be greater tham 2")
        
        # Valida que presence_penalty sea un float
        if not isinstance(presence_penalty, float):
            raise TypeError("presence_penalty must be a float")
        # Validar que presence_penalty sea mayor que 0
        if presence_penalty <= 0:
            raise("presence_penalty canno be less tham 0")
        # Validar que presence_penalty sea menor que 2
        if presence_penalty >= 2:
            raise("presence_penalty canno be greater tham 2")
        
        # Valida que frequency_penalty sea un float
        if not isinstance(frequency_penalty, float):
            raise TypeError("frequency_penalty must be a float")
        # Validar que frequency_penalty sea mayor que 0
        if frequency_penalty <= 0:
            raise("frequency_penalty canno be less tham 0")
        # Validar que frequency_penalty sea menor que 2
        if frequency_penalty >= 2:
            raise("frequency_penalty canno be greater tham 2")
        
        # Valida que max_tokens sea un integer
        if not isinstance(max_tokens, int):
            raise TypeError("max_tokens must be a integer")
        # Validar que max_tokens sea mayor que 0
        if max_tokens <= 0:
            raise("max_tokens canno be less tham 0")
        
        # Valida que max_input_tokens sea un integer
        if not isinstance(max_input_tokens, int):
            raise TypeError("max_input_tokens must be a integer")
        # Validar que max_input_tokens sea mayor que 0
        if max_input_tokens <= 0:
            raise("max_input_tokens canno be less tham 0")
        
        # Id de la conversación
        self.id = str(id) # type: UUID
        # Nombre del agente
        self.name = name # type: str
        # Modelo de gpt que usará el bot
        self.model = model # type: str
        # Comportamiento del agente
        self.behavior = behavior # type: str
        # control de creatividad de las respuestas del bot
        self.temperature = temperature # type: float
        # Castigo de la repetición de conceptos ya mencionados
        self.presence_penalty = presence_penalty # type: float
        # Castigo al repetir demasiado algo
        self.frequency_penalty = frequency_penalty # type: float
        # Tokens maximos los cuales el bot puede usar en el output
        self.max_tokens = max_tokens # type: int
        # Tokens maximos los cuales el usuario puede usar en el input
        self.max_input_tokens = max_input_tokens # type: int


class AgentSQLMapper:
    
    # La columnas de la tabla
    COLUMNS = (
        "id", "name", "model" , "behavior", "temperature", "presence_penalty",
        "frequency_penalty", "max_tokens", "max_input_tokens"
        )

    # Se le tiene que pasar un objeto de tipo TableConversation
    # y usará los datos para ordenar los datos en una tupla
    @staticmethod
    def to_row(message: TableAgent) -> tuple:
        return (
            message.id,
            message.name,
            message.model,
            message.behavior,
            message.temperature,
            message.presence_penalty,
            message.frequency_penalty,
            message.max_tokens,
            message.max_input_tokens,
        )
    
    # Se llama así: AgentSQLMapper.from_row(row)
    # Retorna un objeto valido
    @staticmethod
    def from_row(row) -> TableAgent: 
        # Se crea un objeto valido y lo retorna
        return  TableAgent(
            id=row[0],
            name=row[1],
            model=row[2],
            behavior=row[3],
            temperature=row[4],
            presence_penalty=row[5],
            frequency_penalty=row[6],
            max_tokens=row[7],
            max_input_tokens=row[8],
        )


if __name__ == "__main__":

    mess = TableMessenge(role="user",content="hola",id_conversation=uuid4(),date=datetime.now())
    mesql = MessageSQLMapper.to_row(message=mess)
    cols = MessageSQLMapper.COLUMNS

    print(f"\n{cols}")
    print(mesql)

    conv = TableConversation(id=uuid4(),title="hi",time_start=datetime.now())
    convsql = ConversationSQLMapper.to_row(conv)
    cols = ConversationSQLMapper.COLUMNS

    print(f"\n{cols}")
    print(convsql)