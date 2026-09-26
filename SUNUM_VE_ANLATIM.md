# Projeyi anlamak ve anlatmak

## Senden ne isteniyor?

Stay Focused markası için bir dijital karşılama sistemi. Ziyaretçi soru soruyor, asistan yanıtlıyor. İlgilenirse adını ve telefonunu bırakıyor. İşletme sahibi bu talepleri yönetim panelinde görüyor. Python arka planda bu işleri yapıyor; Wix ziyaretçinin gördüğü yüz.

## İki dakikalık anlatım

“Projemin adı Stay Focused SmartLead AI. Bulmaca ve aktivite kitabı fikrime ilgi duyan ziyaretçilerin sorularını yanıtlamak ve geri dönüş taleplerini toplamak için geliştirdim.

Karşılama sayfasında bir sohbet alanı ve iletişim formu var. Formdaki bilgiler doğrulandıktan sonra SQLite veritabanına kaydediliyor. Yönetim panelinde kayıtları en yeniden eskiye görüyorum. Kişisel bilgileri herkes görmesin diye listeyi yönetici şifresiyle korudum.

Kodda sorumlulukları ayırdım. Ayarlar config dosyasında, SQL database dosyasında, Groq çağrıları AI servisinde. Routes dosyası yalnızca istekleri karşılayıp ilgili katmana yönlendiriyor. Böylece markayı değiştirirken bütün sistemi yeniden yazmam gerekmiyor.

API anahtarı yokken uygulama açıkça demo modunda çalışıyor. Gerçek bağlantıda önce marka talimatı, sonra sohbet geçmişi ve yeni soru yapay zekâ servisine gönderiliyor. Hata olduğunda teknik ayrıntılar yerine anlaşılır bir mesaj dönüyor.”

## Gösterim sırası

1. Ana sayfayı aç ve marka renklerini göster.
2. “Bu kitap kimler için?” diye sor. Demo modundaysa bunu açıkça söyle.
3. “Örnek Ziyaretçi”, “05000000000” ve “Hediye bilgisi” ile formu doldur.
4. Yönetim panelini aç, kendi şifreni gir ve kaydı göster.
5. `/health` adresindeki aktif sonucunu göster.
6. Dosya görevlerini kısaca anlat. Canlı yayın varsa Render ve Wix bağlantılarını göster; yoksa tamamlanmadığını söyle.

## Sorulabilecek sorular

- **Flask nedir?** Tarayıcıdan gelen istekleri karşılayan Python kütüphanesi.
- **API nedir?** Arayüzün sunucuyla konuştuğu adresler ve veri kuralları.
- **Lead nedir?** Ürünle ilgilenip geri dönüş için bilgi bırakan kişi.
- **SQLite nedir?** Kayıtları bir dosyada tutan veritabanı.
- **Neden `?` var?** Kullanıcı verisini SQL komutu gibi çalıştırmadan güvenle kaydetmek için.
- **`.env` neden paylaşılmıyor?** API anahtarı ve yönetici şifresi burada saklanıyor.
- **CORS ne yapıyor?** Hangi site arayüzlerinin API yanıtını tarayıcıdan okuyabileceğini sınırlar. Yönetici şifresinin yerine geçmez.
- **201 / 400 / 503 nedir?** Sırasıyla yeni kayıt, hatalı istek ve geçici servis sorunu.
- **Demo gerçek AI mı?** Hayır. Anahtar yokken verilen sabit örnek yanıttır.

Yönergede kodu sözlü açıklayabilmen isteniyor. Teslim öncesinde bu akışı kendin deneyip her dosyanın görevini öğren.
