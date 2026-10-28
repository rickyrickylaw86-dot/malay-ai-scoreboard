(function(){
const $=(s,r=document)=>r.querySelector(s);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const fmt=v=>typeof v==="number"?(Number.isInteger(v)?v:v.toFixed(2)):esc(v);

function renderTable(cols,rows,primary,asc,withRank,dec){
  const sorted=rows.slice();
  if(primary)sorted.sort((a,b)=>asc?a[primary]-b[primary]:b[primary]-a[primary]);
  let h='<div class="tablewrap" tabindex="0"><table><thead><tr>'+(withRank?'<th>#</th>':'')+cols.map(c=>`<th>${esc(c[1])}</th>`).join('')+'</tr></thead><tbody>';
  sorted.forEach((r,i)=>{
    h+='<tr>'+(withRank?`<td class="rank">${i+1}</td>`:'');
    cols.forEach(([k])=>{
      let v=r[k]===undefined?'—':r[k];
      let cell=(typeof v==='number'&&dec&&dec[k]!==undefined)?v.toFixed(dec[k]):fmt(v);
      if(k==='model'){
        if(r.vendor)cell+=' <span class="pill vendor" title="The maker of this model also runs or reports this benchmark">self-reported/own model</span>';
        if(r.note)cell+=` <span class="pill" title="${esc(r.note)}">note</span>`;
      }
      h+=`<td class="${k===primary?'primary':''}">${cell}</td>`;
    });
    h+='</tr>';
  });
  return h+'</tbody></table></div>';
}
function renderBoard(b){
  const vendor=/VENDOR/i.test(b.owner_type);
  let h=`<div class="card"><h3>${esc(b.title)}</h3>
  <div class="meta">
   <div><span class="pill ${vendor?'vendor':'third'}">${esc(b.owner_type)}</span></div>
   <div><b>Whose numbers:</b> ${esc(b.owner)}</div>
   <div><b>Source date:</b> ${esc(b.date)} · <b>Checked by us:</b> ${esc(b.retrieved)}</div>
   <div><b>What the number means:</b> ${esc(b.metric)}</div>
   <div><a href="${esc(b.url)}" target="_blank" rel="noopener">Source ↗</a>${b.url2?` · <a href="${esc(b.url2)}" target="_blank" rel="noopener">Source 2 ↗</a>`:''}</div>
  </div>
  <div class="caveat"><b>Read this first:</b> ${esc(b.caveat)}</div>`;
  h+=renderTable(b.columns,b.rows,b.primary,b.asc,true,b.dec)+'</div>';
  return h;
}
function renderPrices(p){
  if(!p)return'';
  return `<div class="card"><h3>${esc(p.title)}</h3><div class="meta"><div>Source: <a href="${esc(p.url)}" target="_blank" rel="noopener">${esc(p.source)} ↗</a> · checked ${esc(p.retrieved)}</div></div>`+
   renderTable(p.columns,p.rows,null,false,false)+`<p class="note" style="color:var(--muted)">${esc(p.note)}</p></div>`;
}
function renderTab(t){
  let h=`<p style="color:var(--muted)">${esc(t.intro)}</p>`;
  if(t.boards.length>1){
    h+='<div class="subtabs" role="tablist">'+t.boards.map((b,i)=>`<button role="tab" aria-selected="${i===0}" data-b="${i}">${esc(b.title.split(' — ')[0]+(b.title.includes(' — ')?' · '+(/VENDOR/i.test(b.owner_type)?'vendor claim':b.owner_type.startsWith('Third')?b.owner.split(' (')[0]:''):''))}</button>`).join('')+'</div>';
  }
  h+='<div class="boards">'+(t.boards.length?renderBoard(t.boards[0]):'')+'</div>';
  if(t.coming_soon){const c=t.coming_soon;
    h+=`<div class="coming"><h3>${esc(c.headline)}</h3><p>${esc(c.body)}</p><p>${c.links.map(l=>`<a href="${esc(l[1])}" target="_blank" rel="noopener">${esc(l[0])} ↗</a>`).join(' · ')}</p></div>`;}
  h+=renderPrices(t.prices);
  return h;
}
fetch('data/data.json').then(r=>r.json()).then(d=>{
  const tabs=$('#tabs'),panel=$('#panel');
  $('#disclaimer').textContent=d.site.disclaimer;
  d.tabs.forEach((t,i)=>{
    const b=document.createElement('button');b.role='tab';b.textContent=t.label;b.id='tab-'+t.id;
    b.setAttribute('aria-selected',i===0);b.setAttribute('aria-controls','panel');
    b.onclick=()=>show(i);tabs.appendChild(b);
  });
  function show(i){
    [...tabs.children].forEach((b,j)=>b.setAttribute('aria-selected',i===j));
    const t=d.tabs[i];panel.innerHTML=renderTab(t);
    panel.querySelectorAll('.subtabs button').forEach(btn=>btn.onclick=()=>{
      panel.querySelectorAll('.subtabs button').forEach(x=>x.setAttribute('aria-selected',x===btn));
      panel.querySelector('.boards').innerHTML=renderBoard(t.boards[+btn.dataset.b]);
    });
    history.replaceState(null,'','#'+t.id);
  }
  const start=Math.max(0,d.tabs.findIndex(t=>'#'+t.id===location.hash));
  show(start);
}).catch(e=>{$('#panel').innerHTML='<div class="card">Could not load data/data.json. If you opened this file directly, run a local server: <code>python3 -m http.server</code>.</div>';});

// placeholder forms
document.querySelectorAll('form[data-placeholder]').forEach(f=>f.addEventListener('submit',e=>{
  e.preventDefault();
  let m=f.querySelector('.ok');if(!m){m=document.createElement('div');m.className='ok';f.appendChild(m);}
  m.style.flexBasis='100%';
  m.textContent='Not connected yet — nothing was sent or saved. (Placeholder form.)';
}));
})();
