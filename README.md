# Stay Focused · SmartLead AI

Stay Focused bulmaca ve aktivite kitabı fikri için hazırlanmış öğrenci projesi: ziyaretçi sohbeti, geri dönüş talep formu ve şifre korumalı kayıt listesi.

## Web sitesi sayfaları

- `/`: marka tanıtımı, kapak konsepti, mini görsel keşif alıştırması, asistan, sık sorulan sorular ve form.
- `/koleksiyon`: kitap fikri, kullanım alanları ve ilgili konuya yönlendiren bilgi talebi bağlantıları.
- `/hakkimizda`: marka hikâyesi ve değerleri.
- `/iletisim`: ürün, hediye ve iş birliği konulu geri dönüş formu.
- `/gizlilik`: demo uygulamasının fiilî veri akışının açıklaması.
- `/dashboard`: şifreyle kayıt görüntüleme ve ad/telefon/not üzerinden arama.

Logo, kullanıcı tarafından sağlanan `unnamed.png` dosyasının değiştirilmeden kopyalanmış hâlidir; `app/static/images/stay-focused-logo.png` yolundadır. Ortak menü, alt bölüm ve kapak konseptinde kullanılır. Renkler kaynak paletteki `#F5F0E6` (krem), `#24483E` (orman yesili), `#B4934F` (antik altin), `#E7E8DC` (acik yesil) değerleridir. Kitap görseli, kullanıcının pazarlama planı PDF dosyasının ilk sayfasından değiştirilmeden alınmıştır; app/static/images/stay-focused-book.jpg dosyasındadır.

Mobil menü, klavye gezinmesi, açılır SSS cevapları ve örnek soru düğmeleri desteklenir. Formdaki konu bilgisi mevcut `mesaj` alanının başına eklenir; Wix API alan adlarıyla uyumluluk korunur. Mini alıştırma yalnızca tarayıcıda çalışır ve sonuçları kaydetmez.

## Bu bilgisayarda açma

1. **BASLAT.cmd** dosyasına çift tıkla. Açılan pencere açık kalsın.
2. Tarayıcıda **http://127.0.0.1:5000** adresini aç.
3. Sohbete bir soru yaz. Anahtar eklenmediyse açıkça işaretli demo yanıtı gelir.
4. Formu örnek bilgilerle doldur. Otomatik mesaj/arama gönderilmez.
5. Yönetim paneline gir. Şifre, yerel `.env` dosyasının `ADMIN_TOKEN=` satırında. Bu dosyayı paylaşma.

## Başka bilgisayarda kurulum

Python 3.10 veya üstü gerekir. Proje klasöründe:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env` dosyasında `SECRET_KEY` ve `ADMIN_TOKEN` değerlerini ayrı, uzun, rastgele değerlerle değiştir. Ardından `BASLAT.cmd` çalıştır. macOS/Linux'ta `venv/bin/python run.py` kullan.

## Gerçek yapay zekâ

Anahtarı kolayca eklemek için `AI_ANAHTARI_EKLE.cmd` dosyasına çift tıkla. Açılan pencereye Groq anahtarını yapıştır; anahtar yazılırken ekranda görünmez. Araç anahtarı yalnızca yerel `.env` dosyasına kaydeder. Kaydettikten sonra sunucuyu yeniden başlat. Anahtarın geçerliliği gerçek sohbet isteğiyle ayrıca doğrulanmalıdır.

Groq hesabından alınan anahtarı yalnızca `.env` içindeki `GROQ_API_KEY=` alanına yaz ve uygulamayı yeniden başlat. Anahtarı ekran görüntüsü, Wix sayfa kodu veya GitHub içine koyma. Model: `openai/gpt-oss-20b`. Anahtarsız sohbet, gerçek AI değil sabit demo mesajıdır.

## Dosyalar ne yapıyor?

| Dosya | Görev |
|---|---|
| `config.py` | Ortam ayarları ve markanın asistan talimatı |
| `app/database.py` | Tablo oluşturma, kayıt ekleme ve listeleme; SQL yalnızca burada |
| `app/services/ai_service.py` | Groq bağlantısı, geçmiş mesajlar, demo ve servis hataları |
| `app/routes.py` | Gelen verileri doğrulama ve doğru katmana yönlendirme |
| `app/__init__.py` | Flask uygulamasını birleştirme, CORS ve sağlık kontrolü |
| `run.py` | Uygulamayı başlatma |
| `app/templates/` ve `app/static/` | Yerel karşılama ve yönetim ekranları |
| `wix/` | Wix sayfalarına yerleştirilecek bağlantı kodları |

`POST /api/sohbet`: `mesaj`, isteğe bağlı `gecmis`; sonuç `cevap`.
`POST /api/leads`: `isim`, `telefon`, isteğe bağlı `mesaj`, `onay:true`; başarı 201.
`GET /api/leads`: `Authorization: Bearer <ADMIN_TOKEN>` gerekir; sonuç `leadler`.
`GET /health`: `basari:true`, `durum:aktif`.
Tüm API sonuçları `basari` alanı içerir. Geçersiz giriş 400, yetkisiz listeleme 401, dış servis hatası 503 döndürür.

## Test

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

Testler ayrı geçici veritabanı kullanır. Gerçek müşteri kaydı oluşturmaz, ücretli AI çağrısı yapmaz.

## Wix bağlantısı

Wix editöründe Velo'yu aç. İki sayfa oluştur. Renkler `#F5F0E6`, `#24483E`, `#B4934F`; başlık fontu Garamond. Karşılama sayfasında logo sol üst, sohbet sağ, form altta olsun; sohbet kutusuna yarı saydam arka plan ekle. Yönetim sayfasında başlık üstte, isim ilk sütunda olsun.

Karşılama sayfasına şu ID'leri ver:

| Bileşen | ID |
|---|---|
| Soru girişi / sor düğmesi / yanıt metni | `mesajInput` / `sorButton` / `cevapText` |
| Ad / telefon / not girişleri | `isimInput` / `telefonInput` / `notInput` |
| Geri dönüş onayı / kayıt düğmesi / durum metni | `onayCheckbox` / `kaydetButton` / `durumText` |

Sayfa koduna `wix/karsilama.js` içeriğini ekle.
Yönetim sayfasına `leadRepeater`, şifre türünde `sifreInput`, `yenileButton`, `cikisButton`, `durumText` ekle. Repeater içindeki metin ID'leri: `isimText`, `telefonText`, `mesajText`, `tarihText`. Sayfa koduna `wix/yonetim.js` ekle. Yönetim sayfasını Wix tarafında da yalnızca yetkili kullanıcıya aç. Şifreyi kodda saklama; çalışma sırasında alana gir.

Her iki dosyada `API` değerini gerçek Render adresiyle değiştir. Render `CORS_ORIGINS` değerine yayımlanmış Wix sitenin tam origin'ini ekle (yalnızca `https://alan-adi`, yol ve sondaki `/` olmadan). Yerel HTML ekranlarının çalışması, Wix entegrasyonunun tamamlandığı anlamına gelmez; yayınlanmış iki Wix sayfasını ayrıca test et.

## GitHub ve Render teslimi

`render.yaml` yayın yapılandırması hazırdır. Kaynak dosyaları depo köküne yükledikten sonra Render'da Blueprint ile bu depoyu seçebilirsin. Yapılandırma Free demo planını seçer, sunucu ve sağlık kontrolünü ayarlar; yönetici şifresi ve uygulama sırrını Render'da üretir. Kurulum sırasında Groq anahtarı ve yayımlanmış Wix adresinin origin'i sorulur. Anahtarı yerel bilgisayara eklemek Render'a otomatik aktarmaz. Yönetim panelinin canlı şifresi Render ortamındaki `ADMIN_TOKEN` değeridir.

Bu ücretsiz demo yapılandırması kalıcı depolama sağlamaz. SQLite kayıtlarının yeniden başlatmada kaybolmaması için aşağıdaki disk adımını ayrıca uygulamak gerekir. Hiçbir ücretli kaynak otomatik oluşturulmaz.

Yapılandırma kaynağı: [Render Blueprint belgeleri](https://render.com/docs/blueprint-spec).

1. GitHub deposuna yalnızca bu `smartlead_ai` klasörünün kaynaklarını yükle. `.env`, `venv`, veritabanı ve kişisel veri yükleme; `.gitignore` hazır.
2. Render'da Python Web Service oluştur ve depoyu bağla. Klasör depo kökündeyse Root Directory boş; üst klasörü yüklediysen `smartlead_ai` yaz.
3. Build: `pip install -r requirements.txt`. Start: `gunicorn run:app`. Health Check: `/health`.
4. Ortam değişkenleri: `APP_ENV=production`, rastgele `SECRET_KEY`, güçlü `ADMIN_TOKEN`, `GROQ_API_KEY`, Wix origin'i içeren `CORS_ORIGINS`.
5. SQLite kalıcılığı için persistent disk `/var/data` ve `DATABASE_URL=/var/data/leads.db` kullan. Render ücretsiz serviste kalıcı disk sağlamaz; disk olmadan yeniden başlatmada kayıtlar kaybolabilir. Ücretli kaynak bu proje hazırlanırken oluşturulmadı.
6. Canlı `/health`, gerçek AI yanıtı, Wix form kaydı ve Wix yönetim listesiyle uçtan uca doğrula.

Kaynaklar: [Render kalıcı disk belgeleri](https://render.com/docs/disks), [Render ücretsiz servis sınırları](https://render.com/docs/free), [Wix Fetch](https://dev.wix.com/docs/velo/apis/wix-fetch/introduction).

## Teslim durumu

Yerel uygulama, kaynak kodu, kurulum, testler ve Wix bağlantı kodları hazırlanmıştır. Gerçek Groq çağrısı, GitHub depo bağlantısı, Render canlı adresi ve yayımlanmış Wix sayfaları hesap erişimi/anahtar sağlanmadan tamamlanmış sayılmaz. Teslimden önce bunları tamamla.

Bu bir ders MVP'sidir. Gerçek müşteriye açılmadan önce talep sınırlandırma, kullanıcı bazlı yönetici oturumu ve veri saklama/silme süreci ayrıca ele alınmalıdır.
