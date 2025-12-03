import streamlit as st
from fpdf import FPDF
import datetime

# --- AYARLAR ---
st.set_page_config(page_title="Gelişimsel Tarama Projesi", layout="centered")

# --- TÜRKÇE KARAKTER DÜZELTİCİ (PDF İÇİN) ---
# FPDF kütüphanesi standart fontlarla Türkçe karakterleri bazen bozuk basabilir.
# Bu fonksiyon, PDF basılırken karakterleri düzeltir.
def tr_duzelt(text):
    ceviri = str.maketrans("ğĞıİşŞçÇöÖüÜ", "gGiIsScCoOuU")
    return text.translate(ceviri)

# --- SORU VERİTABANI (Resim ve Yaş Bilgisi Eklendi) ---
# min_ay: Soru en az kaç aylık çocuğa sorulmalı?
# max_ay: Soru en fazla kaç aylık çocuğa sorulmalı?
# gorsel: Buraya internetten bulduğun GIF veya Resim linkini yapıştıracaksın.
sorular = [
    {
        "id": 1,
        "soru": "İsmiyle seslendiğinizde dönüp size bakar mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 6, "max_ay": 60,
        "gorsel": None # Örnek: "https://ornek.com/resim1.jpg"
    },
    {
        "id": 2,
        "soru": "Sizinle oynarken gözlerinizin içine bakar mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 0, "max_ay": 60,
        "gorsel": None
    },
    {
        "id": 3,
        "soru": "İstediği bir şeyi parmağıyla işaret ederek gösterir mi?",
        "risk_cevabi": "Hayır",
        "min_ay": 9, "max_ay": 60,
        "gorsel": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDExbnhwMnZ4bzFzbnhwMnZ4bzFzbnhwMnZ4bzFzbnhwMnZ4bzFzbnhwMnZ4byZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKSjRrfIPjeiVyM/giphy.gif" # Örnek GIF
    },
    {
        "id": 4,
        "soru": "Siz bir yere baktığınızda o da sizin baktığınız yöne bakar mı? (Ortak Dikkat)",
        "risk_cevabi": "Hayır",
        "min_ay": 9, "max_ay": 60,
        "gorsel": None
    },
    {
        "id": 5,
        "soru": "Heyecanlandığında ellerini kanat gibi çırpar mı?",
        "risk_cevabi": "Evet",
        "min_ay": 12, "max_ay": 60,
        "gorsel": None
    },
    {
        "id": 6,
        "soru": "Kendi etrafında amaçsızca döner mi?",
        "risk_cevabi": "Evet",
        "min_ay": 18, "max_ay": 60,
        "gorsel": None
    },
    {
        "id": 7,
        "soru": "Parmak ucunda yürüme davranışı var mı?",
        "risk_cevabi": "Evet",
        "min_ay": 24, "max_ay": 60,
        "gorsel": None
    },
    {
        "id": 8,
        "soru": "Oyuncağıyla amacına uygun oynamak yerine tekerleklerini döndürür mü?",
        "risk_cevabi": "Evet",
        "min_ay": 18, "max_ay": 60,
        "gorsel": None
    },
    {
        "id": 9,
        "soru": "Basit taklit becerileri (alkış, bay bay) var mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 9, "max_ay": 36,
        "gorsel": None
    },
    {
        "id": 10,
        "soru": "Oyuncaklarla 'evcilik' gibi -mış gibi oyunlar oynar mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 24, "max_ay": 60,
        "gorsel": None
    }
    # Buraya daha fazla soru ekleyebilirsin...
]

# --- BAŞLIK VE GİRİŞ ---
st.title("🧩 Gelişimsel Takip Sistemi")
st.markdown("Adnan Menderes Üniversitesi - Özel Eğitim Projesi")
st.info("Bu sistem, çocuğunuzun ayına uygun soruları seçerek gelişimsel riskleri analiz eder ve doktorunuz için bir ön rapor oluşturur.")

# --- ÖZELLİK 3: YAŞA GÖRE FİLTRELEME ---
st.sidebar.header("Çocuk Bilgileri")
cocuk_ay = st.sidebar.number_input("Çocuğunuz kaç aylık?", min_value=0, max_value=72, value=24)
st.sidebar.write(f"Seçilen yaş: **{cocuk_ay} Aylık**")

# Soruları yaşa göre filtrele
filtrelenmis_sorular = [s for s in sorular if s["min_ay"] <= cocuk_ay <= s["max_ay"]]

if len(filtrelenmis_sorular) == 0:
    st.warning("Bu yaş grubu için tanımlı soru bulunamadı.")
else:
    st.write(f"Çocuğunuzun yaşına uygun **{len(filtrelenmis_sorular)} adet** soru listelendi.")
    st.write("---")

    # --- FORM BAŞLANGICI ---
    cevaplar = {}
    with st.form("tarama_formu"):
        
        for soru_data in filtrelenmis_sorular:
            st.subheader(f"Soru: {soru_data['soru']}")
            
            # --- ÖZELLİK 1: GÖRSEL DESTEK ---
            if soru_data["gorsel"]:
                st.image(soru_data["gorsel"], caption="Örnek Davranış", width=300)
            
            # Soru Seçenekleri
            secim = st.radio("Cevabınız:", ["Seçiniz...", "Evet", "Hayır"], key=soru_data["id"])
            cevaplar[soru_data["id"]] = secim
            st.markdown("---")
        
        gonder = st.form_submit_button("Analizi Tamamla")

    # --- SONUÇ VE RAPORLAMA ---
    if gonder:
        # Boş cevap kontrolü
        if "Seçiniz..." in cevaplar.values():
            st.error("Lütfen tüm soruları cevaplayınız.")
        else:
            risk_sayisi = 0
            riskli_maddeler = []

            for s in filtrelenmis_sorular:
                kullanici_cevabi = cevaplar[s["id"]]
                if kullanici_cevabi == s["risk_cevabi"]:
                    risk_sayisi += 1
                    riskli_maddeler.append(s["soru"])

            # Ekrana Yazdırma
            if risk_sayisi >= 3:
                st.error(f"⚠️ **Yüksek Risk:** Toplam {risk_sayisi} belirti tespit edildi.")
                st.write("Bir çocuk psikiyatristine başvurmanız önerilir.")
            elif risk_sayisi >= 1:
                st.warning(f"⚠️ **Takip Önerilir:** Toplam {risk_sayisi} belirti tespit edildi.")
            else:
                st.success("✅ **Düşük Risk:** Gelişim yaşıyla uyumlu görünüyor.")

            # --- ÖZELLİK 2: PDF RAPOR OLUŞTURMA ---
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            # Başlık
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt=tr_duzelt("GELISIMSEL TARAMA ON RAPORU"), ln=1, align='C')
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 10, txt=tr_duzelt(f"Tarih: {datetime.datetime.now().strftime('%d-%m-%Y')}"), ln=1, align='R')
            pdf.cell(200, 10, txt=tr_duzelt(f"Cocuk Yasi: {cocuk_ay} Ay"), ln=1, align='L')
            
            pdf.ln(10) # Boşluk
            
            # Sonuçlar
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt=tr_duzelt(f"Toplam Risk Puani: {risk_sayisi}"), ln=1, align='L')
            
            pdf.ln(5)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 10, txt=tr_duzelt("Tespit Edilen Riskli Maddeler:"))
            
            if len(riskli_maddeler) > 0:
                for madde in riskli_maddeler:
                    pdf.cell(10) # Girinti
                    pdf.cell(0, 10, txt=f"- {tr_duzelt(madde)}", ln=1)
            else:
                pdf.cell(10)
                pdf.cell(0, 10, txt=tr_duzelt("- Herhangi bir risk belirtisine rastlanmamistir."), ln=1)
                
            pdf.ln(20)
            pdf.set_font("Arial", 'I', 8)
            pdf.multi_cell(0, 5, txt=tr_duzelt("Bu rapor tibbi bir tani degildir. Adnan Menderes Universitesi Ozel Egitim Projesi kapsaminda olusturulmustur."))

            # PDF Çıktısı
            pdf_dosyasi = pdf.output(dest='S').encode('latin-1')
            
            st.download_button(
                label="📄 Doktor İçin Raporu İndir (PDF)",
                data=pdf_dosyasi,
                file_name="Gelisim_Raporu.pdf",
                mime="application/pdf"
            )
