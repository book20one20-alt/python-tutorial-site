document.addEventListener('DOMContentLoaded', () => {
    const runButton = document.getElementById('run-code-btn');
    const editor = document.getElementById('code-editor');
    const outputBox = document.getElementById('output-box');

    if (!runButton || !editor || !outputBox) {
        return;
    }

    runButton.addEventListener('click', async () => {
        outputBox.textContent = 'Running...';

        try {
            const response = await fetch('/run-code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: editor.value }),
            });

            const data = await response.json();
            outputBox.textContent = data.output || 'No output returned.';
        } catch (error) {
            outputBox.textContent = 'Unable to run code right now.';
        }
    });
});
