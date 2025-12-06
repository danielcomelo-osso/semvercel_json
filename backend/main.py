"""
Tarot com IA - Backend FastAPI
Sistema de Tarot com Inteligência Artificial focado em experiência ritualística
"""

import os
import random
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from openai import OpenAI
import kerykeion as k

# Carregar variáveis de ambiente
load_dotenv()

# Configurar Sentry (opcional)
if os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[FastApiIntegration()],
        traces_sample_rate=1.0,
    )

# Inicializar FastAPI
app = FastAPI(
    title="Tarot com IA - API",
    description="API para sistema de Tarot com Inteligência Artificial",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
        allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000"), "https://*.vercel.app", "https://taro-frontend1-tsez.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Modelos Pydantic
class DadosNascimento(BaseModel):
    nome: str = Field(..., description="Nome da pessoa")
    data_nascimento: str = Field(..., description="Data de nascimento (YYYY-MM-DD)")
    hora_nascimento: str = Field(..., description="Hora de nascimento (HH:MM)")
    local_nascimento: str = Field(..., description="Local de nascimento (Cidade, País)")

class PerguntaTarot(BaseModel):
    pergunta: str = Field(..., description="Pergunta para o Tarot")
    dados_nascimento: Optional[DadosNascimento] = None
    voz_guru: str = Field(default="companheira", description="Estilo da Guru IA")

class CartaTarot(BaseModel):
    nome: str
    arcano: str
    posicao: str
    significado_geral: str

class RespostaTarot(BaseModel):
    cartas: List[CartaTarot]
    interpretacao: str
    elementos_astrologicos: Optional[Dict[str, Any]] = None
    timestamp: datetime

# Dados do Tarot (Arcanos Maiores)
ARCANOS_MAIORES = [
    {"nome": "O Louco", "significado": "Novos começos, espontaneidade, fé no desconhecido"},
    {"nome": "O Mago", "significado": "Manifestação, recursos, poder pessoal"},
    {"nome": "A Sacerdotisa", "significado": "Intuição, sabedoria interior, mistério"},
    {"nome": "A Imperatriz", "significado": "Fertilidade, feminilidade, abundância"},
    {"nome": "O Imperador", "significado": "Autoridade, estrutura, controle"},
    {"nome": "O Hierofante", "significado": "Tradição, conformidade, moralidade"},
    {"nome": "Os Amantes", "significado": "Amor, harmonia, relacionamentos, escolhas"},
    {"nome": "A Carruagem", "significado": "Controle, determinação, direção"},
    {"nome": "A Força", "significado": "Força interior, bravura, compaixão"},
    {"nome": "O Eremita", "significado": "Busca interior, introspecção, orientação"},
    {"nome": "A Roda da Fortuna", "significado": "Boa sorte, karma, ciclos de vida"},
    {"nome": "A Justiça", "significado": "Justiça, fairness, verdade, causa e efeito"},
    {"nome": "O Enforcado", "significado": "Suspensão, restrição, sacrifício"},
    {"nome": "A Morte", "significado": "Fim, transformação, transição"},
    {"nome": "A Temperança", "significado": "Equilíbrio, moderação, paciência"},
    {"nome": "O Diabo", "significado": "Escravidão, materialismo, ignorância"},
    {"nome": "A Torre", "significado": "Mudança súbita, revelação, despertar"},
    {"nome": "A Estrela", "significado": "Esperança, espiritualidade, renovação"},
    {"nome": "A Lua", "significado": "Ilusão, medo, ansiedade, subconsciente"},
    {"nome": "O Sol", "significado": "Alegria, sucesso, vitalidade, iluminação"},
    {"nome": "O Julgamento", "significado": "Julgamento, renascimento, despertar interior"},
    {"nome": "O Mundo", "significado": "Conclusão, realização, viagem"}
]

# Vozes da Guru IA
VOZES_GURU = {
    "companheira": {
        "tom": "acolhedora e empática",
        "estilo": "Como uma amiga sábia que te conhece há anos",
        "linguagem": "calorosa, próxima e reconfortante"
    },
    "mistica": {
        "tom": "misteriosa e profunda",
        "estilo": "Como uma antiga sacerdotisa com conhecimento ancestral",
        "linguagem": "poética, simbólica e transcendente"
    },
    "sábia": {
        "tom": "sábia e reflexiva",
        "estilo": "Como uma mentora experiente que guia com sabedoria",
        "linguagem": "clara, profunda e inspiradora"
    }
}

def obter_dados_astrologicos(dados: DadosNascimento) -> Dict[str, Any]:
    """Obter dados astrológicos usando Kerykeion"""
    try:
        # Converter local para formato aceito pelo Kerykeion (inglês)
        local_en = dados.local_nascimento
        if "São Paulo" in local_en or "Sao Paulo" in local_en:
            local_en = "Sao Paulo, Brazil"
        elif "Rio de Janeiro" in local_en:
            local_en = "Rio de Janeiro, Brazil"
        elif "Brasil" in local_en or "Brazil" in local_en:
            local_en = local_en.replace("Brasil", "Brazil")
        
        # Criar objeto de nascimento
        nascimento = k.AstrologicalSubject(
            name=dados.nome,
            year=int(dados.data_nascimento.split('-')[0]),
            month=int(dados.data_nascimento.split('-')[1]),
            day=int(dados.data_nascimento.split('-')[2]),
            hour=int(dados.hora_nascimento.split(':')[0]),
            minute=int(dados.hora_nascimento.split(':')[1]),
            city=local_en
        )
        
        return {
            "sol": {
                "signo": nascimento.sun["sign"],
                "casa": nascimento.sun["house"]
            },
            "lua": {
                "signo": nascimento.moon["sign"],
                "casa": nascimento.moon["house"]
            },
            "ascendente": nascimento.first_house["sign"]
        }
    except Exception as e:
        print(f"Erro ao obter dados astrológicos: {e}")
        return None

def sortear_cartas(quantidade: int = 3) -> List[CartaTarot]:
    """Sortear cartas do Tarot"""
    cartas_sorteadas = random.sample(ARCANOS_MAIORES, quantidade)
    posicoes = ["Passado", "Presente", "Futuro"] if quantidade == 3 else [f"Carta {i+1}" for i in range(quantidade)]
    
    cartas = []
    for i, carta in enumerate(cartas_sorteadas):
        cartas.append(CartaTarot(
            nome=carta["nome"],
            arcano="Maior",
            posicao=posicoes[i],
            significado_geral=carta["significado"]
        ))
    
    return cartas

def gerar_interpretacao_ia(pergunta: str, cartas: List[CartaTarot], 
                          elementos_astrologicos: Optional[Dict], voz: str) -> str:
    """Gerar interpretação usando IA"""
    try:
        voz_config = VOZES_GURU.get(voz, VOZES_GURU["companheira"])
        
        # Construir contexto astrológico
        contexto_astro = ""
        if elementos_astrologicos:
            contexto_astro = f"""
            Elementos Astrológicos:
            - Sol em {elementos_astrologicos['sol']['signo']} (Casa {elementos_astrologicos['sol']['casa']})
            - Lua em {elementos_astrologicos['lua']['signo']} (Casa {elementos_astrologicos['lua']['casa']})
            - Ascendente em {elementos_astrologicos['ascendente']}
            """
        
        # Construir contexto das cartas
        contexto_cartas = "\\n".join([
            f"- {carta.posicao}: {carta.nome} - {carta.significado_geral}"
            for carta in cartas
        ])
        
        prompt = f"""
        Você é uma Guru do Tarot com personalidade {voz_config['tom']}. Seu estilo é {voz_config['estilo']} 
        e sua linguagem é {voz_config['linguagem']}.
        
        Pergunta do consulente: "{pergunta}"
        
        Cartas sorteadas:
        {contexto_cartas}
        
        {contexto_astro}
        
        Forneça uma interpretação profunda e personalizada, conectando as cartas com a pergunta e, 
        se disponível, com os elementos astrológicos. Seja empática, sábia e ofereça insights 
        práticos para a vida da pessoa. Use uma linguagem {voz_config['linguagem']}.
        
        Estruture sua resposta de forma fluida e natural, como uma conversa íntima.
        """
        
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Erro ao gerar interpretação IA: {e}")
        return "Desculpe, não foi possível gerar a interpretação no momento. Tente novamente."

# Rotas da API
@app.get("/")
async def root():
    """Rota raiz da API"""
    return {
        "message": "Tarot com IA - API funcionando",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/consulta-tarot", response_model=RespostaTarot)
async def consulta_tarot(pergunta_data: PerguntaTarot):
    """Realizar consulta de Tarot com IA"""
    try:
        # Sortear cartas
        cartas = sortear_cartas(3)
        
        # Obter dados astrológicos se fornecidos
        elementos_astrologicos = None
        if pergunta_data.dados_nascimento:
            elementos_astrologicos = obter_dados_astrologicos(pergunta_data.dados_nascimento)
        
        # Gerar interpretação com IA
        interpretacao = gerar_interpretacao_ia(
            pergunta_data.pergunta,
            cartas,
            elementos_astrologicos,
            pergunta_data.voz_guru
        )
        
        return RespostaTarot(
            cartas=cartas,
            interpretacao=interpretacao,
            elementos_astrologicos=elementos_astrologicos,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/vozes-guru")
async def listar_vozes_guru():
    """Listar vozes disponíveis da Guru IA"""
    return {"vozes": list(VOZES_GURU.keys()), "detalhes": VOZES_GURU}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
