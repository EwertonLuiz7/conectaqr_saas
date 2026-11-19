const API = "";
let token = localStorage.getItem("cq_token");
const $ = (s) => document.querySelector(s);
const headers = () => ({ "Content-Type":"application/json", ...(token ? {Authorization:`Bearer ${token}`} : {}) });
async function api(path, options={}) {
  const response = await fetch(API+path, {...options, headers:{...headers(), ...(options.headers||{})}});
  const data = response.status === 204 ? null : await response.json().catch(()=>({detail:"Resposta inválida do servidor"}));
  if (!response.ok) throw new Error(data?.detail || "Não foi possível concluir a operação");
  return data;
}
function message(selector, text, error=false){const el=$(selector);el.textContent=text;el.classList.toggle("error",error);}
function showDashboard(show){$("#dashboard").classList.toggle("hidden",!show);$("#auth").classList.toggle("hidden",show);$("#logoutBtn").classList.toggle("hidden",!show);}
function switchTab(tab){document.querySelectorAll(".tab").forEach(b=>b.classList.toggle("active",b.dataset.tab===tab));$("#loginForm").classList.toggle("hidden",tab!=="login");$("#registerForm").classList.toggle("hidden",tab!=="register");message("#authMessage","");}
document.querySelectorAll(".tab").forEach(b=>b.addEventListener("click",()=>switchTab(b.dataset.tab)));
$("#heroStart").addEventListener("click",()=>$("#auth").scrollIntoView({behavior:"smooth"}));
$("#logoutBtn").addEventListener("click",()=>{localStorage.removeItem("cq_token");token=null;showDashboard(false);});
$("#loginForm").addEventListener("submit",async e=>{e.preventDefault();const f=new FormData(e.target);try{const d=await api("/api/auth/login",{method:"POST",body:JSON.stringify(Object.fromEntries(f))});token=d.access_token;localStorage.setItem("cq_token",token);await loadDashboard();}catch(err){message("#authMessage",err.message,true);}});
$("#registerForm").addEventListener("submit",async e=>{e.preventDefault();const f=new FormData(e.target);try{const d=await api("/api/auth/register",{method:"POST",body:JSON.stringify(Object.fromEntries(f))});token=d.access_token;localStorage.setItem("cq_token",token);await loadDashboard();}catch(err){message("#authMessage",err.message,true);}});
$("#profileForm").addEventListener("submit",async e=>{e.preventDefault();const data=Object.fromEntries(new FormData(e.target));data.is_published=true;try{await api("/api/profile/me",{method:"PUT",body:JSON.stringify(data)});message("#profileMessage","Perfil atualizado com sucesso.");await loadProfile();}catch(err){message("#profileMessage",err.message,true);}});
$("#qrForm [name=destination_type]").addEventListener("change",e=>{$("#destinationLabel").classList.toggle("hidden",e.target.value==="profile");});
$("#qrForm").addEventListener("submit",async e=>{e.preventDefault();const data=Object.fromEntries(new FormData(e.target));if(data.destination_type==="profile")data.destination_value="";try{await api("/api/qrcodes",{method:"POST",body:JSON.stringify(data)});e.target.reset();$("#destinationLabel").classList.add("hidden");message("#qrMessage","QR Code criado com sucesso.");await loadQRs();await loadStats();}catch(err){message("#qrMessage",err.message,true);}});
$("#refreshBtn").addEventListener("click",loadQRs);
async function loadProfile(){const p=await api("/api/profile/me");const form=$("#profileForm");Object.keys(p).forEach(k=>{if(form.elements[k])form.elements[k].value=p[k]??"";});$("#publicProfileLink").href=`/p/${p.slug}`;$("#publicProfileLink").textContent=`Visualizar perfil público: ${location.origin}/p/${p.slug} ↗`;}
async function loadQRs(){const list=await api("/api/qrcodes");$("#qrList").innerHTML=list.length?list.map(q=>`<article class="qr-item"><div><strong>${escapeHtml(q.title)}</strong><small>${escapeHtml(q.url)}</small><small>${q.is_active?"Ativo":"Desativado"} · ${escapeHtml(q.destination_type)}</small></div><div class="qr-actions"><button data-image="${q.id}">Baixar QR</button><button data-edit="${q.id}">Editar destino</button><button data-delete="${q.id}">Excluir</button></div></article>`).join(""):'<p class="muted">Você ainda não criou QR Codes.</p>';}
function escapeHtml(s){return String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
$("#qrList").addEventListener("click",async e=>{const img=e.target.dataset.image, del=e.target.dataset.delete, edit=e.target.dataset.edit;if(img){const r=await fetch(`/api/qrcodes/${img}/image`,{headers:{Authorization:`Bearer ${token}`}});if(!r.ok)return alert("Não foi possível baixar o QR Code");const blob=await r.blob(),url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download=`conectaqr-${img}.png`;a.click();URL.revokeObjectURL(url);}if(del&&confirm("Excluir este QR Code?")){try{await api(`/api/qrcodes/${del}`,{method:"DELETE"});await loadQRs();await loadStats();}catch(err){alert(err.message);}}if(edit){const kind=prompt("Destino: profile, whatsapp ou url");if(!kind)return;const value=kind==="profile"?"":prompt(kind==="whatsapp"?"WhatsApp com DDI e DDD:":"URL completa:");try{await api(`/api/qrcodes/${edit}`,{method:"PATCH",body:JSON.stringify({destination_type:kind,destination_value:value||""})});await loadQRs();}catch(err){alert(err.message);}}});
async function loadStats(){const s=await api("/api/analytics/summary");$("#statQrs").textContent=s.total_qrs;$("#statScans").textContent=s.total_scans;$("#statRecent").textContent=s.scans_last_30_days;}
async function loadDashboard(){const me=await api("/api/auth/me");$("#userName").textContent=me.name;$("#planName").textContent=`Plano ${me.plan}`;showDashboard(true);await Promise.all([loadProfile(),loadQRs(),loadStats()]);}
if(token){loadDashboard().catch(()=>{localStorage.removeItem("cq_token");token=null;showDashboard(false);});}
