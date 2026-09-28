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

**Veri güncellemek için** sadece `data/atlas.json` dosyasını aynı yapıda
yenisiyle değiştirmek yeterli. Site birkaç dakika içinde yenilenir.

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
