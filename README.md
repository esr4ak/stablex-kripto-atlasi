# Stablex Kripto Atlası

Stablex kullanıcılarının il bazındaki kripto varlık tercihlerini **yalnızca
oranlarla** gösteren, Stablex marka kimliğiyle hazırlanmış statik harita.
Bir il seçildiğinde o ilde öne çıkan varlıklar, Türkiye geneliyle fark ve
kullanıcı yoğunluğu endeksi görüntülenir.

- **Canlı site:** https://esr4ak.github.io/stablex-kripto-atlasi/
- **Gömme (iframe) sürümü:** https://esr4ak.github.io/stablex-kripto-atlasi/?embed=1
  — üstteki Stablex menü çubuğu gizlenir, sayfa yüksekliği otomatik bildirilir.
- **Barındırma:** GitHub Pages (Settings → Pages → `main` / root).

## Dosyalar

| Dosya | Açıklama |
|---|---|
| `index.html` | Harita arayüzü (HTML + CSS + JS, harici kütüphane yok) |
| `data/atlas.json` | İl bazındaki oranlar — sayfa açılışta bu dosyayı okur |
| `embed-ornek.html` | Siteye gömme kodunun çalışan örneği |
| `atlas_uret.py` | Ham Excel'den `data/atlas.json` üreten script |

## Siteye ekleme

Aşağıdaki kodu sayfada haritanın görüneceği yere yapıştırmak yeterli.
`message` dinleyicisi iframe yüksekliğini içeriğe göre otomatik ayarlar
(mobilde kaydırma çubuğu çıkmaz).

```html
<iframe id="stablex-atlas" src="https://esr4ak.github.io/stablex-kripto-atlasi/?embed=1"
        title="Stablex Kripto Atlası" loading="lazy"
        style="width:100%;height:1400px;border:0;display:block;"></iframe>
<script>
  window.addEventListener('message', function (e) {
    if (e.origin !== 'https://esr4ak.github.io') return;
    if (e.data && e.data.type === 'stablex-atlas-height') {
      document.getElementById('stablex-atlas').style.height = e.data.height + 'px';
    }
  });
</script>
```

Web ekibi iframe yerine dosyaları kendi sunucusuna almak isterse
`index.html` ve `data/` klasörünü aynı dizine koyması yeterli.

## `data/atlas.json` yapısı

```json
{
  "İstanbul": {
    "density": 100.0,
    "limited": false,
    "coins": { "BTC": { "users": 12.3, "value": 32.5 }, "...": {} }
  }
}
```

- `users` — ildeki kullanıcıların yüzde kaçının o varlığı tuttuğu (%).
- `value` — varlığın ildeki toplam kripto varlık değeri içindeki payı (%).
- `density` — kullanıcı yoğunluğu endeksi (en yoğun il = 100).
- `limited` — kullanıcı sayısı az olan iller (oranlar daha oynak).

## Veri güncelleme (ham Excel → oranlar)

Ham Excel **asla repoya yüklenmez** (`.gitignore` `*.xlsx`/`*.csv`'yi engeller).
Oranlar bilgisayarda üretilir, repoya sadece `data/atlas.json` gider:

```bash
pip install pandas openpyxl
python atlas_uret.py il_gu_nvl.xlsx      # -> data/atlas.json
```

Beklenen Excel sütunları: `il, il_toplam_kisi, coin, kisi_sayisi, yogunluk_yuzde, toplam_deger_tl`

| Alan | Formül |
|---|---|
| `users` | `kisi_sayisi / il_toplam_kisi × 100` |
| `value` | coinin TL değeri / ildeki tüm coinlerin TL toplamı × 100 |
| `density` | `100 × ln(il_toplam_kisi) / ln(en kalabalık il)` |
| `limited` | `il_toplam_kisi < 10` (`LIMITED_ESIK`) |
| Türkiye geneli | tüm iller toplanarak aynı formüller |

Script, çıktıyı yazmadan önce içinde 0–100 dışında bir sayı ya da izinsiz
bir alan (kişi sayısı, TL tutarı) kalmadığını kontrol eder; kalırsa hata
verir. Sonra GitHub'da `data/` → *Add file → Upload files* ile yeni
`atlas.json` yüklenir; site birkaç dakika içinde yenilenir. Sayfadaki
hikâye kartlarındaki oranlar (Ankara BTC, İzmir ETH) da otomatik güncellenir.

## ⚠️ Notlar

- Dosyada **kullanıcı sayısı ve TL tutarı bulunmaz**; yalnızca bir
  ondalığa yuvarlanmış oranlar ve göreli endeks yer alır. Yeni veri
  eklenirken de bu kural korunmalıdır — repo ve site herkese açıktır.
- İçerik bilgilendirme amaçlıdır, **yatırım tavsiyesi değildir**. Resmi
  siteye eklenmeden önce hukuk/uyum ekibinin metinleri gözden geçirmesi
  önerilir.
- `index.html` doğrudan çift tıklanarak açılırsa veri yüklenmez
  (tarayıcı yerel dosya okumasını engeller). Yerelde denemek için:
  `python3 -m http.server` → http://localhost:8000
- Logo şu an düz metin ("STABLEX"); gömme modunda zaten gizlenir.
