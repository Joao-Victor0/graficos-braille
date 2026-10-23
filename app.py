from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from agente import Agente

# Variáveis globais para armazenar a IA
agente = None
rag_chain_global = None

# O lifespan carrega a IA apenas após a porta do servidor abrir, evitando bloqueios
@asynccontextmanager
async def carregar_ia(app: FastAPI):
    global agente, rag_chain_global
    print("Estruturando o Agente de IA...")
    agente = Agente()
    rag_chain_global = agente.estruturar_agente()
    print("Agente pronto para uso!")
    yield

app = FastAPI(lifespan=carregar_ia)

origens_permitidas = [
    "https://jhonedourado.github.io/graficos-braille/?id=assintotas"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/respostas/{filename}")
async def get_audio_file(filename: str):
    return FileResponse(f"./{filename}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Cliente WebSocket conectado!")
    try:
        while True:
            bytes_recebidos = await websocket.receive_bytes()
            url_resposta_audio = await agente.rodar_agente(rag_chain_global, bytes_recebidos)
            await websocket.send_text(url_resposta_audio)
    except WebSocketDisconnect:
        print('Cliente Desconectado')
    except Exception as e:
        print(f"Erro no WebSocket: {e}")