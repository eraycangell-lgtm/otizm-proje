import streamlit as st
from fpdf import FPDF
import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Gelişimsel Tarama & Erken Tanı", layout="centered")

# --- TÜRKÇE KARAKTER DÜZELTİCİ (PDF İÇİN) ---
# PDF kütüphanesi Türkçe karakterleri basarken hata vermesin diye bu fonksiyonu kullanıyoruz.
def tr_duzelt(text):
    ceviri = str.maketrans("ğĞıİşŞçÇöÖüÜ", "gGiIsScCoOuU")
    return text.translate(ceviri)

# --- GENİŞLETİLMİŞ SORU HAVUZU ---
# min_ay: Soru en az kaç aylık çocuğa sorulmalı?
# max_ay: Soru en fazla kaç aylık çocuğa sorulmalı?
# gorsel: Buraya internetten bulduğun .gif veya .jpg linkini yapıştırabilirsin.
sorular = [
    # --- 0-12 AY (ERKEN BEBEKLİK DÖNEMİ) ---
    {
        "id": 1,
        "soru": "Yüksek bir ses duyduğunda (kapı çarpması gibi) irkilir veya ağlar mı? (İşitme tepkisi)",
        "risk_cevabi": "Hayır",
        "min_ay": 0, "max_ay": 12,
        "gorsel": None
    },
    {
        "id": 2,
        "soru": "Emzirirken veya mama verirken gözlerinizin içine bakar mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 2, "max_ay": 24,
        "gorsel": None
    },
    {
        "id": 3,
        "soru": "Siz ona gülümsediğinizde, o da size gülümseyerek karşılık verir mi?",
        "risk_cevabi": "Hayır",
        "min_ay": 3, "max_ay": 36,
        "gorsel": None
    },
    {
        "id": 4,
        "soru": "Kucağınıza aldığınızda vücudunu aşırı kasma veya bez bebek gibi yığılma durumu olur mu?",
        "risk_cevabi": "Evet",
        "min_ay": 1, "max_ay": 24,
        "gorsel": None
    },
    {
        "id": 5,
        "soru": "İnsan yüzlerine bakmak yerine, sürekli tavandaki ışığa veya dönen pervaneye mi odaklanıyor?",
        "risk_cevabi": "Evet",
        "min_ay": 4, "max_ay": 36,
        "gorsel": None
    },
    {
        "id": 6,
        "soru": "'Agu', 'buu' gibi sesler çıkararak sizinle karşılıklı sesli iletişim kurmaya çalışır mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 6, "max_ay": 24,
        "gorsel": None
    },
    {
        "id": 7,
        "soru": "Kucağa alınmak istediğinde kollarını size doğru uzatır mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 7, "max_ay": 36,
        "gorsel": None
    },
    {
        "id": 8,
        "soru": "'Ce-eee' (Peek-a-boo) gibi oyunlar oynadığınızda keyif alır ve katılır mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 9, "max_ay": 36,
        "gorsel": None
    },

    # --- 12-24 AY (KRİTİK SOSYAL GELİŞİM) ---
    {
        "id": 9,
        "soru": "İsmiyle seslendiğinizde (başka bir şeyle meşgul olsa bile) dönüp size bakar mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 12, "max_ay": 72,
        "gorsel": None
    },
    {
        "id": 10,
        "soru": "İstediği bir oyuncağı parmağıyla işaret ederek gösterir mi? (İşaret etme)",
        "risk_cevabi": "Hayır",
        "min_ay": 14, "max_ay": 72,
        "gorsel": None # Buraya işaret eden bebek GIF'i koyabilirsin
    },
    {
        "id": 11,
        "soru": "Siz odanın bir köşesine baktığınızda, o da sizin baktığınız yere bakar mı? (Ortak Dikkat)",
        "risk_cevabi": "Hayır",
        "min_ay": 14, "max_ay": 72,
        "gorsel": None
    },
    {
        "id": 12,
        "soru": "Bir nesneyi sadece size 'göstermek' ve ilgisini paylaşmak için getirdiği olur mu?",
        "risk_cevabi": "Hayır",
        "min_ay": 15, "max_ay": 72,
        "gorsel": None
    },
    {
        "id": 13,
        "soru": "Bay-bay yapma, alkışlama, öpücük atma gibi hareketleri taklit eder mi?",
        "risk_cevabi": "Hayır",
        "min_ay": 12, "max_ay": 48,
        "gorsel": None
    },
    {
        "id": 14,
        "soru": "Oyuncak arabayı sürmek yerine sadece tekerleklerini döndürmekle ilgilenir mi?",
        "risk_cevabi": "Evet",
        "min_ay": 18, "max_ay": 72,
        "gorsel": None
    },

    # --- 24+ AY (STEREOTİPİ VE İLERİ BECERİLER) ---
    {
        "id": 15,
        "soru": "Heyecanlandığında veya boş kaldığında ellerini kanat gibi çırpar mı?",
        "risk_cevabi": "Evet",
        "min_ay": 18, "max_ay": 72,
        "gorsel": None # Buraya el çırpma GIF'i koyabilirsin
    },
    {
        "id": 16,
        "soru": "Kendi etrafında amaçsızca defalarca döner mi?",
        "risk_cevabi": "Evet",
        "min_ay": 18, "max_ay": 72,
        "gorsel": None
    },
    {
        "id": 17,
        "soru": "Parmak ucunda yürüme davranışı var mı?",
        "risk_cevabi": "Evet",
        "min_ay": 24, "max_ay": 72,
        "gorsel": None
    },
    {
        "id": 18,
        "soru": "Oyuncakları veya ev eşyalarını yan yana/üst üste dizme takıntısı var mı?",
        "risk_cevabi": "Evet",
        "min_ay": 24, "max_ay": 72,
        "gorsel": None
    },
    {
        "id": 19,
        "soru": "Yüksek seslerden (süpürge, mikser vb.) aşırı korkup kulaklarını kapatır mı?",
        "risk_cevabi": "Evet",
        "min_ay": 24, "max_ay": 72,
        "gorsel": None
    },
    {
        "id": 20,
        "soru": "Oyuncaklarla 'mış gibi' (muzdan telefon yapmak, bebeğe yemek yedirmek) oyunlar kurar mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 24, "max_ay": 72,
        "gorsel": None
    },
    {
        "id": 21,
        "soru": "Diğer çocuklara ilgi gösterir mi, onlarla oynamak ister mi?",
        "risk_cevabi": "Hayır",
        "min_ay": 36, "max_ay": 72,
        "gorsel": None
    },
    {
        "id": 22,
        "soru": "Rutinleri bozulduğunda (örneğin markete farklı yoldan gitmek) aşırı öfke nöbeti geçirir mi?",
        "risk_cevabi": "Evet",
        "min_ay": 36, "max_ay": 72,
        "gorsel": None
    },
    {
        "id": 23,
        "soru": "Konuşması yaşıtlarına göre belirgin derecede geride mi?",
        "risk_cevabi": "Evet",
        "min_ay": 24, "max_ay": 72,
        "gorsel": None
    },
    {
        "id": 24,
        "soru": "Söylediklerinizi veya reklamlardaki sözleri anlamsızca tekrar eder mi? (Ekolali)",
        "risk_cevabi": "Evet",
        "min_ay": 30, "max_ay": 72,
        "gorsel": None
    },
    {
        "id": 25,
        "soru": "Parmaklarını gözünün hemen önünde hareket ettirip onlara dalar mı?",
        "risk_cevabi": "Evet",
        "min_ay": 18, "max_ay": 72,
        "gorsel": None
    }
]

# --- ARAYÜZ (FRONTEND) ---
st.title("🧩 Erken Tanı ve Gelişim Takip Sistemi")
st.markdown("**Adnan Menderes Üniversitesi - Özel Eğitim Bölümü Projesi**")
st.info("Bu sistem, ailelerin çocuklarında gözlemledikleri gelişimsel riskleri erken fark etmeleri için tasarlanmış bir ön tarama aracıdır.")

# Yan Menü (Sidebar)
st.sidebar.header("Çocuk Bilgileri")
st.sidebar.write("Lütfen çocuğunuzun ayını giriniz.")
cocuk_ay = st.sidebar.number_input("Ay:", min_value=0, max_value=72, value=12, step=1)
st.sidebar.write(f"Seçilen: **{cocuk_ay} Aylık**")

# --- SORU FİLTRELEME MANTIĞI ---
# Çocuğun yaşına uygun (min_ay ve max_ay aralığındaki) soruları seç
filtrelenmis_sorular = [s for s in sorular if s["min_ay"] <= cocuk_ay <= s["max_ay"]]

if not filtrelenmis_sorular:
    st.warning("Bu yaş grubu için henüz yeterli soru girişi yapılmamıştır.")
else:
    st.success(f"Çocuğunuzun yaşına ({cocuk_ay} ay) uygun **{len(filtrelenmis_sorular)} adet** kontrol sorusu listelendi.")
    st.write("---")

    # --- FORM BAŞLANGICI ---
    cevaplar = {}
    with st.form("tarama_formu"):
        
        for soru in filtrelenmis_sorular:
            st.subheader(soru["soru"])
            
            # Eğer soruda görsel linki varsa göster
            if soru["gorsel"]:
                try:
                    st.image(soru["gorsel"], caption="Örnek Gösterim", width=300)
                except:
                    pass # Link bozuksa hata verme, geç
            
            # Evet/Hayır Seçenekleri
            secim = st.radio("Bu davranışı gözlemliyor musunuz?", ["Seçiniz...", "Evet", "Hayır"], key=soru["id"])
            cevaplar[soru["id"]] = secim
            st.markdown("---")
        
        gonder_butonu = st.form_submit_button("Analizi Tamamla ve Raporla")

    # --- SONUÇ HESAPLAMA VE RAPORLAMA ---
    if gonder_butonu:
        # 1. Boş Cevap Kontrolü
        if "Seçiniz..." in cevaplar.values():
            st.error("Lütfen tüm soruları cevaplayınız. Eksik cevaplar analizi etkileyebilir.")
        else:
            # 2. Risk Hesaplama
            risk_puani = 0
            riskli_maddeler = []

            for s in filtrelenmis_sorular:
                verilen_cevap = cevaplar[s["id"]]
                if verilen_cevap == s["risk_cevabi"]:
                    risk_puani += 1
                    riskli_maddeler.append(s["soru"])
            
            # 3. Ekrana Sonuç Yazdırma
            st.header("Değerlendirme Sonucu")
            
            if risk_puani >= 3:
                st.error(f"⚠️ **YÜKSEK RİSK BELİRTİSİ ({risk_puani} Madde)**")
                st.write("Çocuğunuzda otizm spektrum bozukluğu veya gelişimsel gecikme ile ilişkilendirilebilecek çok sayıda belirti gözlemlendi.")
                st.write("**Öneri:** Vakit kaybetmeden bir Çocuk Psikiyatristine başvurunuz.")
            elif risk_puani >= 1:
                st.warning(f"⚠️ **DİKKAT VE TAKİP GEREKTİRİR ({risk_puani} Madde)**")
                st.write("Bazı riskli belirtiler mevcut. Çocuğunuzu daha dikkatli gözlemleyin ve şüpheleriniz devam ederse bir uzmana danışın.")
            else:
                st.success("✅ **DÜŞÜK RİSK (Gelişim Normal)**")
                st.write("Çocuğunuzun gelişimi şu an için yaşıyla uyumlu görünüyor.")

            # 4. PDF Rapor Oluşturma
            pdf = FPDF()
            pdf.add_page()
            
            # PDF Başlıkları
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, txt=tr_duzelt("GELISIMSEL TARAMA RAPORU"), ln=1, align='C')
            
            pdf.set_font("Arial", size=10)
            pdf.cell(190, 10, txt=tr_duzelt(f"Tarih: {datetime.datetime.now().strftime('%d-%m-%Y')}"), ln=1, align='R')
            pdf.cell(190, 10, txt=tr_duzelt(f"Cocuk Yasi: {cocuk_ay} Ay"), ln=1, align='L')
            
            pdf.ln(10)
            
            # PDF Sonuç
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(190, 10, txt=tr_duzelt(f"Tespit Edilen Risk Sayisi: {risk_puani}"), ln=1, align='L')
            
            pdf.ln(5)
            pdf.set_font("Arial", size=11)
            pdf.cell(190, 10, txt=tr_duzelt("Riskli Bulunan Maddeler:"), ln=1)
            
            # Riskli maddeleri listele
            pdf.set_font("Arial", size=10)
            if len(riskli_maddeler) > 0:
                for madde in riskli_maddeler:
                    pdf.cell(10) # Boşluk
                    pdf.multi_cell(180, 8, txt=f"- {tr_duzelt(madde)}")
            else:
                pdf.cell(10)
                pdf.cell(180, 10, txt=tr_duzelt("- Herhangi bir risk belirtisine rastlanmamistir."), ln=1)
            
            pdf.ln(20)
            pdf.set_font("Arial", 'I', 8)
            pdf.multi_cell(190, 5, txt=tr_duzelt("NOT: Bu belge tibbi bir tani degildir. Adnan Menderes Universitesi Ozel Egitim Bolumu ogrenci projesi kapsaminda on degerlendirme amaciyla olusturulmustur."))

            # PDF İndirme Butonu
            pdf_cikti = pdf.output(dest='S').encode('latin-1')
            st.download_button(
                label="📄 Sonuç Raporunu İndir (PDF)",
                data=pdf_cikti,
                file_name="Gelisim_Tarama_Raporu.pdf",
                mime="application/pdf"
            )
