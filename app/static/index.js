// Aynı dosya, ana sayfa ve bağımsız iletişim sayfasında çalışır.
const chatHistory = [];
const messages = document.querySelector('#messages');
function bubble(text, role='assistant') {
  const item=document.createElement('p'); item.className='bubble '+role;
  item.textContent=text; messages.append(item); messages.scrollTop=messages.scrollHeight; return item;
}
async function post(url, data) {
  const controller=new AbortController();
  const timeout=setTimeout(()=>controller.abort(),30000);
  try {
    const response=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data),signal:controller.signal});
    const result=await response.json();
    if(!response.ok || !result.basari) throw new Error(result.hata || 'İşlem tamamlanamadı.');
    return result;
  } finally { clearTimeout(timeout); }
}
function errorMessage(error) {
  if(error.name==='AbortError') return 'Yanıt gecikti. Lütfen tekrar dene.';
  return error instanceof TypeError ? 'Bağlantı kurulamadı. Lütfen tekrar dene.' : error.message;
}
const chatForm=document.querySelector('#chat-form');
chatForm?.addEventListener('submit',async event=>{
  event.preventDefault();
  const input=document.querySelector('#question'), button=document.querySelector('#ask');
  const text=input.value.trim(); if(!text || button.disabled) return;
  button.disabled=true; button.textContent='…'; input.disabled=true; bubble(text,'user');
  const pending=bubble('Yanıt hazırlanıyor…','pending');
  try {
    const result=await post('/api/sohbet',{mesaj:text,gecmis:chatHistory.slice(-10)});
    pending.remove();bubble(result.cevap);
    chatHistory.push({role:'user',content:text},{role:'assistant',content:result.cevap});
    if(chatHistory.length>10) chatHistory.splice(0,chatHistory.length-10);
    input.value='';
  }catch(error){pending.remove();bubble(errorMessage(error));}
  finally{button.disabled=false;button.textContent='Sor ↗';input.disabled=false;input.focus();}
});
document.querySelectorAll('[data-question]').forEach(button=>button.addEventListener('click',()=>{
  const input=document.querySelector('#question');
  if(input.disabled) return;
  input.value=button.dataset.question;chatForm.requestSubmit();
}));
const leadForm=document.querySelector('#lead-form');
if(leadForm) {
  const topicMap={urun:'Ürün bilgisi',hediye:'Hediye fikri',isbirligi:'Kurumsal iş birliği'};
  const topic=topicMap[new URLSearchParams(location.search).get('konu')];
  if(topic) document.querySelector('#interest').value=topic;
  leadForm.addEventListener('submit',async event=>{
    event.preventDefault();
    const button=document.querySelector('#save'),status=document.querySelector('#lead-status');
    if(button.disabled) return;
    button.disabled=true;status.className='form-status';status.textContent='Kaydediliyor…';
    try{
      const note=document.querySelector('#note').value.trim();
      const subject=document.querySelector('#interest').value;
      const result=await post('/api/leads',{isim:document.querySelector('#name').value,telefon:document.querySelector('#phone').value,mesaj:subject+(note?' — '+note:''),onay:document.querySelector('#consent').checked});
      status.classList.add('success');status.textContent=result.mesaj+' Teşekkürler!';
      leadForm.reset();
    }catch(error){status.classList.add('error');status.textContent=errorMessage(error);}
    finally{button.disabled=false;}
  });
}
