# 👁️ Bina: The Dual-Personality Local AI

<p align="center">
  <img src="https://img.shields.io/badge/100%25-Offline-success?style=for-the-badge" alt="Offline">
  <img src="https://img.shields.io/badge/Privacy-First-blue?style=for-the-badge" alt="Privacy First">
  <img src="https://img.shields.io/badge/Powered%20By-Llama%203.1-orange?style=for-the-badge" alt="Llama 3.1">
  <img src="https://img.shields.io/badge/Engine-FastAPI-009688?style=for-the-badge" alt="FastAPI">
</p>

> **Not your average compliant chatbot. Bina is an experiment in Multi-Agent Architecture where two distinct AIs share a single virtual body, debate with each other, and talk to you in real-time. No physical displays or expensive hardware needed—just your phone and a home server.**

*( Pega tu video/GIF aquí )*
*(Note: The demo above is in Spanish, but Bina's logic supports any language your LLM handles).*

## 🎭 What is Bina?

Bina is a lightweight, privacy-first AI companion designed to run locally on your own hardware, but accessible **anywhere from your smartphone**. Through a hypnotic, minimalist web interface, you interact via voice with two simultaneous entities:

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

The script will handle virtual environments, install dependencies, download the Spanish Piper voice models, and boot the server at `http://your-ip:8000`.

---

## 📱 Mobile & Remote Access (The Magic Trick)

Bina is designed to live in your pocket without draining your phone's battery. All the heavy lifting (LLM, TTS, STT) happens on your home server. 

To use Bina securely from anywhere in the world:
1. Install [Tailscale](https://tailscale.com/) on both your Home Server and your Smartphone.
2. Open your phone's browser (Safari/Chrome) and go to your server's Tailscale IP: `http://YOUR_TAILSCALE_IP:8000`.
3. **Crucial Step (Microphone Permissions):** Since mobile browsers block microphone access on non-HTTPS sites, you must enable this dev flag to allow Tailscale IPs:
   - Go to `chrome://flags/#unsafely-treat-insecure-origin-as-secure`
   - Add your Tailscale IP (`http://100.x.x.x:8000`), set to **Enabled**, and relaunch.
4. Tap the screen and start talking!

---

## ⚙️ Modding & Customization (Play God)

Bina is designed to be ultra-customizable. Just edit `src/config.py`:

```python
# src/config.py
ACTIVE_PRESET = "jedi_sith" # Change this to rotate personalities
```

### Included Presets:
1. `duo_original`: Lia (Empathetic) vs Nox (Logical).
2. `jedi_sith`: Wisdom of the Light vs Power of the Dark Side.
3. `creyente_esceptico`: Paranormal Believer vs Strict Skeptical Scientist.

---

## 🤖 Acknowledgments

This project is the result of a massive collaboration between human creativity and Artificial Intelligence. The architecture, logic, and code were heavily co-developed by Tranzge alongside **Google Antigravity, ChatGPT, Gemini, and Claude**. 

If you ask me how a specific WebSocket buffer or Piper TTS threading works under the hood... I'll probably ask my AI team! We are entering an era where you don't need to be a senior developer to build complex, multi-agent architectures—you just need the right vision and the right AI companions.

> Built with ❤️ by Tranzge & The AIs. If this project blew your mind, drop a ⭐!

---

*(Versión en Español abajo / Spanish version below)*

---

# 👁️ Bina: IA Local de Doble Personalidad

> **No es un chatbot complaciente. Son dos inteligencias artificiales compartiendo una misma mente. No necesitas pantallas físicas caras; la llevas en tu celular mientras tu servidor hace el trabajo pesado en casa.**

## 🎭 ¿Qué es Bina?

Bina es un experimento de Arquitectura de Múltiples Agentes diseñado para correr localmente. Interactúas por voz con dos entidades simultáneas:

- **Lia (Ojo Izquierdo):** Empática, cálida y creativa. Piensa en el "cómo podemos ayudar".
- **Nox (Ojo Derecho):** Frío, calculador y sarcástico. Identifica riesgos y destruye el optimismo ciego.

En lugar de darte una respuesta robótica, **Lia y Nox debaten entre ellos antes de darte una conclusión.**

## 🌍 Llévala en tu bolsillo con Tailscale
Instala **Tailscale** en tu servidor y en tu celular. Accede a la IP de Tailscale desde Chrome/Safari en tu móvil (`http://100.x.x.x:8000`) y tendrás a Bina contigo en cualquier parte del mundo. (No olvides habilitar el flag `unsafely-treat-insecure-origin` en Chrome para que funcione el micrófono).

## 🤖 Créditos
Este código fue co-creado por Tranzge en equipo con **Google Antigravity, ChatGPT, Gemini y Claude**. Un testamento de que hoy en día la visión importa más que saber memorizar sintaxis.

> Creado con ❤️ por Tranzge y las IAs. Si este proyecto te voló la cabeza, ¡déjale una estrellita ⭐!
