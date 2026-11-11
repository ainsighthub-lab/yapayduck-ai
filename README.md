# 🦆 YapayDuck.ai — AI Video Prompt & Workflow Kütüphanesi

Instagram'daki [@yapayduck.ai](https://instagram.com/yapayduck.ai) hesabı için AI video promptları, workflow rehberleri ve araç listeleri. Her gün yeni prompt/rehber eklenir.

[![Instagram](https://img.shields.io/badge/Instagram-@yapayduck.ai-E4405F?logo=instagram&logoColor=white)](https://instagram.com/yapayduck.ai)
[![Lisans](https://img.shields.io/badge/Lisans-MIT-yellow)](#lisans)

---

## 📚 Kütüphane

### Promptlar (`prompts/`)

| Prompt | Açıklama |
|---|---|
| [VOX Master Prompt](prompts/vox-master-prompt.md) | Universal documentary collage/animation prompt motoru. Multi-niche, multi-dil, multi-görsel stil. 11 state'li state-machine: fikir → senaryo → seslendirme → beat → görsel prompt → hareket prompt → thumbnail |
| [50 Slash Komutlu Ürün Promptu](prompts/50-slash-komutlu-urun-promptlari.md) | Google Flow ve benzeri araçlar için 50 profesyonel slash komutu: kamera, lüks, fizik/sıvı, VFX, UGC, kozmetik, yemek, mevsimsel |
| [YouTube Kanalı için 8 Gemini Promptu](prompts/youtube-kanali-icin-8-gemini-promptu.md) | Kanal makeover, bio optimizasyonu, playlist yapısı, banner, CTR audit, keyword mimarisi, pinned comment funnel |
| [AI Brand Logo Reveal Promptu](prompts/logo-reveal-promptu.md) | Storefront referans + logo görselinden 7 sn cinematic logo reveal. Brand-specific malzeme dönüşümü, tek plan |

### Rehberler (`guides/`)

| Rehber | Açıklama |
|---|---|
| [Semt Avcısı — Kendi Semtinde Site Satma Rehberi](guides/semt-avcisi-rehber.md) | Reel'deki sistemin gerçek kurulumu: sitesi olmayan esnafı bul → satış şansına göre puanla → tek komutla site kur → kapıya git. Çalışan Python script + HTML şablon + fiyatlandırma + KVKK sınırları |
| [Google Flow & Omni Flash ile 3D Tom & Jerry Workflow](guides/google-flow-omni-flash-tom-jerry-workflow.md) | Kendi yüzünle Tom & Jerry (veya başka karakter) videosu: Nano Banana Pro ile başlangıç görseli → Omni Flash ile animasyon. Karakter özelleştirme tablosu dahil |
| [Video AI Araçları](guides/video-ai-araclari.md) | OpenMontage, MoneyPrinterTurbo, HyperFrames, Wan2.1 — hangi araç ne için |

### Araçlar (`scripts/`, `sablonlar/`)

| Dosya | Açıklama |
|---|---|
| [`scripts/semt_avci.py`](scripts/semt_avci.py) | Sitesi olmayan yerel esnafı bulur (OpenStreetMap ücretsiz / Google Places ücretli), satış şansına göre puanlar, sektöre özel site üretir. Sıfır bağımlılık, tek dosya |
| [`sablonlar/taban.html`](sablonlar/taban.html) | Üretilen sitenin iskeleti: mobil öncelikli, tek dosya, JS yok, `tel:` linkli |
| [`sablonlar/temalar.json`](sablonlar/temalar.json) | Sektör teması: renk, başlık, slogan, hizmet kartları |

### Kaynaklar (`kaynaklar/`)

| Dosya | Açıklama |
|---|---|
| [Ücretsiz Kaynak Repoları](kaynaklar/ucretsiz-kaynak-repolari.md) | Takipçilerle paylaşılan liste: 3 video reposu + 3 bonus repo, yıldız sayıları ve kullanım amacıyla |

### Kurulum

| Dosya | Açıklama |
|---|---|
| [7/24 Agentic Kurulum](7-24%20Agentic%20Kurulum.md) | Tek VPS'te hiç kapanmayan AI ajanı: Docker + Hermes, ≈50$/ay |

---

## 🔄 Günlük Akış

Bu repo [@yapayduck.ai](https://instagram.com/yapayduck.ai) Instagram hesabının içerik kütüphanesidir:

1. Yeni prompt/rehber önce Notion'da hazırlanır
2. Buraya markdown olarak eklenir
3. Instagram'da duyurulur

## 📬 İletişim

- Instagram: [@yapayduck.ai](https://instagram.com/yapayduck.ai)
- Sorular: Instagram DM

## 📄 Lisans

MIT
