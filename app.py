import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
import os

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CardioCheck Indonesia",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* Hide Streamlit default elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,100,100,0.2);
    border: 1px solid rgba(255,100,100,0.4);
    color: #ff6b6b;
    padding: 0.3rem 1rem;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ff6b6b, #ffd93d, #6bcb77);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.1;
}
.hero-sub {
    color: rgba(255,255,255,0.6);
    font-size: 1rem;
    margin-top: 0.75rem;
    font-weight: 300;
}

/* ── Glass Card ── */
.glass-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
}
.section-title {
    font-size: 1rem;
    font-weight: 700;
    color: #ffd93d;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Inputs ── */
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: white !important;
    border-radius: 10px !important;
}
div[data-testid="stSlider"] .stSlider { color: white; }
label { color: rgba(255,255,255,0.85) !important; font-size: 0.88rem !important; }

/* ── Analyze Button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #ff6b6b, #ee5a24) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    padding: 0.9rem 2rem !important;
    border-radius: 14px !important;
    border: none !important;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    box-shadow: 0 8px 32px rgba(255,107,107,0.35);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(255,107,107,0.5) !important;
}

/* ── Result Cards ── */
.result-positive {
    background: linear-gradient(135deg, rgba(255,107,107,0.25), rgba(238,90,36,0.15));
    border: 2px solid rgba(255,107,107,0.5);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.result-negative {
    background: linear-gradient(135deg, rgba(107,203,119,0.25), rgba(39,174,96,0.15));
    border: 2px solid rgba(107,203,119,0.5);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.result-title { font-size: 1.8rem; font-weight: 800; margin: 0.5rem 0; }
.result-icon { font-size: 3.5rem; }
.result-prob {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.7);
    margin-top: 0.5rem;
}

/* ── Status Chips ── */
.status-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.9rem;
    border-radius: 50px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 0.2rem;
}
.chip-normal { background: rgba(107,203,119,0.2); border: 1px solid rgba(107,203,119,0.5); color: #6bcb77; }
.chip-warning { background: rgba(255,217,61,0.2); border: 1px solid rgba(255,217,61,0.5); color: #ffd93d; }
.chip-danger  { background: rgba(255,107,107,0.2); border: 1px solid rgba(255,107,107,0.5); color: #ff6b6b; }

/* ── Metric Row ── */
.metric-row {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.metric-label { color: rgba(255,255,255,0.6); font-size: 0.85rem; }
.metric-value { color: white; font-weight: 600; font-size: 0.9rem; }

/* ── Food Card ── */
.food-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
}
.food-name { color: white; font-weight: 600; font-size: 0.95rem; }
.food-desc { color: rgba(255,255,255,0.55); font-size: 0.82rem; margin-top: 0.2rem; }

/* ── Risk Gauge ── */
.gauge-container {
    text-align: center;
    padding: 1rem 0;
}
.gauge-value {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ff6b6b, #ffd93d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.gauge-label { color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-top: -0.3rem; }

/* ── Divider ── */
.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    margin: 1.5rem 0;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 3px; }

/* ── Disclaimer ── */
.disclaimer {
    background: rgba(255,217,61,0.08);
    border: 1px solid rgba(255,217,61,0.2);
    border-radius: 12px;
    padding: 0.9rem 1.2rem;
    color: rgba(255,255,255,0.6);
    font-size: 0.8rem;
    text-align: center;
    margin-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Load Model ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "model.pkl"), "rb") as f:
        model = pickle.load(f)
    with open(os.path.join(base, "encoders.json"), "r") as f:
        encoders = json.load(f)
    return model, encoders

model, encoders = load_model()

# ─── Helper: classify vitals ─────────────────────────────────────────────────
def classify_bp(sys, dia):
    if sys < 90 or dia < 60:
        return "danger", "⚠️", "Hipotensi (Tekanan Darah Rendah)"
    elif sys < 120 and dia < 80:
        return "normal", "✅", "Normal"
    elif sys < 130 and dia < 80:
        return "warning", "⚠️", "Elevasi (Sedikit Tinggi)"
    elif sys < 140 or dia < 90:
        return "warning", "⚠️", "Hipertensi Stadium 1"
    elif sys < 180 or dia < 120:
        return "danger", "🔴", "Hipertensi Stadium 2"
    else:
        return "danger", "🚨", "Krisis Hipertensi — Segera Cek Dokter!"

def classify_fbs(fbs):
    if fbs < 70:
        return "danger", "⚠️", "Hipoglikemia (Gula Darah Rendah)"
    elif fbs < 100:
        return "normal", "✅", "Normal (Puasa)"
    elif fbs < 126:
        return "warning", "⚠️", "Prediabetes"
    else:
        return "danger", "🔴", "Indikasi Diabetes"

def classify_chol_total(val):
    if val < 200:
        return "normal", "✅", "Optimal"
    elif val < 240:
        return "warning", "⚠️", "Batas Tinggi"
    else:
        return "danger", "🔴", "Tinggi — Perlu Perhatian"

def classify_hdl(val, gender):
    low = 40 if gender == "Laki-laki" else 50
    if val < low:
        return "danger", "🔴", "Rendah (Risiko Tinggi)"
    elif val < 60:
        return "warning", "⚠️", "Cukup"
    else:
        return "normal", "✅", "Optimal (Pelindung Jantung)"

def classify_ldl(val):
    if val < 100:
        return "normal", "✅", "Optimal"
    elif val < 130:
        return "normal", "✅", "Hampir Optimal"
    elif val < 160:
        return "warning", "⚠️", "Batas Tinggi"
    elif val < 190:
        return "danger", "🔴", "Tinggi"
    else:
        return "danger", "🔴", "Sangat Tinggi"

def classify_trig(val):
    if val < 150:
        return "normal", "✅", "Normal"
    elif val < 200:
        return "warning", "⚠️", "Batas Tinggi"
    elif val < 500:
        return "danger", "🔴", "Tinggi"
    else:
        return "danger", "🔴", "Sangat Tinggi"

def classify_waist(val, gender):
    limit = 90 if gender == "Laki-laki" else 80
    if val < limit:
        return "normal", "✅", "Normal"
    else:
        return "danger", "🔴", f"Obesitas Sentral (>{'90' if gender == 'Laki-laki' else '80'} cm)"

def classify_sleep(val):
    if val < 6:
        return "danger", "⚠️", "Kurang Tidur (< 6 jam)"
    elif val <= 9:
        return "normal", "✅", "Normal (6–9 jam)"
    else:
        return "warning", "⚠️", "Terlalu Banyak Tidur"

def chip_html(level, icon, label):
    cls = f"chip-{level}"
    return f'<span class="status-chip {cls}">{icon} {label}</span>'

# ─── Food Recommendations ────────────────────────────────────────────────────
def get_food_recommendations(risk_high, hypertension, diabetes, high_chol, high_trig, obesity):
    recs = []
    avoid = []

    if risk_high:
        recs += [
            ("🐟 Ikan Salmon / Tuna", "Kaya Omega-3, menurunkan risiko aritmia dan peradangan pembuluh darah"),
            ("🥦 Brokoli & Sayuran Hijau", "Antioksidan tinggi, menjaga elastisitas pembuluh darah"),
            ("🫐 Blueberry & Beri-berian", "Flavonoid menurunkan tekanan darah dan kolesterol LDL"),
            ("🌾 Oatmeal / Gandum Utuh", "Serat larut (beta-glukan) menurunkan kolesterol jahat"),
            ("🫒 Minyak Zaitun Extra Virgin", "Lemak sehat MUFA untuk kesehatan jantung"),
            ("🥑 Alpukat", "Kalium & lemak baik menjaga tekanan darah stabil"),
        ]
        avoid += [
            ("🚫 Makanan Gorengan / Fast Food", "Lemak trans meningkatkan LDL dan memperparah penyakit jantung"),
            ("🚫 Daging Merah Olahan", "Sodium & lemak jenuh tinggi membebani jantung"),
            ("🚫 Minuman Bersoda & Manis", "Memperburuk peradangan dan meningkatkan trigliserida"),
        ]
    else:
        recs += [
            ("🥗 Salad Sayur Segar", "Kaya serat, vitamin, dan mineral untuk jantung sehat"),
            ("🍎 Apel & Buah Segar", "Quercetin dan serat membantu menjaga kolesterol normal"),
            ("🫘 Kacang-kacangan (Almond, Kenari)", "Lemak sehat dan vitamin E mendukung kesehatan jantung"),
            ("🐔 Ayam Tanpa Kulit / Ikan", "Protein tanpa lemak jenuh berlebih"),
        ]

    if hypertension:
        recs += [
            ("🍌 Pisang", "Tinggi kalium, membantu menurunkan tekanan darah"),
            ("🌿 Seledri & Bawang Putih", "Mengandung alicin, terbukti menurunkan hipertensi"),
        ]
        avoid += [("🚫 Garam & Makanan Asin (Kerupuk, Acar)", "Sodium tinggi langsung meningkatkan tekanan darah")]

    if diabetes:
        recs += [
            ("🍠 Ubi Jalar / Kentang Rebus", "Indeks glikemik rendah dibanding nasi putih"),
            ("🥚 Telur Rebus", "Protein tinggi tanpa lonjakan gula darah"),
        ]
        avoid += [("🚫 Nasi Putih Berlebih & Roti Manis", "IG tinggi memperparah kadar gula darah")]

    if high_chol:
        recs += [
            ("🫘 Kedelai & Tempe / Tahu", "Isoflavon menurunkan kolesterol LDL secara signifikan"),
        ]
        avoid += [("🚫 Jeroan & Kuning Telur Berlebih", "Kolesterol tinggi langsung dari makanan hewani")]

    if high_trig:
        avoid += [("🚫 Alkohol & Minuman Manis", "Fruktosa & alkohol adalah pemicu utama trigliserida tinggi")]

    if obesity:
        recs += [
            ("🥒 Mentimun & Semangka", "Rendah kalori, tinggi air — membantu kontrol berat badan"),
            ("☕ Teh Hijau Tanpa Gula", "Meningkatkan metabolisme dan kaya antioksidan"),
        ]

    # Deduplicate
    seen_r, seen_a = set(), set()
    recs_clean = [(n, d) for n, d in recs if n not in seen_r and not seen_r.add(n)]
    avoid_clean = [(n, d) for n, d in avoid if n not in seen_a and not seen_a.add(n)]

    return recs_clean[:8], avoid_clean[:5]

# ─── HERO ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🏥 Alat Deteksi Dini</div>
    <div class="hero-title">CardioCheck Indonesia</div>
    <div class="hero-sub">Sistem Prediksi Risiko Penyakit Jantung berbasis Machine Learning<br>
    Dilatih dengan 158.000+ data pasien Indonesia</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

# ─── FORM ────────────────────────────────────────────────────────────────────
st.markdown("### 📋 Isi Data Kesehatan Anda")
st.markdown("<p style='color:rgba(255,255,255,0.5);font-size:0.85rem;margin-top:-0.8rem;'>Semua data hanya digunakan untuk analisis lokal dan tidak disimpan</p>", unsafe_allow_html=True)

col_l, col_r = st.columns([1, 1], gap="large")

with col_l:
    # ── Identitas
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👤 Identitas & Gaya Hidup</div>', unsafe_allow_html=True)

    age = st.slider("Usia (tahun)", 25, 90, 45)
    gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

    c1, c2 = st.columns(2)
    with c1:
        smoking = st.selectbox("Status Merokok", ["Tidak Pernah", "Pernah (Berhenti)", "Aktif Merokok"])
    with c2:
        alcohol = st.selectbox("Konsumsi Alkohol", ["Tidak Ada", "Sedang", "Tinggi"])

    c3, c4 = st.columns(2)
    with c3:
        physical = st.selectbox("Aktivitas Fisik", ["Tinggi", "Sedang", "Rendah"])
    with c4:
        diet = st.selectbox("Pola Makan", ["Sehat", "Tidak Sehat"])

    c5, c6 = st.columns(2)
    with c5:
        stress = st.selectbox("Tingkat Stres", ["Rendah", "Sedang", "Tinggi"])
    with c6:
        sleep = st.slider("Jam Tidur / Hari", 2.0, 12.0, 7.0, 0.5)

    region = st.selectbox("Wilayah Tempat Tinggal", ["Perkotaan (Urban)", "Pedesaan (Rural)"])
    pollution = st.selectbox("Paparan Polusi Udara", ["Rendah", "Sedang", "Tinggi"])
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Riwayat
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Riwayat Medis</div>', unsafe_allow_html=True)

    c7, c8 = st.columns(2)
    with c7:
        hypertension_hist = st.selectbox("Riwayat Hipertensi", ["Tidak", "Ya"])
        diabetes_hist = st.selectbox("Riwayat Diabetes", ["Tidak", "Ya"])
        obesity_hist = st.selectbox("Obesitas", ["Tidak", "Ya"])
    with c8:
        family_hist = st.selectbox("Riwayat Keluarga Jantung", ["Tidak", "Ya"])
        prev_heart = st.selectbox("Penyakit Jantung Sebelumnya", ["Tidak", "Ya"])
        medication = st.selectbox("Sedang Konsumsi Obat Rutin", ["Tidak", "Ya"])

    ekg = st.selectbox("Hasil EKG Terakhir", ["Normal", "Abnormal", "Belum Pernah"])
    income = st.selectbox("Tingkat Pendapatan", ["Rendah", "Menengah", "Tinggi"])
    chol_cat = st.selectbox("Kategori Kolesterol (Umum)", ["Rendah (<200)", "Sedang (200-239)", "Tinggi (≥240)"])
    st.markdown('</div>', unsafe_allow_html=True)

with col_r:
    # ── Tekanan darah
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💓 Tekanan Darah (mmHg)</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:rgba(255,255,255,0.5);font-size:0.82rem;margin-top:-0.8rem;">Contoh: Tekanan darah 120/80</p>', unsafe_allow_html=True)
    bp_sys = st.slider("Sistolik (angka atas)", 70, 220, 120)
    bp_dia = st.slider("Diastolik (angka bawah)", 40, 140, 80)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Gula & Kolesterol
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🩸 Gula Darah & Kolesterol (mg/dL)</div>', unsafe_allow_html=True)

    fbs = st.slider("Gula Darah Puasa", 50, 400, 95,
                    help="Normal: 70-99 mg/dL | Prediabetes: 100-125 | Diabetes: ≥126")
    chol_hdl = st.slider("Kolesterol HDL (Baik)", 20, 100, 55,
                         help="Laki-laki: >40 | Perempuan: >50 | Optimal: >60 mg/dL")
    chol_ldl = st.slider("Kolesterol LDL (Jahat)", 30, 300, 100,
                         help="Optimal: <100 | Batas: 130-159 | Tinggi: ≥160 mg/dL")
    triglycerides = st.slider("Trigliserida", 30, 800, 130,
                              help="Normal: <150 | Batas: 150-199 | Tinggi: ≥200 mg/dL")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Antropometri
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📏 Antropometri</div>', unsafe_allow_html=True)
    waist = st.slider("Lingkar Pinggang (cm)", 50, 160, 80,
                      help="Risiko: Laki-laki >90 cm | Perempuan >80 cm")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Analyze Button
    st.markdown("<br>", unsafe_allow_html=True)
    analyze = st.button("🔍 Analisis Risiko Jantung Saya", use_container_width=True)

# ─── ANALYSIS ────────────────────────────────────────────────────────────────
if analyze:
    # Map inputs to model format
    enc = encoders
    smoking_map  = {"Tidak Pernah": "Never", "Pernah (Berhenti)": "Past", "Aktif Merokok": "Current"}
    alcohol_map  = {"Tidak Ada": "None", "Sedang": "Moderate", "Tinggi": "High"}
    physical_map = {"Tinggi": "High", "Sedang": "Moderate", "Rendah": "Low"}
    diet_map     = {"Sehat": "Healthy", "Tidak Sehat": "Unhealthy"}
    stress_map   = {"Rendah": "Low", "Sedang": "Moderate", "Tinggi": "High"}
    region_map   = {"Perkotaan (Urban)": "Urban", "Pedesaan (Rural)": "Rural"}
    pollution_map= {"Rendah": "Low", "Sedang": "Moderate", "Tinggi": "High"}
    ekg_map      = {"Normal": "Normal", "Abnormal": "Abnormal", "Belum Pernah": "Normal"}
    income_map   = {"Rendah": "Low", "Menengah": "Middle", "Tinggi": "High"}
    chol_cat_map = {"Rendah (<200)": 1, "Sedang (200-239)": 2, "Tinggi (≥240)": 3}

    def encode(col, val):
        return enc[col].get(val, 0)

    features = [
        age,
        encode("gender", "Male" if gender == "Laki-laki" else "Female"),
        1 if hypertension_hist == "Ya" else 0,
        1 if diabetes_hist == "Ya" else 0,
        chol_cat_map[chol_cat],
        1 if obesity_hist == "Ya" else 0,
        waist,
        1 if family_hist == "Ya" else 0,
        encode("smoking_status", smoking_map[smoking]),
        encode("alcohol_consumption", alcohol_map[alcohol]),
        encode("physical_activity", physical_map[physical]),
        encode("dietary_habits", diet_map[diet]),
        encode("stress_level", stress_map[stress]),
        sleep,
        bp_sys,
        bp_dia,
        fbs,
        chol_hdl,
        chol_ldl,
        triglycerides,
        encode("EKG_results", ekg_map[ekg]),
        1 if prev_heart == "Ya" else 0,
        1 if medication == "Ya" else 0,
    ]

    X = np.array(features).reshape(1, -1)
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    risk_pct = int(proba[1] * 100)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    st.markdown("## 📊 Hasil Analisis")

    # ── Result Banner
    if pred == 1:
        st.markdown(f"""
        <div class="result-positive">
            <div class="result-icon">❤️‍🔥</div>
            <div class="result-title" style="color:#ff6b6b;">RISIKO TINGGI PENYAKIT JANTUNG</div>
            <div class="result-prob">Probabilitas: <strong style="color:#ff6b6b;">{risk_pct}%</strong> — Segera konsultasikan dengan dokter spesialis jantung</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-negative">
            <div class="result-icon">💚</div>
            <div class="result-title" style="color:#6bcb77;">RISIKO RENDAH PENYAKIT JANTUNG</div>
            <div class="result-prob">Probabilitas risiko: <strong style="color:#ff6b6b;">{risk_pct}%</strong> — Pertahankan gaya hidup sehat Anda</div>
        </div>
        """, unsafe_allow_html=True)

    # ── 3 columns: vitals status | risk gauge | lifestyle
    c1, c2, c3 = st.columns([5, 3, 4], gap="large")

    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🩺 Status Parameter Klinis</div>', unsafe_allow_html=True)

        # Blood pressure
        lvl, ico, msg = classify_bp(bp_sys, bp_dia)
        st.markdown(f"""
        <div class="metric-row">
            <div>
                <div class="metric-label">Tekanan Darah</div>
                <div class="metric-value">{bp_sys}/{bp_dia} mmHg</div>
            </div>
            {chip_html(lvl, ico, msg)}
        </div>""", unsafe_allow_html=True)

        # FBS
        lvl, ico, msg = classify_fbs(fbs)
        st.markdown(f"""
        <div class="metric-row">
            <div>
                <div class="metric-label">Gula Darah Puasa</div>
                <div class="metric-value">{fbs} mg/dL</div>
            </div>
            {chip_html(lvl, ico, msg)}
        </div>""", unsafe_allow_html=True)

        # Kolesterol HDL
        lvl, ico, msg = classify_hdl(chol_hdl, gender)
        st.markdown(f"""
        <div class="metric-row">
            <div>
                <div class="metric-label">Kolesterol HDL (Baik)</div>
                <div class="metric-value">{chol_hdl} mg/dL</div>
            </div>
            {chip_html(lvl, ico, msg)}
        </div>""", unsafe_allow_html=True)

        # Kolesterol LDL
        lvl, ico, msg = classify_ldl(chol_ldl)
        st.markdown(f"""
        <div class="metric-row">
            <div>
                <div class="metric-label">Kolesterol LDL (Jahat)</div>
                <div class="metric-value">{chol_ldl} mg/dL</div>
            </div>
            {chip_html(lvl, ico, msg)}
        </div>""", unsafe_allow_html=True)

        # Trigliserida
        lvl, ico, msg = classify_trig(triglycerides)
        st.markdown(f"""
        <div class="metric-row">
            <div>
                <div class="metric-label">Trigliserida</div>
                <div class="metric-value">{triglycerides} mg/dL</div>
            </div>
            {chip_html(lvl, ico, msg)}
        </div>""", unsafe_allow_html=True)

        # Lingkar pinggang
        lvl, ico, msg = classify_waist(waist, gender)
        st.markdown(f"""
        <div class="metric-row">
            <div>
                <div class="metric-label">Lingkar Pinggang</div>
                <div class="metric-value">{waist} cm</div>
            </div>
            {chip_html(lvl, ico, msg)}
        </div>""", unsafe_allow_html=True)

        # Tidur
        lvl, ico, msg = classify_sleep(sleep)
        st.markdown(f"""
        <div class="metric-row">
            <div>
                <div class="metric-label">Jam Tidur</div>
                <div class="metric-value">{sleep} jam/hari</div>
            </div>
            {chip_html(lvl, ico, msg)}
        </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="justify-content:center;">⚡ Skor Risiko</div>', unsafe_allow_html=True)

        bar_color = "#ff6b6b" if risk_pct >= 60 else "#ffd93d" if risk_pct >= 40 else "#6bcb77"
        risk_label = "Tinggi" if risk_pct >= 60 else "Sedang" if risk_pct >= 40 else "Rendah"

        st.markdown(f"""
        <div class="gauge-container">
            <div class="gauge-value" style="background:linear-gradient(135deg,{bar_color},#ffd93d);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
                {risk_pct}%
            </div>
            <div class="gauge-label">Probabilitas Risiko</div>
        </div>
        """, unsafe_allow_html=True)

        st.progress(risk_pct / 100)

        st.markdown(f"""
        <br>
        <div style="background:rgba(255,255,255,0.04);border-radius:12px;padding:1rem;text-align:left;">
            <div style="color:rgba(255,255,255,0.5);font-size:0.75rem;margin-bottom:0.5rem;">FAKTOR RISIKO UTAMA</div>
            {"".join([
                f'<div style="color:rgba(255,255,255,0.8);font-size:0.82rem;padding:0.2rem 0;">{'🔴' if hypertension_hist=='Ya' else '⚪'} Hipertensi: {hypertension_hist}</div>',
                f'<div style="color:rgba(255,255,255,0.8);font-size:0.82rem;padding:0.2rem 0;">{'🔴' if diabetes_hist=='Ya' else '⚪'} Diabetes: {diabetes_hist}</div>',
                f'<div style="color:rgba(255,255,255,0.8);font-size:0.82rem;padding:0.2rem 0;">{'🔴' if smoking=='Aktif Merokok' else '⚪'} Merokok: {smoking}</div>',
                f'<div style="color:rgba(255,255,255,0.8);font-size:0.82rem;padding:0.2rem 0;">{'🔴' if family_hist=='Ya' else '⚪'} Riwayat Keluarga: {family_hist}</div>',
                f'<div style="color:rgba(255,255,255,0.8);font-size:0.82rem;padding:0.2rem 0;">{'🔴' if prev_heart=='Ya' else '⚪'} Riwayat Jantung: {prev_heart}</div>',
            ])}
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Risk Level Card
        st.markdown('<div class="glass-card" style="text-align:center;margin-top:0;">', unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="justify-content:center;">📌 Status Kategori</div>', unsafe_allow_html=True)
        if risk_pct >= 60:
            st.markdown('<p style="font-size:1.5rem;">🚨</p><p style="color:#ff6b6b;font-weight:700;">RISIKO TINGGI</p><p style="color:rgba(255,255,255,0.5);font-size:0.8rem;">Konsultasi dokter segera</p>', unsafe_allow_html=True)
        elif risk_pct >= 40:
            st.markdown('<p style="font-size:1.5rem;">⚠️</p><p style="color:#ffd93d;font-weight:700;">RISIKO SEDANG</p><p style="color:rgba(255,255,255,0.5);font-size:0.8rem;">Pantau kesehatan rutin</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="font-size:1.5rem;">✅</p><p style="color:#6bcb77;font-weight:700;">RISIKO RENDAH</p><p style="color:rgba(255,255,255,0.5);font-size:0.8rem;">Pertahankan gaya hidup sehat</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🏃 Status Gaya Hidup</div>', unsafe_allow_html=True)

        lifestyle_items = [
            ("Merokok", smoking, smoking == "Aktif Merokok"),
            ("Alkohol", alcohol, alcohol == "Tinggi"),
            ("Aktivitas Fisik", physical, physical == "Rendah"),
            ("Pola Makan", diet, diet == "Tidak Sehat"),
            ("Stres", stress, stress == "Tinggi"),
            ("Tidur", f"{sleep} jam/hari", sleep < 6 or sleep > 9),
            ("Polusi Udara", pollution, pollution == "Tinggi"),
        ]

        for label, val, is_bad in lifestyle_items:
            chip_cls = "chip-danger" if is_bad else "chip-normal"
            icon = "🔴" if is_bad else "✅"
            st.markdown(f"""
            <div class="metric-row">
                <div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{val}</div>
                </div>
                <span class="status-chip {chip_cls}">{icon}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Food Recommendations
    st.markdown("---")
    st.markdown("## 🍽️ Rekomendasi Makanan Personal")

    high_chol_flag = chol_ldl >= 160 or (chol_cat == "Tinggi (≥240)")
    high_trig_flag = triglycerides >= 200
    obesity_flag   = obesity_hist == "Ya"

    foods_ok, foods_avoid = get_food_recommendations(
        pred == 1,
        hypertension_hist == "Ya",
        diabetes_hist == "Ya",
        high_chol_flag,
        high_trig_flag,
        obesity_flag,
    )

    fa, fb = st.columns(2, gap="large")
    with fa:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">✅ Makanan yang Dianjurkan</div>', unsafe_allow_html=True)
        for name, desc in foods_ok:
            st.markdown(f"""
            <div class="food-card">
                <div class="food-name">{name}</div>
                <div class="food-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with fb:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🚫 Makanan yang Perlu Dihindari</div>', unsafe_allow_html=True)
        for name, desc in foods_avoid:
            st.markdown(f"""
            <div class="food-card" style="border-color:rgba(255,107,107,0.2);">
                <div class="food-name">{name}</div>
                <div class="food-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Disclaimer
    st.markdown("""
    <div class="disclaimer">
        ⚠️ <strong>Perhatian:</strong> Hasil ini bersifat <em>informatif</em> dan tidak menggantikan diagnosis medis.
        Selalu konsultasikan kondisi kesehatan Anda dengan dokter atau tenaga medis profesional.
        Model dilatih dari 158.355 data pasien Indonesia dengan akurasi ~73%.
    </div>
    """, unsafe_allow_html=True)
