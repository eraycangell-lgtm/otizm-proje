import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Gelişimsel Tarama Testi", layout="centered")

# Başlık ve Logo Bölümü
st.title("🧩 Erken Fark Et: Gelişimsel Tarama Aracı")
st.markdown("""
**Hoş Geldiniz.** Bu proje, Adnan Menderes Üniversitesi Özel Eğitim Bölümü öğrencisi tarafından, ailelerin çocuklarındaki gelişimsel riskleri erken fark etmelerine destek olmak amacıyla hazırlanmıştır.
*Uyarı: Bu test kesin tanı koymaz, sadece risk analizi yapar.*
""")

st.write("---")

# SORU VERİTABANI
# Burada her sorunun metni ve hangi cevabın 'Riskli' olduğu tanımlıdır.
sorular = [
    {"soru": "1. Çocuğunuza ismiyle seslendiğinizde dönüp size bakar mı?", "risk_cevabi": "Hayır"},
    {"soru": "2. Sizinle oynarken gözlerinizin içine bakar mı?", "risk_cevabi": "Hayır"},
    {"soru": "3. Siz ona gülümsediğinizde o da size gülümser mi?", "risk_cevabi": "Hayır"},
    {"soru": "4. İstediği bir şeyi parmağıyla işaret ederek gösterir mi?", "risk_cevabi": "Hayır"},
    {"soru": "5. Siz odanın bir köşesine baktığınızda, o da sizin baktığınız yere bakar mı? (Ortak Dikkat)", "risk_cevabi": "Hayır"},
    {"soru": "6. Bir oyuncağı sadece size 'göstermek' için getirdiği olur mu?", "risk_cevabi": "Hayır"},
    {"soru": "7. Oyuncaklarla 'mış gibi' (örneğin muzu telefon yapmak) oyunlar oynar mı?", "risk_cevabi": "Hayır"},
    {"soru": "8. Basit hareketlerinizi (alkış, bay bay) taklit eder mi?", "risk_cevabi": "Hayır"},
    {"soru": "9. Heyecanlandığında ellerini kanat gibi çırpar mı?", "risk_cevabi": "Evet"},  # Dikkat: Burada Evet riskli
    {"soru": "10. Kendi etrafında amaçsızca döner mi?", "risk_cevabi": "Evet"},
    {"soru": "11. Parmaklarını gözünün önünde hareket ettirip onlara dalar mı?", "risk_cevabi": "Evet"},
    {"soru": "12. Eşyaları sıraya dizme veya tekerlek döndürme takıntısı var mı?", "risk_cevabi": "Evet"},
    {"soru": "13. Yüksek seslerden (süpürge, mikser vb.) aşırı rahatsız olur mu?", "risk_cevabi": "Evet"},
    {"soru": "14. Bazen sanki sizi hiç duymuyormuş gibi (sağır şüphesi) davrandığı olur mu?", "risk_cevabi": "Evet"},
    {"soru": "15. Yürürken sık sık parmak uçlarında yürür mü?", "risk_cevabi": "Evet"},
    {"soru": "16. Rutinleri bozulduğunda aşırı tepki verir mi?", "risk_cevabi": "Evet"},
    {"soru": "17. Bir şey istediğinde konuşmak/bakmak yerine elinizden tutup sizi o şeye götürür mü?", "risk_cevabi": "Evet"},
    {"soru": "18. Yabancı ortamlarda içine kapanıp iletişimi tamamen keser mi?", "risk_cevabi": "Evet"},
    {"soru": "19. İşaret etmeden 'Kapıyı kapat' gibi sözlü yönergeleri anlar mı?", "risk_cevabi": "Hayır"},
    {"soru": "20. Diğer çocuklarla oynamaya ilgi gösterir mi?", "risk_cevabi": "Hayır"}
]

# Kullanıcıdan Cevapları Alma
cevaplar = []
risk_puani = 0

with st.form("test_formu"):
    st.header("Lütfen aşağıdaki soruları 'Evet' veya 'Hayır' olarak cevaplayınız.")
    
    for i, item in enumerate(sorular):
        secim = st.radio(item["soru"], options=["Seçiniz...", "Evet", "Hayır"], key=i)
        
        # Risk Hesaplama Mantığı
        if secim != "Seçiniz...":
            if secim == item["risk_cevabi"]:
                risk_puani += 1
            cevaplar.append(secim)
            
    st.write("---")
    gonder_butonu = st.form_submit_button("Testi Tamamla ve Sonucu Gör")

# Sonuç Ekranı
if gonder_butonu:
    if len(cevaplar) < len(sorular):
        st.warning("Lütfen tüm soruları cevaplayınız.")
    else:
        st.subheader("Değerlendirme Sonucu")
        st.write(f"Tespit Edilen Risk Belirtisi Sayısı: **{risk_puani} / {len(sorular)}**")
        
        if risk_puani >= 3:
            st.error("⚠️ **SONUÇ: Yüksek Risk İhtimali**")
            st.write("""
            Çocuğunuzda otizm spektrum bozukluğu ile ilişkilendirilebilecek bazı belirtiler gözlemlenmiştir. 
            Bu bir tanı değildir ancak **vakit kaybetmeden** bir uzmana görünmeniz önerilir.
            
            **Yapmanız Gerekenler:**
            1. En yakın Çocuk ve Ergen Psikiyatristine başvurunuz.
            2. Bulunduğunuz ilçedeki Rehberlik ve Araştırma Merkezi'ne (RAM) danışınız.
            """)
        elif risk_puani >= 1:
            st.warning("⚠️ **SONUÇ: Takip Gerektirir**")
            st.write("Bazı belirtiler riskli olabilir. Çocuğunuzu bir süre daha gözlemleyip emin olamazsanız bir uzmana danışmanız faydalı olacaktır.")
        else:
            st.success("✅ **SONUÇ: Düşük Risk**")
            st.write("Çocuğunuzun gelişimi şu an için yaşının gerektirdiği sosyal ve iletişimsel becerilerle uyumlu görünüyor.")
