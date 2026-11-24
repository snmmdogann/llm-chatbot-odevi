# LLM Chatbot

Terminalde çalışan basit bir Türkçe chatbot. [OpenRouter](https://openrouter.ai) üzerinden **Google Gemini 2.5 Flash-Lite** modelini kullanır.

## Özellikler

- Konuşma geçmişini hatırlar (her istekte önceki mesajlar da modele gönderilir)
- Kısa ve kibar Türkçe cevaplar veren sistem talimatı
- Hataları (geçersiz anahtar, bakiye yetersizliği, hız sınırı vb.) yakalar, program kapanmaz
- Çıkışta toplam token kullanımını ve maliyeti gösterir

## Kurulum

1. Python 3.10 veya üstü gerekir.
2. Bağımlılıkları yükleyin:

   ```bash
   pip install -r requirements.txt
   ```

3. `.env.example` dosyasını `.env` adıyla kopyalayın ve kendi OpenRouter API anahtarınızı yazın:

   ```
   OPENROUTER_API_KEY=sk-or-v1-...
   ```

   > `.env` dosyası `.gitignore` içindedir, GitHub'a gönderilmez. Anahtarınızı kimseyle paylaşmayın.

## Kullanım

```bash
python chatbot.py
```

Örnek:

```
Chatbot hazır (google/gemini-2.5-flash-lite). Çıkmak için 'çık' yazın.

Sen: Merhaba, kendini bir cümleyle tanıt.
Bot: Merhaba, ben Google tarafından eğitilmiş büyük bir dil modeliyim.

Sen: çık

Görüşürüz! Toplam: 42 giriş + 13 çıkış token, maliyet $0.000009
```

Çıkmak için `çık`, `exit` veya `quit` yazın ya da `Ctrl+C` tuşlayın.

## Dosyalar

| Dosya | Açıklama |
|---|---|
| `chatbot.py` | Chatbot kodu |
| `requirements.txt` | Gerekli Python paketleri |
| `.env.example` | API anahtarı için örnek dosya |
