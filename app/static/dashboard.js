const form=document.querySelector('#login'),rows=document.querySelector('#rows'),status=document.querySelector('#status'),records=document.querySelector('#records'),search=document.querySelector('#search');
let leads=[];
function renderRows() {
  const query=search.value.trim().toLocaleLowerCase('tr-TR');
  const filtered=leads.filter(item=>[item.isim,item.telefon,item.mesaj].join(' ').toLocaleLowerCase('tr-TR').includes(query));
  rows.replaceChildren();
  for(const item of filtered){
    const row=document.createElement('tr');
    for(const value of [item.isim,item.telefon,item.mesaj || '—',new Date(item.tarih.replace(' ','T')+'Z').toLocaleString('tr-TR')]){
      const cell=document.createElement('td');cell.textContent=value;row.append(cell);
    }
    rows.append(row);
  }
  document.querySelector('#count').textContent=leads.length;
  document.querySelector('#empty-search').hidden=filtered.length>0;
}
form.addEventListener('submit',async event=>{
  event.preventDefault();const button=form.querySelector('button');
  if(button.disabled) return;
  button.disabled=true;records.hidden=true;leads=[];rows.replaceChildren();status.textContent='Yükleniyor…';
  try{
    const response=await fetch('/api/leads',{headers:{Authorization:'Bearer '+document.querySelector('#token').value}});
    const data=await response.json();
    if(!response.ok || !data.basari) throw new Error(data.hata || 'Kayıtlar alınamadı.');
    leads=data.leadler;search.value='';renderRows();records.hidden=false;
    status.textContent=leads.length?'En yeni talepler üstte gösteriliyor.':'Henüz talep yok. Ana sayfadaki formdan örnek kayıt ekleyebilirsin.';
  }catch(error){status.textContent=error instanceof TypeError?'Bağlantı kurulamadı.':error.message;}
  finally{button.disabled=false;}
});
search.addEventListener('input',renderRows);
document.querySelector('#logout').addEventListener('click',()=>{form.reset();search.value='';leads=[];rows.replaceChildren();records.hidden=true;status.textContent='Çıkış yapıldı.';});
