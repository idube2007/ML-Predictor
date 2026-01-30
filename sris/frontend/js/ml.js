const API_BASE = window.location.origin.includes('127.0.0.1') || window.location.origin.includes('localhost')
    ? "http://127.0.0.1:8000/api"
    : "/api";
const token = localStorage.getItem('sris_token');

async function predictPrice() {
    const category = document.getElementById('priceCategory').value;
    const resDiv = document.getElementById('priceResult');
    const priceText = document.getElementById('predictedPrice');

    try {
        const res = await fetch(`${API_BASE}/ml/predict/price?category=${category}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await res.json();
        priceText.innerText = `$${data.predicted_price}`;
        resDiv.classList.remove('hidden');
    } catch (err) {
        alert('Could not get prediction. Ensure models are trained.');
    }
}

async function forecastDemand() {
    const category = document.getElementById('demandCategory').value;
    const resDiv = document.getElementById('demandResult');
    const barsContainer = document.getElementById('demandBars');

    try {
        const res = await fetch(`${API_BASE}/ml/forecast/demand?category=${category}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await res.json();

        barsContainer.innerHTML = '';
        const max = Math.max(...data.forecast);

        data.forecast.forEach(val => {
            const bar = document.createElement('div');
            const height = (val / max) * 100;
            bar.className = 'flex-1 bg-emerald-500 rounded-t';
            bar.style.height = `${height}%`;
            bar.title = `${val} units`;
            barsContainer.appendChild(bar);
        });

        resDiv.classList.remove('hidden');
    } catch (err) {
        alert('Could not get forecast');
    }
}

async function getRecs() {
    const custId = document.getElementById('custId').value;
    const recList = document.getElementById('recList');

    if (!custId) return;

    try {
        const res = await fetch(`${API_BASE}/ml/recommendations/${custId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await res.json();

        recList.innerHTML = '';
        data.recommendations.forEach(prod => {
            const card = document.createElement('div');
            card.className = 'glass p-4 rounded-2xl hover:bg-slate-800/50 transition-all cursor-default';
            card.innerHTML = `
                <p class="text-xs text-indigo-400 font-bold uppercase tracking-wider">${prod.category}</p>
                <h4 class="text-lg font-semibold text-white mt-1">${prod.name}</h4>
                <div class="flex justify-between items-center mt-4">
                    <span class="text-slate-400">$${prod.base_price.toFixed(2)}</span>
                    <span class="px-2 py-1 bg-indigo-500/10 text-indigo-400 text-[10px] rounded">MATCH</span>
                </div>
            `;
            recList.appendChild(card);
        });
    } catch (err) {
        alert('Error fetching recommendations');
    }
}
