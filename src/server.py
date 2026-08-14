import os
import json
import base64
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager

# Importamos la lógica que ya construimos
from core import chat_bina
from stt_engine import get_stt
from tts_engine import get_tts

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--------------------------------------------------")
    print("🚀 INICIANDO BINA CORE - CARGANDO MOTORES DE IA")
    print("--------------------------------------------------")
    # Precargar STT y TTS en hilos separados para no bloquear
    import asyncio
    await asyncio.gather(
        asyncio.to_thread(get_stt),
        asyncio.to_thread(get_tts)
    )
    print("✅ BINA CORE LISTO. Ya puedes abrir el navegador.")
    print("--------------------------------------------------")
    yield
    print("Apagando Bina Core...")

app = FastAPI(lifespan=lifespan)

# Primero definimos el WebSocket
@app.websocket("/ws/bina")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    history = []
    
    stt = get_stt()
    tts = get_tts()
    
    try:
        while True:
            # Recibir datos del navegador (texto o audio en bytes)
            message = await websocket.receive()
            
            user_text = ""
            if "text" in message:
                # Recibimos texto
                user_text = message["text"]
                print(f"[WS] Recibido texto: {user_text}")
            elif "bytes" in message:
                # Recibimos audio (webm) desde el MediaRecorder del navegador
                print("[WS] Recibido audio del navegador. Transcribiendo...")
                audio_bytes = message["bytes"]
                # Ejecutar STT (bloqueante) en un hilo para no colgar el WebSocket
                user_text = await asyncio.to_thread(stt.transcribe_bytes, audio_bytes)
                print(f"[WS] Transcrito: {user_text}")
                
                # Le regresamos la transcripción al cliente para que la lea en pantalla
                await websocket.send_json({"type": "transcription", "text": user_text})
                
            if not user_text.strip():
                continue
                
            # Bina empieza a pensar
            await websocket.send_json({"type": "state", "value": "thinking"})
            
            # Obtener respuesta del LLM (qwen2.5) en un hilo
            respuesta, raw_msg = await asyncio.to_thread(chat_bina, user_text, history)
            
            if not respuesta:
                await websocket.send_json({"type": "state", "value": "idle"})
                continue
                
            history.append({"role": "user", "content": user_text})
            history.append(raw_msg)
            
            # [NUEVO] Rolling Window: Mantener solo los últimos 6 mensajes (3 turnos completos)
            if len(history) > 6:
                history = history[-6:]
            
            # Procesar el diálogo estructurado generado por el LLM
            for inter in respuesta.dialogo:
                personaje = inter.personaje.lower() # lia o nox
                
                # Avisar al frontend quién habla, su emoción y su texto
                await websocket.send_json({
                    "type": "state", 
                    "value": f"speaking_{personaje}",
                    "emotion": inter.emocion,
                    "text": inter.texto,
                    "character": personaje
                })
                
                # Generar el audio localmente en un hilo y enviarlo al navegador
                audio_bytes = await asyncio.to_thread(tts.get_audio_bytes, inter.personaje, inter.texto)
                if audio_bytes:
                    await websocket.send_bytes(audio_bytes)
                
            # Al terminar el turno, regresamos a estado neutral
            await websocket.send_json({"type": "state", "value": "idle"})

    except WebSocketDisconnect:
        print("[WS] Cliente desconectado")
    except Exception as e:
        print(f"[WS Error] Ocurrió un error inesperado: {e}")

# Montamos la carpeta UI para servir el HTML/CSS/JS estático
app.mount("/", StaticFiles(directory="src/ui", html=True), name="ui")

if __name__ == "__main__":
    import uvicorn
    # Correr servidor en puerto 8000
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["src"])
