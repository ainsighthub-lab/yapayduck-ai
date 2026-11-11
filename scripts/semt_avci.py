#!/usr/bin/env python3
"""Semt Avcısı — sitesi olmayan yerel esnafı bulur, puanlar, site üretir.

Üç komut:
    semt_avci.py tara  "Kadıköy, İstanbul"            # ücretsiz, OpenStreetMap
    semt_avci.py tara  "Kadıköy, İstanbul" --google   # Google Places (ücretli, daha zengin)
    semt_avci.py kur   leads.csv --en-iyi 50

Bağımlılık yok: sadece Python 3.8+ standart kütüphanesi.

Veri kaynakları
---------------
OpenStreetMap (varsayılan) — ücretsiz, ODbL lisanslı, günde sınırsız.
    `website` ve `contact:website` etiketi olmayan işletmeleri bulur.
    Eksisi: etiket eksikliği "sitesi yok" demek değildir, doğrula.
Google Places API (New) — işletme başına ücretli (websiteUri = Enterprise SKU).
    `places.websiteUri` alanı boş olanlar gerçekten sitesizdir.
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

UA = "semt-avci/1.0 (https://github.com/ainsighthub-lab/yapayduck-ai)"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "sablonlar", "taban.html")
THEMES = os.path.join(ROOT, "sablonlar", "temalar.json")

# OSM etiketi -> (Türkçe ad, taban puan ağırlığı)
NISLER = {
    "shop": {"hairdresser": "Kuaför", "beauty": "Güzellik Salonu", "barber": "Berber",
             "bakery": "Fırın", "butcher": "Kasap", "clothes": "Butik",
             "car_repair": "Oto Tamir", "car_wash": "Oto Yıkama",
             "florist": "Çiçekçi", "pet": "Petshop", "shoes": "Ayakkabıcı",
             "electronics": "Elektronik", "furniture": "Mobilya", "jewelry": "Kuyumcu"},
    "amenity": {"cafe": "Kafe", "restaurant": "Restoran", "fast_food": "Fast Food",
                "pharmacy": "Eczane", "dentist": "Diş Hekimi", "veterinary": "Veteriner",
                "car_wash": "Oto Yıkama", "driving_school": "Sürücü Kursu"},
    "craft": {"photographer": "Fotoğrafçı", "electrician": "Elektrikçi",
              "plumber": "Tesisatçı", "carpenter": "Marangoz"},
}

# Satış şansı: bu sektörler "hazır site"ye daha çok evet der
SEKTOR_AGIRLIK = {
    "Kuaför": 22, "Güzellik Salonu": 22, "Berber": 20, "Oto Yıkama": 20,
    "Kafe": 18, "Restoran": 18, "Diş Hekimi": 18, "Veteriner": 16,
    "Fotoğrafçı": 14, "Butik": 14, "Sürücü Kursu": 14, "Petshop": 12,
    "Oto Tamir": 12, "Fırın": 10, "Çiçekçi": 10, "Elektrikçi": 10,
    "Tesisatçı": 10, "Marangoz": 10, "Fast Food": 10, "Eczane": 6,
    "Kasap": 6, "Mobilya": 8, "Kuyumcu": 6, "Ayakkabıcı": 8, "Elektronik": 6,
}


# ---------------------------------------------------------------- yardımcılar

def http_json(url, data=None, headers=None, timeout=90, tries=3):
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    body = urllib.parse.urlencode(data).encode() if isinstance(data, dict) else data
    last = None
    for n in range(tries):
        try:
            req = urllib.request.Request(url, data=body, headers=h,
                                         method="POST" if body else "GET")
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read()[:200].decode('utf-8', 'replace')}"
            if e.code == 429 or e.code >= 500:
                time.sleep(3 * (n + 1))
                continue
            raise RuntimeError(last) from None
        except (urllib.error.URLError, TimeoutError) as e:
            last = str(e)
            time.sleep(3 * (n + 1))
    raise RuntimeError(f"istek başarısız: {last}")


def slug(s):
    s = s.replace("ı", "i").replace("İ", "i").replace("ş", "s").replace("Ş", "s")
    s = s.replace("ğ", "g").replace("Ğ", "g").replace("ü", "u").replace("Ü", "u")
    s = s.replace("ö", "o").replace("Ö", "o").replace("ç", "c").replace("Ç", "c")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "isletme"


def tel_norm(t):
    d = re.sub(r"\D", "", t or "")
    if len(d) == 12 and d.startswith("90"):
        d = d[2:]
    if len(d) == 10 and not d.startswith("0"):
        d = "0" + d
    if len(d) != 11 or not d.startswith("0"):
        return ""
    return f"{d[:4]} {d[4:7]} {d[7:9]} {d[9:]}"


def bbox_of(yer):
    """Semt adı -> (güney, kuzey, batı, doğu). Nominatim ile."""
    url = ("https://nominatim.openstreetmap.org/search?"
           + urllib.parse.urlencode({"q": yer, "format": "json", "limit": 1,
                                     "accept-language": "tr"}))
    res = http_json(url)
    if not res:
        sys.exit(f"semt bulunamadı: {yer}")
    s, n, w, e = (float(x) for x in res[0]["boundingbox"])
    print(f"  alan: {res[0]['display_name'][:70]}")
    return s, n, w, e


# ---------------------------------------------------------------- tarama

def tara_osm(yer, sinir=800):
    s, n, w, e = bbox_of(yer)
    parcalar = []
    for anahtar, degerler in NISLER.items():
        for v in degerler:
            parcalar.append(f'nwr["{anahtar}"="{v}"][!"website"][!"contact:website"]'
                            f'["name"]({s},{w},{n},{e});')
    q = f'[out:json][timeout:90];\n({"".join(parcalar)});\nout center tags {sinir};'
    print(f"  OSM taranıyor ({len(parcalar)} kategori)…")
    res = http_json("https://overpass-api.de/api/interpreter", {"data": q})
    out, gorulen = [], set()
    for el in res.get("elements", []):
        t = el.get("tags", {})
        ad = (t.get("name") or "").strip()
        if not ad:
            continue
        anahtar = (ad.lower(), t.get("addr:street", ""))
        if anahtar in gorulen:
            continue
        gorulen.add(anahtar)
        sektor = ""
        for k in ("shop", "amenity", "craft"):
            if t.get(k) in NISLER.get(k, {}):
                sektor = NISLER[k][t[k]]
                break
        out.append({
            "ad": ad, "sektor": sektor or "Diğer",
            "telefon": tel_norm(t.get("phone") or t.get("contact:phone") or ""),
            "adres": " ".join(x for x in [t.get("addr:street", ""),
                                          t.get("addr:housenumber", "")] if x),
            "semt": yer.split(",")[0].strip(),
            "site": "", "puan": 0, "yorum": 0, "kaynak": "osm",
        })
    return out


def tara_google(yer, anahtar, sektorler=None):
    sektorler = sektorler or ["kuaför", "berber", "kafe", "oto yıkama", "butik"]
    out, gorulen = [], set()
    mask = ("places.id,places.displayName,places.formattedAddress,places.websiteUri,"
            "places.nationalPhoneNumber,places.rating,places.userRatingCount,"
            "places.primaryTypeDisplayName,nextPageToken")
    for s in sektorler:
        soru = f"{s} {yer}"
        print(f"  Google: {soru}")
        body = {"textQuery": soru, "regionCode": "TR", "languageCode": "tr",
                "maxResultCount": 20}
        for _ in range(3):  # 3 sayfa = 60 sonuç
            res = http_json("https://places.googleapis.com/v1/places:searchText",
                            json.dumps(body).encode(),
                            {"Content-Type": "application/json",
                             "X-Goog-Api-Key": anahtar,
                             "X-Goog-FieldMask": mask})
            for p in res.get("places", []):
                if p.get("websiteUri"):
                    continue
                pid = p.get("id", "")
                if pid in gorulen:
                    continue
                gorulen.add(pid)
                out.append({
                    "ad": p.get("displayName", {}).get("text", "").strip(),
                    "sektor": p.get("primaryTypeDisplayName", {}).get("text", s.title()),
                    "telefon": tel_norm(p.get("nationalPhoneNumber", "")),
                    "adres": p.get("formattedAddress", ""),
                    "semt": yer.split(",")[0].strip(),
                    "site": "", "puan": round(p.get("rating", 0), 1),
                    "yorum": p.get("userRatingCount", 0), "kaynak": "google",
                })
            tok = res.get("nextPageToken")
            if not tok:
                break
            body["pageToken"] = tok
            time.sleep(1.2)
    return out


# ---------------------------------------------------------------- puanlama

def puanla(k):
    """0-100 satış şansı. Yüksek = ara, göster, sat."""
    p = SEKTOR_AGIRLIK.get(k["sektor"], 6)          # sektör uyumu (0-22)
    yorum = k["yorum"]
    if yorum >= 200:
        p += 24                                     # oturmuş işletme, ödeme gücü var
    elif yorum >= 80:
        p += 20
    elif yorum >= 25:
        p += 15
    elif yorum >= 8:
        p += 9
    elif yorum >= 1:
        p += 4
    else:
        p += 1                                      # hiç yorum yok: ölü ya da yeni
    puan = k["puan"]
    if puan >= 4.5:
        p += 16                                     # itibarı iyi, dijitalleşmeye açık
    elif puan >= 4.0:
        p += 12
    elif puan >= 3.5:
        p += 7
    elif puan > 0:
        p += 3
    if k["telefon"]:
        p += 18                                     # aranamıyorsa satılamaz
    if k["adres"]:
        p += 8
    if k["kaynak"] == "google":
        p += 4                                      # kayıt doğrulanmış
    return max(0, min(100, p))


# ---------------------------------------------------------------- site üretimi

def yukle_tema(sektor):
    with open(THEMES, encoding="utf-8") as f:
        temalar = json.load(f)
    for anahtar, t in temalar.items():
        if sektor in t.get("sektorler", []):
            return t
    return temalar["_varsayilan"]


def kur(k, cikti_dir):
    with open(TPL, encoding="utf-8") as f:
        tpl = f.read()
    t = yukle_tema(k["sektor"])
    ad = k["ad"]
    semt = k["semt"]
    tel = k["telefon"]
    harita = "https://www.google.com/maps/search/?api=1&query=" + \
             urllib.parse.quote(f"{ad} {semt}")
    hizmetler = t["hizmetler"]
    kartlar = "\n".join(
        f'      <div class="kart"><div class="ikon">{h[2]}</div>'
        f'<h3>{h[0]}</h3><p>{h[1]}</p></div>' for h in hizmetler)
    doldur = {
        "AD": ad, "AD_UPPER": ad.upper(), "SEKTOR": k["sektor"], "SEMT": semt,
        "TEL": tel, "TEL_LINK": re.sub(r"\D", "", tel), "ADRES": k["adres"] or semt,
        "HARITA": harita, "KARTLAR": kartlar, "SLOGAN": t["slogan"],
        "RENK": t["renk"], "RENK2": t["renk2"], "ZEMIN": t["zemin"],
        "BASLIK": t["baslik"], "ALT": t["alt"],
        "CTA": t["cta"], "YIL": time.strftime("%Y"),
    }
    # tek isim alanı: değerler kendi içinde başka token taşıyabilir ({{BASLIK}} -> {{SEMT}}),
    # bu yüzden 3 geçiş yeter (derinlik 2'yi garanti eder)
    html = tpl
    for _ in range(3):
        for a, b in doldur.items():
            html = html.replace("{{" + a + "}}", str(b))
    hedef = os.path.join(cikti_dir, slug(ad))
    os.makedirs(hedef, exist_ok=True)
    with open(os.path.join(hedef, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return os.path.join(hedef, "index.html")


# ---------------------------------------------------------------- komutlar

def cmd_tara(a):
    print(f"Semt Avcısı → {a.yer}")
    if a.google:
        anahtar = os.environ.get("GOOGLE_PLACES_KEY") or a.key
        if not anahtar:
            sys.exit("--google için GOOGLE_PLACES_KEY ortam değişkeni ya da --key gerekli")
        kayitlar = tara_google(a.yer, anahtar)
    else:
        kayitlar = tara_osm(a.yer)
    for k in kayitlar:
        k["puan_satis"] = puanla(k)
    kayitlar.sort(key=lambda k: -k["puan_satis"])
    print(f"\n  sitesi olmayan: {len(kayitlar)}")
    print(f"  telefonu olan : {sum(1 for k in kayitlar if k['telefon'])}")
    if kayitlar:
        print(f"  en yüksek puan: {kayitlar[0]['puan_satis']} ({kayitlar[0]['ad']})")
    with open(a.cikti, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["puan_satis", "ad", "sektor", "telefon",
                                          "adres", "semt", "puan", "yorum", "kaynak"])
        w.writeheader()
        for k in kayitlar:
            w.writerow({x: k[x] for x in w.fieldnames})
    print(f"  yazıldı: {a.cikti}")


def cmd_kur(a):
    with open(a.csv, encoding="utf-8-sig") as f:
        satirlar = list(csv.DictReader(f))
    satirlar = [s for s in satirlar if s.get("telefon")]      # aranamayanı atla
    satirlar.sort(key=lambda s: -int(s["puan_satis"]))
    secili = satirlar[:a.en_iyi]
    os.makedirs(a.cikti, exist_ok=True)
    print(f"Semt Avcısı → {len(secili)} site kuruluyor ({a.cikti})")
    for s in secili:
        yol = kur({
            "ad": s["ad"], "sektor": s["sektor"], "semt": s["semt"],
            "telefon": s["telefon"], "adres": s.get("adres", ""),
        }, a.cikti)
        print(f"  {s['puan_satis']:>3} puan  {s['ad'][:34]:34} {os.path.basename(os.path.dirname(yol))}")
    print(f"\n  bitti. Netlify Drop'a {a.cikti} klasörünü sürükle.")


def main():
    ap = argparse.ArgumentParser(description="Semt Avcısı — sitesi olmayan esnafı bul ve site kur")
    sub = ap.add_subparsers(dest="komut", required=True)

    t = sub.add_parser("tara", help="semtteki sitesi olmayan işletmeleri listele")
    t.add_argument("yer", help='örn. "Kadıköy, İstanbul"')
    t.add_argument("--google", action="store_true", help="Google Places kullan (ücretli)")
    t.add_argument("--key", default="", help="Google Places API anahtarı")
    t.add_argument("--cikti", default="leads.csv")
    t.set_defaults(f=cmd_tara)

    k = sub.add_parser("kur", help="CSV'den site üret")
    k.add_argument("csv")
    k.add_argument("--en-iyi", type=int, default=50)
    k.add_argument("--cikti", default="siteler")
    k.set_defaults(f=cmd_kur)

    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
