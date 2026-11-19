(async function(){
 const slug=location.pathname.split("/").pop();
 try{
  const r=await fetch(`/api/public/profile/${encodeURIComponent(slug)}`);
  if(!r.ok)throw new Error("Perfil indisponível");
  const p=await r.json();
  document.title=`${p.display_name} — CONECTAQR`;
  document.querySelector("#pName").textContent=p.display_name;
  document.querySelector("#pProfession").textContent=p.profession||"";
  document.querySelector("#pBio").textContent=p.bio||"";
  document.querySelector("#avatar").textContent=(p.display_name||"CQ").trim().slice(0,2).toUpperCase();
  const links=[];
  if(p.whatsapp)links.push(["Conversar pelo WhatsApp",`https://wa.me/${p.whatsapp}`]);
  if(p.email_public)links.push(["Enviar e-mail",`mailto:${p.email_public}`]);
  if(p.website)links.push(["Acessar meu site",p.website]);
  if(p.instagram)links.push(["Conhecer meu Instagram",p.instagram]);
  document.querySelector("#pLinks").innerHTML=links.map(([label,url])=>`<a href="${safeUrl(url)}" target="_blank" rel="noopener noreferrer">${label} ↗</a>`).join("");
 }catch(e){document.querySelector("#pName").textContent=e.message;document.querySelector("#pBio").textContent="Verifique o endereço ou entre em contato com o responsável pelo perfil.";}
 function safeUrl(url){try{const u=new URL(url,location.origin);return ["https:","http:","mailto:"].includes(u.protocol)?u.href:"#"}catch{return "#"}}
})();
