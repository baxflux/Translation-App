let translationStartTime = null;
let currentExpandTarget = null;

function clearText() {
    const source = document.getElementById("source_text");
    const translation = document.getElementById("translation");

    if (source) source.value = "";
    if (translation) translation.value = "";
}

function getHistory() {
    return JSON.parse(localStorage.getItem('translationHistory') || '[]');
}

function saveHistory(entry) {
    if (!entry.source || !entry.target) return;
    const history = getHistory();
    const last = history[0];

    if (last && last.source === entry.source && last.target === entry.target) return;

    const time = new Date();
    entry.time = time.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    entry.summary = `${entry.source.slice(0, 50)}${entry.source.length > 50 ? '...' : ''}`;
    entry.language = 'English → Vietnamese';
    entry.words_source = entry.source.trim() ? entry.source.trim().split(/\s+/).length : 0;
    entry.words_target = entry.target.trim() ? entry.target.trim().split(/\s+/).length : 0;
    
    // Duration được truyền từ ngoài, nếu không có thì dùng default
    if (!entry.duration) {
        entry.duration = '0.2s';
    }

    history.unshift(entry);
    localStorage.setItem('translationHistory', JSON.stringify(history.slice(0, 10)));
}

function renderHistory() {
    const list = document.getElementById('historyList');
    const history = getHistory();

    if (!list) return;
    list.innerHTML = '';

    if (!history.length) {
        list.innerHTML = '<div class="history-empty">No history yet. Translate a sentence to save entries.</div>';
        return;
    }

    history.forEach((item, index) => {
        const container = document.createElement('div');
        container.className = 'history-item-container';
        
        const node = document.createElement('button');
        node.type = 'button';
        node.className = 'history-item';
        const itemNumber = history.length - index;
        node.innerHTML = `
            <div class="history-item-title">
                <h3>Script ${itemNumber}</h3>
                <span class="history-time">${escapeHtml(item.time)}</span>
            </div>
        `;
        node.addEventListener('click', () => openHistoryModal(item));
        
        const deleteBtn = document.createElement('button');
        deleteBtn.type = 'button';
        deleteBtn.className = 'history-delete-btn';
        deleteBtn.textContent = '✕';
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            deleteHistoryItem(index);
        });
        
        container.appendChild(node);
        container.appendChild(deleteBtn);
        list.appendChild(container);
    });
}

function deleteHistoryItem(index) {
    const history = getHistory();
    history.splice(index, 1);
    localStorage.setItem('translationHistory', JSON.stringify(history));
    renderHistory();
}

function openHistoryModal(item) {
    const modal = document.getElementById('historyModal');
    if (!modal) return;

    document.getElementById('modalTimestamp').textContent = item.time;
    document.getElementById('modalSource').textContent = item.source;
    document.getElementById('modalTarget').textContent = item.target;
    document.getElementById('modalMetadata').innerHTML = `
        <span>Language: ${escapeHtml(item.language)}</span>
        <span>Words (EN): ${escapeHtml(item.words_source || 0)}</span>
        <span>Words (VI): ${escapeHtml(item.words_target || 0)}</span>
        <span>Duration: ${escapeHtml(item.duration)}</span>
    `;

    modal.classList.remove('hidden');
}

function closeHistoryModal() {
    const modal = document.getElementById('historyModal');
    if (!modal) return;
    modal.classList.add('hidden');
}

function openExpandModal(targetId) {
    const modal = document.getElementById('expandModal');
    const expandTextarea = document.getElementById('expandTextarea');
    const targetElement = document.getElementById(targetId);
    
    if (!modal || !expandTextarea || !targetElement) return;
    
    currentExpandTarget = targetId;
    expandTextarea.value = targetElement.value;
    modal.classList.remove('hidden');
    expandTextarea.focus();
}

function closeExpandModal() {
    const modal = document.getElementById('expandModal');
    if (!modal) return;
    modal.classList.add('hidden');
    currentExpandTarget = null;
}

function submitExpandModal() {
    if (!currentExpandTarget) return;
    
    const expandTextarea = document.getElementById('expandTextarea');
    const targetElement = document.getElementById(currentExpandTarget);
    
    if (expandTextarea && targetElement) {
        targetElement.value = expandTextarea.value;
    }
    
    closeExpandModal();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('theme', getCurrentTheme());
    updateThemeButton();
}

function getCurrentTheme() {
    return document.body.classList.contains('dark-mode') ? 'dark' : 'light';
}

function updateThemeButton() {
    const btn = document.querySelector('.theme-toggle');
    if (!btn) return;
    btn.textContent = getCurrentTheme() === 'dark' ? 'Mode: Dark' : 'Mode: Light';
}

document.addEventListener('DOMContentLoaded', () => {
    renderHistory();

    // restore theme from localStorage
    const saved = localStorage.getItem('theme');
    if (saved === 'dark') document.body.classList.add('dark-mode');
    else document.body.classList.remove('dark-mode');
    updateThemeButton();

    const source = document.getElementById('source_text');
    const translation = document.getElementById('translation');
    const durationInput = document.getElementById('duration_input');

    // Check if this is a result from form submission
    if (source && translation && source.value.trim() && translation.value.trim()) {
        let duration = '0.2s';
        
        // Get duration from backend (passed via hidden input)
        if (durationInput && durationInput.value) {
            const durationSec = parseFloat(durationInput.value);
            duration = `${durationSec}s`;
        }
        
        saveHistory({
            source: source.value.trim(),
            target: translation.value.trim(),
            duration: duration
        });
        renderHistory();
    }

    // Track translation start time on form submit
    const form = document.querySelector('.translator-form');
    if (form) {
        form.addEventListener('submit', () => {
            translationStartTime = new Date();
            sessionStorage.setItem('translationStartTime', translationStartTime.toISOString());
        });
    }
    
    // Handle Enter in expand modal (Ctrl+Enter to submit)
    const expandTextarea = document.getElementById('expandTextarea');
    if (expandTextarea) {
        expandTextarea.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                submitExpandModal();
            }
        });
    }
});
