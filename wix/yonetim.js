// Yönetici anahtarını bu dosyaya YAZMA. Şifre alanından oturum sırasında gir.
import { fetch } from 'wix-fetch';
const API = 'https://YOUR-SERVICE.onrender.com';
$w.onReady(() => {
  $w('#leadRepeater').data=[];
  $w('#leadRepeater').onItemReady(($item,itemData)=>{
    $item('#isimText').text=itemData.isim;
    $item('#telefonText').text=itemData.telefon;
    $item('#mesajText').text=itemData.mesaj || '—';
    $item('#tarihText').text=new Date(itemData.tarih.replace(' ','T')+'Z').toLocaleString('tr-TR');
  });
  $w('#yenileButton').onClick(async()=>{
    $w('#yenileButton').disable(); $w('#leadRepeater').data=[];
    try {const response=await fetch(API+'/api/leads',{headers:{Authorization:'Bearer '+$w('#sifreInput').value}});const data=await response.json();
      if(!response.ok || !data.basari) throw new Error(data.hata || 'Kayıtlar alınamadı.');
      $w('#leadRepeater').data=data.leadler.map(item=>({...item,_id:String(item.id)}));
      $w('#durumText').text=data.leadler.length+' kayıt';
    }catch(error){$w('#durumText').text=error.message;}
    finally{$w('#yenileButton').enable();}
  });
  $w('#cikisButton').onClick(()=>{$w('#sifreInput').value='';$w('#leadRepeater').data=[];$w('#durumText').text='Çıkış yapıldı.';});
});
