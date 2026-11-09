# Google Flow & Omni Flash ile 3D Tom & Jerry Video Workflow Rehberi

Bu rehber, kendi yüz fotoğrafınızı kullanarak Tom & Jerry (veya dilediğiniz herhangi bir karakter) ile etkileşime giren yüksek kaliteli, karakter tutarlılığına sahip yapay zeka videoları oluşturmak için adım adım hazırlanmıştır.

### 🛠️ Gereksinimler & Kullanılan Araçlar

- Google Flow / Labs (Nano Banana Pro & Omni Flash)
  - Erişim: Google Labs Flow Platformu
- Kişisel fotoğraf
  - Net, önden çekilmiş, iyi ışık alan portre/özçekim
- Ücretsiz Google hesabı

### 🚀 Süreç Özeti

1. AŞAMA 1: Görüntü oluşturma
2. AŞAMA 2: Video animasyonu
3. AŞAMA 3: İndirme & paylaşım

---

### 📍 Adım 1: Başlangıç Görselinin Üretilmesi (Gelişmiş Işık & Doku Tespiti)

Amaç: Kendi yüz hatlarınızı korurken Tom ve Jerry karakterlerini omuz ve baş hizanıza fiziksel olarak doğru ışık ve gölgelerle yerleştirmek.

1. Google Labs Flow adresine gidin ve New Project’e tıklayın.
2. Sol panelden model olarak Nano Banana Pro seçin.
3. Upload Image ile kendi yüz fotoğrafınızı yükleyin.
4. Aşağıdaki prompt’u yapıştırıp Generate’e basın.

#### 💡 1. AŞAMA PROMPT (Nano Banana Pro)

```
Photorealistic close-up portrait of the attached person sitting in a comfortable office chair in an average American home bedroom.

On their shoulder sits a highly detailed 3D animated Tom Cat, looking playfully toward the camera. On top of their head sits a stylized 3D animated Jerry the Mouse, balanced naturally with his feet ruffling the hair slightly.

Tom and Jerry maintain their iconic animated appearance but rendered with realistic 3D textures, ambient occlusion, and lighting that matches the room's warm key light. The person looks up toward them with a genuine, amused smile. Shot on a 35mm lens, shallow depth of field, soft natural indoor lighting.
```

İpucu: Üretilen 4 varyasyon arasından karakterlerin yüz hatlarının en net çıktığı ve yüzünüze en doğal oturduğu görseli indirip saklayın.

---

### 📍 Adım 2: Görseli Videoya Dönüştürme (Karakter & Hareket Tutarlılığı)

Bu aşamada, ürettiğimiz durağan resmi video modeline vererek karakterlere hareket kazandıracağız.

1. Model seçiminden Google Omni Flash’e geçin.
2. Adım 1’de indirdiğiniz en iyi başlangıç görselini yükleyin.
3. Aşağıdaki video prompt’unu yapıştırıp Run’a basın.

#### 💡 2. AŞAMA PROMPT (Google Omni Flash)

```
Subtle handheld camera movement with natural micro-shakes, captured at 24fps.

Character Animation & Interaction:
Tom Cat angrily lunges and reaches around the person's neck to chase Jerry, while Jerry scrambles and dodges around the top of the person's head. Both characters maintain their exact 3D cartoon style, proportions, and lighting consistency from the source image.

Subject Reaction & Physics:
The person reacts naturally in real-time—flinching slightly, blinking, and laughing as their head sways to dodge the movement. Dynamic shadows cast by Tom and Jerry shift seamlessly across the person's neck, face, and collar.
```

---

### 🎨 Farklı Karakterler İçin Nasıl Özelleştirilir?

Bu prompt yapısını diğer popüler karakterlerle değiştirmek için Prompt 1 ve Prompt 2 içindeki karakter isimlerini güncelleyin:

- Spider-Man & Spider-Ham
  - Tom Cat ➔ Mini 3D Spider-Man
  - Jerry the Mouse ➔ 3D Cartoon Spider-Ham
- Pikachu & Ash
  - Tom Cat ➔ 3D Realistic Pikachu
  - Jerry the Mouse ➔ 3D Mini Ash Ketchum

### 📌 En İyi Sonuçlar İçin Püf Noktaları (Pro-Tips)

- Yüz ifadesi: İlk fotoğrafta donuk durmamaya çalışın. Hafif tebessüm/yukarı bakış daha doğal tepkiler üretir.
- Kamera sarsıntısı: Video prompt’undaki “handheld camera movement with natural micro-shakes” ifadesini çıkarmayın; gerçek çekim hissi verir.
- Işık uyumu: Fotoğrafınızdaki ışık yönü ne kadar netse (ör. soldan gelen sıcak ışık), karakterler o kadar iyi oturur.

### 💬 Sorular

Instagram DM üzerinden bana ulaşabilirsiniz.
