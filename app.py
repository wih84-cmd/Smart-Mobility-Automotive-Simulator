import streamlit as st
import streamlit.components.v1 as components
 
st.set_page_config(
    page_title="모빌리티 주행 공학 시뮬레이터",
    page_icon="🏎️",
    layout="wide",
)
 
st.markdown("## 🏎️ 스마트 모빌리티 경로 추적 및 동력 해석 시뮬레이터")
st.markdown(
    "<p style='color:gray;font-size:13px;margin-top:-12px;'>타일을 <b>드래그</b>해 도로를 그리고 차량·구동 방식을 선택한 뒤 주행을 시작하세요.</p>",
    unsafe_allow_html=True,
)
 
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css"/>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Segoe UI',sans-serif;background:transparent;color:#1e293b;padding:12px 4px;}
 
/* ── controls ── */
.ctrl-row{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:12px;}
.sel-g{display:flex;flex-direction:column;gap:3px;flex:1;min-width:120px;}
.sel-g label{font-size:11px;color:#64748b;}
.sel-g select{font-size:13px;padding:5px 8px;border:1px solid #cbd5e1;border-radius:8px;background:#fff;color:#1e293b;}
 
/* ── grid ── */
.grid-outer{position:relative;border:1px solid #e2e8f0;border-radius:12px;background:#f8fafc;padding:10px;user-select:none;}
#road-grid{position:relative;width:600px;height:270px;}
.tile{position:absolute;width:28px;height:28px;border-radius:3px;background:#fff;border:1px solid #e2e8f0;cursor:crosshair;transition:background .1s;}
.tile:hover{background:#fde68a;}
.tile.road{background:#f59e0b;border-color:#d97706;}
.tile.start{background:#34d399;border-color:#059669;}
.tile.end{background:#f87171;border-color:#dc2626;}
#car-el{position:absolute;z-index:10;pointer-events:none;transition:left .42s ease,top .42s ease;}
 
/* ── buttons ── */
.btn-row{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;align-items:center;}
.btn{padding:6px 14px;font-size:13px;border-radius:8px;border:1px solid #cbd5e1;background:#fff;cursor:pointer;color:#1e293b;display:inline-flex;align-items:center;gap:5px;}
.btn:hover{background:#f1f5f9;}
.btn.primary{background:#1e40af;color:#fff;border-color:#1e40af;}
.btn.primary:hover{background:#1d4ed8;}
.hint{font-size:11px;color:#94a3b8;}
 
/* ── metrics ── */
.metrics-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px;margin:12px 0;}
.mc{background:#f8fafc;border-radius:8px;padding:10px 12px;border:1px solid #e2e8f0;}
.mc .ml{font-size:10px;color:#64748b;margin-bottom:3px;}
.mc .mv{font-size:19px;font-weight:600;color:#1e293b;}
.mc .mu{font-size:10px;color:#64748b;margin-left:2px;}
 
/* ── viz row ── */
.viz-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px;}
.panel{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:12px;}
.panel h3{font-size:12px;font-weight:600;color:#64748b;margin-bottom:8px;}
 
/* ── power bars ── */
.pbar-wrap{display:flex;flex-direction:column;gap:5px;}
.pbar-row{display:flex;align-items:center;gap:7px;font-size:11px;}
.pbar-label{width:52px;color:#64748b;flex-shrink:0;}
.pbar-track{flex:1;height:9px;border-radius:5px;background:#f1f5f9;overflow:hidden;}
.pbar-fill{height:100%;border-radius:5px;transition:width .4s ease;}
.pbar-val{width:46px;text-align:right;color:#1e293b;font-size:11px;}
 
/* ── chart ── */
.chart-wrap{position:relative;height:160px;margin-top:8px;}
 
/* ── engine ── */
.engine-viz{display:flex;align-items:center;justify-content:center;height:150px;}
#engine-svg{width:100%;height:100%;}
 
@keyframes piston-a{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
@keyframes spark-a{0%,100%{opacity:0}50%{opacity:1}}
@keyframes spin-a{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
</style>
</head>
<body>
 
<!-- controls -->
<div class="ctrl-row">
  <div class="sel-g"><label>차종</label>
    <select id="sel-size"><option value="small">소형차</option><option value="mid" selected>중형차</option><option value="large">대형차</option></select>
  </div>
  <div class="sel-g"><label>구동 방식</label>
    <select id="sel-type"><option value="ice">내연기관</option><option value="hybrid">하이브리드</option><option value="ev">전기차</option></select>
  </div>
  <div class="sel-g"><label>주행 속도 (km/h)</label>
    <select id="sel-speed"><option value="30">30</option><option value="60" selected>60</option><option value="100">100</option><option value="130">130</option></select>
  </div>
  <div class="sel-g"><label>도로 경사 (%)</label>
    <select id="sel-grade"><option value="0" selected>평지 (0%)</option><option value="5">완만 (5%)</option><option value="10">경사 (10%)</option><option value="15">급경사 (15%)</option></select>
  </div>
</div>
 
<!-- grid -->
<div class="grid-outer">
  <div id="road-grid"></div>
  <div id="car-el"></div>
</div>
 
<div class="btn-row">
  <button class="btn primary" onclick="startDrive()">▶ 주행 시작</button>
  <button class="btn" onclick="clearRoad()">🗑 초기화</button>
  <button class="btn" onclick="autoPath()">↩ 예시 경로</button>
  <span class="hint">타일을 드래그해 경로를 그리세요 · 시작(초록) → 끝(빨강)</span>
</div>
 
<!-- metrics -->
<div class="metrics-grid">
  <div class="mc"><div class="ml">총 주행 거리</div><div class="mv" id="m-dist">0<span class="mu">km</span></div></div>
  <div class="mc"><div class="ml">에너지 소비</div><div class="mv" id="m-energy">0<span class="mu">kWh</span></div></div>
  <div class="mc"><div class="ml">연료 소비</div><div class="mv" id="m-fuel">0<span class="mu">L</span></div></div>
  <div class="mc"><div class="ml">CO₂ 배출</div><div class="mv" id="m-co2">0<span class="mu">kg</span></div></div>
  <div class="mc"><div class="ml">순간 출력</div><div class="mv" id="m-power">0<span class="mu">kW</span></div></div>
  <div class="mc"><div class="ml">주행 효율</div><div class="mv" id="m-eff">—</div></div>
</div>
 
<!-- viz -->
<div class="viz-row">
  <div class="panel">
    <h3>⚙ 엔진 / 모터 상태</h3>
    <div class="engine-viz"><svg id="engine-svg" viewBox="0 0 260 150" xmlns="http://www.w3.org/2000/svg"></svg></div>
  </div>
  <div class="panel">
    <h3>⚡ 전력 부하량</h3>
    <div class="pbar-wrap">
      <div class="pbar-row"><span class="pbar-label">구동력</span><div class="pbar-track"><div class="pbar-fill" id="pb-drive" style="width:0%;background:#2563eb"></div></div><span class="pbar-val" id="pv-drive">0 kW</span></div>
      <div class="pbar-row"><span class="pbar-label">에어컨</span><div class="pbar-track"><div class="pbar-fill" id="pb-hvac" style="width:0%;background:#059669"></div></div><span class="pbar-val" id="pv-hvac">0 kW</span></div>
      <div class="pbar-row"><span class="pbar-label">전장부품</span><div class="pbar-track"><div class="pbar-fill" id="pb-elec" style="width:0%;background:#d97706"></div></div><span class="pbar-val" id="pv-elec">0 kW</span></div>
      <div class="pbar-row"><span class="pbar-label">회생제동</span><div class="pbar-track"><div class="pbar-fill" id="pb-regen" style="width:0%;background:#0d9488"></div></div><span class="pbar-val" id="pv-regen">0 kW</span></div>
      <div class="pbar-row"><span class="pbar-label">총 부하</span><div class="pbar-track"><div class="pbar-fill" id="pb-total" style="width:0%;background:#dc2626"></div></div><span class="pbar-val" id="pv-total">0 kW</span></div>
    </div>
    <div class="chart-wrap"><canvas id="powerChart" role="img" aria-label="전력 부하 추이"></canvas></div>
  </div>
</div>
 
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
/* ── constants ── */
const COLS=20,ROWS=9,TILE=28,GAP=2;
const VEHICLE={
  small:{mass:1100,Cd:.30,A:1.9},
  mid:  {mass:1500,Cd:.28,A:2.2},
  large:{mass:2200,Cd:.35,A:2.6},
};
const DRIVETRAIN={
  ice:   {eff:.35,regen:0,   co2:2400,fuelFactor:1,   color:'#c2410c'},
  hybrid:{eff:.45,regen:.40, co2:1400,fuelFactor:.55, color:'#059669'},
  ev:    {eff:.92,regen:.70, co2:0,   fuelFactor:0,   color:'#1d4ed8'},
};
 
/* ── state ── */
let roadOrder=[], tileEls=[], driving=false;
let mouseDown=false, lastPainted=-1;
let powerChart=null, chartLabels=[], chartData=[];
 
/* ── grid build ── */
function buildGrid(){
  const grid=document.getElementById('road-grid');
  grid.innerHTML=''; tileEls=[];
  for(let r=0;r<ROWS;r++){
    for(let c=0;c<COLS;c++){
      const t=document.createElement('div');
      t.className='tile';
      t.style.left=(c*(TILE+GAP))+'px';
      t.style.top =(r*(TILE+GAP))+'px';
      t.dataset.idx=r*COLS+c;
 
      /* click */
      t.addEventListener('mousedown', e=>{ if(driving)return; mouseDown=true; paintTile(t); e.preventDefault(); });
      t.addEventListener('mouseenter',()=>{ if(mouseDown&&!driving) paintTile(t); });
 
      grid.appendChild(t); tileEls.push(t);
    }
  }
  document.addEventListener('mouseup',()=>{ mouseDown=false; lastPainted=-1; });
  /* touch */
  grid.addEventListener('touchstart', onTouch,{passive:false});
  grid.addEventListener('touchmove',  onTouch,{passive:false});
  grid.addEventListener('touchend',   ()=>{ mouseDown=false; lastPainted=-1; });
}
 
function onTouch(e){
  if(driving)return; e.preventDefault();
  const touch=e.touches[0];
  const el=document.elementFromPoint(touch.clientX,touch.clientY);
  if(el&&el.classList.contains('tile')) paintTile(el);
}
 
function paintTile(t){
  const idx=parseInt(t.dataset.idx);
  if(idx===lastPainted)return;
  lastPainted=idx;
  if(roadOrder.indexOf(idx)===-1){
    roadOrder.push(idx);
    t.classList.add('road');
    updateTileClasses();
  }
}
 
function updateTileClasses(){
  tileEls.forEach(t=>t.classList.remove('start','end'));
  if(roadOrder.length>0){
    tileEls[roadOrder[0]].classList.add('start');
    tileEls[roadOrder[roadOrder.length-1]].classList.add('end');
  }
}
 
function clearRoad(){
  if(driving)return;
  roadOrder=[];
  tileEls.forEach(t=>t.classList.remove('road','start','end'));
  const ce=document.getElementById('car-el'); ce.innerHTML=''; ce.style.display='none';
  resetMetrics(); drawIdleEngine();
  updatePowerBars(0,0,0,0,0);
  if(powerChart){powerChart.data.labels=[];powerChart.data.datasets[0].data=[];powerChart.update();}
  chartLabels=[]; chartData=[];
}
 
function autoPath(){
  if(driving)return; clearRoad();
  /* S-curve path */
  const path=[
    21,22,23,24,25,26,27,28,
    48,68,88,108,128,148,168,
    167,166,165,164,163,162,161,160,
    140,120,100,80,60,40,
    41,42,43,44,45,46,47,48
  ];
  const seen=new Set();
  path.forEach(idx=>{
    if(seen.has(idx))return; seen.add(idx);
    if(idx>=0&&idx<COLS*ROWS){ roadOrder.push(idx); tileEls[idx].classList.add('road'); }
  });
  updateTileClasses();
}
 
/* ── physics ── */
function getParams(){
  const size =document.getElementById('sel-size').value;
  const type =document.getElementById('sel-type').value;
  const speed=parseInt(document.getElementById('sel-speed').value);
  const grade=parseInt(document.getElementById('sel-grade').value);
  return {v:VEHICLE[size],dt:DRIVETRAIN[type],speed,grade,sizeKey:size,typeKey:type};
}
 
function calcPower(p,v_kmh){
  const v=v_kmh/3.6, rho=1.225, g=9.81, Crr=0.012;
  const gradeRad=Math.atan(p.grade/100);
  const F_aero =.5*rho*p.v.Cd*p.v.A*v*v;
  const F_roll =p.v.mass*g*Crr*Math.cos(gradeRad);
  const F_grade=p.v.mass*g*Math.sin(gradeRad);
  const P_wheel=(F_aero+F_roll+F_grade)*v;
  const P_drive=Math.max(0,P_wheel/p.dt.eff)/1000;
  const P_hvac =p.sizeKey==='large'?3.5:p.sizeKey==='mid'?2.5:1.8;
  const P_elec =p.sizeKey==='large'?1.8:.9;
  const P_regen=p.typeKey==='ev'?P_drive*p.dt.regen*.3:p.typeKey==='hybrid'?P_drive*p.dt.regen*.15:0;
  const P_total=P_drive+P_hvac+P_elec-P_regen;
  return {P_drive,P_hvac,P_elec,P_regen,P_total};
}
 
/* ── metrics ── */
function resetMetrics(){
  setM('m-dist','0','km'); setM('m-energy','0','kWh');
  setM('m-fuel','0','L'); setM('m-co2','0','kg');
  setM('m-power','0','kW');
  document.getElementById('m-eff').innerHTML='—';
}
function setM(id,val,unit){
  document.getElementById(id).innerHTML=val+'<span class="mu">'+unit+'</span>';
}
 
function updatePowerBars(Pd,Ph,Pe,Pr,Pt){
  const mx=Math.max(Pt,80);
  [['drive',Pd],['hvac',Ph],['elec',Pe],['regen',Pr],['total',Pt]].forEach(([k,v])=>{
    document.getElementById('pb-'+k).style.width=Math.min(100,(v/mx)*100).toFixed(1)+'%';
    document.getElementById('pv-'+k).textContent=v.toFixed(1)+' kW';
  });
}
 
/* ── chart ── */
function initChart(){
  const ctx=document.getElementById('powerChart').getContext('2d');
  if(powerChart) powerChart.destroy();
  chartLabels=[]; chartData=[];
  powerChart=new Chart(ctx,{
    type:'line',
    data:{labels:chartLabels,datasets:[{
      label:'총 부하 (kW)',data:chartData,
      borderColor:'#dc2626',backgroundColor:'rgba(220,38,38,.07)',
      borderWidth:1.5,pointRadius:0,fill:true,tension:.4
    }]},
    options:{
      responsive:true,maintainAspectRatio:false,animation:false,
      plugins:{legend:{display:false}},
      scales:{
        x:{display:false},
        y:{min:0,ticks:{font:{size:10},color:'#94a3b8',callback:v=>v+'kW'},
           grid:{color:'rgba(0,0,0,.05)'}}
      }
    }
  });
}
 
/* ── engine animations ── */
function drawIdleEngine(){
  const svg=document.getElementById('engine-svg');
  svg.innerHTML=`
    <rect x="60" y="40" width="140" height="70" rx="8" fill="none" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="130" y="78" text-anchor="middle" font-size="12" fill="#94a3b8">주행 대기 중</text>
    <text x="130" y="95" text-anchor="middle" font-size="10" fill="#cbd5e1">경로를 그린 후 주행을 시작하세요</text>`;
}
 
function drawICEEngine(typeKey,pct){
  const col=typeKey==='hybrid'?'#059669':'#c2410c';
  const light=typeKey==='hybrid'?'#d1fae5':'#ffedd5';
  const label=typeKey==='hybrid'?'하이브리드 엔진':'내연기관 엔진';
  const exhaust=typeKey==='ice'?`<circle cx="236" cy="90" r="4" fill="#94a3b8" opacity=".5">
    <animate attributeName="r" values="4;12" dur="1s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values=".5;0" dur="1s" repeatCount="indefinite"/>
  </circle>`:'';
  document.getElementById('engine-svg').innerHTML=`
    <defs><style>
      .pa{animation:piston-a .4s ease-in-out infinite;}
      .pb{animation:piston-a .4s ease-in-out infinite .2s;}
      .sa{animation:spark-a .4s ease-in-out infinite;}
      .sb{animation:spark-a .4s ease-in-out infinite .2s;}
      .cr{animation:spin-a .4s linear infinite;transform-origin:130px 110px;}
    </style></defs>
    <rect x="20" y="55" width="220" height="75" rx="6" fill="${light}" stroke="${col}" stroke-width="1.5"/>
    <rect x="50" y="20" width="40" height="55" rx="4" fill="white" stroke="${col}" stroke-width="1.2"/>
    <rect class="pa" x="54" y="44" width="32" height="18" rx="3" fill="${col}"/>
    <circle class="sa" cx="70" cy="24" r="4" fill="#fbbf24" opacity="0"/>
    <rect x="170" y="20" width="40" height="55" rx="4" fill="white" stroke="${col}" stroke-width="1.2"/>
    <rect class="pb" x="174" y="44" width="32" height="18" rx="3" fill="${col}"/>
    <circle class="sb" cx="190" cy="24" r="4" fill="#fbbf24" opacity="0"/>
    <g class="cr">
      <circle cx="130" cy="110" r="18" fill="none" stroke="${col}" stroke-width="2"/>
      <line x1="130" y1="92" x2="130" y2="128" stroke="${col}" stroke-width="2"/>
      <line x1="112" y1="110" x2="148" y2="110" stroke="${col}" stroke-width="2"/>
    </g>
    ${exhaust}
    <text x="130" y="148" text-anchor="middle" font-size="11" fill="${col}" font-weight="bold">${label} · ${Math.round(pct)}% 부하</text>`;
}
 
function drawEVMotor(pct){
  let rings='';
  for(let i=0;i<4;i++){
    const r=28+i*15;
    rings+=`<circle cx="108" cy="73" r="${r}" fill="none" stroke="#2563eb" stroke-width="1.2" stroke-dasharray="6 4" opacity="${.8-i*.15}">
      <animateTransform attributeName="transform" type="rotate" from="0 108 73" to="360 108 73" dur="${.7+i*.2}s" repeatCount="indefinite"/>
    </circle>`;
  }
  const bh=Math.round(Math.min(pct,100)*.88);
  document.getElementById('engine-svg').innerHTML=`
    <rect x="8" y="18" width="200" height="110" rx="10" fill="#eff6ff" stroke="#2563eb" stroke-width="1.5"/>
    ${rings}
    <circle cx="108" cy="73" r="14" fill="#2563eb"/>
    <text x="108" y="77" text-anchor="middle" font-size="9" fill="white" font-weight="bold">모터</text>
    <text x="108" y="146" text-anchor="middle" font-size="11" fill="#2563eb" font-weight="bold">전기 모터 · ${Math.round(pct)}% 부하</text>
    <rect x="220" y="22" width="28" height="96" rx="4" fill="#eff6ff" stroke="#2563eb" stroke-width="1"/>
    <rect x="224" y="${26+(88-bh)}" width="20" height="${bh}" rx="2" fill="#2563eb"/>
    <text x="234" y="130" text-anchor="middle" font-size="9" fill="#2563eb">${Math.round(pct)}%</text>`;
}
 
/* ── drive loop ── */
function tilePos(idx){
  const c=idx%COLS, r=Math.floor(idx/COLS);
  return {x:c*(TILE+GAP), y:r*(TILE+GAP)};
}
 
async function startDrive(){
  if(driving)return;
  if(roadOrder.length<2){alert('타일을 2개 이상 드래그해 경로를 만드세요.');return;}
  driving=true; resetMetrics(); initChart();
 
  const p=getParams();
  const carEl=document.getElementById('car-el');
  const gridEl=document.getElementById('road-grid');
  carEl.innerHTML=`<svg width="36" height="18" viewBox="0 0 36 18" xmlns="http://www.w3.org/2000/svg">
    <rect x="1" y="5" width="34" height="10" rx="3" fill="${p.dt.color}"/>
    <rect x="6" y="2" width="20" height="7" rx="2" fill="${p.dt.color}" opacity=".7"/>
    <circle cx="8" cy="16" r="3" fill="#1e293b"/><circle cx="28" cy="16" r="3" fill="#1e293b"/>
    <rect x="28" y="7" width="6" height="4" rx="1" fill="#fbbf24" opacity=".9"/>
  </svg>`;
  carEl.style.display='block';
 
  let totalDist=0, totalEnergy=0, step=0;
  const DIST=.05;
 
  for(let i=0;i<roadOrder.length;i++){
    const pos=tilePos(roadOrder[i]);
    carEl.style.left=(gridEl.offsetLeft+pos.x-4)+'px';
    carEl.style.top =(gridEl.offsetTop +pos.y+5)+'px';
 
    const pw=calcPower(p,p.speed);
    totalDist+=DIST;
    totalEnergy+=pw.P_total*(DIST/p.speed);
    step++;
 
    const pct=Math.min(100,(pw.P_drive/120)*100);
    setM('m-dist',  totalDist.toFixed(2),'km');
    setM('m-energy',totalEnergy.toFixed(3),'kWh');
    setM('m-fuel',  (totalDist*p.dt.fuelFactor*.07).toFixed(2),'L');
    setM('m-co2',   (p.dt.co2/1000*totalDist).toFixed(3),'kg');
    setM('m-power', pw.P_total.toFixed(1),'kW');
    const eff=p.typeKey==='ev'
      ?(totalEnergy>0?(totalDist/totalEnergy).toFixed(1):'—')
      :(totalDist>0?(totalDist/(totalDist*p.dt.fuelFactor*.07)).toFixed(1):'—');
    document.getElementById('m-eff').innerHTML=eff+(p.typeKey==='ev'?'<span class="mu">km/kWh</span>':'<span class="mu">km/L</span>');
 
    updatePowerBars(pw.P_drive,pw.P_hvac,pw.P_elec,pw.P_regen,pw.P_total);
    chartLabels.push(step); chartData.push(parseFloat(pw.P_total.toFixed(1)));
    if(powerChart) powerChart.update('none');
 
    if(p.typeKey==='ev') drawEVMotor(pct);
    else drawICEEngine(p.typeKey,pct);
 
    await new Promise(r=>setTimeout(r,450));
  }
  driving=false;
}
 
/* ── init ── */
buildGrid(); drawIdleEngine(); initChart();
</script>
</body>
</html>
"""
 
components.html(HTML, height=900, scrolling=False)
