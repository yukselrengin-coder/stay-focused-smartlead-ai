// Wix karşılama sayfası kodu. API adresini Render adresinle değiştir.
import { fetch } from 'wix-fetch';
const API = 'https://YOUR-SERVICE.onrender.com';
let gecmis = [];
async function post(path, body) {
  const response = await fetch(API + path, {method:'post', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
  const data = await response.json();
  if (!response.ok || !data.basari) throw new Error(data.hata || 'İşlem tamamlanamadı.');
  return data;
}
$w.onReady(() => {
  $w('#sorButton').onClick(async () => {
    const mesaj = ($w('#mesajInput').value || '').trim();
    if (!mesaj) { $w('#cevapText').text='Lütfen bir soru yazın.'; return; }
    $w('#sorButton').disable();
    try {const data=await post('/api/sohbet',{mesaj,gecmis:gecmis.slice(-10)}); $w('#cevapText').text=data.cevap; gecmis.push({role:'user',content:mesaj},{role:'assistant',content:data.cevap});}
    catch(error){$w('#cevapText').text=error.message;}
    finally{$w('#sorButton').enable();}
  });
  $w('#kaydetButton').onClick(async () => {
    $w('#kaydetButton').disable();
    try {const data=await post('/api/leads',{isim:$w('#isimInput').value,telefon:$w('#telefonInput').value,mesaj:$w('#notInput').value || '',onay:$w('#onayCheckbox').checked});$w('#durumText').text=data.mesaj;}
    catch(error){$w('#durumText').text=error.message;}
    finally{$w('#kaydetButton').enable();}
  });
});
