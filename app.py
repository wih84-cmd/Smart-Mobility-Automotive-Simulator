import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="모빌리티 통합 제어 시스템", layout="wide")

st.markdown("## 🏎️ 스마트 모빌리티 동력 제어 및 주행 시뮬레이터")

components.html("""
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f8fafc; padding: 20px; }
        .wrapper { display: flex; gap: 20px; }
        .track-panel { background: white; padding: 15px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .grid { display: grid; grid-template-columns: repeat(12, 30px); gap: 2px; }
        .tile { width: 30px; height: 30px; background: #e2e8f0; border-radius: 4px; cursor: pointer; }
        .tile.road { background: #475569; }
        .car { position: absolute; width: 25px; height: 25px; background: #ef4444; border-radius: 5px; transition: all 0.3s linear; }
        
        .dashboard { width: 350px; background: #1e293b; color: white; padding: 20px; border-radius: 12px; }
        .val { font-size: 24px; font-weight: bold; color: #38bdf8; }
        .btn-group { display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }
        select, button { padding: 10px; border-radius: 6px; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="track-panel">
            <div class="grid" id="grid"></div>
            <div id="road-view" style="position:relative; height:40px; margin-top:10px;">
                <div id="car" class="car"></div>
            </div>
        </div>
        <div class="dashboard">
            <h3>대시보드</h3>
            <p>모드: <span id="val-mode">-</span></p>
            <p>에너지 소비율: <span id="val-eng">0</span></p>
            <div class="btn-group">
                <select id="mode">
                    <option value="EV">전기 (EV)</option>
                    <option value="OIL">내연기관 (ICE)</option>
                    <option value="HYBRID">하이브리드 (HEV)</option>
                </select>
                <select id="carType">
                    <option value="1.0">소형차</option>
                    <option value="2.0">중형차</option>
                    <option value="3.5">대형차</option>
                </select>
                <button onclick="start()">주행 시작</button>
            </div>
        </div>
    </div>

    <script>
        const grid = document.getElementById('grid');
        let path = Array(144).fill(false);
        for(let i=0; i<144; i++) {
            let t = document.createElement('div'); t.className = 'tile';
            t.onclick = () => { path[i] = !path[i]; t.classList.toggle('road'); };
            grid.appendChild(t);
        }

        function start() {
            let roadLen = path.filter(v => v).length;
            let mode = document.getElementById('mode').value;
            let type = document.getElementById('carType').value;
            
            // 에너지 계산 공식
            let factor = (mode === 'EV') ? 0.8 : (mode === 'OIL' ? 1.2 : 0.9);
            let energy = (roadLen * type * factor).toFixed(1);
            
            document.getElementById('val-mode').innerText = mode;
            document.getElementById('val-eng').innerText = energy + " Unit";
            
            // 애니메이션
            let car = document.getElementById('car');
            car.style.left = (roadLen * 2) + 'px';
        }
    </script>
</body>
</html>
""", height=600)
