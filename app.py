import streamlit as st
import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt

# ================= LOAD MODEL =================
model_path = 'NOTEBOOK/model_diabetes.pkl'

if os.path.exists(model_path):
    model = pickle.load(open(model_path, 'rb'))
else:
    st.error("❌ Model tidak ditemukan!")
    st.stop()

# ================= CONFIG =================
# layout="centered" lebih responsif di HP dibanding "wide"
st.set_page_config(
    page_title="Early Diabetes Screening",
    page_icon="🩺",
    layout="centered"
)

# ================= RESPONSIVE STYLE =================
st.markdown("""
<style>

/* ============================================
   RESPONSIVE BASE — berlaku semua ukuran layar
   ============================================ */

/* Konten utama selalu 100% lebar kontainer */
.block-container {
    padding: 1.5rem 1rem 2rem 1rem !important;
    max-width: 860px !important;
}

/* ===== SIDEBAR PINK ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8a4c8 0%, #f472b6 50%, #ec4899 100%);
    padding: 20px 10px;
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background-color: rgba(255,255,255,0.25) !important;
    border: 1px solid rgba(255,255,255,0.5) !important;
    border-radius: 8px !important;
    color: white !important;
}

/* ===== SIDEBAR LOGO ===== */
.sidebar-logo { text-align: center; padding: 20px 0 30px 0; }
.sidebar-logo .icon { font-size: 48px; display: block; margin-bottom: 8px; }
.sidebar-logo h2 {
    color: white !important; font-size: 16px;
    font-weight: 800; margin: 0; line-height: 1.3;
}
.sidebar-logo p { color: rgba(255,255,255,0.85) !important; font-size: 11px; margin-top: 6px; }
.sidebar-divider { border: none; border-top: 1px solid rgba(255,255,255,0.4); margin: 16px 0; }

/* ===== BACKGROUND ===== */
[data-testid="stAppViewContainer"] > .main { background-color: #f9fafb; }

/* ===== TOMBOL — lebar penuh di semua layar ===== */
.stButton > button {
    width: 100% !important;
    height: 50px;
    border-radius: 12px;
    font-weight: bold;
    font-size: 16px;
    background: linear-gradient(135deg, #f472b6, #ec4899);
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(236,72,153,0.35);
    transition: all 0.2s ease;
    touch-action: manipulation;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #ec4899, #db2777);
    transform: translateY(-1px);
}
.stButton > button:active { transform: translateY(0px); }

/* ===== CARD ===== */
.home-card {
    background: white;
    border-radius: 16px;
    padding: 20px 22px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    margin-bottom: 16px;
}
.input-card {
    background: white;
    border-radius: 16px;
    padding: 20px 22px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    margin-bottom: 16px;
}

/* ===== FEATURE LIST ===== */
.feature-item {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 0; border-bottom: 1px solid #f3f4f6;
    font-size: 14px; color: #374151;
}
.feature-icon { font-size: 20px; width: 32px; text-align: center; }

/* ===== DISCLAIMER ===== */
.disclaimer-box {
    background-color: #fff7ed;
    border-left: 5px solid #f97316;
    border-radius: 0 10px 10px 0;
    padding: 14px 16px;
    margin-top: 16px;
    font-size: 14px;
    color: #92400e;
    line-height: 1.6;
}
.disclaimer-box strong { color: #c2410c; }

/* ===== INPUT FIELD ===== */
.stNumberInput input, .stSelectbox > div > div {
    border-radius: 8px !important;
    border: 1.5px solid #f9a8d4 !important;
    font-size: 15px !important;
    min-height: 42px !important;
}
.stNumberInput input:focus {
    border-color: #ec4899 !important;
    box-shadow: 0 0 0 2px rgba(236,72,153,0.15) !important;
}

/* ===== JUDUL — otomatis menyesuaikan lebar layar ===== */
.page-title {
    font-size: clamp(20px, 5vw, 28px);
    color: #db2777;
    font-weight: 800;
    margin-bottom: 4px;
}
.page-subtitle {
    font-size: clamp(12px, 3vw, 14px);
    color: #6b7280;
    margin-bottom: 20px;
}

/* ===== HASIL PREDIKSI ===== */
.hasil-box {
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
    margin-bottom: 12px;
}
.hasil-emoji { font-size: clamp(32px, 8vw, 44px); }
.hasil-teks  { font-size: clamp(15px, 4vw, 20px); font-weight: 800; margin-top: 8px; }
.hasil-prob  { font-size: clamp(12px, 3vw, 13px); color: #6b7280; margin-top: 6px; }

/* ============================================
   TABLET — 481px s/d 768px
   ============================================ */
@media (max-width: 768px) {
    .block-container { padding: 1rem 0.75rem 2rem 0.75rem !important; }
    .home-card  { padding: 16px 18px; }
    .input-card { padding: 16px 18px; }
    .stButton > button { height: 52px; }
}

/* ============================================
   HP / MOBILE — maksimal 480px
   ============================================ */
@media (max-width: 480px) {
    .block-container { padding: 0.75rem 0.5rem 2rem 0.5rem !important; }
    .home-card  { padding: 14px 14px; border-radius: 12px; }
    .input-card { padding: 14px 14px; border-radius: 12px; }
    .stButton > button { height: 54px; border-radius: 10px; }

    /* font-size 16px mencegah zoom otomatis Safari iOS */
    .stNumberInput input, .stSelectbox > div > div {
        min-height: 46px !important;
        font-size: 16px !important;
    }
    .disclaimer-box { font-size: 13px; padding: 12px 14px; }
    .feature-item   { font-size: 13px; }
    .sidebar-logo p { font-size: 10px; }
}

/* ===== METRIC CARDS ===== */
[data-testid="stMetric"] {
    background: white;
    border-radius: 10px;
    padding: 12px 10px !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
    text-align: center;
}
[data-testid="stMetricLabel"] { font-size: 12px !important; }
[data-testid="stMetricValue"] { font-size: clamp(14px, 3.5vw, 18px) !important; }
[data-testid="stMetricDelta"] { font-size: 12px !important; }

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="icon">🩺</span>
        <h2>Early Diabetes<br>Screening</h2>
        <p>Sistem Skrining Dini<br>Diabetes Melitus Tipe 2</p>
    </div>
    <hr class="sidebar-divider">
    """, unsafe_allow_html=True)

    menu = st.selectbox("📋 Menu Navigasi", ["🏠 Home", "🔍 Prediksi"])

    st.markdown("""
    <hr class="sidebar-divider">
    <div style="text-align:center; padding-top:10px;">
        <p style="font-size:11px; color:rgba(255,255,255,0.75);">
            Universitas Negeri Medan<br>
            Ilmu Komputer · FMIPA<br><br>
            © 2026 Adzkia Nur Nasution
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==================== HOME ====================
if menu == "🏠 Home":

    st.markdown("""
    <div class="home-card">
        <h1 class="page-title">🩺 Sistem Skrining Awal Diabetes</h1>
        <p class="page-subtitle">
            Deteksi dini risiko Diabetes Melitus Tipe 2 berbasis <em>Machine Learning</em>
        </p>
        <hr style="border-color:#f9a8d4; margin-bottom:0;">
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown("""
        <div class="home-card">
            <h3 style="color:#ec4899; font-size:16px; margin-bottom:10px;">📌 Tentang Sistem</h3>
            <p style="color:#4b5563; line-height:1.7; font-size:14px; margin:0;">
                Sistem ini memprediksi kemungkinan seseorang terkena
                <strong>Diabetes Melitus Tipe 2</strong> menggunakan algoritma
                <strong>Random Forest</strong> yang dilatih berdasarkan data rekam
                medis pasien <strong>RSUD Pintu Padang</strong>, Tapanuli Selatan.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="home-card">
            <h3 style="color:#ec4899; font-size:16px; margin-bottom:6px;">🎯 Tujuan</h3>
            <div class="feature-item"><span class="feature-icon">🔍</span> Skrining awal kesehatan masyarakat</div>
            <div class="feature-item"><span class="feature-icon">👨‍⚕️</span> Membantu tenaga medis deteksi dini</div>
            <div class="feature-item"><span class="feature-icon">📚</span> Edukasi masyarakat risiko diabetes</div>
            <div class="feature-item" style="border:none;"><span class="feature-icon">🏥</span> Mendukung layanan kesehatan daerah</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="home-card" style="background:linear-gradient(135deg,#fdf2f8,#fce7f3);">
        <h3 style="color:#ec4899; font-size:16px; margin-bottom:8px;">⚠️ Penting Diketahui</h3>
        <div class="disclaimer-box">
            <strong>⚠️ Perhatian</strong><br>
            Sistem ini merupakan alat bantu skrining awal dan
            <strong>bukan pengganti diagnosis medis</strong>.
            Hasil prediksi tidak dapat dijadikan dasar keputusan medis secara mandiri.
            Selalu konsultasikan kondisi kesehatan Anda kepada dokter atau
            tenaga kesehatan yang berkompeten.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== PREDIKSI ====================
elif menu == "🔍 Prediksi":

    st.markdown("""
    <p class="page-title">🔍 Early Diabetes Screening</p>
    <p class="page-subtitle">Isi seluruh data di bawah ini untuk mendapatkan hasil prediksi</p>
    """, unsafe_allow_html=True)

    # ===== FORM INPUT =====
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("#### 📝 Data Diri")

    r1c1, r1c2 = st.columns(2, gap="medium")
    with r1c1:
        usia = st.number_input("👤 Usia (tahun)", min_value=1, value=None, placeholder="Contoh: 45")
    with r1c2:
        jk   = st.selectbox("⚧ Jenis Kelamin", ["Pilih", "Laki-laki", "Perempuan"])

    r2c1, r2c2 = st.columns(2, gap="medium")
    with r2c1:
        berat  = st.number_input("⚖️ Berat Badan (kg)", value=None, placeholder="Contoh: 70")
    with r2c2:
        tinggi = st.number_input("📏 Tinggi Badan (cm)", value=None, placeholder="Contoh: 165")

    st.markdown("#### 🩸 Data Tekanan Darah")
    r3c1, r3c2 = st.columns(2, gap="medium")
    with r3c1:
        sistolik  = st.number_input("💉 Sistolik (mmHg)",  value=None, placeholder="Contoh: 120")
    with r3c2:
        diastolik = st.number_input("💉 Diastolik (mmHg)", value=None, placeholder="Contoh: 80")

    st.markdown("<br>", unsafe_allow_html=True)
    tombol = st.button("🔍 Mulai Prediksi", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ===== OUTPUT =====
    if tombol:

        if None in [usia, berat, tinggi, sistolik, diastolik] or jk == "Pilih":
            st.warning("⚠️ Harap isi semua data terlebih dahulu!")
            st.stop()

        jk_val = 1 if jk == "Laki-laki" else 0

        bmi = berat / ((tinggi / 100) ** 2)
        if   bmi < 18.5: bmi_kat = "Kurus"
        elif bmi < 25.0: bmi_kat = "Normal"
        elif bmi < 30.0: bmi_kat = "Gemuk"
        else:            bmi_kat = "Obesitas"

        input_data = pd.DataFrame([[
            usia, jk_val, berat, tinggi, bmi, sistolik, diastolik
        ]], columns=[
            'Usia','Jenis Kelamin','Berat Badan',
            'Tinggi Badan','BMI','Sistolik','Diastolik'
        ])

        pred  = model.predict(input_data)
        proba = model.predict_proba(input_data)

        # RINGKASAN DATA
        st.markdown("---")
        st.markdown("#### 📋 Ringkasan Data")
        m1, m2, m3 = st.columns(3, gap="small")
        m1.metric("👤 Usia",  f"{int(usia)} thn")
        m2.metric("⚖️ BMI",   f"{bmi:.1f}", bmi_kat)
        m3.metric("💉 TD",    f"{int(sistolik)}/{int(diastolik)}")

        st.markdown("<br>", unsafe_allow_html=True)

        # HASIL PREDIKSI
        st.markdown("#### 🎯 Hasil Prediksi")
        if pred[0] == 1:
            st.markdown("""
            <div class="hasil-box" style="background:#fef2f2; border:2px solid #f87171;">
                <div class="hasil-emoji">⚠️</div>
                <div class="hasil-teks" style="color:#dc2626;">
                    Terindikasi Diabetes Melitus Tipe 2
                </div>
                <div class="hasil-prob">
                    Probabilitas diabetes:
                    <strong style="color:#dc2626;">{:.1f}%</strong>
                </div>
            </div>
            """.format(proba[0][1] * 100), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="hasil-box" style="background:#f0fdf4; border:2px solid #4ade80;">
                <div class="hasil-emoji">✅</div>
                <div class="hasil-teks" style="color:#16a34a;">
                    Tidak Terindikasi Diabetes Melitus Tipe 2
                </div>
                <div class="hasil-prob">
                    Probabilitas tidak diabetes:
                    <strong style="color:#16a34a;">{:.1f}%</strong>
                </div>
            </div>
            """.format(proba[0][0] * 100), unsafe_allow_html=True)

        # DIAGRAM
        st.markdown("#### 📊 Diagram Probabilitas")
        labels = ['Tidak Diabetes', 'Diabetes']
        values = [proba[0][0] * 100, proba[0][1] * 100]
        colors = ['#4ade80', '#f87171']

        fig, ax = plt.subplots(figsize=(5, 3))
        bars = ax.bar(labels, values, color=colors, width=0.45,
                      edgecolor='white', linewidth=1.5, zorder=3)
        ax.set_ylim(0, 115)
        ax.set_ylabel('Persentase (%)', fontsize=11)
        ax.set_title('Probabilitas Prediksi', fontsize=12, fontweight='bold', pad=12)
        ax.yaxis.grid(True, linestyle='--', alpha=0.5, zorder=0)
        ax.set_axisbelow(True)
        ax.spines[['top', 'right']].set_visible(False)
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                    f'{val:.1f}%', ha='center', va='bottom',
                    fontsize=12, fontweight='bold')
        fig.patch.set_facecolor('#f9fafb')
        ax.set_facecolor('#f9fafb')
        st.pyplot(fig, use_container_width=True)  # otomatis menyesuaikan lebar layar

        # DISCLAIMER
        st.markdown("""
        <div class="disclaimer-box">
            <strong>⚠️ Disclaimer Penting</strong><br>
            Hasil ini <strong>bukan merupakan diagnosis medis</strong>.
            Sistem ini hanya berfungsi sebagai alat bantu skrining awal.
            Segera <strong>konsultasikan ke dokter atau tenaga kesehatan terdekat</strong>
            untuk pemeriksaan lebih lanjut dan penanganan yang tepat.
        </div>
        """, unsafe_allow_html=True)
