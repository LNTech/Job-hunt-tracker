$(document).ready(function() {
    document.getElementById('login').addEventListener('submit', async (e) => {
        e.preventDefault();
        const form = e.target;
        const username = form.username.value.trim();
        const password = form.password.value;

        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });

        const data = await response.json();
        if (response.ok) {
            alert(data.message);
            window.location.href = '/dashboard'; // redirect to your app
        } else {
            alert(data.message);
        }
    });
});