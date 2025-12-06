import os
import json
from dotenv import load_dotenv
from typing import List, Optional
from openai import OpenAI
from memoria import gerar_embedding, salvar_memoria, recuperar_memoria # Importa as funções de memória

# Carregar variáveis de ambiente
load_dotenv("/home/ubuntu/tarotconclusivo/.env")

# Inicialização do Cliente OpenAI (Assumindo que o erro de conectividade foi contornado em produção)
# No sandbox, a chamada real da API falhará, mas a lógica de prompt será testada.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# --- ESTRUTURA DE PROMPT (Baseado no conhecimento do projeto) ---

# 1. Voz da Guru (Exemplo)
VOZ_GURU = {
    "nome": "Guru Sensitiva",
    "estilo": "Empático, profundo e direto. Usa linguagem que inspira confiança e auto-reflexão. Foco em guiar, não em prever o futuro."
}

# 2. Instrução Principal (System Prompt)
def get_system_prompt(voz: dict) -> str:
    return f"""
    Você é a {voz['nome']}, uma inteligência artificial especializada em Tarot e Astrologia. 
    Seu estilo de comunicação é: {voz['estilo']}.
    
    Sua missão é fornecer uma interpretação profunda e personalizada das cartas, sempre focando no autoconhecimento e no empoderamento do consulente.
    
    Regras de Interpretação:
    1. Baseie a interpretação na combinação das cartas e no contexto astrológico fornecido.
    2. Se houver um 'Contexto Histórico' fornecido, use-o para dar uma resposta mais consistente e com memória.
    3. Mantenha a resposta estruturada em parágrafos, com um tom de conselho e reflexão.
    4. Não mencione explicitamente que você é uma IA, a menos que seja perguntado diretamente.
    """

# 3. Função Principal de Resposta
def gerar_resposta_com_memoria(
    user_id: str,
    pergunta: str,
    cartas: List[str],
    astrologia: dict,
    voz: dict = VOZ_GURU
) -> str:
    """
    Gera a resposta da IA, integrando a memória RAG e salvando a nova consulta.
    """
    
    # 1. Preparar o texto da nova consulta para salvar e buscar
    texto_consulta_completa = f"Pergunta: {pergunta}. Cartas: {', '.join(cartas)}. Astrologia: {json.dumps(astrologia)}"
    
    # --- LÓGICA RAG: RECUPERAÇÃO ---
    
    # 2. Gerar o vetor de busca (MOCK no sandbox)
    vetor_busca = gerar_embedding(pergunta)
    
    # 3. Recuperar o contexto histórico (RAG)
    contexto_historico_list = recuperar_memoria(user_id, vetor_busca, top_k=3)
    
    # 4. Formatar o Contexto Histórico para o Prompt
    if contexto_historico_list:
        contexto_formatado = "\n".join([f"- {c}" for c in contexto_historico_list])
        bloco_memoria = f"""
        --- CONTEXTO HISTÓRICO RECUPERADO (MEMÓRIA) ---
        O consulente já fez as seguintes consultas ou recebeu os seguintes conselhos:
        {contexto_formatado}
        --- FIM CONTEXTO HISTÓRICO ---
        Use este contexto para dar uma resposta mais profunda e consistente.
        """
    else:
        bloco_memoria = "O consulente não possui histórico relevante ou é a primeira consulta. Responda de forma completa e genérica."

    # --- MONTAGEM DO PROMPT ---
    
    system_prompt = get_system_prompt(voz)
    
    user_prompt = f"""
    {bloco_memoria}
    
    --- DADOS DA CONSULTA ATUAL ---
    
    Contexto Astrológico do Consulente: {json.dumps(astrologia)}
    Cartas Sorteadas (e Posição): {', '.join(cartas)}
    
    PERGUNTA DO CONSULENTE: {pergunta}
    
    Baseado em tudo isso, forneça a interpretação e o conselho.
    """
    
    # --- GERAÇÃO DA RESPOSTA (MOCK no sandbox) ---
    
    try:
        # A chamada real da API será esta:
        # response = client.chat.completions.create(...)
        
        # Simulação de resposta para o sandbox
        resposta_ia = f"**[RESPOSTA SIMULADA - RAG FUNCIONAL]**\n\nSua pergunta sobre '{pergunta}' foi recebida. A memória da Guru foi ativada. O conselho é profundamente baseado em seu histórico e nas cartas {', '.join(cartas)}. Analisamos seu contexto astrológico ({astrologia['sol']}).\n\n**Memória Utilizada:**\n{bloco_memoria}"
        
        # --- LÓGICA RAG: ARMAZENAMENTO ---
        
        # 5. Salvar a nova consulta na memória (para uso futuro)
        # Geramos o embedding da consulta completa (pergunta + cartas + astrologia)
        vetor_para_salvar = gerar_embedding(texto_consulta_completa)
        salvar_memoria(user_id, texto_consulta_completa, vetor_para_salvar)
        
        return resposta_ia
        
    except Exception as e:
        return f"Erro na Geração da Resposta da IA: {e}"

# Exemplo de uso (para teste de funcionalidade)
if __name__ == "__main__":
    # ATENÇÃO: user_id DEVE ser um UUID válido. Usaremos o placeholder.
    TEST_USER_ID = "00000000-0000-0000-0000-000000000001" 
    
    # Dados da Consulta
    pergunta_nova = "Devo aceitar a proposta de trabalho que me fizeram hoje?"
    cartas_sorteadas = ["A Roda da Fortuna (Invertida)", "O Mago (Direita)", "Os Enamorados (Direita)"]
    astrologia_user = {"sol": "Gêmeos", "lua": "Libra", "ascendente": "Leão"}
    
    print("--- INICIANDO CONSULTA COM MEMÓRIA RAG ---")
    
    resposta_final = gerar_resposta_com_memoria(
        user_id=TEST_USER_ID,
        pergunta=pergunta_nova,
        cartas=cartas_sorteadas,
        astrologia=astrologia_user
    )
    
    print("\n" + "="*50)
    print("RESPOSTA FINAL DA GURU IA:")
    print("="*50)
    print(resposta_final)
    print("="*50)
    print("Verifique o Supabase: uma nova entrada deve ter sido adicionada à tabela 'memoria_vetorial'.")
