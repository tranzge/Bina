# 👁️ Bina: The Dual-Personality Local AI

<p align="center">
  <img src="https://img.shields.io/badge/100%25-Offline-success?style=for-the-badge" alt="Offline">
  <img src="https://img.shields.io/badge/Privacy-First-blue?style=for-the-badge" alt="Privacy First">
  <img src="https://img.shields.io/badge/Powered%20By-Llama%203.1-orange?style=for-the-badge" alt="Llama 3.1">
  <img src="https://img.shields.io/badge/Engine-FastAPI-009688?style=for-the-badge" alt="FastAPI">
</p>

> **Not your average compliant chatbot. Bina is an experiment in Multi-Agent Architecture where two distinct AIs share a single virtual body, debate with each other, and talk to you in real-time, 100% offline.**

*( Pega tu video/GIF aquí )*
*(Note: The demo above is in Spanish, but Bina's logic supports any language your LLM handles).*

## 🎭 What is Bina?

Bina is a lightweight, privacy-first AI companion designed to run locally on your own hardware. Through a hypnotic, minimalist web interface, you interact via voice with two simultaneous entities:

- **Lia (Left Eye):** Empathetic, dreamer, warm, and creative. She focuses on the human element and "how we can help."
- **Nox (Right Eye):** Cold, calculating, hyper-logical, and sarcastic. He identifies risks and actively destroys blind optimism.

Instead of giving you a robotic, single-turn answer, **Lia and Nox debate each other before giving you a conclusion.** They listen to your voice in real-time, process logic using structured outputs, and reply with high-quality synthesized voices while their eyes dynamically react on screen.

---

## 🏗️ Privacy-First Architecture

Bina was built with one philosophy: **your data never leaves your house.** No third-party APIs, no token fees, no cloud storage. The entire stack runs on your machine:

1. **Speech-to-Text (STT):** `Faster-Whisper` transcribes your voice locally.
2. **Brain (LLM):** `Ollama` running `llama3.1:8b` (recommended) with **Structured Outputs (Pydantic)**.
3. **Vector Memory:** `ChromaDB` (`nomic-embed-text`) for long-term context (WIP).
4. **Text-to-Speech (TTS):** `Piper` generates Lia and Nox's voices in milliseconds using hyper-optimized `.onnx` models.
5. **Backend:** `FastAPI` + WebSockets.
6. **Frontend:** Vanilla JS / CSS (Organic animations, 100dvh mobile-responsive design).

---

## 🚀 2-Minute Setup (Linux / Ubuntu Server)

Assuming you have [Ollama installed](https://ollama.com/), firing up Bina is absurdly simple:

```bash
# 1. Clone the repository
git clone https://github.com/tranzge/Bina.git
cd Bina

# 2. Run the magic installer
bash install_bina.sh
```

The script will handle virtual environments, install dependencies (`fastapi`, `faster-whisper`, `piper-tts`), automatically download the Spanish Piper voice models, and boot the server at `http://your-ip:8000`.

---

## ⚙️ Modding & Customization (Play God)

Bored of the original personalities? Want Bina to speak like a Jedi Master and a Sith Lord?

Bina is designed to be ultra-customizable. Just edit `src/config.py`:

```python
# src/config.py
ACTIVE_PRESET = "jedi_sith" # Change this to rotate personalities
```

### Included Presets:
1. `duo_original`: Lia (Empathetic) vs Nox (Logical).
2. `jedi_sith`: Wisdom of the Light vs Power of the Dark Side.
3. `creyente_esceptico`: Paranormal Believer vs Strict Skeptical Scientist.

You can also change the Piper voice paths and your Ollama host address directly from the config file.

---

## 📱 Mobile Usage

1. Open your browser (Safari / Chrome) and go to `http://YOUR_SERVER_IP:8000`.
2. Since browsers block microphone access on non-HTTPS sites, you **must** enable this dev flag if you are not using SSL:
   - Go to: `chrome://flags/#unsafely-treat-insecure-origin-as-secure`
   - Add your IP (`http://192.168.x.x:8000`), set to **Enabled**, and relaunch.
3. Tap the bottom button and start talking!

---

*(Versión en Español abajo / Spanish version below)*

---

# 👁️ Bina: IA Local de Doble Personalidad

> **No es un chatbot complaciente. Son dos inteligencias artificiales compartiendo una misma mente, debatiendo entre ellas y hablándote en tiempo real, 100% offline.**

## 🎭 ¿Qué es Bina?

Bina es un experimento de Arquitectura de Múltiples Agentes diseñado para correr localmente. Interactúas por voz con dos entidades simultáneas:

- **Lia (Ojo Izquierdo):** Empática, soñadora, cálida y creativa. Piensa en el "cómo podemos ayudar".
- **Nox (Ojo Derecho):** Frío, calculador, hiper-lógico y sarcástico. Identifica riesgos y destruye el optimismo ciego.

En lugar de darte una respuesta robótica, **Lia y Nox debaten entre ellos antes de darte una conclusión.**

## 🏗️ Arquitectura "Privacy-First"

Tus datos no salen de tu casa. Todo corre en tu hardware:
1. **STT:** `Faster-Whisper` transcribe tu voz localmente.
2. **LLM:** `Ollama` ejecutando `llama3.1:8b` usando **Salidas Estructuradas (Pydantic)**.
3. **Memoria:** `ChromaDB` guarda contexto a largo plazo.
4. **TTS:** `Piper` genera las voces en milisegundos.
5. **Orquestador:** `FastAPI` + WebSockets.
6. **Frontend:** Vanilla JS / CSS.

> Creado con ❤️ por Tranzge. Si este proyecto te voló la cabeza, ¡déjale una estrellita ⭐!
