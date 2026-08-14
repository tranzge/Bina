const body = document.body;
const liaContainer = document.getElementById('lia-container');
const noxContainer = document.getElementById('nox-container');

// Máquinas de estado
const globalStates = ['idle', 'listening', 'thinking', 'speaking_lia', 'speaking_nox'];
const validEmotions = ['neutral', 'happy', 'angry', 'sad', 'surprise'];

// Mapeo de emociones en español (LLM) a clases CSS en inglés
const emotionMap = {
    'feliz': 'happy',
    'alegre': 'happy',
    'contenta': 'happy',
    'contento': 'happy',
    'satisfecho': 'happy',
    'satisfecha': 'happy',
    'enojado': 'angry',
    'enojada': 'angry',
    'molesto': 'angry',
    'molesta': 'angry',
    'crítico': 'angry',
    'critico': 'angry',
    'triste': 'sad',
    'decepcionado': 'sad',
    'pensativo': 'neutral',
    'analítico': 'neutral',
    'analitico': 'neutral',
    'empático': 'happy',
    'empatica': 'happy',
    'curiosa': 'surprise',
    'curioso': 'surprise',
    'serio': 'neutral',
    'sorprendido': 'surprise',
    'sorprendida': 'surprise',
    'sorpresa': 'surprise'
};

// Estado actual
let currentState = 'idle';

function setGlobalState(newState) {
    if (!globalStates.includes(newState)) return;
    
    // Limpiar clases state- globales
    globalStates.forEach(s => body.classList.remove(`state-${s}`));
    
    body.classList.add(`state-${newState}`);
    currentState = newState;
    console.log(`Bina Estado Global: ${newState}`);
}

function setEmotion(character, emotionRaw) {
    // Convertir emoción del LLM a nuestra clase CSS, limpiando espacios y signos de puntuación
    let raw = (emotionRaw || 'neutral').toLowerCase().trim().replace(/[^a-zñáéíóú]/g, '');
    let emotion = emotionMap[raw] || (validEmotions.includes(raw) ? raw : 'neutral');
    
    if (!validEmotions.includes(emotion)) emotion = 'neutral';
    
    const container = character === 'lia' ? liaContainer : noxContainer;
    
    // Limpiar emociones anteriores
    validEmotions.forEach(e => container.classList.remove(`emotion-${e}`));
    
    container.classList.add(`emotion-${emotion}`);
    console.log(`${character.toUpperCase()} Emoción Parseada: ${emotion} (Recibida: '${emotionRaw}', Limpia: '${raw}')`);
}

// === Sistema de Parpadeo Natural === //
function blinkEye(characterElement) {
    // Buscar todos los párpados de este personaje (los dos ojos)
    const topLids = characterElement.querySelectorAll('.top-lid');
    const bottomLids = characterElement.querySelectorAll('.bottom-lid');

    // Forzar párpados cerrados (sobreescribiendo las transformaciones de emoción temporalmente)
    topLids.forEach(lid => {
        lid.style.transition = 'transform 0.1s cubic-bezier(0.25, 0.8, 0.25, 1)';
        lid.style.transform = 'translateY(100%) rotate(0deg)';
    });
    
    bottomLids.forEach(lid => {
        lid.style.transition = 'transform 0.1s cubic-bezier(0.25, 0.8, 0.25, 1)';
        lid.style.transform = 'translateY(-100%) rotate(0deg)';
    });

    // Abrir ojo después de 150ms
    setTimeout(() => {
        // Restaurar a vacío para que el CSS (o la emoción actual) tome el control de nuevo
        topLids.forEach(lid => lid.style.transform = '');
        bottomLids.forEach(lid => lid.style.transform = '');
        
        // Retornar transición original
        setTimeout(() => {
            topLids.forEach(lid => lid.style.transition = '');
            bottomLids.forEach(lid => lid.style.transition = '');
        }, 150);

    }, 150);
}

function randomBlinkLoop() {
    // Solo parpadear si no están muy concentrados (puedes ajustar esta lógica)
    if (currentState !== 'thinking') {
        // Probabilidad de parpadeo (simula comportamiento orgánico)
        if (Math.random() > 0.4) {
            // A veces parpadean juntos, a veces separados
            const both = Math.random() > 0.7;
            if (both) {
                blinkEye(liaContainer);
                blinkEye(noxContainer);
            } else {
                if (Math.random() > 0.5) blinkEye(liaContainer);
                else blinkEye(noxContainer);
            }
        }
    }
    
    // Siguiente parpadeo entre 2 y 6 segundos
    const nextBlink = Math.floor(Math.random() * 4000) + 2000;
    setTimeout(randomBlinkLoop, nextBlink);
}

// === SISTEMA WEBSOCKET Y AUDIO === //
let ws;
let mediaRecorder;
let audioChunks = [];

let audioQueue = [];
let isPlaying = false;
let pendingState = null;

const micBtn = document.getElementById('mic-btn');

function addChatMessage(role, text) {
    const chatHistory = document.getElementById('chat-history');
    if (!chatHistory) return;
    
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('chat-msg');
    
    if (role === 'user') {
        msgDiv.classList.add('msg-user');
        msgDiv.innerText = text;
    } else if (role === 'lia') {
        msgDiv.classList.add('msg-lia');
        msgDiv.innerText = `Lia: ${text}`;
    } else if (role === 'nox') {
        msgDiv.classList.add('msg-nox');
        msgDiv.innerText = `Nox: ${text}`;
    } else {
        msgDiv.classList.add('msg-system');
        msgDiv.innerText = text;
    }
    
    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function initWebSocket() {
    const wsUrl = `ws://${window.location.host}/ws/bina`;
    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        console.log("Conectado a BINA Core");
        addChatMessage('system', '¡Conectado! Presiona el botón para hablar.');
    };

    ws.onmessage = async (event) => {
        // Si recibimos un blob (audio en bytes desde Piper)
        if (event.data instanceof Blob) {
            // Forzar el tipo MIME a WAV para que el navegador sepa cómo reproducirlo
            const wavBlob = new Blob([event.data], { type: 'audio/wav' });
            
            if (pendingState) {
                audioQueue.push({ blob: wavBlob, stateData: pendingState });
                pendingState = null; // Limpiar para el siguiente
                if (!isPlaying) {
                    playNextInQueue();
                }
            }
            return;
        }

        // Si recibimos JSON
        try {
            const data = JSON.parse(event.data);
            
            if (data.type === 'state') {
                if (data.value.startsWith('speaking')) {
                    // Es un estado de hablar, lo guardamos para emparejarlo con el audio que viene inmediatamente después
                    pendingState = data;
                } else if (data.value === 'thinking') {
                    setGlobalState('thinking');
                } else if (data.value === 'idle' && !isPlaying) {
                    setGlobalState('idle');
                    micBtn.innerText = "🎙️ Mantener presionado para hablar";
                }
            } else if (data.type === 'transcription') {
                addChatMessage('user', data.text);
            }
        } catch (e) {
            console.error("Mensaje WS no parseable:", e);
        }
    };

    ws.onclose = () => {
        addChatMessage('system', "Desconectado. Reconectando en 3s...");
        setTimeout(initWebSocket, 3000);
    };
}

// Reproductor de Audio Secuencial
function playNextInQueue() {
    if (audioQueue.length === 0) {
        isPlaying = false;
        setGlobalState('idle');
        micBtn.innerText = "🎙️ Mantener presionado para hablar";
        return;
    }
    
    isPlaying = true;
    const { blob, stateData } = audioQueue.shift();
    
    // Aplicar estado visual antes de hablar
    setGlobalState(stateData.value);
    setEmotion(stateData.character, stateData.emotion);
    
    // Añadir al historial limpio (sin etiquetas de debug)
    addChatMessage(stateData.character, stateData.text);
    
    // Reproducir audio
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);
    audio.play().catch(e => {
        console.error("Error reproduciendo audio:", e);
        URL.revokeObjectURL(url);
        playNextInQueue();
    });
    
    audio.onended = () => {
        URL.revokeObjectURL(url);
        playNextInQueue(); // Reproducir el siguiente de la cola (ej. Nox respondiendo a Lia)
    };
}

// === CAPTURA DE MICRÓFONO === //
async function initAudio() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });

        mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) {
                audioChunks.push(e.data);
            }
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            if (ws && ws.readyState === WebSocket.OPEN && audioBlob.size > 0) {
                // Mensaje del sistema aleatorio mientras piensa
                const frasesEspera = ["Lia buscando recuerdos...", "Nox analizando dependencias...", "Buscando contexto...", "Procesando LLM..."];
                const fraseAleatoria = frasesEspera[Math.floor(Math.random() * frasesEspera.length)];
                addChatMessage('system', fraseAleatoria);
                
                ws.send(audioBlob);
            }
            audioChunks = [];
        };

        const startRecording = (e) => {
            e.preventDefault();
            if (mediaRecorder.state === 'inactive') {
                audioChunks = [];
                mediaRecorder.start();
                micBtn.classList.add('recording');
                micBtn.innerText = "🔴 Escuchando...";
            }
        };

        const stopRecording = (e) => {
            e.preventDefault();
            if (mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
                micBtn.classList.remove('recording');
                micBtn.innerText = "🧠 Procesando LLM...";
            }
        };

        micBtn.addEventListener('mousedown', startRecording);
        micBtn.addEventListener('mouseup', stopRecording);
        micBtn.addEventListener('mouseleave', stopRecording);
        
        micBtn.addEventListener('touchstart', startRecording);
        micBtn.addEventListener('touchend', stopRecording);

    } catch (err) {
        console.error("No se pudo acceder al micrófono:", err);
        addChatMessage('system', "Error: Sin acceso al micrófono");
    }
}


// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    setGlobalState('idle');
    setEmotion('lia', 'neutral');
    setEmotion('nox', 'neutral');
    
    // Iniciar loop orgánico de parpadeo
    setTimeout(randomBlinkLoop, 2000);
    
    // Iniciar WS y Audio
    initWebSocket();
    initAudio();
});
