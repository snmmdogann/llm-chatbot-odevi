"""
Gemini 2.5 Flash-Lite ile basit, terminalde çalışan bir chatbot (OpenRouter üzerinden).

API anahtarı bu klasördeki .env dosyasındaki OPENROUTER_API_KEY'den okunur.

Çalıştırmak için:
    python chatbot.py

Çıkmak için "çık" yazın (veya Ctrl+C).
"""
from pathlib import Path
import os

from dotenv import load_dotenv
from openai import OpenAI

MODEL = "google/gemini-2.5-flash-lite"

SISTEM_TALIMATI = (
    "Sen yardımsever, kibar ve kısa cevaplar veren bir Türkçe asistansın. "
    "Bilmediğin bir şeyi uydurma, bilmediğini söyle."
)


def main() -> None:
    # Bu dosyanın yanındaki .env dosyasını oku
    load_dotenv(Path(__file__).resolve().parent / ".env")
    anahtar = os.getenv("OPENROUTER_API_KEY")
    if not anahtar or "buraya" in anahtar:
        raise SystemExit(".env dosyasına geçerli bir OPENROUTER_API_KEY yazın.")

    client = OpenAI(api_key=anahtar, base_url="https://openrouter.ai/api/v1", timeout=60)

    # Konuşma geçmişi: her istekte tümü modele gönderilir, böylece bot önceki mesajları hatırlar
    gecmis = [{"role": "system", "content": SISTEM_TALIMATI}]
    toplam_giris = toplam_cikis = 0
    toplam_maliyet = 0.0

    print(f"Chatbot hazır ({MODEL}). Çıkmak için 'çık' yazın.\n")

    while True:
        try:
            mesaj = input("Sen: ").strip()
        except (KeyboardInterrupt, EOFError):
            break
        if not mesaj:
            continue
        if mesaj.lower() in ("çık", "cik", "exit", "quit"):
            break

        gecmis.append({"role": "user", "content": mesaj})
        try:
            yanit = client.chat.completions.create(
                model=MODEL,
                messages=gecmis,
                temperature=0.7,
                max_tokens=800,
                extra_body={"usage": {"include": True}},  # OpenRouter gerçek maliyeti de döndürsün
            )
        except Exception as hata:  # geçersiz anahtar, bakiye (402), hız sınırı (429) vb.
            gecmis.pop()  # başarısız mesajı geçmişten çıkar
            print(f"[hata] {hata}\n")
            continue

        cevap = (yanit.choices[0].message.content or "").strip()
        gecmis.append({"role": "assistant", "content": cevap})
        print(f"Bot: {cevap}\n")

        kullanim = yanit.usage
        if kullanim:
            toplam_giris += kullanim.prompt_tokens or 0
            toplam_cikis += kullanim.completion_tokens or 0
            toplam_maliyet += getattr(kullanim, "cost", None) or 0.0

    print(f"\nGörüşürüz! Toplam: {toplam_giris} giriş + {toplam_cikis} çıkış token, "
          f"maliyet ${toplam_maliyet:.6f}")


if __name__ == "__main__":
    main()
