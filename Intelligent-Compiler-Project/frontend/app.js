let editor;

// Initialize Monaco Editor
window.onload = function() {
    editor = monaco.editor.create(document.getElementById('editor-container'), {
        value: [
            'int n = 5;',
            'int result = 1;',
            'while (n > 0) {',
            '    result = result * n;',
            '    n = n - 1;',
            '}',
            'print(result);'
        ].join('\n'),
        language: 'cpp', // syntax highlighting similar to minic
        theme: 'vs-dark',
        minimap: { enabled: false }
    });
};

// Tab switching logic
document.querySelectorAll('.tab').forEach(button => {
    button.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.content').forEach(c => c.style.display = 'none');
        
        button.classList.add('active');
        document.getElementById(button.dataset.target).style.display = 'block';
    });
});

// Compile logic
document.getElementById('compile-btn').addEventListener('click', async () => {
    const code = editor.getValue();
    const optimize = document.getElementById('optimize-toggle').checked;
    
    document.getElementById('vm-output').innerText = "Compiling...";
    document.getElementById('ai-output').innerText = "Analyzing...";
    document.getElementById('ai-output').className = "ai-box";
    
    try {
        const response = await fetch('http://localhost:8000/api/compile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, optimize })
        });
        
        const data = await response.json();
        
        if (data.error) {
            document.getElementById('vm-output').innerText = `ERROR: ${data.error}`;
            document.getElementById('ai-output').innerText = data.ai_explanation || data.error;
            document.getElementById('ai-output').classList.add('error');
        } else {
            // Success
            // Tokens
            const tbody = document.querySelector('#tokens-table tbody');
            tbody.innerHTML = '';
            data.tokens.forEach(t => {
                tbody.innerHTML += `<tr><td>${t.type}</td><td>${t.value}</td><td>${t.line}</td></tr>`;
            });
            
            // IR
            document.getElementById('ir-unopt-output').innerText = data.tac_unoptimized.map(i => i.str).join('\n');
            document.getElementById('ir-opt-output').innerText = data.tac_optimized.map(i => i.str).join('\n');
            
            // Assembly
            document.getElementById('assembly-output').innerText = data.assembly.join('\n');
            
            // Output
            document.getElementById('vm-output').innerText = data.output.join('\n');
            
            // AI Explanation (if any)
            if (data.ai_explanation) {
                document.getElementById('ai-output').innerText = data.ai_explanation;
            } else {
                document.getElementById('ai-output').innerText = "Compilation successful. No specific AI insights for this run.";
            }
        }
    } catch (err) {
        document.getElementById('vm-output').innerText = `Network Error: ${err.message}. Is the backend running?`;
    }
});
