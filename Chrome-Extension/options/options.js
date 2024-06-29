document.querySelector('form').addEventListener('submit', e => {
    e.preventDefault();
    const apiKey = document.querySelector('#apiKey').value;
    chrome.storage.sync.set({
        "apiKey": apiKey
    }, () => {
        const status = document.getElementById('status');
        status.textContent = 'Options saved.';
        setTimeout(() => {
            status.textContent = '';
        }, 750);
    });
});