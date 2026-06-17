#!/usr/bin/env python3
"""Generate two self-contained, interactive RFM dashboards (Akos Szakaly brand style)
from dashboard_data.json. Outputs: dashboard_executive.html, dashboard_operative.html"""
import json

with open('dashboard_data.json') as f:
    DATA = json.load(f)
DATA_JSON = json.dumps(DATA)

# ---------------------------------------------------------------- shared brand CSS
BRAND_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Spectral:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
:root{
  --paper:#f7f8fb; --card:#fdfdfe; --ink:#2b2f38; --ink-2:#4d525c; --ink-3:#757a84;
  --cobalt:#3b5bc0; --cobalt-deep:#2f4ba8; --cobalt-soft:#cdd7f0; --cobalt-wash:#eef1f9;
  --steel:#5f6b82; --positive:#3f9476; --negative:#c75a4a; --amber:#c79a3a;
  --hairline:#dde0e5; --strong:#c4c8cf; --frame:#2b2f38;
  --display:'Manrope',system-ui,sans-serif; --body:'Spectral',Georgia,serif;
  --mono:'IBM Plex Mono',ui-monospace,monospace;
}
*{box-sizing:border-box;}
body{
  margin:0; font-family:var(--body); color:var(--ink);
  background:
    repeating-linear-gradient(0deg, transparent, transparent 31px, rgba(95,107,130,0.05) 31px, rgba(95,107,130,0.05) 32px),
    repeating-linear-gradient(90deg, transparent, transparent 31px, rgba(95,107,130,0.05) 31px, rgba(95,107,130,0.05) 32px),
    var(--paper);
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:1180px; margin:0 auto; padding:34px 30px 30px;}
.mono{font-family:var(--mono);} .num{font-family:var(--mono); font-variant-numeric:tabular-nums; letter-spacing:-0.01em;}
.kick{font-family:var(--mono); text-transform:uppercase; letter-spacing:0.14em; font-size:11px; color:var(--cobalt-deep); font-weight:500;}
/* header */
.hdr{display:flex; justify-content:space-between; align-items:flex-start; border-top:2px solid var(--frame); border-bottom:1px solid var(--hairline); padding:16px 0 18px; margin-bottom:26px; gap:20px; flex-wrap:wrap;}
.hdr-l{max-width:620px;}
.hdr h1{font-family:var(--display); font-weight:800; font-size:30px; line-height:1.04; margin:9px 0 7px; letter-spacing:-0.02em;}
.hdr .sub{font-size:14px; color:var(--ink-2); font-style:italic;}
.hdr-r{display:flex; flex-direction:column; align-items:flex-end; gap:11px;}
.reg{width:32px; height:32px; color:var(--cobalt);}
.ctrls{display:flex; gap:8px; flex-wrap:wrap; justify-content:flex-end;}
.ctrl{font-family:var(--mono); font-size:10.5px; letter-spacing:0.06em; text-transform:uppercase; border:1px solid var(--strong); padding:0; color:var(--ink-2); background:var(--card); display:flex; align-items:center;}
.ctrl label{padding:7px 4px 7px 11px; color:var(--ink-3);}
.ctrl select, .ctrl input{font-family:var(--mono); font-size:10.5px; text-transform:uppercase; letter-spacing:0.05em; border:none; background:transparent; color:var(--ink); font-weight:600; padding:7px 11px 7px 4px; outline:none; cursor:pointer;}
.ctrl input{text-transform:none; cursor:text;}
.daterange{font-family:var(--mono); font-size:10.5px; color:var(--ink-3); letter-spacing:0.04em;}
/* kpi drafted cards */
.kpis{display:grid; grid-template-columns:repeat(5,1fr); gap:17px; margin-bottom:32px;}
.kpi{position:relative;}
.kpi .face{border:1px solid var(--ink); background:var(--card); padding:14px 13px 15px; position:relative; z-index:2; height:100%;}
.kpi::before{content:""; position:absolute; left:5px; top:5px; right:-5px; bottom:-5px; background:var(--cobalt); z-index:1;}
.kpi.alt::before{background:var(--steel);} .kpi.risk::before{background:var(--negative);}
.kpi .lab{font-family:var(--mono); font-size:9.5px; letter-spacing:0.12em; text-transform:uppercase; color:var(--ink-3); display:block; margin-bottom:9px; line-height:1.3;}
.kpi .val{font-family:var(--mono); font-size:25px; font-weight:600; color:var(--ink); letter-spacing:-0.02em; line-height:1;}
.kpi .val small{font-size:14px; color:var(--ink-2);}
.kpi .foot{font-size:11.5px; color:var(--ink-3); margin-top:7px;}
/* panels */
.row{display:grid; grid-template-columns:1.15fr 1fr; gap:22px; margin-bottom:22px;}
.panel{border:1px solid var(--hairline); background:var(--card); padding:18px 19px 20px;}
.sec-h{display:flex; justify-content:space-between; align-items:baseline; margin-bottom:16px; border-bottom:1px solid var(--hairline); padding-bottom:11px;}
.sec-h .t{font-family:var(--display); font-weight:700; font-size:15px; letter-spacing:-0.01em;}
.sec-h .idx{font-family:var(--mono); font-size:10px; letter-spacing:0.14em; text-transform:uppercase; color:var(--cobalt-deep);}
/* concentration bars */
.conc{display:flex; flex-direction:column; gap:9px;}
.crow{display:grid; grid-template-columns:120px 1fr 46px; align-items:center; gap:11px;}
.crow .nm{font-size:12.5px; color:var(--ink-2);} .crow .nm.s{color:var(--ink); font-weight:600;}
.bar{height:15px; background:var(--cobalt-wash); position:relative; border:1px solid var(--hairline);}
.bar i{position:absolute; left:0; top:0; bottom:0; display:block;}
.crow .pc{font-family:var(--mono); font-size:11.5px; text-align:right; color:var(--ink); font-weight:500;}
.note{font-family:var(--mono); font-size:10px; letter-spacing:0.05em; color:var(--ink-3); margin-top:13px; text-transform:uppercase;}
/* customers vs revenue */
.cvr{display:flex; flex-direction:column; gap:12px;}
.cvr-item .top{display:flex; justify-content:space-between; align-items:baseline; margin-bottom:5px;}
.cvr-item .top .n{font-size:12.5px; color:var(--ink-2);} .cvr-item .top .n b{color:var(--ink); font-weight:600;}
.cvr-item .top .d{font-family:var(--mono); font-size:10.5px; color:var(--ink-3);}
.duo{display:flex; gap:4px; height:12px;}
.duo .c,.duo .r{position:relative; border:1px solid var(--hairline); background:#fff; flex:1;}
.duo .c i{position:absolute; inset:0 auto 0 0; background:var(--steel);} .duo .r i{position:absolute; inset:0 auto 0 0; background:var(--cobalt);}
.duo-key{display:flex; gap:16px; font-family:var(--mono); font-size:9px; letter-spacing:0.1em; text-transform:uppercase; color:var(--ink-3); margin-top:4px;}
.duo-key span{display:flex; align-items:center; gap:5px;} .duo-key .sw{width:9px;height:9px;} .duo-key .sw.s{background:var(--steel);} .duo-key .sw.r{background:var(--cobalt);}
/* trend */
svg.trend{width:100%; height:auto; display:block;}
.trend-meta{display:flex; justify-content:space-between; font-family:var(--mono); font-size:9.5px; letter-spacing:0.07em; text-transform:uppercase; color:var(--ink-3); margin-top:8px;}
/* insight */
.insight{border:1px solid var(--ink); border-left:5px solid var(--cobalt); background:var(--cobalt-wash); padding:20px 22px; display:grid; grid-template-columns:auto 1fr; gap:24px; align-items:center; margin-bottom:24px;}
.insight .big{font-family:var(--mono); font-size:50px; font-weight:600; color:var(--cobalt-deep); line-height:0.9; letter-spacing:-0.03em;}
.insight .big small{display:block; font-family:var(--mono); font-size:10.5px; letter-spacing:0.1em; text-transform:uppercase; color:var(--steel); margin-top:8px;}
.insight .txt h3{font-family:var(--display); font-weight:700; font-size:17px; margin:0 0 7px; letter-spacing:-0.01em;}
.insight .txt p{font-size:13.5px; line-height:1.5; color:var(--ink-2); margin:0;} .insight .txt p b{color:var(--ink); font-weight:600;}
/* footer */
.ftr{display:flex; justify-content:space-between; align-items:center; border-top:2px solid var(--frame); padding-top:13px; margin-top:6px; flex-wrap:wrap; gap:8px;}
.ftr .tag{font-family:var(--mono); font-size:11px; letter-spacing:0.22em; text-transform:uppercase; color:var(--ink); font-weight:500;}
.ftr .meta{font-family:var(--mono); font-size:9.5px; letter-spacing:0.07em; text-transform:uppercase; color:var(--ink-3);}
/* ---- operative ---- */
.work{display:grid; grid-template-columns:240px 1fr; gap:22px; margin-bottom:22px;}
.seglist{border:1px solid var(--hairline); background:var(--card); align-self:start;}
.seglist .lh{font-family:var(--mono); font-size:10px; letter-spacing:0.14em; text-transform:uppercase; color:var(--cobalt-deep); padding:13px 14px 11px; border-bottom:1px solid var(--hairline);}
.seg{display:flex; align-items:center; gap:9px; padding:9px 14px; border-bottom:1px solid var(--hairline); cursor:pointer; transition:background .12s;}
.seg:last-child{border-bottom:none;} .seg:hover{background:var(--paper);}
.seg .mk{width:9px; height:9px; flex:none;}
.seg .nm{font-size:12.5px; color:var(--ink-2); flex:1; line-height:1.15;}
.seg .ct{font-family:var(--mono); font-size:11px; color:var(--ink-3);}
.seg.sel{background:var(--cobalt-wash); border-left:3px solid var(--cobalt); padding-left:11px;}
.seg.sel .nm{color:var(--ink); font-weight:600;} .seg.sel .ct{color:var(--cobalt-deep);}
.rcol{display:flex; flex-direction:column; gap:22px;}
.detail{position:relative;}
.detail .face{border:1px solid var(--ink); background:var(--card); padding:19px 21px 20px; position:relative; z-index:2;}
.detail::before{content:""; position:absolute; left:6px; top:6px; right:-6px; bottom:-6px; background:var(--cobalt); z-index:1;}
.detail .dh{display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px; gap:12px;}
.detail .dh .nm{font-family:var(--display); font-weight:800; font-size:21px; letter-spacing:-0.02em; display:flex; align-items:center; gap:10px;}
.detail .dh .nm .mk{width:12px; height:12px;}
.detail .dh .badge{font-family:var(--mono); font-size:10px; letter-spacing:0.1em; text-transform:uppercase; color:#fff; padding:5px 10px; font-weight:500; white-space:nowrap;}
.detail .ddesc{font-size:13px; color:var(--ink-2); font-style:italic; margin-bottom:14px;}
.dstats{display:grid; grid-template-columns:repeat(4,1fr); gap:14px; border-top:1px solid var(--hairline); border-bottom:1px solid var(--hairline); padding:14px 0; margin-bottom:15px;}
.dstat .l{font-family:var(--mono); font-size:9px; letter-spacing:0.1em; text-transform:uppercase; color:var(--ink-3); display:block; margin-bottom:6px;}
.dstat .v{font-family:var(--mono); font-size:20px; font-weight:600; letter-spacing:-0.02em;}
.dact{display:grid; grid-template-columns:2fr 1fr 1fr; gap:18px;}
.dact .l{font-family:var(--mono); font-size:9px; letter-spacing:0.1em; text-transform:uppercase; color:var(--cobalt-deep); display:block; margin-bottom:5px;}
.dact .v{font-size:13px; color:var(--ink); line-height:1.35;}
.camps{display:grid; grid-template-columns:repeat(3,1fr); gap:14px;}
.camp{border:1px solid var(--hairline); background:var(--card); padding:14px 15px; display:flex; flex-direction:column; gap:9px;}
.camp.active{border-color:var(--cobalt); box-shadow:4px 4px 0 0 var(--cobalt-soft);}
.camp .ctop{display:flex; justify-content:space-between; align-items:center; gap:8px;}
.camp .cseg{font-family:var(--mono); font-size:9.5px; letter-spacing:0.07em; text-transform:uppercase; color:var(--ink-3); display:flex; align-items:center; gap:6px;}
.camp .cseg .mk{width:8px;height:8px;}
.camp .pri{font-family:var(--mono); font-size:9px; letter-spacing:0.07em; text-transform:uppercase; padding:3px 7px; font-weight:500;}
.pri.P1{background:var(--negative); color:#fff;} .pri.P2{background:var(--cobalt); color:#fff;} .pri.P3{background:var(--cobalt-wash); color:var(--cobalt-deep); border:1px solid var(--cobalt-soft);}
.camp .cact{font-family:var(--display); font-weight:700; font-size:13.5px; line-height:1.25;}
.camp .crow2{font-size:12px; color:var(--ink-2); line-height:1.4;} .camp .crow2 b{color:var(--ink); font-weight:600;}
.camp .chan{font-family:var(--mono); font-size:9.5px; letter-spacing:0.03em; color:var(--steel); border-top:1px solid var(--hairline); padding-top:8px; margin-top:auto;}
.tablecard{border:1px solid var(--hairline); background:var(--card);}
.tbar{display:flex; justify-content:space-between; align-items:center; padding:14px 16px; border-bottom:1px solid var(--hairline); gap:14px; flex-wrap:wrap;}
.tbar .tl{display:flex; align-items:baseline; gap:12px;}
.tbar .tl .t{font-family:var(--display); font-weight:700; font-size:15px; letter-spacing:-0.01em;}
.tbar .tl .idx{font-family:var(--mono); font-size:10px; letter-spacing:0.12em; text-transform:uppercase; color:var(--cobalt-deep);}
.reach{font-family:var(--mono); font-size:11px; color:var(--ink-2);} .reach b{color:var(--cobalt-deep); font-weight:600;}
.export{font-family:var(--mono); font-size:10.5px; letter-spacing:0.1em; text-transform:uppercase; background:var(--ink); color:#fff; border:1px solid var(--ink); padding:9px 16px; font-weight:500; cursor:pointer;}
.export:hover{background:var(--cobalt-deep); border-color:var(--cobalt-deep);}
table{width:100%; border-collapse:collapse;}
thead th{font-family:var(--mono); font-size:9.5px; letter-spacing:0.09em; text-transform:uppercase; color:var(--ink-3); text-align:left; padding:11px 16px; border-bottom:1px solid var(--strong); font-weight:500; cursor:pointer; user-select:none;}
thead th.r,tbody td.r{text-align:right;}
thead th:hover{color:var(--cobalt-deep);}
tbody td{font-family:var(--mono); font-size:12px; padding:9px 16px; border-bottom:1px solid var(--hairline); font-variant-numeric:tabular-nums;}
tbody tr:last-child td{border-bottom:none;} tbody tr:hover td{background:var(--paper);}
tbody td.cty{color:var(--ink-2);}
.segtag{display:inline-flex; align-items:center; gap:6px; font-family:var(--body); font-size:11.5px; color:var(--ink-2);} .segtag .mk{width:8px;height:8px;}
.rfm{letter-spacing:0.08em; color:var(--cobalt-deep); font-weight:500;}
.tfoot{padding:11px 16px; font-family:var(--mono); font-size:10px; letter-spacing:0.05em; text-transform:uppercase; color:var(--ink-3); border-top:1px solid var(--hairline);}
@media(max-width:900px){.kpis{grid-template-columns:repeat(2,1fr);} .row{grid-template-columns:1fr;} .work{grid-template-columns:1fr;} .camps{grid-template-columns:1fr;} .dact{grid-template-columns:1fr;}}
"""

# segment colors (shared JS)
SEG_COLORS = """
const SEG_COLORS = {
 'Champions':'#3f9476','Loyal Customers':'#3b5bc0','Potential Loyalists':'#7f8cb0',
 'New Customers':'#4aa888','Promising':'#9fb0d8','Need Attention':'#c79a3a',
 'About to Sleep':'#b07a3a','At Risk':'#c75a4a',"Can't Lose Them":'#9e3729','Hibernating':'#9aa0aa'
};
const SEG_ORDER = ['Champions','Loyal Customers','Potential Loyalists','New Customers','Promising','Need Attention','About to Sleep','At Risk',"Can't Lose Them",'Hibernating'];
const fmtGBP = n => '£'+Math.round(n).toLocaleString('en-GB');
const fmtGBPk = n => n>=1e6 ? '£'+(n/1e6).toFixed(1)+'M' : (n>=1e3 ? '£'+(n/1e3).toFixed(0)+'k' : '£'+Math.round(n));
"""

# ---------------------------------------------------------------- EXECUTIVE
EXEC_HTML = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RFM — Executive Brief</title>
<style>__CSS__</style></head><body>
<div class="wrap">
  <div class="hdr">
    <div class="hdr-l">
      <span class="kick">RFM — EXECUTIVE BRIEF</span>
      <h1>Where the revenue actually lives.</h1>
      <div class="sub">Customer-value segmentation for a UK online retailer — read the concentration, act on the few that matter.</div>
    </div>
    <div class="hdr-r">
      <svg class="reg" viewBox="0 0 34 34" fill="none" stroke="currentColor" stroke-width="1.3"><circle cx="17" cy="17" r="10.5"/><path d="M17 1.5v31M1.5 17h31"/></svg>
      <div class="ctrls">
        <span class="ctrl"><label>COUNTRY</label><select id="country"></select></span>
        <span class="ctrl"><label>PERIOD</label><select id="period" disabled><option>DEC 09 – DEC 11</option></select></span>
      </div>
      <div class="daterange" id="snap"></div>
    </div>
  </div>
  <div class="kpis" id="kpis"></div>
  <div class="row">
    <div class="panel">
      <div class="sec-h"><span class="t">Revenue Concentration</span><span class="idx">01 — REVENUE SHARE</span></div>
      <div class="conc" id="conc"></div>
      <div class="note" id="concnote"></div>
    </div>
    <div class="panel">
      <div class="sec-h"><span class="t">Customers vs Revenue</span><span class="idx">02 — THE IMBALANCE</span></div>
      <div class="cvr" id="cvr"></div>
    </div>
  </div>
  <div class="panel" style="margin-bottom:22px;">
    <div class="sec-h"><span class="t">Revenue Trend — Monthly</span><span class="idx">03 — SEASONALITY · ALL COUNTRIES</span></div>
    <svg class="trend" id="trend" viewBox="0 0 1000 230" preserveAspectRatio="none"></svg>
    <div class="trend-meta" id="trendmeta"></div>
  </div>
  <div class="insight" id="insight"></div>
  <div class="ftr"><span class="tag">BUILT, NOT DECORATED.</span><span class="meta" id="ftrmeta"></span></div>
</div>
<script>
const DATA = __DATA__;
__SEGCOLORS__

const $ = s => document.querySelector(s);
// country dropdown
const countrySel = $('#country');
['All countries', ...DATA.countries.map(c=>c.country)].forEach((c,i)=>{
  const o=document.createElement('option'); o.value=(i===0?'__ALL__':c); o.textContent=(c.length>22?c.slice(0,22):c); countrySel.appendChild(o);
});
$('#snap').textContent = 'SNAPSHOT '+DATA.meta.snapshot+' · '+DATA.meta.n_countries+' COUNTRIES';
$('#ftrmeta').textContent = 'RFM MODEL · RECENCY · FREQUENCY · MONETARY · ÁKOS SZAKÁLY';

function aggregate(country){
  const cs = country==='__ALL__' ? DATA.customers : DATA.customers.filter(c=>c.country===country);
  const totalRev = cs.reduce((a,c)=>a+c.m,0);
  const n = cs.length;
  const bySeg = {};
  SEG_ORDER.forEach(s=>bySeg[s]={n:0,rev:0});
  cs.forEach(c=>{ if(!bySeg[c.seg]) bySeg[c.seg]={n:0,rev:0}; bySeg[c.seg].n++; bySeg[c.seg].rev+=c.m; });
  return {cs,totalRev,n,bySeg};
}

function render(country){
  const A = aggregate(country);
  const m = DATA.meta;
  const top2rev = (A.bySeg['Champions'].rev + A.bySeg['Loyal Customers'].rev);
  const top2pct = A.totalRev? (top2rev/A.totalRev*100):0;
  const atrisk = A.bySeg['At Risk'].n + A.bySeg["Can't Lose Them"].n;
  const avgVal = A.n? A.totalRev/A.n : 0;
  // KPIs
  $('#kpis').innerHTML = [
    {c:'',   l:'Total Revenue', v:fmtGBPk(A.totalRev), f:(country==='__ALL__'?'Dec 2009 → Dec 2011':country)},
    {c:'',   l:'Customers',     v:A.n.toLocaleString('en-GB'), f:(country==='__ALL__'?'UK ~92% of base':'in '+country)},
    {c:'',   l:'Avg Customer Value', v:fmtGBP(avgVal), f:'lifetime, all segments'},
    {c:'',   l:'Top-2 Segment Revenue', v:top2pct.toFixed(1)+'%', f:'Champions + Loyal'},
    {c:'risk',l:'At-Risk Customers', v:atrisk.toLocaleString('en-GB'), f:'At Risk + Can\\'t Lose'},
  ].map(k=>`<div class="kpi ${k.c}"><div class="face"><span class="lab">${k.l}</span><div class="val">${k.v}</div><div class="foot">${k.f}</div></div></div>`).join('');
  // concentration bars (sorted by rev)
  const segsByRev = SEG_ORDER.map(s=>({name:s, rev:A.bySeg[s].rev, pct:A.totalRev?A.bySeg[s].rev/A.totalRev*100:0})).sort((a,b)=>b.rev-a.rev);
  const maxpct = Math.max(...segsByRev.map(s=>s.pct),1);
  $('#conc').innerHTML = segsByRev.map((s,i)=>`<div class="crow"><span class="nm ${i<2?'s':''}">${s.name}</span><span class="bar"><i style="width:${(s.pct/maxpct*100).toFixed(1)}%;background:${SEG_COLORS[s.name]}"></i></span><span class="pc">${s.pct.toFixed(1)}%</span></div>`).join('');
  $('#concnote').textContent = `TWO SEGMENTS CARRY ${top2pct.toFixed(1)}% OF ${fmtGBPk(A.totalRev)}`;
  // customers vs revenue (pick notable segments)
  const picks = ['Champions','Loyal Customers','Hibernating','At Risk','Potential Loyalists'];
  $('#cvr').innerHTML = picks.map(s=>{
    const cp = A.n? A.bySeg[s].n/A.n*100:0, rp = A.totalRev? A.bySeg[s].rev/A.totalRev*100:0;
    return `<div class="cvr-item"><div class="top"><span class="n"><b>${s}</b></span><span class="d">${cp.toFixed(1)}% cust → ${rp.toFixed(1)}% rev</span></div>
      <div class="duo"><span class="c"><i style="width:${cp.toFixed(1)}%"></i></span><span class="r"><i style="width:${rp.toFixed(1)}%"></i></span></div></div>`;
  }).join('') + `<div class="duo-key"><span><span class="sw s"></span>Share of customers</span><span><span class="sw r"></span>Share of revenue</span></div>`;
  // insight
  const c2 = A.n? (A.bySeg['Champions'].n+A.bySeg['Loyal Customers'].n)/A.n*100:0;
  $('#insight').innerHTML = `<div class="big">${top2pct.toFixed(1)}%<small>OF REVENUE · ${c2.toFixed(1)}% OF CUSTOMERS</small></div>
    <div class="txt"><h3>Two segments fund the business.</h3>
    <p><b>Champions and Loyal Customers</b> are ${c2.toFixed(1)}% of the ${country==='__ALL__'?'base':country+' base'} but pull ${top2pct.toFixed(1)}% of ${fmtGBPk(A.totalRev)} revenue. Protect them first — retention here outweighs acquisition. Move the <b>${atrisk.toLocaleString('en-GB')} At-Risk &amp; Can't-Lose</b> accounts before they slip to Hibernating.</p></div>`;
}

// monthly trend (global, drawn once)
(function drawTrend(){
  const mo = DATA.monthly, W=1000,H=230, pad=18;
  const max = Math.max(...mo.map(d=>d.revenue)), min=Math.min(...mo.map(d=>d.revenue));
  const x = i => pad + i*(W-2*pad)/(mo.length-1);
  const y = v => 205 - (v-min)/(max-min)*(205-25);
  const pts = mo.map((d,i)=>`${x(i).toFixed(0)},${y(d.revenue).toFixed(0)}`);
  let grid=''; [40,95,150,205].forEach(g=>grid+=`<line x1="0" y1="${g}" x2="1000" y2="${g}" stroke="#dde0e5"/>`);
  const area = `<polygon fill="#eef1f9" points="${x(0).toFixed(0)},205 ${pts.join(' ')} ${x(mo.length-1).toFixed(0)},205"/>`;
  const line = `<polyline fill="none" stroke="#3b5bc0" stroke-width="2.2" points="${pts.join(' ')}"/>`;
  // mark peaks (Nov)
  let marks='';
  mo.forEach((d,i)=>{ if(d.month.endsWith('-11')){ marks+=`<circle cx="${x(i).toFixed(0)}" cy="${y(d.revenue).toFixed(0)}" r="3.5" fill="#2f4ba8"/><text x="${x(i).toFixed(0)}" y="${(y(d.revenue)-9).toFixed(0)}" text-anchor="middle" font-family="'IBM Plex Mono',monospace" font-size="11" fill="#2f4ba8">${d.month.slice(2,4)==='09'?'Nov 09':'Nov '+d.month.slice(2,4)}</text>`; }});
  $('#trend').innerHTML = grid+area+line+marks;
  $('#trendmeta').innerHTML = `<span>${mo[0].month}</span><span>OCT–NOV PEAKS ≈ 2× JAN–FEB BASELINE</span><span>${mo[mo.length-1].month}</span>`;
})();

countrySel.addEventListener('change', e=>render(e.target.value));
render('__ALL__');
</script>
</body></html>"""

# ---------------------------------------------------------------- OPERATIVE
OPS_HTML = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RFM — Segment Operations</title>
<style>__CSS__</style></head><body>
<div class="wrap">
  <div class="hdr">
    <div class="hdr-l">
      <span class="kick">RFM — SEGMENT OPERATIONS</span>
      <h1>Target the right list. Today.</h1>
      <div class="sub">Pick a segment, read the play, export the audience — built for CRM execution, not reporting.</div>
    </div>
    <div class="hdr-r">
      <svg class="reg" viewBox="0 0 34 34" fill="none" stroke="currentColor" stroke-width="1.3"><circle cx="17" cy="17" r="10.5"/><path d="M17 1.5v31M1.5 17h31"/></svg>
      <div class="ctrls">
        <span class="ctrl"><label>COUNTRY</label><select id="country"></select></span>
        <span class="ctrl"><label>RECENCY</label><select id="recency">
          <option value="all">ALL</option><option value="0-90">0–90d</option><option value="91-365">91–365d</option><option value="365+">365d+</option></select></span>
        <span class="ctrl"><label>SEARCH</label><input id="search" placeholder="Customer ID…" size="12"></span>
      </div>
    </div>
  </div>
  <div class="work">
    <div class="seglist"><div class="lh" id="lh"></div><div id="seglist"></div></div>
    <div class="rcol">
      <div class="detail"><div class="face" id="detail"></div></div>
      <div>
        <div class="sec-h" style="border:none;padding:0;margin-bottom:14px;"><span class="t">Recommended Campaigns</span><span class="idx">PLAYS — BY PRIORITY</span></div>
        <div class="camps" id="camps"></div>
      </div>
    </div>
  </div>
  <div class="tablecard">
    <div class="tbar">
      <div class="tl"><span class="t" id="tabletitle"></span><span class="idx">04 — CUSTOMER LIST</span></div>
      <div style="display:flex;align-items:center;gap:18px;">
        <span class="reach" id="reach"></span>
        <button class="export" id="export">EXPORT LIST →</button>
      </div>
    </div>
    <table>
      <thead><tr>
        <th data-k="id">Customer ID</th><th data-k="country">Country</th>
        <th class="r" data-k="r">Recency</th><th class="r" data-k="f">Freq</th>
        <th class="r" data-k="m">Monetary £</th><th data-k="rfm">RFM</th><th data-k="seg">Segment</th>
      </tr></thead>
      <tbody id="tbody"></tbody>
    </table>
    <div class="tfoot" id="tfoot"></div>
  </div>
  <div class="ftr" style="margin-top:22px;"><span class="tag">BUILT, NOT DECORATED.</span><span class="meta" id="ftrmeta"></span></div>
</div>
<script>
const DATA = __DATA__;
__SEGCOLORS__
const $ = s => document.querySelector(s);
const SEGMAP = {}; DATA.segments.forEach(s=>SEGMAP[s.name]=s);

let state = { seg:"Can't Lose Them", country:'__ALL__', recency:'all', search:'', sortK:'m', sortDir:-1 };

// country dropdown
const countrySel=$('#country');
['All countries', ...DATA.countries.map(c=>c.country)].forEach((c,i)=>{
  const o=document.createElement('option'); o.value=(i===0?'__ALL__':c); o.textContent=(c.length>20?c.slice(0,20):c); countrySel.appendChild(o);
});
$('#ftrmeta').textContent='SNAPSHOT '+DATA.meta.snapshot+' · '+DATA.meta.total_customers.toLocaleString('en-GB')+' CUSTOMERS · ÁKOS SZAKÁLY';

function segCounts(){ // counts respecting country filter only
  const cs = state.country==='__ALL__'?DATA.customers:DATA.customers.filter(c=>c.country===state.country);
  const m={}; SEG_ORDER.forEach(s=>m[s]=0); cs.forEach(c=>m[c.seg]++); return m;
}
function renderSegList(){
  const counts=segCounts(); const tot=Object.values(counts).reduce((a,b)=>a+b,0);
  $('#lh').textContent=`${SEG_ORDER.length} SEGMENTS · ${tot.toLocaleString('en-GB')}`;
  $('#seglist').innerHTML = SEG_ORDER.map(s=>`<div class="seg ${s===state.seg?'sel':''}" data-seg="${s.replace(/"/g,'&quot;')}">
    <span class="mk" style="background:${SEG_COLORS[s]}"></span><span class="nm">${s}</span><span class="ct">${counts[s].toLocaleString('en-GB')}</span></div>`).join('');
  $('#seglist').querySelectorAll('.seg').forEach(el=>el.addEventListener('click',()=>{state.seg=el.dataset.seg; renderAll();}));
}
function renderDetail(){
  const s=SEGMAP[state.seg];
  const filt = filteredForSeg();
  const segRev = filt.reduce((a,c)=>a+c.m,0);
  $('#detail').innerHTML = `
   <div class="dh"><div class="nm"><span class="mk" style="background:${SEG_COLORS[s.name]}"></span>${s.name}</div>
     <span class="badge pri ${s.prio}">${s.tag} · ${s.prio}</span></div>
   <div class="ddesc">${s.desc}</div>
   <div class="dstats">
     <div class="dstat"><span class="l">Customers</span><span class="v">${filt.length.toLocaleString('en-GB')}</span></div>
     <div class="dstat"><span class="l">Avg Recency</span><span class="v">${s.avg_recency}d</span></div>
     <div class="dstat"><span class="l">Avg Frequency</span><span class="v">${s.avg_frequency}</span></div>
     <div class="dstat"><span class="l">Avg Value</span><span class="v">${fmtGBP(s.avg_monetary)}</span></div>
   </div>
   <div class="dact">
     <div><span class="l">Recommended action</span><div class="v">${s.action}</div></div>
     <div><span class="l">Channel</span><div class="v">${s.channel}</div></div>
     <div><span class="l">Segment value</span><div class="v"><span class="num">${fmtGBPk(segRev)}</span> · ${s.pct_revenue}% of total</div></div>
   </div>`;
}
function renderCamps(){
  const order=[...DATA.segments].sort((a,b)=> (a.prio>b.prio?1:a.prio<b.prio?-1:b.total_revenue-a.total_revenue));
  $('#camps').innerHTML = order.slice(0,6).map(s=>`
    <div class="camp ${s.name===state.seg?'active':''}" data-seg="${s.name.replace(/"/g,'&quot;')}">
      <div class="ctop"><span class="cseg"><span class="mk" style="background:${SEG_COLORS[s.name]}"></span>${s.name}</span><span class="pri ${s.prio}">${s.prio}</span></div>
      <div class="cact">${s.tag.charAt(0)+s.tag.slice(1).toLowerCase()}</div>
      <div class="crow2">Offer: <b>${s.offer}</b></div>
      <div class="chan">${s.channel.toUpperCase()} · ${s.customers.toLocaleString('en-GB')} REACH</div>
    </div>`).join('');
  $('#camps').querySelectorAll('.camp').forEach(el=>el.addEventListener('click',()=>{state.seg=el.dataset.seg; renderAll();}));
}
function filteredForSeg(){ // customers in selected seg, respecting country + recency + search
  let cs = DATA.customers.filter(c=>c.seg===state.seg);
  if(state.country!=='__ALL__') cs=cs.filter(c=>c.country===state.country);
  if(state.recency==='0-90') cs=cs.filter(c=>c.r<=90);
  else if(state.recency==='91-365') cs=cs.filter(c=>c.r>90&&c.r<=365);
  else if(state.recency==='365+') cs=cs.filter(c=>c.r>365);
  if(state.search.trim()) cs=cs.filter(c=>String(c.id).includes(state.search.trim()));
  return cs;
}
function renderTable(){
  let cs = filteredForSeg();
  const k=state.sortK, dir=state.sortDir;
  cs=[...cs].sort((a,b)=>{ let av,bv;
    if(k==='rfm'){av=a.rs*100+a.fs*10+a.ms; bv=b.rs*100+b.fs*10+b.ms;}
    else if(k==='seg'||k==='country'){av=a[k];bv=b[k]; return dir*String(av).localeCompare(String(bv));}
    else {av=a[k];bv=b[k];}
    return dir*(av-bv);
  });
  $('#tabletitle').textContent='Audience — '+state.seg;
  const segRev=cs.reduce((a,c)=>a+c.m,0);
  $('#reach').innerHTML=`ESTIMATED REACH <b>${cs.length.toLocaleString('en-GB')}</b> ACCOUNTS · <b>${fmtGBPk(segRev)}</b> VALUE`;
  const rows=cs.slice(0,200);
  $('#tbody').innerHTML=rows.map(c=>`<tr>
    <td>${c.id}</td><td class="cty">${c.country}</td><td class="r">${c.r}</td><td class="r">${c.f}</td>
    <td class="r">${Math.round(c.m).toLocaleString('en-GB')}</td>
    <td class="rfm">${c.rs}-${c.fs}-${c.ms}</td>
    <td><span class="segtag"><span class="mk" style="background:${SEG_COLORS[c.seg]}"></span>${c.seg}</span></td></tr>`).join('');
  $('#tfoot').textContent = `SHOWING ${rows.length.toLocaleString('en-GB')} OF ${cs.length.toLocaleString('en-GB')} · SORTED BY ${k.toUpperCase()} ${dir<0?'▼':'▲'} · CLICK A COLUMN TO RE-SORT`;
  window.__exportRows = cs;
}
function renderAll(){ renderSegList(); renderDetail(); renderCamps(); renderTable(); }

// sorting
document.querySelectorAll('thead th').forEach(th=>th.addEventListener('click',()=>{
  const k=th.dataset.k; if(state.sortK===k) state.sortDir*=-1; else {state.sortK=k; state.sortDir=(k==='country'||k==='seg')?1:-1;}
  renderTable();
}));
// filters
countrySel.addEventListener('change',e=>{state.country=e.target.value; renderAll();});
$('#recency').addEventListener('change',e=>{state.recency=e.target.value; renderTable(); renderDetail();});
$('#search').addEventListener('input',e=>{state.search=e.target.value; renderTable(); renderDetail();});
// export
$('#export').addEventListener('click',()=>{
  const rows=window.__exportRows||[];
  const head=['CustomerID','Country','Recency','Frequency','Monetary','R','F','M','Segment'];
  const lines=[head.join(',')].concat(rows.map(c=>[c.id,'"'+c.country+'"',c.r,c.f,c.m,c.rs,c.fs,c.ms,'"'+c.seg+'"'].join(',')));
  const blob=new Blob([lines.join('\\n')],{type:'text/csv'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob);
  a.download='rfm_'+state.seg.replace(/[^a-z0-9]+/gi,'_').toLowerCase()+'.csv'; a.click();
});
renderAll();
</script>
</body></html>"""

def build(tmpl):
    return (tmpl.replace('__CSS__', BRAND_CSS)
                .replace('__SEGCOLORS__', SEG_COLORS)
                .replace('__DATA__', DATA_JSON))

with open('dashboard_executive.html','w') as f: f.write(build(EXEC_HTML))
with open('dashboard_operative.html','w') as f: f.write(build(OPS_HTML))
print("Wrote dashboard_executive.html and dashboard_operative.html")
