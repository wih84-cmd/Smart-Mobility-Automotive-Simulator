import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="스마트 모빌리티 엔지니어링 툴", layout="wide")

st.markdown("## 🏎️ 모빌리티 동력 제어 및 에너지 최적화 스튜디오")

components.html("""
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: white; display: flex; gap: 20px; padding: 20px; }
        .canvas-area { background: #1e293b; padding: 20px; border-radius: 16px; border: 1px solid #334155; }
        .grid { display: grid; grid-template-columns: repeat(20, 25px); gap: 1px; }
        .tile { width: 25px; height: 25px; background: #334155; cursor: crosshair; }
        .tile.road { background: #fbbf24; }
        .dashboard { width: 350px; background: #1e293b; padding: 20px; border-radius: 16px; border: 1px solid #334155; }
        .meter { height: 20px; background: #0f172a; border-radius: 10px; margin: 10px 0; overflow: hidden; }
        .fill { height: 100%; width: 0%; transition: width 0.3s ease, background 0.3s; }
        .car-anim { width: 40px; height: 20px; background: #ef4444; border-radius: 4px; position: relative; left: 0; transition: left 0.5s linear; }
    </style>
</head>
<body>
    <div class="canvas-area">
        <div class="grid" id="grid" onmousedown="startDrag()" onmouseup="stopDrag()"></div>
        <div style="margin-top:20px; height:40px; border-bottom: 2px solid #475569;">
            <div id="car" class="car-anim"></div>
        </div>
    </div>
    
    <div class="dashboard">
        <h3>모빌리티 제어 시스템</h3>
        <p>도로 길이: <span id="roadLen">0</span> m</p>
        <p>부하율(%)</p>
        <div class="meter"><div id="load-bar" class="fill"></div></div>
        <select id="mode" style="width:100%; padding:10px; margin:10px 0;">
            <option value="EV">전기 (EV)</option>
            <option value="OIL">내연기관 (ICE)</option>
            <option value="HYBRID">하이브리드 (HEV)</option>
        </select>
        <button onclick="run()" style="width:100%; padding:10px; background:#fbbf24; border:none; font-weight:bold;">시뮬레이션 시작</button>
    </div>

    <script>
        let isDragging = false;
        function startDrag() { isDragging = true; }
        function stopDrag() { isDragging = false; }

        const grid = document.getElementById('grid');
        for(let i=0; i<300; i++) {
            let t = document.createElement('div');
            t.className = 'tile';
            t.onmouseover = () => { if(isDragging) { t.classList.add('road'); updateRoad(); } };
            t.onclick = () => { t.classList.toggle('road'); updateRoad(); };
            grid.appendChild(t);
        }

        function updateRoad() {
            let count = document.querySelectorAll('.tile.road').length;
            document.getElementById('roadLen').innerText = count;
        }

        function run() {
            let count = document.querySelectorAll('.tile.road').length;
            let mode = document.getElementById('mode').value;
            let load = Math.min((count / 100) * 100, 100);
            
            // UI 업데이트
            let bar = document.getElementById('load-bar');
            bar.style.width = load + '%';
            bar.style.backgroundColor = load > 80 ? '#ef4444' : '#22c55e';
            
            // 자동차 애니메이션
            let car = document.getElementById('car');
            car.style.left = (count * 1.5) + 'px';
        }
    </script>
</body>
</html>
""", height=600)
