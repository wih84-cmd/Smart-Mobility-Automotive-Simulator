import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="모빌리티 주행 공학 시뮬레이터", layout="wide")

st.markdown("## 🏎️ 스마트 모빌리티 경로 추적 및 동력 해석 시뮬레이터")

components.html("""
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; }
        .grid-container { position: relative; width: 600px; height: 300px; background: #1e293b; border-radius: 12px; }
        .tile { position: absolute; width: 30px; height: 30px; background: #334155; border: 1px solid #1e293b; }
        .tile.road { background: #fbbf24; }
        #car { position: absolute; width: 30px; height: 15px; background: #ef4444; border-radius: 4px; z-index: 10; transition: all 0.5s ease; }
    </style>
</head>
<body>
    <div id="grid" class="grid-container"></div>
    <div style="margin-top:20px;">
        <button onclick="drive()">경로 주행 시작</button>
        <p>에너지 소비량: <span id="energy">0</span> kWh | 주행 거리: <span id="dist">0</span> km</p>
    </div>

    <script>
        const grid = document.getElementById('grid');
        let roadTiles = [];
        for(let i=0; i<10; i++) {
            for(let j=0; j<20; j++) {
                let t = document.createElement('div');
                t.className = 'tile';
                t.style.left = (j * 30) + 'px'; t.style.top = (i * 30) + 'px';
                t.onclick = () => { t.classList.toggle('road'); updatePath(); };
                grid.appendChild(t);
            }
        }

        function updatePath() {
            roadTiles = Array.from(document.querySelectorAll('.tile.road'))
                             .map(t => ({x: parseInt(t.style.left), y: parseInt(t.style.top)}));
        }

        async function drive() {
            let car = document.createElement('div'); car.id = 'car';
            grid.appendChild(car);
            
            for(let tile of roadTiles) {
                car.style.left = tile.x + 'px';
                car.style.top = (tile.y + 7) + 'px';
                // 공학적 계산: 거리 0.03km당 에너지 0.5kWh 소비 가정
                document.getElementById('energy').innerText = (roadTiles.indexOf(tile) * 0.5).toFixed(1);
                document.getElementById('dist').innerText = (roadTiles.indexOf(tile) * 0.03).toFixed(2);
                await new Promise(r => setTimeout(r, 500));
            }
        }
    </script>
</body>
</html>
""", height=450)
