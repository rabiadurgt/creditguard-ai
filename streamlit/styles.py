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

/* ======================================================
RISK DRIVER CARDS (Positive / Negative Factors)
====================================================== */

.risk-driver-card {
    background: #23242A;
    border: 1px solid #33353F;
    border-radius: 18px;
    padding: 16px 20px;
    margin-bottom: 12px;
    color: white;
    box-sizing: border-box;
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 6px;
    transition: all 0.25s ease;
}

.risk-driver-card:hover {
    transform: translateY(-4px);
    border-color: #4B4E5C;
}

.model-info-card {
    min-height: 320px;
    height: auto !important;
    overflow: visible !important;
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
POLICY EVIDENCE CARDS
====================================================== */

.policy-evidence-card {
    background: #23242A;
    border: 1px solid #33353F;
    border-left: 4px solid #3B82F6;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 12px;
    transition: all 0.2s ease;
}

.policy-evidence-card:hover {
    border-color: #4B4E5C;
    transform: translateY(-2px);
}

.policy-evidence-title {
    display: flex;
    align-items: center;
    color: #FFFFFF;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 6px;
}

.policy-evidence-icon {
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 4px;
    margin-right: 10px;
}

.policy-evidence-text {
    color: #A8B1C3;
    font-size: 13.5px;
    line-height: 1.6;
    padding-left: 22px;
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
DIVIDER
====================================================== */

hr{
    margin:22px 0;
}


/* ======================================================
RISK RESULTS - CONTAINER CARDS & PLOTLY GAUGE ALIGNMENT
====================================================== */


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
EXPLAINABLE AI TABS - PILL / GRADIENT UNDERLINE
====================================================== */

div[data-baseweb="tab-list"] {
    gap: 6px !important;
    border-bottom: 1px solid #26272E !important;
    padding-bottom: 0 !important;
}

button[data-baseweb="tab"] {
    height: 46px !important;
    padding: 0 18px !important;
    border-radius: 10px 10px 0 0 !important;
    font-weight: 600 !important;
    color: #8B93A7 !important;
    background: transparent !important;
    border: none !important;
    transition: all 0.2s ease !important;
}

button[data-baseweb="tab"] p {
    font-size: 14px !important;
}

button[data-baseweb="tab"]:hover {
    color: #E4E4E7 !important;
    background: rgba(255, 255, 255, 0.04) !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #FFFFFF !important;
    background: rgba(10, 147, 166, 0.14) !important;
}

button[data-baseweb="tab"]:focus-visible {
    outline: 2px solid #2A9FD6 !important;
    outline-offset: -2px !important;
}

/* Baseweb'in hareketli, tüm sekmenin altında kayan çizgisi */
div[data-baseweb="tab-highlight"] {
    background: linear-gradient(90deg, #0A93A6, #2A9FD6) !important;
    height: 3px !important;
    border-radius: 4px !important;
}

/* Sekme içeriği ile tab bar arası boşluk */
div[data-testid="stTabsPanel"] {
    padding-top: 20px !important;
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
EXECUTIVE DECISION CARD (gauge gömülü)
====================================================== */

.executive-decision-card {
    height: auto !important;
    min-height: 200px !important;
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 28px;
    border-radius: 18px !important;
}

.executive-decision-content {
    flex: 1;
}

.exec-decision-gauge {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-width: 130px;
}

.exec-gauge-circle {
    width: 116px;
    height: 116px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.exec-gauge-inner {
    width: 90px;
    height: 90px;
    background: #181920;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.exec-gauge-value {
    color: #FFFFFF;
    font-size: 19px;
    font-weight: 700;
}

.exec-gauge-label {
    margin-top: 10px;
    color: #A8B1C3;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

/* ======================================================
AI REASONING TIMELINE
====================================================== */

.reasoning-timeline {
    display: flex;
    flex-direction: column;
}

.reasoning-step {
    display: flex;
    gap: 16px;
    padding-bottom: 26px;
}

.reasoning-step:last-child {
    padding-bottom: 0;
}

.reasoning-step-marker {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.reasoning-step-number {
    width: 30px;
    height: 30px;
    min-width: 30px;
    border-radius: 50%;
    background: #EEF1F6 !important;
    border: 2px solid #CBD3E1 !important;
    display: flex !important;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700 !important;
    color: #4B5563 !important;
}

.reasoning-step-line {
    width: 2px;
    flex: 1;
    background: #CBD3E1 !important;
    margin-top: 4px;
    min-height: 20px;
}

.reasoning-step:last-child .reasoning-step-line {
    display: none !important;
}

.reasoning-step-text {
    padding-top: 5px;
    color: #1F2937 !important;
    font-size: 14.5px;
    font-weight: 500 !important;
    opacity: 1 !important;
}


/* ======================================================
AUDIT TRAIL TABLE
====================================================== */

.audit-table-wrapper {
    width: 100%;
    border: 1px solid #33353F;
    border-radius: 16px;
    overflow: hidden;
    background: #23242A;
}

.audit-table {
    width: 100%;
    border-collapse: collapse;
}

.audit-table thead th {
    background: #2A2B33;
    color: #8F98A8;
    font-size: 13px;
    font-weight: 600;
    text-align: left;
    padding: 12px 16px;
    border-bottom: 1px solid #33353F;
}

.audit-attr-cell {
    color: #A8B1C3;
    font-size: 13px;
    font-weight: 500;
    padding: 11px 16px;
    border-bottom: 1px solid #2E2F38;
    width: 40%;
}

.audit-value-cell {
    color: #FFFFFF;
    font-size: 13px;
    font-weight: 600;
    padding: 11px 16px;
    border-bottom: 1px solid #2E2F38;
}

.audit-table tbody tr:last-child td {
    border-bottom: none;
}

.audit-table tbody tr:hover {
    background: #2A2B33;
}
/* ======================================================
DATAFRAME
====================================================== */

[data-testid="stDataFrame"]{
    background:#23242A !important;
    border-radius:18px !important;
    border:1px solid #33353F !important;
    padding:8px;
    width:100% !important;
    overflow:hidden !important;
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

/* ======================================================
FEATURE IMPACT TABLE
====================================================== */

.feature-table-card {
    width: 100%;
    max-width: 1000px;
    margin: 0 auto;
    box-sizing: border-box;
}


/* Table wrapper */

.feature-table-wrapper {
    width: 100%;
    border: 1px solid #33353F;
    border-radius: 16px;
    overflow: hidden;
    background: #23242A;
}

/* Table */

.feature-impact-table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
    background: #23242A;
}


/* Header */

.feature-impact-table thead th {
    background: #2A2B33;
    color: #8F98A8;
    font-size: 13px;
    font-weight: 600;
    text-align: left;
    padding: 12px 14px;
    border-bottom: 1px solid #33353F;
}


/* Body */

.feature-impact-table tbody td {
    padding: 11px 14px;
    border-bottom: 1px solid #2E2F38;
    font-size: 13px;
    color: #E4E4E7;
    vertical-align: middle;
}

/* Last row */

.feature-impact-table tbody tr:last-child td {
    border-bottom: none;
}

/* Rank */

.feature-impact-table th:first-child,
.feature-impact-table td:first-child {
    width: 70px;
    text-align: center;
    color: #8F98A8;
}

/* Feature */

.feature-cell {
    font-weight: 600;
    color: #FFFFFF;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Impact */

.impact-cell {
    width: 28%;
}

.impact-number {
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 5px;
    color: #E4E4E7;
}

/* Impact bar */

.impact-track {
    width: 100%;
    height: 5px;
    background: #33353F;
    border-radius: 10px;
    overflow: hidden;
}

.impact-bar {
    height: 100%;
    border-radius: 10px;
}

.bar-green {
    background: #22C55E;
}

.bar-red {
    background: #EF4444;
}

/* Direction */

.direction-cell {
    white-space: nowrap;
}

.direction-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 13px;
    font-weight: 600;
}

.risk-reducing {
    color: #4ADE80;
}

.risk-increasing {
    color: #F87171;
}


/* Dots */

.direction-dot {
    width: 9px;
    height: 9px;
    min-width: 9px;
    border-radius: 50%;
    display: inline-block;
}

.dot-green {
    background: #22C55E;
}

.dot-red {
    background: #EF4444;
}


/* Hover */

.feature-impact-table tbody tr:hover {
    background: #2A2B33;
}
</style>
"""

