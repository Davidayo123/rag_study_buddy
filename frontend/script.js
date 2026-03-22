const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const pdfUpload = document.getElementById('pdf-upload');
const uploadBanner = document.getElementById('upload-banner');
const uploadStatus = document.getElementById('upload-status');
const uploadSpinner = document.getElementById('upload-spinner');

// --- CHAT LOGIC ---
function appendMessage(sender, text, type) {
    // Remove the welcome card if it exists
    const welcomeCard = chatContainer.querySelector('.welcome-card');
    if (welcomeCard) welcomeCard.remove();

    const messageDiv = document.createElement('div');

    let className = 'message ';
    switch (type) {
        case 'user':    className += 'message-user'; break;
        case 'ai':      className += 'message-ai'; break;
        case 'system':  className += 'message-system'; break;
        case 'error':   className += 'message-error'; break;
        default:        className += 'message-ai';
    }
    messageDiv.className = className;

    // Parse markdown-style bold text and newlines
    let formattedText = text.replace(/\n/g, '<br>');
    formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    messageDiv.innerHTML = `<strong>${sender}</strong>${formattedText}`;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showLoadingMessage() {
    const welcomeCard = chatContainer.querySelector('.welcome-card');
    if (welcomeCard) welcomeCard.remove();

    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'loading-indicator';
    loadingDiv.className = 'message message-loading';
    loadingDiv.innerHTML = `
        <strong>Tutor</strong>
        Thinking
        <span class="dot-pulse">
            <span></span><span></span><span></span>
        </span>
    `;
    chatContainer.appendChild(loadingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeLoadingMessage() {
    const loader = document.getElementById('loading-indicator');
    if (loader) loader.remove();
}

async function sendMessage() {
    const question = userInput.value.trim();
    if (!question) return;

    appendMessage('You', question, 'user');
    userInput.value = '';
    showLoadingMessage();

    try {
        const response = await fetch('http://127.0.0.1:8000/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question })
        });

        const data = await response.json();
        removeLoadingMessage();

        if (response.ok) {
            appendMessage('Tutor', data.answer, 'ai');
        } else {
            appendMessage('Error', data.detail || 'Something went wrong.', 'error');
        }
    } catch (error) {
        removeLoadingMessage();
        appendMessage('Connection Error', 'Could not connect to the backend. Is your Python server running?', 'error');
    }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// --- UPLOAD LOGIC ---
function setBannerStatus(status, message) {
    uploadBanner.classList.remove('hidden', 'status-loading', 'status-success', 'status-error');
    uploadBanner.classList.add('status-' + status);
    uploadStatus.textContent = message;
    uploadSpinner.style.display = status === 'loading' ? 'block' : 'none';
}

pdfUpload.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setBannerStatus('loading', `Processing "${file.name}"... This may take a moment.`);

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://127.0.0.1:8000/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            setBannerStatus('success', data.message);
            appendMessage('System', `Finished reading "${file.name}". You can now ask questions about it.`, 'system');

            // Auto-hide success banner after 5 seconds
            setTimeout(() => {
                uploadBanner.classList.add('hidden');
            }, 5000);
        } else {
            throw new Error(data.detail || 'Upload failed');
        }
    } catch (error) {
        setBannerStatus('error', 'Upload failed. Check terminal for errors.');
        console.error(error);
    }

    pdfUpload.value = '';
});