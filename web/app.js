const $ = (id) => document.getElementById(id);
async function jget(url){ const r = await fetch(url); return r.json(); }
async function jpost(url, data){ const r = await fetch(url,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(data)}); return r.json(); }
async function refresh(){
  const h = await jget('/api/health'); $('health').textContent = `${h.provider}/${h.model}`;
  const agents = await jget('/api/agents'); $('agent').innerHTML = agents.map(a=>`<option value="${a.name}">${a.name}</option>`).join('');
  $('memory').textContent = JSON.stringify(await jget('/api/memory'), null, 2);
  $('runs').textContent = JSON.stringify(await jget('/api/runs'), null, 2);
}
$('askBtn').onclick = async () => { $('answer').textContent = 'running...'; const res = await jpost('/api/ask',{agent:$('agent').value,prompt:$('prompt').value}); $('answer').textContent = res.content || res.error; await refresh(); };
$('scanBtn').onclick = async () => { $('scan').textContent = JSON.stringify(await jget('/api/scan'), null, 2); };
$('memSave').onclick = async () => { await jpost('/api/memory',{namespace:'project',key:$('memKey').value,value:$('memValue').value}); await refresh(); };
refresh().catch(e => { $('health').textContent = 'offline'; console.error(e); });
