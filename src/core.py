import os
import json
from pydantic import BaseModel
from typing import List, Literal
from ollama import Client

import config

# Configuración del entorno usando config.py
OLLAMA_HOST = config.OLLAMA_HOST
MODEL_NAME = config.MODEL_NAME

# Modelos Pydantic para validar y estructurar la salida de Ollama
class Intervencion(BaseModel):
    personaje: Literal['Lia', 'Nox']
    emocion: str
    texto: str

class RespuestaDual(BaseModel):
    dialogo: List[Intervencion]
    terminar_interaccion: bool

from memory_engine import LongTermMemory

_memory_instance = None
def get_memory():
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = LongTermMemory(ollama_host=OLLAMA_HOST)
    return _memory_instance

def chat_bina(prompt: str, history: list = None):
    if history is None:
        history = []
        
    client = Client(host=OLLAMA_HOST)
    memory = get_memory()
    
    # 1. Recuperar contexto relevante de interacciones pasadas (Memoria a Largo Plazo)
    relevant_context = memory.retrieve_relevant(prompt)
    
    dynamic_system_prompt = config.get_active_prompt()
    if relevant_context:
        dynamic_system_prompt += f"\n\n{relevant_context}"
    
    messages = [
        {"role": "system", "content": dynamic_system_prompt},
    ]
    messages.extend(history)
    messages.append({"role": "user", "content": prompt})
    
    try:
        # Llamada a Ollama con enforced JSON schema
        response = client.chat(
            model='llama3.1:8b',
            messages=messages,
            format=RespuestaDual.model_json_schema(),
            options={"temperature": 0.8}
        )
        
        raw_content = response['message']['content']
        # Validamos usando Pydantic
        resultado_dict = json.loads(raw_content)
        respuesta_validada = RespuestaDual(**resultado_dict)
        
        # 2. Guardar el nuevo recuerdo en la Memoria a Largo Plazo
        lia_text = "(No intervino)"
        nox_text = "(No intervino)"
        for inter in respuesta_validada.dialogo:
            if inter.personaje.lower() == 'lia': lia_text = inter.texto
            elif inter.personaje.lower() == 'nox': nox_text = inter.texto
            
        memory.save_interaction(prompt, lia_text, nox_text)
        
        return respuesta_validada, response['message']
        
    except Exception as e:
        print(f"\n[Error] Fallo en la comunicación o validación con Ollama: {e}")
        return None, None

def run_cli():
    print("="*50)
    print("  BINA CORE TEXTUAL - MODO DESARROLLO (HITO 1)  ")
    print("="*50)
    print(f"Servidor IA: {OLLAMA_HOST}")
    print(f"Modelo LLM:  {MODEL_NAME}")
    print("Escribe 'salir' para terminar la prueba.\n")
    
    history = []
    
    while True:
        try:
            user_input = input("\nTú (Escribe tu mensaje o presiona ENTER vacío para hablar) ['salir' para terminar]: ").strip()
            
            if user_input.lower() in ['salir', 'exit', 'quit']:
                print("Saliendo...")
                break
                
            if user_input == '':
                # Modo voz
                try:
                    from stt_engine import get_stt
                    stt = get_stt()
                    user_input = stt.listen_and_transcribe()
                    if not user_input:
                        continue
                    print(f"\nTú (Transcrito): {user_input}")
                except Exception as e:
                    print(f"\n[Aviso] No se pudo usar el micrófono: {e}")
                    continue
            
            print("\nBina está pensando...")
            respuesta, msg = chat_bina(user_input, history)
            
            if respuesta:
                print("-" * 40)
                
                # Cargar TTS solo cuando se necesita
                try:
                    from tts_engine import get_tts
                    tts = get_tts()
                except Exception as e:
                    print(f"[Aviso] No se pudo cargar TTS: {e}")
                    tts = None

                for inter in respuesta.dialogo:
                    print(f"[{inter.personaje}] ({inter.emocion}): {inter.texto}")
                    if tts:
                        tts.speak(inter.personaje, inter.texto)
                        
                print("-" * 40)
                
                # Añadimos contexto para recordar el flujo
                history.append({"role": "user", "content": user_input})
                history.append(msg)
                
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break
        except Exception as e:
            print(f"\nError inesperado: {e}")

if __name__ == "__main__":
    run_cli()
