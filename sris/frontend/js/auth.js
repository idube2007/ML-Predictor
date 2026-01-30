const API_URL = window.location.origin.includes('127.0.0.1') || window.location.origin.includes('localhost')
    ? "http://127.0.0.1:8000/api"
    : "/api";

const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const response = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('sris_token', data.access_token);
                window.location.href = 'dashboard.html';
            } else {
                alert('Login failed. Please check your credentials.');
            }
        } catch (error) {
            console.error('Login error:', error);
            alert('An error occurred. Please try again.');
        }
    });
}

async function checkServerConnection() {
    try {
        const response = await fetch(`${API_URL}/`);
        if (response.ok) {
            console.log("SRIS Backend connection established!");
            return true;
        }
    } catch (error) {
        console.error("SRIS Backend unreachable:", error);
    }
    return false;
}

const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const isConnected = await checkServerConnection();
        if (!isConnected) {
            alert(`CRITICAL ERROR: The backend server at ${API_URL} is NOT responding.\n\nPlease ensure you have run START_SRIS.bat and the terminal window is open.`);
            return;
        }

        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(`${API_URL}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('sris_token', data.access_token);
                window.location.href = 'dashboard.html';
            } else {
                const errorData = await response.json().catch(() => ({}));
                alert(`Registration failed: ${errorData.detail || 'Unknown error'} (Status: ${response.status})`);
            }
        } catch (error) {
            console.error('Registration error:', error);
            alert(`NETWORK TIMEOUT: The browser blocked the request or the server closed the connection. Check your browser console (F12) for detailed CORS/Network errors.`);
        }
    });
}

function checkAuth() {
    const token = localStorage.getItem('sris_token');
    if (!token && !window.location.pathname.includes('login.html') && !window.location.pathname.includes('register.html')) {
        window.location.href = 'login.html';
    }
}

function logout() {
    localStorage.removeItem('sris_token');
    window.location.href = 'login.html';
}

checkAuth();
