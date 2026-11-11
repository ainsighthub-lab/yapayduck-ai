# Semt Avcısı — Kendi Semtinde Site Satma Rehberi

Bu rehber, [@yapayduck.ai](https://instagram.com/yapayduck.ai) reel'inde anlatılan sistemi
gerçek araçlarla kurmayı gösterir: oturduğun semtteki **sitesi olmayan esnafı bul**,
satış şansına göre **puanla**, tek komutla her birine **kendi adıyla site kur**, kapıya git.

> Reel'deki rakamlar (125.000 ₺, 50 dükkan, 5 evet) bir örnektir. Aşağıdaki sistem
> çalışır durumda; senin semtinin verisi ve senin fiyatın geçerli.

---

## İçindekiler

1. [Sistem nasıl çalışıyor](#1-sistem-nasıl-çalışıyor)
2. [Kurulum](#2-kurulum)
3. [Adım 1 — Tara](#3-adım-1--tara)
4. [Adım 2 — Puanla ve filtrele](#4-adım-2--puanla-ve-filtrele)
5. [Adım 3 — Site kur](#5-adım-3--site-kur)
6. [Adım 4 — Yayına al](#6-adım-4--yayına-al)
7. [Adım 5 — Kapıya git](#7-adım-5--kapıya-git)
8. [Fiyatlandırma](#8-fiyatlandırma)
9. [Yasal sınırlar](#9-yasal-sınırlar)
10. [Sık yapılan hatalar](#10-sık-yapılan-hatalar)

---

## 1. Sistem nasıl çalışıyor

```
semt_avci.py tara  ──► leads.csv          (kimin sitesi yok + puan)
        │
        └─► semt_avci.py kur ──► siteler/<isletme>/index.html
                                        │
                                        └─► Netlify Drop ──► semt-avci.netlify.app/<isletme>
```

Üç parça var, hepsi bu repoda:

| Dosya | Ne yapar |
|---|---|
| `scripts/semt_avci.py` | Tarama + puanlama + site üretimi. Tek dosya, sıfır bağımlılık. |
| `sablonlar/taban.html` | Üretilen sitenin iskeleti. Mobil öncelikli, hızlı, tek dosya. |
| `sablonlar/temalar.json` | Sektöre göre renk, başlık, slogan ve hizmet kartları. |

Tasarım kararı: **her site tek bir `index.html` dosyasıdır**. CSS içine gömülü,
JavaScript yok, dış istek yok. Sebebi pratik — esnafa "siten hazır" dediğinde
gerçekten açılıyor olması gerekir; build aracı, npm, framework yok.

---

## 2. Kurulum

Gereken: **Python 3.8 veya üzeri.** Başka hiçbir şey yok — `pip install` bile gerekmez.

```bash
git clone https://github.com/ainsighthub-lab/yapayduck-ai.git
cd yapayduck-ai
python scripts/semt_avci.py --help
```

Çıktı olarak `tara` ve `kur` komutlarını görmelisin.

---

## 3. Adım 1 — Tara

```bash
python scripts/semt_avci.py tara "Kadıköy, İstanbul"
```

Örnek gerçek çıktı (bu komut çalıştırıldı):

```
Semt Avcısı → Kadıköy, İstanbul
  alan: Kadıköy, İstanbul, Marmara Bölgesi, Türkiye
  OSM taranıyor (26 kategori)…

  sitesi olmayan: 778
  telefonu olan : 252
  en yüksek puan: 49 (Divanes Kuaför)
  yazıldı: leads.csv
```

Kadıköy'de 778 işletmenin kaydında site etiketi yok; bunların 252'sinde telefon var.
Telefonu olmayan 526 kayıt satılamaz, o yüzden `kur` komutu onları otomatik atlar.

### İki veri kaynağı var

**OpenStreetMap (varsayılan, ücretsiz)**
- `website` ve `contact:website` etiketi **olmayan** işletmeleri bulur.
- Sınırsız, anahtar gerekmez, ODbL lisanslı.
- Eksisi: etiket eksikliği "sitesi yok" demek değildir. Haritacı yazmayı unutmuş
  olabilir. **Kapıya gitmeden önce Google'da adı arat, teyit et.**
- Küçük semtlerde ve esnaf dükkanlarında kapsama zayıf; büyük ilçelerde iyi.

**Google Places API (ücretli, daha kesin)**
- `places.websiteUri` alanı boş olanları getirir. Bu alan Enterprise SKU'da,
  işletme başına ücretlidir.
- Kayıt gerçekten doğrulanmıştır; "etiket eksik" sorunu yoktur.
- Puan ve yorum sayısı da gelir, satış şansı puanı daha isabetli olur.

```bash
export GOOGLE_PLACES_KEY="AIza..."
python scripts/semt_avci.py tara "Kadıköy, İstanbul" --google
```

### Ne taranıyor

26 kategori: kuaför, güzellik salonu, berber, kafe, restoran, fast food, fırın,
kasap, butik, ayakkabıcı, elektronik, mobilya, kuyumcu, çiçekçi, petshop,
oto yıkama, oto tamir, eczane, diş hekimi, veteriner, sürücü kursu, fotoğrafçı,
elektrikçi, tesisatçı, marangoz.

Listeyi değiştirmek için `semt_avci.py` içindeki `NISLER` sözlüğüne bak.

---

## 4. Adım 2 — Puanla ve filtrele

`tara` komutu her işletmeye **0-100 satış şansı** verir. Yüksek puan = ara, göster, sat.

| Faktör | Etki | Neden |
|---|---|---|
| Sektör uyumu | 0-22 | Kuaför/berber/oto yıkama "hazır site"ye en çok evet diyen grup |
| Yorum sayısı | 1-24 | 200+ yorum = oturmuş işletme, ödeme gücü var |
| Puan | 3-16 | 4.5+ puan = itibarı iyi, dijitalleşmeye açık |
| Telefon var mı | +18 | Aranamıyorsa satılamaz |
| Adres var mı | +8 | Kapıya gidilemiyorsa satılamaz |
| Google kaydı | +4 | Veri doğrulanmış |

`leads.csv`'yi Excel'de aç, `puan_satis` sütununa göre büyükten küçüğe sırala.
İlk 50 satır senin çalışma listendir.

**Gerçek ilk 3 satır (Kadıköy taraması):**

```
puan_satis, ad,                    sektor,   telefon
49,         Divanes Kuaför,        Kuaför,   0216 357 19 19
45,         Kolombo Kebap,         Restoran, 0216 338 15 08
45,         Draft Gastropub,       Restoran, 0216 325 00 51
```

> **Uyarı:** OSM kaydında `puan=0` ve `yorum=0` görünür çünkü OSM yorum taşımaz.
> Puanlama bu durumda sektör + telefon + adres üzerinden çalışır.
> Gerçek yorum/puan verisi istiyorsan `--google` kullan.

---

## 5. Adım 3 — Site kur

```bash
python scripts/semt_avci.py kur leads.csv --en-iyi 50 --cikti siteler
```

Gerçek çıktı:

```
Semt Avcısı → 6 site kuruluyor (siteler)
   49 puan  Divanes Kuaför                     divanes-kuafor
   45 puan  Kolombo Kebap                      kolombo-kebap
   45 puan  Draft Gastropub                    draft-gastropub
   45 puan  Komşu Kafe Collective              komsu-kafe-collective
   45 puan  Rucio Cafe                         rucio-cafe
   45 puan  fitty feed - clean eating          fitty-feed-clean-eating

  bitti. Netlify Drop'a siteler klasörünü sürükle.
```

Her siteye ne giriyor:

- **İşletme adı** — başlık, logo kutusu, sayfa başlığı
- **Sektöre özel slogan ve başlık** — kuaför için "saç ve bakım", kafe için "kahve"
- **Telefon** — `tel:` linki (mobilde tek dokunuşla arama) + üst barda ve altta sabit buton
- **Adres** — Google Maps yol tarifi linki
- **Hizmet kartları** — sektöre göre 3-6 kart (örn. kuaför: kesim, boya, bakım, gelin, cilt, tırnak)
- **Çalışma saatleri** — esnafa sorup güncelleyeceğin varsayılan
- **Marka sarısı** — `#FFC61E`, YapaDuck sarısı

Üretilen dosya boyutu ~9,5 KB. Tek dosya, tek istek, anında açılır.

### Siteyi kendine özelleştirme

`--en-iyi` yerine tek bir işletme için: CSV'yi tek satıra indir, sonra `kur`.

Tema değiştirmek için `sablonlar/temalar.json`:
```json
"kuafor": {
  "sektorler": ["Kuaför", "Güzellik Salonu"],
  "renk": "#FFC61E",
  "baslik": "{{AD}} — {{SEMT}} içinde saç ve bakım",
  "slogan": "Güzellik zaman ayırır. Randevunu şimdi al.",
  "hizmetler": [["Saç kesimi", "Yüzüne göre kesim, yıkamalı.", "✂"], ...]
}
```

Şablon değişkenleri: `{{AD}}`, `{{AD_UPPER}}`, `{{SEKTOR}}`, `{{SEMT}}`, `{{TEL}}`,
`{{TEL_LINK}}`, `{{ADRES}}`, `{{HARITA}}`, `{{KARTLAR}}`, `{{SLOGAN}}`,
`{{BASLIK}}`, `{{ALT}}`, `{{CTA}}`, `{{RENK}}`, `{{RENK2}}`, `{{ZEMIN}}`, `{{YIL}}`.

---

## 6. Adım 4 — Yayına al

En hızlı yol: **Netlify Drop**.

1. [app.netlify.com/drop](https://app.netlify.com/drop) adresine git
2. `siteler` klasörünü sayfaya sürükle
3. Netlify bir URL verir: `random-name-123.netlify.app`
4. Site adresleri: `random-name-123.netlify.app/divanes-kuafor/`

Alan adı bağlamak istersen: Netlify → Domain settings → Add custom domain.
`semt-avci.com/divanes-kuafor` gibi bir yapı kurmak için tek alan adı yeter,
50 site için 50 alan adı gerekmez.

**Alternatifler:** GitHub Pages (ücretsiz, `gh-pages` dalı), Cloudflare Pages
(ücretsiz, hızlı), Vercel.

> Her site tek dosya olduğu için hosting maliyeti pratikte sıfır.
> 50 site ~475 KB toplam.

---

## 7. Adım 5 — Kapıya git

Reel'deki asıl numara burada: **"Site ister misiniz?" diye sormuyorsun.**
Siteyi kurmuş gidiyorsun, telefonu uzatıyorsun.

### Kapıda 60 saniye

1. **Açılış (10 sn):** "Merhaba, ben semt avcısıyım. Sizin dükkanı haritada gördüm,
   siteniz yoktu. Bir tane hazırladım, bakmak ister misiniz?"
2. **Telefonu uzat (20 sn):** Site açık. İsimleri, telefonları, hizmetleri doğru.
   *"Bunu sizin için yaptım, ücretsiz göstermek istedim."*
3. **Fiyat (15 sn):** "Kurulum [X] ₺. Alan adı ve güncellemeler dahil.
   İsterseniz şimdi devreye alalım, yarın müşterileriniz görebilir."
4. **Kapanış (15 sn):** Kartvizit/QR bırak. "Beğenmezseniz hiçbir şey ödemiyorsunuz."

### Neden işe yarıyor

- **Hazır şeye hayır demek zor.** Site zaten var, sadece "evet" demesi gerekiyor.
- **Risk algısı sıfır.** Beğenmezse ödemiyor.
- **Somut.** "Site yaptırır mısınız?" soyut; açılmış site somut.

### Yapma

- ❌ Toplu mesaj / spam DM. Kapıya git, yüz yüze konuş.
- ❌ "Rakibiniz site yaptırdı" gibi baskı. Esnaf bunu hisseder, kapanır.
- ❌ Olmayan özellik vaat etme (online ödeme, rezervasyon sistemi). Site neyse onu göster.
- ❌ İlk görüşmede indirim yapma. Fiyat net olsun.

---

## 8. Fiyatlandırma

Reel'deki hesap: 50 dükkan → 5 evet → tanesi 25.000 ₺ → 125.000 ₺.

Kendi fiyatını belirlerken:

| Kalem | Öneri |
|---|---|
| Tek seferlik kurulum | 8.000 – 25.000 ₺ (semte ve işletme tipine göre) |
| Alan adı (yıllık) | 300 – 500 ₺ (maliyeti yansıt) |
| Aylık bakım (opsiyonel) | 300 – 800 ₺ (içerik güncelleme, yedek) |

**Dönüşüm beklentisi:** 50 kapı → 5-10 evet gerçekçi bir aralık. İlk 10 kapıda
0 evet alırsan sunumu değiştir, fiyatı değil.

**Nakit akışı:** Kurulum ücretinin yarısını başta, yarısını site yayına girince al.
Bakım ücretini aylık alırsan iş tek seferlik olmaktan çıkar.

---

## 9. Yasal sınırlar

Bunlar önemli, atlama.

**Veri kullanımı**
- OpenStreetMap verisi **ODbL** lisanslı. Yayımlarsan "© OpenStreetMap contributors"
  yazmak zorundasın. Ticari kullanım serbest.
- Google Places verisi: çoğu alan **30 günden fazla önbelleğe alınamaz**.
  Place ID kalıcı saklanabilir. Listeyi kalıcı veritabanı olarak satma, çalışma
  dosyası olarak tut ve yenile.
- İşletmenin iletişim bilgisini **kendi sitelerinde** yayımlamak için sözlü onay al.
  Kapıda "sitenizde telefonunuz görünecek, tamam mı?" diye sor.

**KVKK**
- Ticari işletmelerin kamuya açık işletme bilgileri (ad, adres, iş telefonu)
  kişisel veri sayılmaz — ama gerçek kişi esnafta (şahıs işletmesi) sınır incelir.
- Müşteri listesi tutuyorsan (kim ne dedi, kim ilgilendi), bunu aydınlatma
  yükümlülüğü kapsamında tut. Basit bir not defteri bile yeterli.
- Siteye iletişim formu koyarsan gizlilik metni gerekir. Bu şablonlarda form yok —
  bilinçli bir tercih.

**Site içeriği**
- İşletmenin adını, logosunu, fotoğrafını izinsiz kullanma. Sözlü izin al.
- "En iyi kuaför" gibi doğrulanamaz iddialar yazma.
- Çalışma saatlerini esnafa teyit ettir. Yanlış saat = müşteri kaybı = senin sorunun.

---

## 10. Sık yapılan hatalar

| Hata | Sonucu | Çözüm |
|---|---|---|
| OSM "site yok" verisine körü körüne güvenmek | Esnafın sitesi çıkar, itibar kaybı | Google'da adı arat, teyit et |
| Telefonsuz kayıtları listeye almak | Aranamaz, satılamaz | `kur` zaten atlıyor |
| 50 siteyi tek tek elle yapmak | 3 gün sürer | `kur` komutu 50 siteyi 2 saniyede üretir |
| Her siteye aynı metni koymak | Esnaf "bu benim değil" der | Sektör teması + işletme adı otomatik |
| Siteyi pazarlamadan bırakmak | 0 müşteri | Google Business Profile'a site linki ekle (esnafla birlikte) |
| Bakım ücreti almamak | 6 ay sonra site eskir, ilişki biter | Aylık bakım paketi sat |
| Toplu DM/e-posta | Spam, hesap kapanır | Sadece yüz yüze |

---

## Ek: Komut özeti

```bash
# ücretsiz tarama
python scripts/semt_avci.py tara "Kadıköy, İstanbul"

# Google Places ile (ücretli)
export GOOGLE_PLACES_KEY="AIza..."
python scripts/semt_avci.py tara "Kadıköy, İstanbul" --google

# ilk 50'ye site kur
python scripts/semt_avci.py kur leads.csv --en-iyi 50 --cikti siteler

# yardım
python scripts/semt_avci.py tara --help
python scripts/semt_avci.py kur --help
```

---

## Ek: Reel ile rehber arasındaki fark

Reel bir **hikaye**, bu rehber bir **sistem**. İkisini ayır:

| Reel'de | Gerçekte |
|---|---|
| "Kendi sistemimizi kurduk" | OpenStreetMap + Python script |
| "Haritayı taradı" | Overpass API sorgusu |
| "472 işletme" | Semte göre değişir (Kadıköy'de 778) |
| "Satış şansı puanı" | Sektör + yorum + puan + telefon ağırlıklı formül |
| "Tek komutla 50 site" | `semt_avci.py kur` — gerçekten tek komut |
| "125.000 ₺" | Senin fiyatın × senin dönüşümün |

Reel'deki hiçbir sayı uydurma değil ama hiçbiri de garanti değil.
Sistem çalışıyor; sonucu semtin ve sunumun belirler.

---

**Lisans:** MIT (kod) · ODbL (OpenStreetMap verisi)
**Soru:** [@yapayduck.ai](https://instagram.com/yapayduck.ai) DM
