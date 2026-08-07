def load_css():
    return """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');


/* ======================================================
GLOBAL
====================================================== */

html, body, [class*="css"]{
    font-family:"Inter",sans-serif;
}

body{
    background:#F4F7FB;
}

.block-container{
    max-width:1450px;
    padding-top:1rem;
    padding-bottom:2rem;
}


/* ======================================================
SIDEBAR
====================================================== */

section[data-testid="stSidebar"]{
    background:#2A2B32;
    border-right:1px solid #27272A;
}

/* Başlıklar ve Metinler */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p {
    color: #E4E4E7 !important; 
}

/* Navigasyon Linkleri ve Menü Elemanları (Home, Executive Dashboard vb.) */
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"],
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] span {
    color: #D1D5DB !important;
    font-weight: 500;
}

/* Menü Öğelerine On-Hover (Üzerine Gelince) Effect */
section[data-testid="stSidebar"] a:hover,
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover {
    color: #FFFFFF !important;
    background-color: rgba(255, 255, 255, 0.08) !important;
    border-radius: 8px;
}

/* Aktif / Seçili Menü Elemanı */
section[data-testid="stSidebar"] [aria-selected="true"],
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] {
    background-color: rgba(255, 255, 255, 0.15) !important;
    color: #FFFFFF !important;
    border-radius: 8px;
    font-weight: 600;
}

/* Input Alanlarının İç Yazıları ve Arka Planı */
section[data-testid="stSidebar"] input {
    background-color: #383942 !important;
    color: #FFFFFF !important;
    border: 1px solid #4B5563 !important;
    border-radius: 10px;
}


/* ======================================================
HEADINGS
====================================================== */

.main-title{
    font-size:40px;
    font-weight:700;
    color:#111827;
}

.subtitle{
    font-size:16px;
    color:#6B7280;
}

.section-title{
    font-size:24px;
    font-weight:700;
    color:#111827;
    margin-bottom:18px;
    margin-top:6px;
}

/* TÜM KART TİPLERİ İÇİN STANDART VE BİREBİR EŞİT YÜKSEKLİK / STİL */
.card {
    background: #23242A;
    border: 1px solid #33353F;
    border-radius: 18px;
    padding: 20px;
    height: 180px !important;
    min-height: 180px !important;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    color: white;
    box-sizing: border-box;
    width: 100%;
}

.overview-card{
    all:unset;
}

/* Hover Effect */
.card:hover,
.kpi-card:hover,
.overview-card:hover{

    transform:translateY(-4px);
    border-color:#4B4E5C;

}

.status-badge-approved:hover, 
.status-badge-review:hover, 
.status-badge-rejected:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 14px 30px rgba(0, 0, 0, 0.35) !important;
}

/* Kart İçi Başlıklar */
.kpi-title{

    font-size:14px;
    color:#A8B1C3;
    font-weight:500;

}

/* Kart İçi Büyük Değerler (Örn: $300,000, 40, 2.35%) */
.kpi-value, .overview-value {
    font-size: 30px !important;
    font-weight: 700 !important;
    color: #FFFFFF !important; /* Beyaz parlak yazı */
    letter-spacing: -0.5px !important;
    margin-top: 0px !important;
    text-align: left !important;
}


/* ======================================================
AI DECISION BADGES / APPROVED CARD (EXECUTIVE SUMMARY HİZALAMASI)
====================================================== */

.status-badge-approved,
.status-badge-review,
.status-badge-rejected {
    width: 100% !important;
    height: 180px !important;
    min-height: 180px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    border-radius: 18px !important;
    box-sizing: border-box !important;
    padding: 20px !important;
    transition: all 0.25s ease !important;
}

/* APPROVE - Yeşil Işıltılı Kart */
.status-badge-approved {
    background: #122B1E !important;
    color: #4ADE80 !important;
    border: 2px solid #22C55E !important;
    box-shadow: 0 0 20px rgba(34, 197, 94, 0.3) !important;
}

.status-badge-approved span {
    color: #4ADE80 !important;
}

/* REVIEW - Sarı/Turuncu Kart */
.status-badge-review {
    background: #2A2415 !important;
    color: #FACC15 !important;
    border: 2px solid #FACC15 !important;
    box-shadow: 0 0 20px rgba(250, 204, 21, 0.3) !important;
}

/* REJECT - Kırmızı Kart */
.status-badge-rejected {
    background: #2B1212 !important;
    color: #EF4444 !important;
    border: 2px solid #EF4444 !important;
    box-shadow: 0 0 20px rgba(239, 68, 68, 0.3) !important;
}


/* ======================================================
INFO BOX
====================================================== */

.info-box{
    background:#F9FAFB;
    border-radius:14px;
    border:1px solid #E5E7EB;
    padding:18px;
}


/* ======================================================
RISK DRIVER
====================================================== */

.driver-positive{
    background:#ECFDF5;
    border-left:5px solid #22C55E;
    border-radius:12px;
    padding:14px;
    margin-bottom:12px;
}

.driver-negative{
    background:#FEF2F2;
    border-left:5px solid #EF4444;
    border-radius:12px;
    padding:14px;
    margin-bottom:12px;
}


/* ======================================================
POLICY
====================================================== */

.policy-box{
    background:#23242A;
    border-radius:14px;
    border:1px solid #33353F;
    padding:16px;
    margin-bottom:12px;
}


/* ======================================================
FORM BUTTONS
====================================================== */

div[data-testid="stForm"] .stButton>button{
    border-radius:12px !important;
    height:48px !important;
    font-weight:600 !important;
    transition:.25s;
}

/* Analyze */
div[data-testid="stForm"] button[kind="primary"]{
    background:linear-gradient(90deg,#1BA8C8,#2A9FD6) !important;
    color:white !important;
    border:none !important;
    box-shadow:0 8px 20px rgba(43,173,214,.35);
}

div[data-testid="stForm"] button[kind="primary"]:hover{
    transform:translateY(-2px);
    box-shadow:0 12px 24px rgba(43,173,214,.45);
}

/* Reset */
div[data-testid="stForm"] button[kind="secondary"]{
    background:white !important;
    color:#374151 !important;
    border:1px solid #D1D5DB !important;
}

/* ======================================================
EXPANDER
====================================================== */

details{
    border-radius:14px;
    border:1px solid #E5E7EB;
    background:white;
}


/* ======================================================
DATAFRAME
====================================================== */

[data-testid="stDataFrame"]{
    border-radius:16px;
    overflow:hidden;
}


/* ======================================================
DIVIDER
====================================================== */

hr{
    margin:22px 0;
}


/* ======================================================
RISK RESULTS - CONTAINER CARDS & PLOTLY GAUGE ALIGNMENT
====================================================== */

.st-key-confidence_gauge_card,
.st-key-shap_chart_card,
.st-key-feature_table_card,
.st-key-prediction_breakdown_card {
    background: #23242A !important;
    border: 1px solid #33353F !important;
    border-radius: 18px !important;
    padding: 16px 20px !important;
    min-height: 140px !important;
    height: 100% !important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.3s ease !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    box-sizing: border-box !important;
}

.st-key-confidence_gauge_card:hover,
.st-key-shap_chart_card:hover,
.st-key-feature_table_card:hover,
.st-key-prediction_breakdown_card:hover {
    transform: translateY(-4px) !important;
    border-color: #4B4E5C !important;
    box-shadow: 0 14px 30px rgba(0, 0, 0, 0.35) !important;
}

.st-key-confidence_gauge_card > div,
.st-key-shap_chart_card > div {
    gap: 0 !important;
}

.card-top{

    display:flex;
    align-items:center;
    gap:12px;
    margin-bottom:16px;

}

.card-icon{

    font-size:20px;
    width:28px;
    text-align:center;

}

.kpi-subtitle{
    color:#8F98A8;
    font-size:13px;
    margin-top:8px;
}


/* ======================================================
POLICY CARD
====================================================== */

.st-key-policy_card{

    background:#23242A;

    border:1px solid #33353F;

    border-radius:18px;

    padding:22px;

    min-height:420px;

    box-shadow:0 8px 24px rgba(0,0,0,.22);

}

/* ======================================================
GAUGE ALIGNMENT
====================================================== */

.st-key-gauge_card .stPlotlyChart{

    margin-top:-18px;

    margin-bottom:-18px;

}

.st-key-gauge_card iframe{

    border-radius:14px;

}

/* ======================================================
EXECUTIVE SUMMARY & GAUGE FIX
====================================================== */

/* Confidence Gauge Kartının 180px Yüksekliğe Tam Oturması */
.st-key-confidence_gauge_card {
    background: #23242A !important;
    border: 1px solid #33353F !important;
    border-radius: 18px !important;
    height: 180px !important;
    min-height: 180px !important;
    padding: 10px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
}

/* Gauge Grafiğinin Dışına Taşmasını Önleme */
.st-key-confidence_gauge_card .stPlotlyChart {
    height: 100% !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* ======================================================
EXPLAINABLE AI TABS
====================================================== */

button[data-baseweb="tab"]{

    height:52px !important;
    border-radius:12px 12px 0 0 !important;
    font-weight:600 !important;
    color:#9CA3AF !important;
    transition:.25s !important;

}

button[data-baseweb="tab"]:hover{

    color:white !important;

}

button[data-baseweb="tab"][aria-selected="true"]{

    color:#3B82F6 !important;
    border-bottom:3px solid #2563EB !important;

}

/* ======================================================
EXPLAINABLE AI CARDS
====================================================== */

.xai-card{

    background:#23242A;

    border:1px solid #33353F;
    border-radius:18px;
    padding:20px;
    margin-bottom:14px;
    transition:.25s;

}

.xai-card:hover{

    transform:translateY(-3px);
    border-color:#4B4E5C;

}

.xai-title{

    font-size:14px;
    color:#A8B1C3;
    margin-bottom:10px;

}

.xai-text{

    color:white;
    line-height:1.7;
    font-size:14px;

}

/* ======================================================
DATAFRAME
====================================================== */

[data-testid="stDataFrame"]{

    background:#23242A !important;
    border-radius:18px !important;
    border:1px solid #33353F !important;
    padding:8px;

}


/* ======================================================
DEBT TO INCOME (DTI) PROGRESS BAR
====================================================== */

.progress-container {

    width:100%;
    height:6px;
    background:#374151;
    border-radius:10px;
    overflow:hidden;
    margin-top:12px;
    margin-bottom:8px;

}


.progress-bar {

    height:100%;
    background:#22C55E;
    border-radius:10px;
    transition:width 0.4s ease;

}


</style>
"""

