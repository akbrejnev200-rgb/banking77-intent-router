import streamlit as st
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("omw-1.4", quiet=True)
nltk.download("punkt_tab", quiet=True)

st.set_page_config(
    page_title="Banking77 · Intent Router",
    page_icon="◈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Montserrat:wght@300;400;500&display=swap');

:root {
    --navy:    #0b1628;
    --navy2:   #112040;
    --navy3:   #1a2f55;
    --gold:    #c9a84c;
    --gold2:   #e8c97a;
    --gold3:   #f5e6b8;
    --cream:   #faf7f0;
    --muted:   #8a9ab8;
    --border:  rgba(201,168,76,0.25);
}

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
    color: var(--cream);
}

/* Background dégradé luxe */
.stApp {
    background: linear-gradient(145deg, var(--navy) 0%, var(--navy2) 50%, #0d1e3a 100%);
    min-height: 100vh;
}

/* Grain texture overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.6;
}

.block-container {
    padding-top: 56px !important;
    max-width: 720px;
    position: relative;
    z-index: 1;
}

/* ── Header ── */
.lux-header {
    text-align: center;
    margin-bottom: 56px;
    position: relative;
    padding-bottom: 32px;
}
.lux-eyebrow {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.6rem;
    font-weight: 500;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 14px;
    display: block;
}
.lux-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.2rem;
    font-weight: 300;
    letter-spacing: 0.06em;
    color: var(--cream);
    margin: 0 0 6px 0;
    line-height: 1.1;
}
.lux-title em {
    font-style: italic;
    color: var(--gold2);
}
.lux-subtitle {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.68rem;
    font-weight: 300;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 10px;
}
.lux-divider {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-top: 28px;
    justify-content: center;
}
.lux-divider-line {
    height: 1px;
    width: 80px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
.lux-divider-gem {
    color: var(--gold);
    font-size: 0.7rem;
    letter-spacing: 0.1em;
}

/* ── Card container ── */
.lux-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 36px 40px;
    margin-bottom: 24px;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}
.lux-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}

/* ── Labels ── */
.lux-label {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.58rem;
    font-weight: 500;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.lux-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Textarea ── */
.stTextArea > div > div > textarea {
    background: rgba(11,22,40,0.6) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    color: var(--cream) !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.05rem !important;
    font-weight: 300 !important;
    letter-spacing: 0.02em !important;
    padding: 16px 20px !important;
    caret-color: var(--gold) !important;
    transition: border-color 0.3s ease !important;
    resize: none !important;
}
.stTextArea > div > div > textarea::placeholder {
    color: rgba(138,154,184,0.5) !important;
    font-style: italic !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 1px rgba(201,168,76,0.15), 0 4px 24px rgba(201,168,76,0.05) !important;
    outline: none !important;
}

/* ── Bouton principal ── */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold2) 100%) !important;
    color: var(--navy) !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.6rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.28em !important;
    text-transform: uppercase !important;
    padding: 14px 36px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(201,168,76,0.3) !important;
    width: 100% !important;
}
div.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 30px rgba(201,168,76,0.5) !important;
    transform: translateY(-1px) !important;
}
div.stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
}

/* ── Boutons exemples ── */
div.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: var(--muted) !important;
    border: 1px solid rgba(138,154,184,0.2) !important;
    border-radius: 2px !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.55rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.12em !important;
    padding: 8px 10px !important;
    transition: all 0.25s ease !important;
    white-space: nowrap !important;
}
div.stButton > button[kind="secondary"]:hover {
    border-color: var(--gold) !important;
    color: var(--gold2) !important;
    background: rgba(201,168,76,0.05) !important;
}

/* ── Résultat ── */
.result-wrapper {
    margin-top: 28px;
    position: relative;
}
.result-card {
    background: linear-gradient(135deg, var(--navy3) 0%, var(--navy2) 100%);
    border: 1px solid var(--gold);
    border-radius: 2px;
    padding: 36px 40px;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--gold), var(--gold2), var(--gold));
}
.result-card::after {
    content: '';
    position: absolute;
    bottom: -60px; right: -60px;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(201,168,76,0.06) 0%, transparent 70%);
}
.result-tag {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.55rem;
    font-weight: 500;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 20px;
    display: block;
}
.result-intent {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.4rem;
    font-weight: 300;
    letter-spacing: 0.04em;
    color: var(--cream);
    margin: 0 0 24px 0;
    line-height: 1.1;
}
.result-route {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.68rem;
    font-weight: 300;
    letter-spacing: 0.08em;
    color: var(--muted);
    border-top: 1px solid rgba(201,168,76,0.15);
    padding-top: 20px;
}
.result-route strong {
    color: var(--gold2);
    font-weight: 400;
}
.preprocessed-lux {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.6rem;
    font-weight: 300;
    letter-spacing: 0.08em;
    color: rgba(138,154,184,0.6);
    margin-top: 14px;
    padding: 12px 18px;
    border-left: 2px solid rgba(201,168,76,0.3);
    background: rgba(255,255,255,0.01);
    word-break: break-word;
}

/* ── Footer ── */
.lux-footer {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.55rem;
    font-weight: 300;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(138,154,184,0.4);
    margin-top: 64px;
    padding-top: 24px;
    border-top: 1px solid rgba(201,168,76,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.lux-footer-gem { color: var(--gold); opacity: 0.4; }

/* ── Masquer éléments Streamlit ── */
#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_assets():
    with open("best_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("tfidf_vectorizer (1).pkl", "rb") as f:
        vectorizer = pickle.load(f)
    with open("label_map.pkl", "rb") as f:
        label_map = pickle.load(f)
    return model, vectorizer, label_map


def preprocess(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english")) - {
        "not", "no", "never", "without", "wrong", "failed"
    }
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words and len(t) > 1]
    return " ".join(tokens)


# ── Header
st.markdown("""
<div class="lux-header">
    <span class="lux-eyebrow">Private Banking Intelligence</span>
    <h1 class="lux-title">Banking<em>77</em></h1>
    <p class="lux-subtitle">Automated Intent Classification System</p>
    <div class="lux-divider">
        <div class="lux-divider-line"></div>
        <span class="lux-divider-gem">◈</span>
        <div class="lux-divider-line"></div>
    </div>
</div>
""", unsafe_allow_html=True)

try:
    model, vectorizer, label_map = load_assets()
except FileNotFoundError as e:
    st.error(f"Fichier manquant : {e}")
    st.stop()

if "msg" not in st.session_state:
    st.session_state.msg = ""

EXAMPLES = [
    "Card not received",
    "Charged twice",
    "Card declined",
    "Lost my card",
    "Change currency",
]
EXAMPLES_FULL = [
    "I haven't received my card after 2 weeks",
    "Why was I charged twice for the same payment?",
    "My card was declined but I have enough funds",
    "I lost my card and need to block it immediately",
    "Can I change my account currency?",
]

# ── Card saisie
st.markdown('<div class="lux-card">', unsafe_allow_html=True)
st.markdown('<span class="lux-label">Quick scenarios</span>', unsafe_allow_html=True)

cols = st.columns(len(EXAMPLES))
for i, ex in enumerate(EXAMPLES):
    if cols[i].button(ex, key=f"ex_{i}"):
        st.session_state.msg = EXAMPLES_FULL[i]
        st.rerun()

st.markdown('<span class="lux-label" style="margin-top:28px;">Client message</span>', unsafe_allow_html=True)

user_input = st.text_area(
    label="client_message",
    value=st.session_state.msg,
    placeholder="Describe the client request in natural language...",
    height=130,
    label_visibility="collapsed",
)

st.markdown('</div>', unsafe_allow_html=True)

# ── Bouton
analyze = st.button("◈  Analyse intent", type="primary")

# ── Résultat
if analyze:
    if user_input.strip():
        cleaned    = preprocess(user_input)
        vectorized = vectorizer.transform([cleaned])
        pred_label  = model.predict(vectorized)[0]
        pred_intent = label_map.get(pred_label, "Unknown")
        intent_display = pred_intent.replace("_", " ").title()

        st.markdown(f"""
        <div class="result-wrapper">
            <div class="result-card">
                <span class="result-tag">Detected intent</span>
                <p class="result-intent">{intent_display}</p>
                <div class="result-route">
                    This request will be automatically routed to the
                    <strong>{intent_display}</strong> department.
                </div>
            </div>
            <div class="preprocessed-lux">
                Preprocessed tokens &rarr;&nbsp; {cleaned}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Please enter a client message before analysing.")

# ── Footer
model_name = type(model).__name__ if model else ""
st.markdown(f"""
<div class="lux-footer">
    <span>Banking77 &nbsp;·&nbsp; NLP Classification</span>
    <span class="lux-footer-gem">◈</span>
    <span>{model_name}</span>
</div>
""", unsafe_allow_html=True)
