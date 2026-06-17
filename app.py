import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="모빌리티 종합 시뮬레이터", page_icon="🏎️", layout="wide")

st.markdown("## 🏎️ 하이브리드 모빌리티 통합 주행 & 에너지 시뮬레이터")

components.html("""
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; background: #f8fafc; display: flex; flex-direction: column; align-items: center; padding: 20px; }
        .main-ui { display: flex; gap: 20px; }
        .grid { display: grid; grid-template-columns: repeat(10, 35px); gap: 2px; background: #cbd5e1; padding: 4px; border-radius: 8px; }
        .tile { width: 35px; height: 35px; background: white; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 8px; border-radius: 2px; }
        .tile.road { background: #475569; color: white; }
        .panel { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 300px; }
        .meter { height: 10px; background: #e2e8f0; border-radius: 5px; overflow: hidden; margin-top: 5px; }
        .fill { height: 100%; width: 0%; transition: width 0.3s; }
    </style>
</head>
<body>
    <div class="main-ui">
        <div>
            <div class="grid" id="grid"></div>
            <div style="margin-top:10px">
                <select id="carType">
                    <option value="small">소형차 (1.0L)</option>
                    <option value="medium">중형차 (2.0L)</option>
                    <option value="large">대형차 (3.5L)</option>
                </select>
                <button onclick="startSim()">주행 시작</button>
            </div>
        </div>
        <div class="panel">
            <h3>실시간 모니터링</h3>
            <p>엔진 RPM: <span id="val-rpm">0</span></p>
            <p>소모 전류(A): <span id="val-amps">0.0</span></p>
            <p>시스템 부하율: <span id="val-load">0%</span></p>
            <div class="meter"><div id="load-bar" class="fill"></div></div>
            <p id="msg" style="font-weight:bold; margin-top:10px;"></p>
        </div>
    </div>

    <script>
        const gridEl = document.getElementById('grid');
        let gridState = Array(100).fill(false);
        for(let i=0; i<100; i++) {
            let div = document.createElement('div');
            div.className = 'tile';
            div.onclick = () => { gridState[i] = !gridState[i]; div.classList.toggle('road'); };
            gridEl.appendChild(div);
        }

        const specs = { 
            small: { hp: 100, amp: 15 }, 
            medium: { hp: 150, amp: 25 }, 
            large: { hp: 250, amp: 45 } 
        };

        function startSim() {
            let roadCount = gridState.filter(v => v).length;
            if(roadCount === 0) return;
            let type = document.getElementById('carType').value;
            
            // 물리 계산 로직
            let rpm = roadCount * 80;
            let amps = (roadCount * specs[type].amp) / 10;
            let load = Math.min((roadCount / 20) * 100, 100);
            
            document.getElementById('val-rpm').innerText = rpm;
            document.getElementById('val-amps').innerText = amps.toFixed(1);
            document.getElementById('val-load').innerText = load + '%';
            
            let bar = document.getElementById('load-bar');
            bar.style.width = load + '%';
            bar.style.backgroundColor = load > 80 ? 'red' : 'green';
            
            document.getElementById('msg').innerText = load > 80 ? '⚠️ 과부하 경고!' : '✓ 정상 주행 중';
            document.getElementById('msg').style.color = load > 80 ? 'red' : 'green';
        }
    </script>
</body>
</html>
""", height=500)
