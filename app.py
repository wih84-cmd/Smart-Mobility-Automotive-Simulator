import streamlit as st
import streamlit.components.v1 as components

# 웹페이지 기본 설정
st.set_page_config(page_title="스마트 모빌리티 엔진 시뮬레이터", page_icon="🏎️", layout="wide", initial_sidebar_state="collapsed")

# 스타일 깔끔하게 정리
st.markdown("""
<style>
    .block-container {padding-top: 1.5rem; max-width: 1200px}
    footer {visibility: hidden}
    div[data-testid="stDecoration"] {background-image: linear-gradient(90deg, #dc2626, #1e40af);}
</style>
""", unsafe_allow_html=True)

st.markdown("## 🏎️ 자동차 엔진 진로 연계: 하이브리드 모빌리티 동력 분배 시뮬레이터")
st.caption("내연기관 엔진과 전기 모터의 가상 주행 조건을 조절하며 시스템 부하율과 연비를 모니터링하는 프로그램입니다.")

# HTML5 Canvas 2D 기반 인터페이스 삽입
components.html("""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#f8fafc;color:#0f172a;-webkit-user-select:none;user-select:none}
.app{display:grid;grid-template-columns:1fr 340px;gap:20px;background:#ffffff;border-radius:24px;padding:20px;box-shadow:0 20px 40px -15px rgba(15,23,42,0.08);border:1px solid #e2e8f0;height:690px}
.left{display:flex;flex-direction:column;background:#fdfdfd;border-radius:18px;border:1px solid #f1f5f9;padding:16px;position:relative}
.right{display:flex;flex-direction:column;gap:12px;padding:4px;overflow-y:auto;overflow-x:hidden}
.sec{font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#475569;margin-bottom:10px;display:flex;align-items:center;gap:6px}
.sec::before{content:'';display:inline-block;width:6px;height:6px;background:#dc2626;border-radius:50%}
canvas#trackCv{display:block;width:100%;height:auto;aspect-ratio:4/3;border-radius:14px;background:#1e293b;max-height:400px}
.mode-container{display:flex;gap:8px;background:#e2e8f0;padding:6px;border-radius:12px;margin-top:10px}
.mbtn{flex:1;padding:10px 4px;border:1px solid #cbd5e1;border-radius:8px;background:#fff;font-size:11px;font-weight:700;cursor:pointer;color:#475569;transition:all .15s;text-align:center}
.mbtn:hover{background:#f1f5f9}
.mbtn.on{background:#1e40af;color:#fff;border-color:#1e3a8a;box-shadow:0 4px 6px -1px rgba(30,64,175,0.2)}
.mbtn.on.engine{background:#dc2626;border-color:#991b1b}
.mbtn.on.hybrid{background:#0d9488;border-color:#115e59}
.sbar{padding:12px;border-radius:12px;font-size:12px;font-weight:700;text-align:center;border:1px solid #e2e8f0;transition:all .3s}
.ss{background:#ecfdf5;color:#065f46;border-color:#a7f3d0}
.sw{background:#fffbeb;color:#92400e;border-color:#fde68a}
.sd{background:#fff1f2;color:#9f1239;border-color:#fecdd3}
.sgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.sc2{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:10px;box-shadow:0 2px 4px rgba(0,0,0,0.01)}
.sl{font-size:10px;color:#64748b;font-weight:600;margin-bottom:4px}
.sv{font-size:18px;font-weight:800;color:#0f172a;letter-spacing:-0.02em}
.su{font-size:10px;color:#94a3b8;font-weight:500;margin-left:2px}
.gw{display:flex;flex-direction:column;gap:5px;background:#f8fafc;padding:10px;border-radius:12px;border:1px solid #e2e8f0}
.gh{display:flex;justify-content:space-between;font-size:11px;font-weight:700;color:#334155}
.gt{height:8px;background:#e2e8f0;border-radius:99px;overflow:hidden}
.gf{height:100%;border-radius:99px;transition:width .15s ease}
.row{display:flex;align-items:center;gap:8px;font-size:11px;font-weight:600;color:#475569}
.row input[type=range]{flex:1;accent-color:#1e40af;cursor:pointer;height:4px}
.row input[type=range].eng-range{accent-color:#dc2626}
.row b{min-width:32px;text-align:right;color:#0f172a;font-weight:800;font-size:12px}
.btn-group{display:flex;gap:6px}
.bb{flex:1;padding:8px;border:1px solid #e2e8f0;border-radius:10px;background:#fff;font-size:11px;font-weight:700;cursor:pointer;color:#475569;transition:all .15s}
.bb.on{border-color:#b45309;background:#fffbeb;color:#b45309;box-shadow:0 0 0 1px #b45309}
.hint{font-size:11px;color:#475569;margin-top:8px;text-align:center;background:#f1f5f9;padding:6px;border-radius:6px;font-weight:600}
@keyframes shake {
  0%,100%{transform:translate(0,0)} 20%,60%{transform:translate(-1px,1px)} 40%,80%{transform:translate(1px,-1px)}
}
.app.danger-shake{animation:shake 0.15s infinite}
</style></head><body>
<div class="app" id="app">
  <div class="left">
    <div class="sec">스마트 가상 주행 트랙 디스플레이 (차량 애니메이션)</div>
    <canvas id="trackCv" width="580" height="380"></canvas>
    <div class="mode-container">
      <div class="mbtn on" id="m-ev" onclick="setMode('EV')">🔌 EV 모터 전용</div>
      <div class="mbtn" id="m-engine" onclick="setMode('ENGINE')">⛽ 엔진 전용</div>
      <div class="mbtn" id="m-hybrid" onclick="setMode('HYBRID')">⚡ 하이브리드(융합)</div>
    </div>
    <div class="hint">💡 주행 모드와 도로 상태(경사도)를 바꾸면 엔진 출력과 배터리 부하가 실시간 계산됩니다.</div>
  </div>
  <div class="right">
    <div id="sbar" class="sbar ss">✓ 정상 주행 — 에코 상태</div>
    <div class="sgrid">
      <div class="sc2"><div class="sl">엔진 회전수</div><div class="sv"><span id="v-rpm">0</span><span class="su">RPM</span></div></div>
      <div class="sc2"><div class="sl">모터 전류 소모</div><div class="sv"><span id="v-current">0.0</span><span class="su">A</span></div></div>
      <div class="sc2"><div class="sl">실시간 연료 소비</div><div class="sv"><span id="v-fuel">0.0</span><span class="su">cc/s</span></div></div>
      <div class="sc2"><div class="sl">가상 차량 속도</div><div class="sv"><span id="v-speed">0</span><span class="su">km/h</span></div></div>
    </div>
    <div class="gw">
      <div class="gh"><span>동력 시스템 전체 부하율</span><span id="v-loadpct">0%</span></div>
      <div class="gt"><div class="gf" id="v-loadfill" style="width:0%;background:#10b981"></div></div>
    </div>
    <div class="row"><span>🚗 가속 페달 가속도</span><input type="range" min="0" max="100" value="40" step="5" id="r-throttle" oninput="upd()"><b id="t-val">40</b><span>%</span></div>
    <div class="row"><span>⛰️ 도로 오르막 경사</span><input type="range" min="0" max="30" value="0" step="5" id="r-incline" oninput="upd()"><b id="i-val">0</b><span>°</span></div>
    <div class="row"><span>⚠️ 엔진 안전 한계치</span><input type="range" min="3000" max="8000" value="6000" step="500" id="r-maxrpm" class="eng-range" oninput="upd()"><b id="m-val">6000</b><span>RPM</span></div>
    <div class="btn-group">
      <button class="bb on" id="road-clean" onclick="setRoad('NORMAL')">🛣️ 일반 포장도로</button>
      <button class="bb" id="road-rough" onclick="setRoad('ROUGH')">🚜 비포장 험로</button>
    </div>
  </div>
</div>
<script>
let mode='EV', road='NORMAL', carX=50, carY=190, angle=0;
let rpm=0, current=0, fuel=0, speed=0, loadRatio=0;
const cv=document.getElementById('trackCv'), cx=cv.getContext('2d');

function setMode(m){
  mode=m;
  ['ev','engine','hybrid'].forEach(k=>{
    const el=document.getElementById('m-'+k);
    el.className='mbtn'+(k===m.toLowerCase()?' on':'');
    if(k===m.toLowerCase()){
      if(k==='engine') el.classList.add('engine');
      if(k==='hybrid') el.classList.add('hybrid');
    }
  });
  upd();
}

function setRoad(r){
  road=r;
  document.getElementById('road-clean').className='bb'+(r==='NORMAL'?' on':'');
  document.getElementById('road-rough').className='bb'+(r==='ROUGH'?' on':'');
  upd();
}

function drawTrack(){
  cx.clearRect(0,0,580,380);
  
  // 1. 도로 배경 그리기
  cx.strokeStyle='#475569'; cx.lineWidth=40; cx.lineCap='round'; cx.lineJoin='round';
  cx.beginPath();
  cx.moveTo(40,190); cx.lineTo(240,190);
  const incline=Number(document.getElementById('r-incline').value)||0;
  // 오르막 경사 시각화 반영
  carY = 190 - (incline * 3);
  cx.lineTo(540, carY);
  cx.stroke();

  // 도로 중앙선
  cx.strokeStyle='#fef08a'; cx.lineWidth=2; cx.setLineDash([10,10]);
  cx.beginPath(); cx.moveTo(40,190); cx.lineTo(240,190); cx.lineTo(540, carY); cx.stroke();
  cx.setLineDash([]);

  // 2. 가상 모빌리티 자동차 본체 그리기
  angle = Math.atan2(carY-190, 300);
  if(speed>0){
    carX += (speed * 0.04);
    if(carX > 520) carX = 40;
  }
  
  // 현재 달리는 위치의 가상 Y축 계산
  let currentCarY = 190;
  if(carX > 240){
    let t = (carX - 240) / 300;
    currentCarY = 190 + (carY - 190) * t;
  }

  cx.save();
  cx.translate(carX, currentCarY - 12);
  cx.rotate(angle);

  // 자동차 바디
  cx.fillStyle = mode==='EV'?'#2563eb':mode==='ENGINE'?'#dc2626':'#0d9488';
  cx.fillRect(-22,-10,44,20);
  // 차창
  cx.fillStyle='#93c5fd'; cx.fillRect(6,-8,10,16);
  // 바퀴 (엔진/모터 가동 시 회전 효과 대용으로 진동 표현)
  cx.fillStyle='#1e293b';
  let shake = (speed > 0)? Math.sin(Date.now() * 0.05) * 1 : 0;
  cx.fillRect(-16,-13 + shake,8,3); cx.fillRect(8,-13 + shake,8,3);
  cx.fillRect(-16,10 + shake,8,3);  cx.fillRect(8,10 + shake,8,3);
  
  // 엔진 배기가스 파티클 효과 (엔진 가동 시에만 나타남)
  if((mode==='ENGINE' || mode==='HYBRID') && speed>0 && Math.random()>0.4){
    cx.fillStyle='rgba(148,163,184,0.5)';
    cx.beginPath(); cx.arc(-28, 4 + (Math.random()-0.5)*6, 3 + Math.random()*4, 0, Math.PI*2); cx.fill();
  }
  cx.restore();
}

function upd(){
  const throttle=Number(document.getElementById('r-throttle').value)||0;
  const incline=Number(document.getElementById('r-incline').value)||0;
  const maxRpm=Number(document.getElementById('r-maxrpm').value)||6000;
  
  document.getElementById('t-val').textContent=throttle;
  document.getElementById('i-val').textContent=incline;
  document.getElementById('m-val').textContent=maxRpm;

  // 가 부하 저항 가중치 (경사도 및 노면 상태 반영)
  let roadWeight = road==='ROUGH'? 1.3 : 1.0;
  let loadFactor = 1 + (incline / 15) * roadWeight;

  // 동력 분배 수학적 설계 논리
  if(throttle === 0){
    rpm = 0; current = 0; fuel = 0; speed = 0;
  } else {
    if(mode === 'EV'){
      rpm = 0;
      fuel = 0;
      current = (throttle * 0.35) * loadFactor;
      speed = (throttle * 1.2) / loadFactor;
    } else if(mode === 'ENGINE'){
      current = 0;
      rpm = (throttle * 65) * loadFactor;
      fuel = (rpm * 0.0012);
      speed = (throttle * 1.4) / loadFactor;
    } else if(mode === 'HYBRID'){
      // 하이브리드는 엔진과 모터가 일을 나누어 분담함 (효율화 극대화)
      rpm = (throttle * 35) * loadFactor;
      current = (throttle * 0.15) * loadFactor;
      fuel = (rpm * 0.0010);
      speed = (throttle * 1.6) / loadFactor; // 합산 시너지로 최고 속도 증가
    }
  }

  // 차량 최고속도 제한 및 라운딩 처리
  speed = Math.min(Math.round(speed), 180);
  rpm = Math.min(Math.round(rpm), 9000);
  current = Number(current.toFixed(1));
  fuel = Number(fuel.toFixed(2));

  // 시스템 부하율 계산 기준 (설정된 최대 가속 RPM 대비 현재 엔진 상태)
  let currentLoad = (mode==='EV')? (current / 45) : (rpm / maxRpm);
  loadRatio = Math.min(currentLoad, 1.5);
  let loadPct = Math.min(Math.round(loadRatio * 100), 100);

  // 상단 바 UI 상태 업데이트 알림
  const appEl = document.getElementById('app');
  const sbarEl = document.getElementById('sbar');
  const gfEl = document.getElementById('v-loadfill');

  document.getElementById('v-rpm').textContent = rpm;
  document.getElementById('v-current').textContent = current;
  document.getElementById('v-fuel').textContent = fuel;
  document.getElementById('v-speed').textContent = speed;
  document.getElementById('v-loadpct').textContent = loadPct + '%';
  gfEl.style.width = loadPct + '%';

  appEl.classList.toggle('danger-shake', loadRatio >= 1.0);

  if(loadRatio >= 1.0){
    gfEl.style.background = '#dc2626';
    sbarEl.className = 'sbar sd';
    sbarEl.textContent = '❌ 과부하! 엔진 및 모터 한계 출력 초과 (위험)';
  } else if(loadRatio >= 0.75){
    gfEl.style.background = '#f59e0b';
    sbarEl.className = 'sbar sw';
    sbarEl.textContent = '⚠ 경고 — 고부하 주행 조건 (연비 악화)';
  } else {
    gfEl.style.background = (mode==='EV')?'#2563eb':(mode==='ENGINE')?'#dc2626':'#0d9488';
    sbarEl.className = 'sbar ss';
    sbarEl.textContent = '✓ 정상 주행 — 시스템 효율적 에코 동력 제어 중';
  }
}

function animLoop(){
  drawTrack();
  requestAnimationFrame(animLoop);
}

setTimeout(()=>{ upd(); animLoop(); }, 150);
</script></body></html>""", height=730, scrolling=False)

st.markdown("---")
st.caption("🏎️ 모빌리티 제어 모델 v1.1 | 진로 포트폴리오용 친환경 하이브리드 엔진 아키텍처 예시")
