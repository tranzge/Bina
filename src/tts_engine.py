import os
import wave
import tempfile
import subprocess
import shutil
from piper.voice import PiperVoice
import config

class BinaTTS:
    def __init__(self, models_dir="models"):
        self.voices = {}
        print("Cargando motores de voz TTS (Piper)... esto tomará unos segundos.")
        
        lia_model = os.path.join(models_dir, config.VOICE_LIA)
        nox_model = os.path.join(models_dir, config.VOICE_NOX)
        
        if os.path.exists(lia_model):
            self.voices['Lia'] = PiperVoice.load(lia_model)
        else:
            print(f"[Advertencia] Modelo de Lia no encontrado en: {lia_model}")
            
        if os.path.exists(nox_model):
            self.voices['Nox'] = PiperVoice.load(nox_model)
        else:
            print(f"[Advertencia] Modelo de Nox no encontrado en: {nox_model}")
            
        # Detectar reproductor de audio disponible en Linux
        self.player_cmd = None
        for cmd in ['aplay', 'paplay', 'mpv', 'ffplay']:
            if shutil.which(cmd):
                self.player_cmd = cmd
                break
        
        if not self.player_cmd:
            print("[Aviso] No se detectó aplay, paplay, mpv ni ffplay. No habrá audio.")

    def synthesize_to_file(self, personaje: str, texto: str, output_path: str):
        if personaje not in self.voices:
            return False
            
        voice = self.voices[personaje]
        try:
            with wave.open(output_path, "wb") as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(voice.config.sample_rate)
                # Piper devuelve un iterador de objetos AudioChunk
                for audio_chunk in voice.synthesize(texto):
                    f.writeframes(audio_chunk.audio_int16_bytes)
            return True
        except Exception as e:
            print(f"[TTS Error] Fallo al sintetizar audio: {e}")
            return False

    def get_audio_bytes(self, personaje: str, texto: str) -> bytes:
        """Sintetiza texto y retorna los bytes crudos del archivo WAV."""
        temp_wav = tempfile.mktemp(suffix=".wav")
        success = self.synthesize_to_file(personaje, texto, temp_wav)
        
        if not success:
            return b""
            
        try:
            with open(temp_wav, "rb") as f:
                wav_bytes = f.read()
            return wav_bytes
        except Exception:
            return b""
        finally:
            if os.path.exists(temp_wav):
                try:
                    os.remove(temp_wav)
                except OSError:
                    pass

    def speak(self, personaje: str, texto: str):
        """Método de desarrollo local (reproduce en la laptop)."""
        if not self.player_cmd:
            return

        temp_wav = tempfile.mktemp(suffix=".wav")
        if not self.synthesize_to_file(personaje, texto, temp_wav):
            return
            
        # Reproducir el audio secuencialmente usando subprocess
        try:
            if self.player_cmd == 'ffplay':
                cmd = ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', temp_wav]
            elif self.player_cmd == 'mpv':
                cmd = ['mpv', '--really-quiet', temp_wav]
            else:
                cmd = [self.player_cmd, '-q', temp_wav]
                
            subprocess.run(cmd, check=True)
        except Exception as e:
            print(f"[TTS Error] No se pudo reproducir audio con {self.player_cmd}: {e}")
        finally:
            if os.path.exists(temp_wav):
                try:
                    os.remove(temp_wav)
                except OSError:
                    pass

# Singleton para uso global si se desea
_tts_instance = None

def get_tts():
    global _tts_instance
    if _tts_instance is None:
        _tts_instance = BinaTTS()
    return _tts_instance
