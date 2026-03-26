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

        # Valida que el id_conversation sea un UUID
        if not isinstance(id_conversation, UUID):
            raise TypeError("id_conversation must be a UUID")
        
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
        self.id_conversation = id_conversation # UUID
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
    @classmethod 
    def from_row(cls, row): # cls es misma clase sobre la que se llamó el método 
        # Se crea un objeto valido y lo retorna
        return cls( id_conversation=row[0],
                    role=row[1],
                    date=row[2],
                    content=row[3]
                )
    

class TableConversation:

    def __init__(self, id:UUID, title:str, time_start:datetime, behavior:str):
        
        # Valida que el id sea UUID
        if not isinstance(id, UUID):
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
        
        # Valida que behavior sea un str
        if not isinstance(behavior, str):
            raise TypeError("behavior must be a string")
        # Valida que el behavior no esté vacío
        if not behavior.strip():
            raise ValueError("behavior cannot be empty")

        # Id de la conversación
        self.id = str(id) # type: UUID
        # Título de la conversación
        self.title = title # type: str
        # Hora en la que se creo la conversación
        self.time_start = time_start # type: datetime
        # Comportamiento en la que se basa el agente para responder
        self.behavior = behavior # type: str


class ConversationSQLMapper:

    # La columnas de la tabla
    COLUMNS = ("id", "title", "time_start", "behavior")

    # Se le tiene que pasar un objeto de tipo TableConversation
    # y usara los datos para ordenar los datos en una tupla
    @staticmethod
    def to_row(message: TableConversation):
        return (
            message.id,
            message.title,
            message.time_start,
            message.behavior
        )
    
    # Se llama así ConversationSQLMapper.from_row(row)
    # Retorna un objeto valido
    @classmethod 
    def from_row(cls, row): # cls es misma clase sobre la que se llamó el método 
        # Se crea un objeto valido y lo retorna
        return cls( id=row[0],
                    title=row[1],
                    time_start=row[2],
                    behavior=row[3]
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