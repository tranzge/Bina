#!/bin/bash
echo "==============================================="
echo "   INSTALADOR DE BINA CORE (UBUNTU SERVER)   "
echo "==============================================="

# 1. Instalar dependencias del sistema operativo
echo "[1/4] Instalando dependencias de sistema (ffmpeg y python)..."
sudo apt update
sudo apt install -y python3 python3-venv python3-pip ffmpeg

# 2. Crear y activar el entorno virtual
echo "[2/4] Creando entorno virtual de Python..."
python3 -m venv venv
source venv/bin/activate

# 3. Instalar librerías de Python
echo "[3/4] Instalando librerías requeridas (FastAPI, Whisper, Piper, etc)..."
pip install --upgrade pip
pip install fastapi uvicorn websockets ollama faster-whisper piper-tts requests pydantic soundfile

echo "Descargando modelos de voz (Piper)..."
mkdir -p models
cd models
wget -nc https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_MX/claude/high/es_MX-claude-high.onnx
wget -nc https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_MX/claude/high/es_MX-claude-high.onnx.json
wget -nc https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_MX/ald/medium/es_MX-ald-medium.onnx
wget -nc https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_MX/ald/medium/es_MX-ald-medium.onnx.json
cd ..

# 4. Crear un servicio de Systemd para que arranque solo (Opcional)
echo "[4/4] Configurando servicio automático..."
read -p "¿Quieres que Bina inicie automáticamente con el servidor? (s/n): " AUTO
if [[ "$AUTO" == "s" || "$AUTO" == "S" ]]; then
    SERVICE_FILE="/etc/systemd/system/bina.service"
    CURRENT_DIR=$(pwd)
    USER=$(whoami)
    
    sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Bina AI Core Server
After=network.target

[Service]
User=$USER
WorkingDirectory=$CURRENT_DIR
Environment="OLLAMA_HOST=http://127.0.0.1:11434"
ExecStart=$CURRENT_DIR/venv/bin/python src/server.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL

    sudo systemctl daemon-reload
    sudo systemctl enable bina
    sudo systemctl start bina
    echo "¡Servicio Systemd creado y arrancado!"
    echo "Puedes ver los logs con: sudo journalctl -fu bina"
else
    echo "Omitido. Puedes arrancar Bina manualmente con:"
    echo "export OLLAMA_HOST=http://127.0.0.1:11434 && ./venv/bin/python src/server.py"
fi

echo "==============================================="
echo " ¡INSTALACIÓN COMPLETA! Bina está en el servidor "
echo "==============================================="
