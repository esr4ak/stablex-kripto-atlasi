"""
Kripto Atlası — ham Excel'den data/atlas.json üretir.

KULLANIM
    pip install pandas openpyxl
    python atlas_uret.py il_gu_nvl.xlsx

    -> data/atlas.json dosyasını yazar. GitHub'a SADECE bu dosya yüklenir.
       Ham Excel bilgisayarında kalır (.gitignore zaten engelliyor).

BEKLENEN SÜTUNLAR (Excel'in ilk sayfası)
    il | il_toplam_kisi | coin | kisi_sayisi | yogunluk_yuzde | toplam_deger_tl
    (yogunluk_yuzde kullanılmaz; kisi_sayisi / il_toplam_kisi'den yeniden hesaplanır)

HESAPLAMALAR (sitedeki "Bu harita ne anlatıyor?" metniyle aynı)
    users   = kisi_sayisi / il_toplam_kisi * 100
              -> ildeki kullanıcıların yüzde kaçı o varlığı tutuyor
    value   = coinin TL değeri / ildeki tüm coinlerin toplam TL değeri * 100
    density = 100 * ln(il_toplam_kisi + 1) / ln(en kalabalık ilin il_toplam_kisi + 1)
              -> en yoğun il = 100 olan göreli endeks (log ölçek)
    limited = il_toplam_kisi < LIMITED_ESIK  (sitede "oranlar oynak" notu çıkar)
    "Türkiye geneli" = tüm illerin toplamı üzerinden aynı formüller

    Tüm oranlar bir ondalığa yuvarlanır. Çıktıda hiçbir kişi sayısı veya
    TL tutarı yer almaz; script bunu yazmadan önce ayrıca kontrol eder.
"""
import json
import math
import sys
from pathlib import Path

import pandas as pd

LIMITED_ESIK = 10          # bu sayının altında kullanıcısı olan iller "limited" işaretlenir
CIKTI = Path(__file__).parent / "data" / "atlas.json"
GEREKLI = ["il", "il_toplam_kisi", "coin", "kisi_sayisi", "toplam_deger_tl"]


def yuzde(pay, payda):
    return round(100 * pay / payda, 1) if payda else 0.0


def coin_adi(kod):
    kod = str(kod).strip().upper()
    return kod[:-3] if kod.endswith("TRY") else kod


def il_blogu(grup, toplam_kisi, yogunluk, limited, sirala=True):
    toplam_tl = grup["toplam_deger_tl"].sum()
    coins = {}
    if sirala:
        grup = grup.sort_values("kisi_sayisi", ascending=False, kind="stable")
    for _, r in grup.iterrows():
        coins[r["c"]] = {
            "users": yuzde(r["kisi_sayisi"], toplam_kisi),
            "value": yuzde(r["toplam_deger_tl"], toplam_tl),
        }
    return {"coins": coins, "limited": bool(limited), "density": yogunluk}


def guvenlik_kontrolu(veri):
    """Çıktıda ham veri kalmadığından emin ol: sadece izinli alanlar, tüm sayılar 0-100."""
    for il, blok in veri.items():
        assert set(blok) == {"coins", "limited", "density"}, f"{il}: beklenmeyen alan {set(blok)}"
        assert 0 <= blok["density"] <= 100, f"{il}: density aralık dışı"
        for coin, o in blok["coins"].items():
            assert set(o) == {"users", "value"}, f"{il}/{coin}: beklenmeyen alan {set(o)}"
            for k, v in o.items():
                assert isinstance(v, float) and 0 <= v <= 100, f"{il}/{coin}/{k}={v} oran değil!"


def main(yol):
    df = pd.read_excel(yol)
    eksik = [c for c in GEREKLI if c not in df.columns]
    if eksik:
        sys.exit(f"HATA: Excel'de şu sütunlar yok: {eksik}")

    df = df.dropna(subset=["il", "coin"]).copy()
    df["il"] = df["il"].astype(str).str.strip()
    df["c"] = df["coin"].map(coin_adi)
    df = df.groupby(["il", "c"], as_index=False, sort=False).agg(
        il_toplam_kisi=("il_toplam_kisi", "first"),
        kisi_sayisi=("kisi_sayisi", "sum"),
        toplam_deger_tl=("toplam_deger_tl", "sum"),
    )

    il_kisi = df.groupby("il", sort=False)["il_toplam_kisi"].first()  # Excel'deki il sırası korunur
    ln_max = math.log1p(il_kisi.max())

    veri = {}
    for il, kisi in il_kisi.items():
        yog = round(100 * math.log1p(kisi) / ln_max, 1)
        veri[il] = il_blogu(df[df["il"] == il], kisi, yog, kisi < LIMITED_ESIK)

    tr = df.groupby("c", as_index=False, sort=False)[["kisi_sayisi", "toplam_deger_tl"]].sum()
    veri["Türkiye geneli"] = il_blogu(tr, il_kisi.sum(), 100.0, False, sirala=False)

    guvenlik_kontrolu(veri)
    CIKTI.parent.mkdir(exist_ok=True)
    CIKTI.write_text(json.dumps(veri, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"OK: {len(veri) - 1} il + Türkiye geneli -> {CIKTI}")
    if len(veri) - 1 != 81:
        print(f"UYARI: 81 il bekleniyordu, {len(veri) - 1} il geldi. İl adlarını kontrol et.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Kullanım: python atlas_uret.py <ham_excel.xlsx>")
    main(sys.argv[1])
