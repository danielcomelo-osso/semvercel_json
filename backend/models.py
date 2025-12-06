from pydantic import BaseModel
from typing import List

class ConsultaRequest(BaseModel):
    """Modelo de dados para a requisição de consulta à Guru IA."""
    user_id: str
    pergunta: str
    cartas: List[str]
    astrologia: dict
    
class ConsultaResponse(BaseModel):
    """Modelo de dados para a resposta da Guru IA."""
    resposta_guru: str

