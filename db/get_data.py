import uuid
from datetime import datetime as dt

# Genera un ID UUID
def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()
    

# cear un diccionario con la hora y fecha actual
def generate_date():
    # optener la hora y fecha actual
    return dt.now()

    
if __name__ == "__main__":

    d = generate_date()
    f = generate_uuid()
    
    print(f"{f}\n{d}")