# services.py
from mock_data import EXERCICIOS

def buscar_exercicios(materia: str):
    """
    Simula uma busca no backend. 
    Futuramente: requests.get(f"http://localhost:8080/exercicios/{materia}").json()\
    L>>>>>> no supabase
    """
    return EXERCICIOS.get(materia, [])