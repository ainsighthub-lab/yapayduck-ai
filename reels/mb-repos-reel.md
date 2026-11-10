# Reel: 60 Saniyede 3 Repo (Yıllar Kazandıran)

@yapayduck.ai için üretilen tanıtım reelsi. Kendi yüzünü kullanan geliştiricilere
yönelik: public-apis, free-programming-books, project-based-learning repolarını
60 saniyede tanıtır.

## Video

- Süre: 62.1 sn · 1080×1920 (9:16) · 30 fps
- Stil: Neo-brutalist (krem zemin, lacivert kontur, sarı vurgu, offset gölge)
- Maskot: YapaDuck (ördek-robot, kamera-lens göz) — sağ-orta-alt bantta, kafa/anten/göz animasyonlu
- Ses: Kadın VO (Chatterbox, prolit referansı) + Newer Wave müzik yatağı (-31 dB)

## Sahne Akışı

| Zaman | Sahne | İçerik |
|---|---|---|
| 0-5.8 | Hook | "YILLAR KAZANDIRAN 3 REPO" + soru kartı |
| 5.8-14.9 | Repo 1 | public-apis — 490k yıldız sayaç animasyonu |
| 14.9-22.9 | Repo 2 | free-programming-books — 400k yıldız |
| 22.9-32.8 | Repo 3 | project-based-learning — 287k yıldız |
| 32.8-47.2 | CTA | "Bu videoyu beğen, paylaş ve yoruma REPO yaz" |
| 47.2-54.3 | Total | 1.176.000 YILDIZ sayaç reveal |
| 54.3-62.1 | Outro | @yapayduck.ai + maskot alt-ortada |

## VO Scripti (Outro)

> 54.3s: "Yoruma repo yaz, beğen ve paylaş."
> 58.0s: "Devamı için yapayduck.ai'ı takip et."

## Yapım Pipeline'ı

1. **Kompozisyon:** HyperFrames (HTML → MP4) — `index.html`, GSAP timeline
2. **Seslendirme:** Chatterbox MTL (kadın prolit v2_dynamic referansı)
   - RNNoise temizlik → sessizlik kırpma → statik gain → limiter 0.93
   - Cızırtı yok, -15.5 LUFS master
3. **Müzik:** Newer Wave (Kevin MacLeod) — -31 dB yatak, fade in/out
4. **Maskot:** YapaDuck SVG — production-lock karakter sheet
   - Bacaklar ayna transform ile ayrık
   - Kafa sallanma + anten bob + göz kırpma (14x) + sahne geçiş zıplaması
5. **Render:** hyperframes CLI → 1080×1920 MP4 → CRF 26 teslim (<10 MB)

## Tekrar Üretim

Kaynak proje: `mb-repos-hf` (HyperFrames). VO pipeline scriptleri
`vo_outro/` altında: `gen_vo.py` (TTS) → `rebuild_vo.py` (mix) → `install_mix.py` (kurulum).
