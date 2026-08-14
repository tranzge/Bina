# 👁️ Bina: The Dual-Personality Local AI

<p align="center">
  <img src="https://img.shields.io/badge/100%25-Offline-success?style=for-the-badge" alt="Offline">
  <img src="https://img.shields.io/badge/Privacy-First-blue?style=for-the-badge" alt="Privacy First">
  <img src="https://img.shields.io/badge/Powered%20By-Llama%203.1-orange?style=for-the-badge" alt="Llama 3.1">
  <img src="https://img.shields.io/badge/Engine-FastAPI-009688?style=for-the-badge" alt="FastAPI">
</p>

> **No es un chatbot complaciente. Son dos inteligencias artificiales compartiendo una misma mente, debatiendo entre ellas y hablándote en tiempo real, 100% offline.**

*( Inserta tu GIF de demostración animado aquí )*

## 🎭 ¿Qué es Bina?

Bina es un experimento de Arquitectura de Múltiples Agentes (Multi-Agent Architecture) diseñado para correr localmente en tu propio hardware. A través de una interfaz web minimalista e hipnótica, interactúas por voz con dos entidades simultáneas:

- **Lia (Ojo Izquierdo):** Empática, soñadora, cálida y creativa. Piensa en el "cómo podemos ayudar".
- **Nox (Ojo Derecho):** Frío, calculador, hiper-lógico y sarcástico. Identifica riesgos y destruye el optimismo ciego.

En lugar de darte una respuesta robótica, **Lia y Nox debaten entre ellos antes de darte una conclusión.** Escuchan tu voz en tiempo real, procesan la lógica y te responden con voces sintetizadas de alta calidad, mientras ves sus expresiones cambiar dinámicamente en pantalla.

---

## 🏗️ Arquitectura "Privacy-First"

Bina está construida con la filosofía de que **tus datos no deben salir de tu casa**. No se conecta a APIs de terceros, no cobra por token y no almacena tu información en la nube. Todo el stack tecnológico corre en tu hardware:

1. **Voz a Texto (STT):** `Faster-Whisper` transcribe tu voz localmente evadiendo ruidos de fondo.
2. **Cerebro (LLM):** `Ollama` ejecutando (recomendado) `llama3.1:8b` o `qwen2.5:14b` usando **Salidas Estructuradas (Pydantic)**.
3. **Memoria Vectorial:** `ChromaDB` (con `nomic-embed-text`) guarda contexto a largo plazo.
4. **Texto a Voz (TTS):** `Piper` genera las voces de Lia y Nox en milisegundos con modelos `.onnx` hiper optimizados.
5. **Orquestador:** `FastAPI` + WebSockets.
6. **Frontend:** Vanilla JS / CSS (Animaciones orgánicas, diseño 100dvh responsivo para móviles).

---

## 🚀 Instalación en 2 Minutos (Linux / Ubuntu Server)

Si ya tienes [Ollama instalado](https://ollama.com/), levantar a Bina es absurdamente fácil:

```bash
# 1. Clona este repositorio
git clone https://github.com/tu-usuario/Bina.git
cd Bina

# 2. Ejecuta el instalador mágico
bash install_bina.sh
```

El script se encargará de crear el entorno virtual, instalar dependencias (`fastapi`, `faster-whisper`, `piper-tts`), descargar automáticamente los modelos de voz en español y levantar el servicio en `http://tu-ip:8000`.

---

## ⚙️ Modding y Personalización (¡Juega a ser Dios!)

¿Te aburriste de la personalidad original? ¿Quieres que Bina hable como un Maestro Jedi y un Lord Sith? 

Bina está diseñada para ser ultra-personalizable. Solo abre el archivo `src/config.py`:

```python
# src/config.py
ACTIVE_PRESET = "jedi_sith" # Cambia esto para rotar personalidades
```

### Presets Incluidos de Fábrica:
1. `duo_original`: Lia (Empática) vs Nox (Lógico).
2. `jedi_sith`: Sabiduría de la Luz vs Poder del Lado Oscuro.
3. `creyente_esceptico`: Conspiraciones Paranormales vs Método Científico Estricto.

También puedes cambiar los modelos de voz de Piper y la dirección de tu servidor de Ollama directamente desde este mismo archivo de configuración.

---

## 📱 ¿Cómo usarlo desde el celular?

1. Abre tu navegador (Safari / Chrome) y entra a `http://IP_DE_TU_SERVIDOR:8000`.
2. Como los navegadores bloquean el micrófono en sitios sin `https://`, **es vital** habilitar este flag de desarrollador en tu celular si no usas SSL:
   - Ve a: `chrome://flags/#unsafely-treat-insecure-origin-as-secure`
   - Agrega tu IP (`http://192.168.x.x:8000`), marca **Enabled** y reinicia el navegador.
3. ¡Presiona el botón inferior y empieza a hablar!

---
> Creado con ❤️ por Tranzge. Si este proyecto te voló la cabeza, ¡déjale una estrellita ⭐ en GitHub!
