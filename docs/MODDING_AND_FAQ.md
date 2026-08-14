# 🛠️ Bina: Modding, Customization & FAQ

Bina was built to be highly customizable. Whether you want to change her language, create new personalities, or understand how the under-the-hood engine works, this guide has you covered.

---

## 1. How to Change Bina's Language (English, etc.)

By default, Bina is configured to speak **Spanish**. This includes both the LLM's internal prompt and the Text-to-Speech (Piper) `.onnx` models.

If you speak English to Bina, she will understand you (Whisper is multilingual), but she will reply in Spanish. To make her fully English-speaking, follow these steps:

### Step 1: Change the System Prompt
1. Open `src/config.py`.
2. Find the `SYSTEM_PROMPT` inside your `ACTIVE_PRESET`.
3. Translate the instructions to English (e.g., change *"Deben responder siempre en español"* to *"You must always reply in English"*).

### Step 2: Download English Piper Models
Piper requires specific phonetic models for each language.
1. Go to the [Piper Voices Repository](https://github.com/rhasspy/piper/wiki/Voices).
2. Download an English model (e.g., `en_US-lessac-high.onnx` and its `.json` file). You need two different voices (one for Lia, one for Nox).
3. Place these files inside your `models/` folder.

### Step 3: Update `config.py` Paths
In `src/config.py`, update the paths to point to your new English models:
```python
LIA_VOICE_PATH = "models/en_US-lessac-high.onnx"
NOX_VOICE_PATH = "models/en_US-ryan-high.onnx"
```
Restart your server, and Bina will now speak fluent English!

---

## 2. How to Change Personalities (Jedi Mode)

Bina comes with built-in personality presets. The LLM acts out whatever characters you define in the prompt.

**To activate a different preset:**
1. Open `src/config.py`.
2. Find the line: `ACTIVE_PRESET = "duo_original"`
3. Change it to one of the available presets, for example: `ACTIVE_PRESET = "jedi_sith"`
4. Restart the server (`sudo systemctl restart bina` or relaunch `server.py`).

**Available Presets:**
- `duo_original`: Lia (Empathetic) vs Nox (Logical).
- `jedi_sith`: Wisdom of the Light vs Power of the Dark Side.
- `creyente_esceptico`: Paranormal Believer vs Strict Skeptical Scientist.

**Create your own:**
You can easily add a new preset in the `PRESETS` dictionary inside `config.py` by defining the characters' names, their core philosophies, and rules of engagement.

---

## 3. Deep Dive: How the Architecture Works

If you are a developer looking to tinker with the code, here is a quick overview of Bina's engine:

- **Single LLM, Dual Persona:** Bina doesn't run two heavy LLMs. She uses a single Llama 3 instance with a highly engineered System Prompt. The prompt forces the LLM to output a strict JSON array (using Pydantic Structured Outputs) containing a sequential dialogue between the two characters. 
- **Lightning Fast Audio:** Bina doesn't wait for the whole paragraph to be generated to start speaking. When the LLM generates a line for Lia, the server sends a JSON state to the frontend (`{"type": "speaking_lia"}`), immediately followed by the binary audio blob for just that sentence. 
- **Organic CSS Animations:** The eyes on the frontend are not videos or canvas. They are 100% Vanilla CSS HTML elements manipulating `border-radius`, `box-shadow`, and `transform: translateY` based on the emotions sent by the LLM.

---

## 4. FAQ & Common Issues

**Q: Bina gets stuck on "Pensando..." and never answers.**
* **A:** Check if Ollama is running. If Ollama is hosted on a different machine, ensure `OLLAMA_HOST` is correctly set in your environment before running the server (`export OLLAMA_HOST=http://IP:11434`).

**Q: The microphone button doesn't work on my phone.**
* **A:** Mobile browsers (Safari/Chrome) block microphone access on `http://` sites for security reasons. You MUST access Bina via `https://` or use the Chrome Dev Flag trick mentioned in the main README (`chrome://flags/#unsafely-treat-insecure-origin-as-secure`) to whitelist your Tailscale/Local IP.

**Q: Can I run this on Windows?**
* **A:** The `install_bina.sh` script is designed for Linux (Ubuntu/Debian). However, the Python code is cross-platform. You can manually install the `requirements.txt` on Windows, but you will need to download the Piper models manually and adjust the paths.
