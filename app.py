import streamlit as st
from fpdf import FPDF
import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Gelişimsel Tarama & Erken Tanı", layout="centered")

# --- TÜRKÇE KARAKTER DÜZELTİCİ (PDF İÇİN) ---
def tr_duzelt(text):
    """PDF oluştururken Türkçe karakter sorununu çözer."""
    ceviri = str.maketrans("ğĞıİşŞçÇöÖüÜ", "gGiIsScCoOuU")
    return text.translate(ceviri)

# --- SORU VE GÖRSEL VERİTABANI ---
# Şu an görseller için 'placehold.co' kullanarak geçici resimler atadım.
# Sen gerçek GIF'leri buldukça bu linkleri değiştirebilirsin.
sorular = [
    # --- 0-12 AY (ERKEN BEBEKLİK) ---
    {
        "id": 1,
        "soru": "Yüksek bir ses duyduğunda (kapı çarpması gibi) irkilir veya ağlar mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 0, "max_ay": 12,
        "gorsel": "https://placehold.co/600x400/png?text=Bebek+Isitme+Refleksi+(GIF)"
    },
    {
        "id": 2,
        "soru": "Emzirirken veya mama verirken gözlerinizin içine bakar mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 2, "max_ay": 24,
        "gorsel": "https://placehold.co/600x400/png?text=Goz+Temasi+Kuran+Bebek"
    },
    {
        "id": 3,
        "soru": "Siz ona gülümsediğinizde, o da size gülümseyerek karşılık verir mi?",
        "risk_cevabi": "Hayır",
        "min_ay": 3, "max_ay": 36,
        "gorsel": "https://placehold.co/600x400/png?text=Sosyal+Gulumseme"
    },
    {
        "id": 4,
        "soru": "Kucağınıza aldığınızda vücudunu aşırı kasma veya bez bebek gibi yığılma durumu olur mu?",
        "risk_cevabi": "Evet",
        "min_ay": 1, "max_ay": 24,
        "gorsel": "https://placehold.co/600x400/png?text=Vucut+Kasilmasi+(Hipotoni)"
    },
    {
        "id": 5,
        "soru": "İnsan yüzlerine bakmak yerine, sürekli tavandaki ışığa veya dönen pervaneye mi odaklanıyor?",
        "risk_cevabi": "Evet",
        "min_ay": 4, "max_ay": 36,
        "gorsel": "https://placehold.co/600x400/png?text=Isiga+Odaklanma"
    },
    {
        "id": 6,
        "soru": "'Agu', 'buu' gibi sesler çıkararak sizinle karşılıklı sesli iletişim kurmaya çalışır mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 6, "max_ay": 24,
        "gorsel": "https://placehold.co/600x400/png?text=Bebek+Mirladanmasi+(Babbling)"
    },
    {
        "id": 7,
        "soru": "Kucağa alınmak istediğinde kollarını size doğru uzatır mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 7, "max_ay": 36,
        "gorsel": "https://placehold.co/600x400/png?text=Kucaga+Alma+Tepkisi"
    },
    {
        "id": 8,
        "soru": "'Ce-eee' (Peek-a-boo) gibi oyunlar oynadığınızda keyif alır ve katılır mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 9, "max_ay": 36,
        "gorsel": "https://placehold.co/600x400/png?text=Ce-eee+Oyunu"
    },

    # --- 12-24 AY (KRİTİK SOSYAL GELİŞİM) ---
    {
        "id": 9,
        "soru": "İsmiyle seslendiğinizde (başka bir şeyle meşgul olsa bile) dönüp size bakar mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 12, "max_ay": 72,
        "gorsel": "https://placehold.co/600x400/png?text=Isme+Tepki"
    },
    {
        "id": 10,
        "soru": "İstediği bir oyuncağı parmağıyla işaret ederek gösterir mi? (İşaret etme)",
        "risk_cevabi": "Hayır",
        "min_ay": 14, "max_ay": 72,
        "gorsel": "https://placehold.co/600x400/png?text=Isaret+Etme+(Pointing)"
    },
    {
        "id": 11,
        "soru": "Siz odanın bir köşesine baktığınızda, o da sizin baktığınız yere bakar mı? (Ortak Dikkat)",
        "risk_cevabi": "Hayır",
        "min_ay": 14, "max_ay": 72,
        "gorsel": "https://placehold.co/600x400/png?text=Ortak+Dikkat"
    },
    {
        "id": 12,
        "soru": "Bir nesneyi sadece size 'göstermek' ve ilgisini paylaşmak için getirdiği olur mu?",
        "risk_cevabi": "Hayır",
        "min_ay": 15, "max_ay": 72,
        "gorsel": "https://placehold.co/600x400/png?text=Oyuncak+Gosterme"
    },
    {
        "id": 13,
        "soru": "Bay-bay yapma, alkışlama, öpücük atma gibi hareketleri taklit eder mi?",
        "risk_cevabi": "Hayır",
        "min_ay": 12, "max_ay": 48,
        "gorsel": "https://placehold.co/600x400/png?text=Taklit+Becerisi"
    },
    {
        "id": 14,
        "soru": "Oyuncak arabayı sürmek yerine sadece tekerleklerini döndürmekle ilgilenir mi?",
        "risk_cevabi": "Evet",
        "min_ay": 18, "max_ay": 72,
        "gorsel": "https://placehold.co/600x400/png?text=Tekerlek+Dondurme"
    },

    # --- 24+ AY (STEREOTİPİ VE İLERİ BECERİLER) ---
    {
        "id": 15,
        "soru": "Heyecanlandığında veya boş kaldığında ellerini kanat gibi çırpar mı?",
        "risk_cevabi": "Evet",
        "min_ay": 18, "max_ay": 72,
        "gorsel": "https://placehold.co/600x400/png?text=El+Cirpma+(Hand+Flapping)"
    },
    {
        "id": 16,
        "soru": "Kendi etrafında amaçsızca defalarca döner mi?",
        "risk_cevabi": "Evet",
        "min_ay": 18, "max_ay": 72,
        "gorsel": "https://placehold.co/600x400/png?text=Kendi+Etrafinda+Donme"
    },
    {
        "id": 17,
        "soru": "Parmak ucunda yürüme davranışı var mı?",
        "risk_cevabi": "Evet",
        "min_ay": 24, "max_ay": 72,
        "gorsel": "https://placehold.co/600x400/png?text=Parmak+Ucu+Yurume"
    },
    {
        "id": 18,
        "soru": "Oyuncakları veya ev eşyalarını yan yana/üst üste dizme takıntısı var mı?",
        "risk_cevabi": "Evet",
        "min_ay": 24, "max_ay": 72,
        "gorsel": "https://placehold.co/600x400/png?text=Esyalari+Dizme"
    },
    {
        "id": 19,
        "soru": "Yüksek seslerden (süpürge, mikser vb.) aşırı korkup kulaklarını kapatır mı?",
        "risk_cevabi": "Evet",
        "min_ay": 24, "max_ay": 72,
        "gorsel": "https://placehold.co/600x400/png?text=Kulaklarini+Kapatma"
    },
    {
        "id": 20,
        "soru": "Oyuncaklarla 'mış gibi' (muzdan telefon yapmak, bebeğe yemek yedirmek) oyunlar kurar mı?",
        "risk_cevabi": "Hayır",
        "min_ay": 24, "max_ay": 72,
        "gorsel": "https://placehold.co/600x400/png?text=Sembolik+Oyun"
    },
    {
        "id": 21,
        "soru": "Diğer çocuklara ilgi gösterir mi, onlarla oynamak ister mi?",
        "risk_cevabi": "Hayır",
        "min_ay": 36, "max_ay": 72,
        "gorsel": "https://placehold.co/600x400/png?text=Akran+Iletisimi"
    },
    {
        "id": 22,
        "soru": "Rutinleri bozulduğunda (örneğin markete farklı yoldan gitmek) aşırı öfke nöbeti geçirir mi?",
        "risk_cevabi": "Evet",
        "min_ay": 36, "max_ay": 72,
        "gorsel": "https://placehold.co/600x400/png?text=Rutine+Baglilik"
    },
    {
        "id": 23,
        "soru": "Konuşması yaşıtlarına göre belirgin derecede geride mi?",
        "risk_cevabi": "Evet",
        "min_ay": 24, "max_ay": 72,
        "gorsel": "https://placehold.co/600x400/png?text=Konusma+Gecikmesi"
    },
    {
        "id": 24,
        "soru": "Söylediklerinizi veya reklamlardaki sözleri anlamsızca tekrar eder mi? (Ekolali)",
        "risk_cevabi": "Evet",
        "min_ay": 30, "max_ay": 72,
        "gorsel": "https://placehold.co/600x400/png?text=Ekolali+(Tekrar)"
    },
    {
        "id": 25,
        "soru": "Parmaklarını gözünün hemen önünde hareket ettirip onlara dalar mı?",
        "risk_cevabi": "Evet",
        "min_ay": 18, "max_ay": 72,
        "gorsel": "https://placehold.co/600x400/png?text=Gorsel+Takinti"
    }
]

# --- YAN MENÜ (SIDEBAR) ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/tr/6/62/Adnan_Menderes_%C3%9Cniversitesi_logo.png", width=100)
st.sidebar.title("Çocuk Bilgileri")
st.sidebar.info("Lütfen çocuğunuzun ayını giriniz. Sistem sadece o yaş grubuna uygun soruları getirecektir.")

cocuk_ay = st.sidebar.number_input("Ay:", min_value=0, max_value=72, value=24, step=1)
st.sidebar.write(f"Seçilen Yaş: **{cocuk_ay} Aylık**")

st.sidebar.markdown("---")
st.sidebar.markdown("**Hazırlayan:**\n\nAdnan Menderes Üniversitesi\nÖzel Eğitim Bölümü Öğrencisi Eray CANGEL")

# --- ANA EKRAN (HEADER) ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/tr/6/62/Adnan_Menderes_%C3%9Cniversitesi_logo.png", width=80)
with col2:
    st.title("Gelişimsel Tarama Sistemi")
    st.markdown("**Erken Tanı ve Farkındalık Aracı**")

st.markdown("---")

# --- FİLTRELEME VE FORM ---
filtrelenmis_sorular = [s for s in sorular if s["min_ay"] <= cocuk_ay <= s["max_ay"]]

if not filtrelenmis_sorular:
    st.warning("Bu yaş grubu için tanımlı soru bulunamadı.")
else:
    st.success(f"Çocuğunuzun yaşına ({cocuk_ay} Ay) uygun **{len(filtrelenmis_sorular)} adet** gelişim sorusu listelendi.")
    
    cevaplar = {}
    with st.form("tarama_formu"):
        for soru in filtrelenmis_sorular:
            st.subheader(soru["soru"])
            
            # Görsel Gösterimi
            if soru["gorsel"]:
                st.image(soru["gorsel"], caption="Örnek Gösterim", width=400)
            
            # Soru Seçenekleri
            secim = st.radio("Gözlemliyor musunuz?", ["Seçiniz...", "Evet", "Hayır"], key=soru["id"])
            cevaplar[soru["id"]] = secim
            st.markdown("---")
        
        gonder_butonu = st.form_submit_button("Analizi Tamamla ve Raporla")

    # --- SONUÇ HESAPLAMA ---
    if gonder_butonu:
        if "Seçiniz..." in cevaplar.values():
            st.error("Lütfen tüm soruları cevaplayınız.")
        else:
            risk_puani = 0
            riskli_maddeler = []

            for s in filtrelenmis_sorular:
                verilen_cevap = cevaplar[s["id"]]
                if verilen_cevap == s["risk_cevabi"]:
                    risk_puani += 1
                    riskli_maddeler.append(s["soru"])

            # Sonuç Ekranı
            st.header("Değerlendirme Sonucu")
            
            if risk_puani >= 3:
                st.error(f"⚠️ **YÜKSEK RİSK ({risk_puani} Belirti)**")
                st.write("Çocuğunuzda otizm spektrum bozukluğu veya gelişimsel gecikme ile ilişkilendirilebilecek çok sayıda belirti gözlemlendi. Vakit kaybetmeden bir uzmana başvurunuz.")
            elif risk_puani >= 1:
                st.warning(f"⚠️ **TAKİP GEREKTİRİR ({risk_puani} Belirti)**")
                st.write("Bazı riskli belirtiler var. Çocuğunuzu gözlemlemeye devam ediniz.")
            else:
                st.success("✅ **DÜŞÜK RİSK**")
                st.write("Gelişim yaşıyla uyumlu görünüyor.")

            # --- PDF RAPOR OLUŞTURMA ---
            pdf = FPDF()
            pdf.add_page()
            
            # Başlık
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, txt=tr_duzelt("GELISIMSEL TARAMA ON RAPORU"), ln=1, align='C')
            
            pdf.set_font("Arial", size=10)
            pdf.cell(190, 10, txt=tr_duzelt(f"Tarih: {datetime.datetime.now().strftime('%d-%m-%Y')}"), ln=1, align='R')
            pdf.cell(190, 10, txt=tr_duzelt(f"Cocuk Yasi: {cocuk_ay} Ay"), ln=1, align='L')
            
            pdf.ln(10)
            
            # Risk Listesi
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(190, 10, txt=tr_duzelt(f"Tespit Edilen Risk Sayisi: {risk_puani}"), ln=1, align='L')
            
            pdf.ln(5)
            pdf.set_font("Arial", size=11)
            pdf.cell(190, 10, txt=tr_duzelt("Riskli Bulunan Maddeler:"), ln=1)
            
            pdf.set_font("Arial", size=10)
            if len(riskli_maddeler) > 0:
                for madde in riskli_maddeler:
                    pdf.cell(10)
                    pdf.multi_cell(180, 8, txt=f"- {tr_duzelt(madde)}")
            else:
                pdf.cell(10)
                pdf.cell(180, 10, txt=tr_duzelt("- Risk belirtisine rastlanmamistir."), ln=1)
                
            pdf.ln(20)
            pdf.set_font("Arial", 'I', 8)
            pdf.multi_cell(190, 5, txt=tr_duzelt("NOT: Bu belge tibbi bir tani degildir. Adnan Menderes Universitesi Ozel Egitim Bolumu ogrenci projesi kapsaminda olusturulmustur."))

            pdf_cikti = pdf.output(dest='S').encode('latin-1')
            
            st.download_button(
                label="📄 Sonuç Raporunu İndir (PDF)",
                data=pdf_cikti,
                file_name="Gelisim_Raporu.pdf",
                mime="application/pdf"
            )
