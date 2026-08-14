import os
import tempfile
import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

class BinaSTT:
    def __init__(self, model_size="tiny", compute_type="int8"):
        print(f"Cargando motor de escucha STT (Whisper {model_size})... esto tomará un momento.")
        # Usamos CPU para desarrollo en la laptop. En el servidor final usaremos GPU.
        self.model = WhisperModel(model_size, device="cpu", compute_type=compute_type)
        self.sample_rate = 16000
        print("[STT] Motor de Escucha Listo.")

    def listen_and_transcribe(self, silence_threshold=0.08, silence_duration=1.5):
        import sounddevice as sd
        print("\n[Bina] 🎙️ Escuchando... (Habla ahora, me detendré al detectar silencio)")
        
        audio_data = []
        silence_frames = 0
        chunk_duration = 0.1 # 100ms
        chunk_samples = int(self.sample_rate * chunk_duration)
        max_silence_chunks = int(silence_duration / chunk_duration)
        has_spoken = False
        
        try:
            stream = sd.InputStream(samplerate=self.sample_rate, channels=1, dtype='float32')
            with stream:
                while True:
                    chunk, _ = stream.read(chunk_samples)
                    audio_data.append(chunk)
                    
                    # Calcular volumen RMS para detectar silencio
                    rms = np.sqrt(np.mean(chunk**2))
                    
                    # Imprimir un indicador visual cada segundo
                    if len(audio_data) % int(1.0 / chunk_duration) == 0:
                        print(f"  ... escuchando (ruido actual: {rms:.4f})", flush=True)
                    
                    if rms < silence_threshold:
                        silence_frames += 1
                    else:
                        silence_frames = 0
                        has_spoken = True
                        
                    # Si ya habló y ahora hay silencio prolongado, detener grabación
                    if has_spoken and silence_frames > max_silence_chunks:
                        print("\n[Bina] Silencio detectado, procesando...")
                        break
                        
                    # Abortar si pasan 10 segundos de puro silencio al inicio
                    if not has_spoken and (len(audio_data) * chunk_duration) > 10.0:
                        print("\n[Aviso] No se detectó voz. Grabación cancelada.")
                        return ""
                        
                    # Timeout duro de 20 segundos máximo para evitar que se quede colgado por ruido
                    if (len(audio_data) * chunk_duration) > 20.0:
                        print("\n[Aviso] Tiempo máximo de grabación (20s) alcanzado. Procesando...")
                        break
        except Exception as e:
            print(f"[Error de Micrófono] {e}")
            return ""
            
        print("[Bina] ⚙️ Procesando voz a texto...")
        
        recording = np.concatenate(audio_data, axis=0)
        temp_wav = tempfile.mktemp(suffix=".wav")
        sf.write(temp_wav, recording, self.sample_rate)
        
        # Transcribir
        try:
            segments, _ = self.model.transcribe(temp_wav, beam_size=5, language="es")
            text = " ".join([segment.text for segment in segments])
        except Exception as e:
            print(f"[Error STT] {e}")
            text = ""
            
        try:
            os.remove(temp_wav)
        except OSError:
            pass
            
        return text.strip()

    def transcribe_bytes(self, audio_bytes: bytes) -> str:
        """Transcribe audio recibido desde el cliente web (WebSockets)"""
        if not audio_bytes:
            return ""
            
        temp_webm = tempfile.mktemp(suffix=".webm")
        with open(temp_webm, "wb") as f:
            f.write(audio_bytes)
            
        print("[Bina] ⚙️ Procesando voz del navegador...")
        # Transcribir usando faster-whisper con filtros anti-alucinaciones
        try:
            segments, _ = self.model.transcribe(
                temp_webm, 
                beam_size=5, 
                language="es",
                condition_on_previous_text=False,
                vad_filter=True, # Importante para evitar que el ruido de fondo sea interpretado
                vad_parameters=dict(min_silence_duration_ms=500),
                initial_prompt="Lia, Nox, Bina, Tranzge."
            )
            
            valid_texts = []
            for segment in segments:
                # Evitar alucinaciones típicas de Whisper ("¡Gracias por ver el video!", etc.)
                if segment.no_speech_prob < 0.6:
                    valid_texts.append(segment.text.strip())
            
            text = " ".join(valid_texts)
        except Exception as e:
            print(f"[Error STT WebSocket] {e}")
            text = ""
            
        try:
            os.remove(temp_webm)
        except OSError:
            pass
            
        return text.strip()

_stt_instance = None

def get_stt():
    global _stt_instance
    if _stt_instance is None:
        _stt_instance = BinaSTT()
    return _stt_instance
