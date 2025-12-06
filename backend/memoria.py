import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import List, Optional
import numpy as np 
from openai import OpenAI

# Carregar variáveis de ambiente
load_dotenv("/home/ubuntu/tarotconclusivo/.env")

# Configuração do Cliente Supabase
SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Chave Service Role (JWT)

# Inicialização do Cliente Supabase
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Erro ao inicializar cliente Supabase: {e}")

# Inicialização do Cliente OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Dimensão do embedding 
EMBEDDING_DIMENSION = 1536

def gerar_embedding(texto: str) -> List[float]:
    """Gera o embedding de um texto usando a API da OpenAI."""
    try:
        response = client.embeddings.create(
            input=texto,
            model="text-embedding-ada-002" # Modelo de 1536 dimensões
        )
        # Retorna a lista de floats do embedding
        return response.data[0].embedding
    except Exception as e:
        print(f"ERRO REAL NA GERAÇÃO DE EMBEDDING: {e}")
        # Em caso de falha, retorne um vetor de zeros para evitar quebrar o fluxo
        # ou levante o erro, dependendo da sua estratégia de produção.
        return [0.0] * EMBEDDING_DIMENSION

def salvar_memoria(user_id: str, consulta_texto: str, embedding: List[float]):
    """
    Salva o texto da consulta e seu embedding na tabela memoria_vetorial.
    """
    try:
        embedding_str = json.dumps(embedding)
        
        data, count = supabase.table('memoria_vetorial').insert({
            "user_id": user_id,
            "consulta_texto": consulta_texto,
            "embedding": embedding_str
        }).execute()
        
        return data
    except Exception as e:
        print(f"❌ Erro ao salvar memória no Supabase: {e}")
        return None

def recuperar_memoria(user_id: str, vetor_busca: List[float], top_k: int = 3) -> List[str]:
    """
    Recupera as consultas mais similares do histórico do usuário usando pgvector (RAG).
    """
    try:
        # 1. Formata o vetor de busca para a query SQL
        vetor_busca_str = json.dumps(vetor_busca)
        
        # 2. Executa a query SQL de busca por similaridade (coseno)
        # Usamos a função 'rpc' para chamar uma função de banco de dados que executa a query vetorial.
        
        # ATENÇÃO: Esta chamada falhará até que a função 'match_memoria' seja criada no Supabase.
        
        response = supabase.rpc(
            'match_memoria', 
            {
                'query_embedding': vetor_busca_str,
                'match_user_id': user_id,
                'match_threshold': 0.5, # Limite de similaridade (ajustável)
                'match_count': top_k
            }
        ).execute()
        
        # O resultado do RPC é um objeto com a chave 'data'
        contexto_recuperado = [item['consulta_texto'] for item in response.data]
        
        return contexto_recuperado
        
    except Exception as e:
        print(f"❌ Erro ao recuperar memória: {e}")
        # Retorna um contexto vazio em caso de falha
        return []

# Exemplo de uso (para teste de funcionalidade)
if __name__ == "__main__":
    # ATENÇÃO: user_id DEVE ser um UUID válido. Usaremos o placeholder.
    TEST_USER_ID = "00000000-0000-0000-0000-000000000001" 
    
    # 1. Simular uma nova pergunta (que será o vetor de busca)
    nova_pergunta = "Estou pensando em mudar de carreira, o que devo fazer?"
    vetor_busca = gerar_embedding(nova_pergunta)
    
    # 2. Recuperar as consultas mais similares (RAG)
    print("\nIniciando Recuperação (RAG)...")
    contexto = recuperar_memoria(TEST_USER_ID, vetor_busca, top_k=1)
    
    if contexto:
        print(f"✅ Contexto recuperado com sucesso (Top {len(contexto)}):")
        print("--- CONTEXTO PARA IA ---")
        for c in contexto:
            print(f"- {c}")
        print("------------------------")
    else:
        print("❌ Falha na recuperação. (Esperado, pois a função 'match_memoria' não existe no Supabase ainda).")
        print("Avançando para a instrução de criação de função no Supabase.")
