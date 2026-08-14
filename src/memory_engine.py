import os
import json
import math
import requests
from typing import List, Dict, Any

class LongTermMemory:
    def __init__(self, memory_file="memory.json", ollama_host=None):
        self.memory_file = memory_file
        # Usar la variable de entorno si no se pasa host
        self.ollama_host = ollama_host or os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
        self.embedding_model = "nomic-embed-text"
        self.memories = self._load_memory()

    def _load_memory(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Memoria] Error cargando {self.memory_file}: {e}")
        return []

    def _save_memory(self):
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.memories, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[Memoria] Error guardando {self.memory_file}: {e}")

    def get_embedding(self, text: str) -> List[float]:
        try:
            url = f"{self.ollama_host.rstrip('/')}/api/embeddings"
            response = requests.post(url, json={
                "model": self.embedding_model,
                "prompt": text
            }, timeout=30)
            
            if response.status_code == 200:
                return response.json().get("embedding", [])
            else:
                print(f"[Memoria] Error Ollama Embedding: {response.text}")
        except Exception as e:
            print(f"[Memoria] Error conectando a Ollama para embedding: {e}")
        return []

    def cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        if not v1 or not v2 or len(v1) != len(v2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(v1, v2))
        magnitude1 = math.sqrt(sum(a * a for a in v1))
        magnitude2 = math.sqrt(sum(b * b for b in v2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
            
        return dot_product / (magnitude1 * magnitude2)

    def save_interaction(self, user_text: str, lia_text: str, nox_text: str):
        # Creamos un resumen del intercambio para incrustar semánticamente
        memory_text = f"Usuario dijo: {user_text}\nLia respondió: {lia_text}\nNox respondió: {nox_text}"
        
        print("[Memoria] Guardando recuerdo a largo plazo...")
        vector = self.get_embedding(memory_text)
        if vector:
            self.memories.append({
                "text": memory_text,
                "vector": vector
            })
            self._save_memory()
            print("[Memoria] ¡Recuerdo guardado con éxito!")

    def retrieve_relevant(self, query: str, top_k: int = 2) -> str:
        if not self.memories:
            return ""
            
        print("[Memoria] Buscando recuerdos relevantes...")
        query_vector = self.get_embedding(query)
        if not query_vector:
            return ""
            
        scored_memories = []
        for mem in self.memories:
            score = self.cosine_similarity(query_vector, mem["vector"])
            scored_memories.append((score, mem["text"]))
            
        # Ordenar por puntuación descendente
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        
        # Filtrar los que tengan un score decente (ej. > 0.35 para nomic-embed-text)
        relevant_texts = []
        for score, text in scored_memories[:top_k]:
            if score > 0.35:
                relevant_texts.append(text)
                print(f"[Memoria] Recuerdo encontrado (Score: {score:.3f})")
                
        if not relevant_texts:
            return ""
            
        context = "RECUERDOS RELEVANTES DE CONVERSACIONES PASADAS (Usa esto si aplica a la conversación actual):\n"
        for i, text in enumerate(relevant_texts, 1):
            context += f"--- Recuerdo {i} ---\n{text}\n"
        
        return context
