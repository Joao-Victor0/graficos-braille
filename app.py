from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from agente import Agente

app = FastAPI()

# A variável global sobe junto com o servidor
agente = Agente()
rag_chain_global = agente.estruturar_agente()

@app.get("/respostas/{filename}")
async def get_audio_file(filename: str):
    return FileResponse(f"./{filename}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Cliente WebSocket conectado!")

    try:
        while True:
            # 1. Recebe o áudio do navegador
            bytes_recebidos = await websocket.receive_bytes()

            # 2. Roda o RAG e gera o arquivo de áudio físico no servidor
            url_resposta_audio = await agente.rodar_agente(rag_chain_global, bytes_recebidos)

            # 3. Envia a string (URL ou nome do arquivo) para o JS
            await websocket.send_text(url_resposta_audio)

    except WebSocketDisconnect:
        print('Cliente Desconectado')
    except Exception as e:
        print(f"Erro no WebSocket: {e}")
