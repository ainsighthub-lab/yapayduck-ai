🦆 YapayDuck.ai — 7/24 Hiç Kapanmayan Ajan Kurulumu

Tek sunucu, ayda 50. Yedi gün, kesintisiz.

[![Rehber](https://img.shields.io/badge/Rehber-@yapayduck.ai-orange)](#)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04-E95420?logo=ubuntu&logoColor=white)](#)
[![Docker](https://img.shields.io/badge/Docker-Konteyner-2496ED?logo=docker&logoColor=white)](#)
[![Hermes](https://img.shields.io/badge/Hermes-NousResearch%20%C2%B7%20MIT-111111)](#)
[![Lisans](https://img.shields.io/badge/Lisans-MIT-yellow)](#)

---

📖 İçindekiler

- [Genel Bakış](#-genel-bakış)
- [Mimari](#-mimari)
- [Maliyet Tablosu](#-maliyet-tablosu)
- [Adım 01 — VPS / Sunucu](#-adım-01--vps--sunucu)
- [Adım 02 — SSH Anahtarı](#-adım-02--ssh-anahtarı)
- [Adım 03 — Docker / Kutu](#-adım-03--docker--kutu)
- [Adım 04 — Hermes](#-adım-04--hermes)
- [Adım 05 — Model](#-adım-05--model)
- [Adım 06 — Bakım](#-adım-06--bakım)
- [Toplam ve Özet](#-toplam-ve-özet)
- [Sık Sorulan Sorular](#-sık-sorulan-sorular)

---

🧭 Genel Bakış

Bu depo, tek bir VPS üzerinde 7 gün 24 saat çalışan, hiç kapanmayan bir yapay zekâ ajanı kurulum rehberidir. Hazırlanmış / managed servislere aylık yüzlerce dolar ödemeden, bileşenleri kendin seçip çalıştırırsın.

> 💡 Temel prensip: Ajan bozulursa kutuyu sil, yenisini aç. Hafıza (veri) her zaman kutunun dışında tutulur.

---

🏗️ Mimari

```
┌──────────────────────────────────────────────┐
│                 VPS (Ubuntu 24.04)           │
│              7/24 açık · hiç kapanmaz         │
│                                              │
│   ┌────────────────────────────────────┐     │
│   │  Docker Konteyner (Hermes Ajan)    │     │
│   │  bozulursa → sil, yeniden aç       │     │
│   └────────────────────────────────────┘     │
│              ▲                               │
│              │ hafıza DİŞARIDA                │
│   /data/  (kalıcı veri · silinmez)           │
│                                              │
│   ┌────────────────────────────────────┐     │
│   │  Model aboneliği + yedek model     │     │
│   └────────────────────────────────────┘     │
└──────────────────────────────────────────────┘
```

Katman	Araç	Neden?	
Sunucu	VPS + Ubuntu 24.04	Ayda 25–30, hiç kapanmaz	
Erişim	SSH anahtarı	Şifre girişi kapalı — botlar kapıda bekliyor	
Çalıştırma	Docker	Ajan bozarsa kutuyu sil, yenisi açılır	
Zamanlama	Hermes (NousResearch)	MIT lisans, açık kaynak, ücretsiz, zamanlı işler	
Beyin	Model aboneliği	Ayda 20, yedek model şart	
Sürdürülebilirlik	Kendi bakımın	Güncelleme + yedek doğrulama sende (hazırı aya 30)	

---

💰 Maliyet Tablosu

Bileşen	Maliyet	Not	
VPS (Ubuntu 24.04)	25–30 /ay	7/24 açık	
Model aboneliği	20 /ay	En kolay yol	
TOPLAM	≈ 50 /ay	Sunucu + Model	

> Hazır (managed) çözüm istersen aya 30 ekstra; toplam 80 /ay bandına çıkar. Kendi bakımını üstlenerek 50 /ayda kalırsın.

---

🖥️ Adım 01 — VPS / Sunucu

1. Herhangi bir VPS sağlayıcıdan Ubuntu 24.04 imajlı bir sunucu kirala.
2. Minimum öneri: 2 vCPU / 4 GB RAM / 40 GB SSD.
3. Sunucuyu başlattıktan sonra SSH ile bağlan:

```bash
ssh root@SUNUCU_IP_ADRESI
```

4. Sistemi güncelle:

```bash
apt update && apt upgrade -y
```

> ✅ Kontrol noktası: Sunucu yeniden başlatmada bile otomatik açılmalı. VPS sağlayıcılarının tamamında varsayılan olarak böyledir — kendi bilgisayarınla karıştırma!

---

🔑 Adım 02 — SSH Anahtarı

Şifreyle girişi tamamen kapat — botlar sürekli deniyor.

2.1 — Anahtar üret (kendi bilgisayarında)

```bash
ssh-keygen -t ed25519 -C "yapayduck"
# Üretilen anahtar: ~/.ssh/id_ed25519.pub
```

2.2 — Anahtarı sunucuya yükle

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@SUNUCU_IP_ADRESI
```

2.3 — Şifreli girişi kapat (sunucuda)

```bash
nano /etc/ssh/sshd_config
```

```ini
PasswordAuthentication no
PermitRootLogin prohibit-password
```

```bash
systemctl restart sshd
```

> ⚠️ Çıkış yapmadan önce yeni bir terminale anahtarla girebildiğinden emin ol! Yoksa kendini dışarıda bulursun.

---

📦 Adım 03 — Docker / Kutu

Her şeyi kapalı kutuya al; hafızayı kutunun dışında tut.

3.1 — Docker kur

```bash
curl -fsSL https://get.docker.com | sh
```

3.2 — Kalıcı veri dizini

```bash
mkdir -p /data/yapayduck
```

3.3 — Konteyner çalıştır (örnek)

```bash
docker run -d   --name yapayduck   --restart unless-stopped   -v /data/yapayduck:/data   --env-file /data/yapayduck/.env   ghcr.io/nousresearch/hermes:latest
```

> 🔄 Kural: Ajan bozarsa → `docker rm -f yapayduck` → yeniden `docker run`. Veriler `/data` dizininde güvende kalır, çünkü kutu gider, hafıza kalır.

---

⏰ Adım 04 — Hermes

Hermes, NousResearch tarafından geliştirilen açık kaynaklı bir ajan çalıştırma çatısıdır: MIT lisans, ücretsiz ve zamanlı işleri (cron / scheduled jobs) senin için çevirir.

```bash
# docker-compose ile örnek — bkz. docs/docker-compose.yml
docker compose up -d
```

Öne çıkanlar:

- ✅ MIT lisans — ticari kullanım serbest
- ✅ Zamanlı işler: `hermes job add "0 * * * *" /data/gorevler.sh`
- ✅ Açık kaynak — bağımlılık kalmadan taşıyabilirsin

---

🧠 Adım 05 — Model

Bir model bağla. En kolay yol abonelik (20 /ay).

```bash
# .env dosyası örneği
MODEL_API_KEY=xxxxx
MODEL_PRIMARY=ana-model
MODEL_FALLBACK=yedek-model
```

> 🔁 Yedek model şart! Birincil model düştüğünde ajan durmasın; yedek devreye girer.

---

🛠️ Adım 06 — Bakım

Güncelleme ve yedek doğrulama sende. (Hazır istersen aya 30 daha.)

```bash
# Güncelleme rutini — scripts/update.sh içinde hazır
./scripts/update.sh

# Yedeği test et (kutuyu sil, geri yükle, çalıştığını doğrula)
./scripts/restore-test.sh
```

Bakım kontrol listesi:

- Haftalık: `apt update && apt upgrade`
- Haftalık: konteyner imajını güncelle (`docker compose pull && docker compose up -d`)
- Aylık: yedek geri yükleme testi — yedeğin çalıştığından emin ol
- Aylık: disk doluluğunu kontrol et (`df -h`)

---

🧾 Toplam ve Özet

		
💵 Toplam	≈ 50 /ay	
🖥️ Sunucu	Tek VPS, Ubuntu 24.04	
⏱️ Çalışma	7 gün, kesintisiz	

Altı adım: Sunucu → SSH anahtarı → Docker kutusu → Hermes → Model (+yedek) → Bakım.

---

❓ Sık Sorulan Sorular

Ajan çökerse ne olur?
`docker compose restart` yeterli. Bozulduysa konteyneri silip yeniden aç; hafıza `/data` içinde olduğu için hiçbir şey kaybolmaz.

Neden şifreyle giriş kapalı?
Şifre girişi aktif olan her sunucu dakikada onlarca bot saldırısı yer. Anahtarla giriş pratik olarak kırılmaz.

Hazır servis alsam fark ne olur?
Aynı kurulumu 80 /aya managed olarak alırsın. Kendin kurarsan 50 /ay ve tam kontrol sende.

---

📬 İletişim

Rehber profilde: [@yapayduck.ai](https://instagram.com/yapayduck.ai)

---
