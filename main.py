import streamlit as st
import anthropic
import time
import json
from datetime import datetime

# =============================================================
# 페이지 설정
# =============================================================
st.set_page_config(
    page_title="Claude AI Studio",
    page_icon="✦",
    layout="centered",
)

# =============================================================
# 프리미엄 CSS
# =============================================================
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }
code, pre, .stCode { font-family: 'JetBrains Mono', monospace !important; }

/* ── Animated Background ── */
.stApp {
    background: #050510;
    background-image:
        radial-gradient(ellipse 80% 50% at 10% -10%, rgba(124,58,237,0.18) 0%, transparent 55%),
        radial-gradient(ellipse 60% 45% at 90% 100%, rgba(6,182,212,0.12) 0%, transparent 55%),
        radial-gradient(ellipse 40% 30% at 50% 50%, rgba(168,85,247,0.06) 0%, transparent 50%);
    min-height: 100vh;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #7c3aed, #06b6d4);
    border-radius: 10px;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2rem 1rem 0.5rem;
    position: relative;
}
@keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: linear-gradient(90deg,
        rgba(124,58,237,0.15) 0%,
        rgba(6,182,212,0.25) 50%,
        rgba(124,58,237,0.15) 100%);
    background-size: 200% 100%;
    animation: shimmer 3s ease-in-out infinite;
    border: 1px solid rgba(124,58,237,0.25);
    padding: 0.4rem 1.2rem;
    border-radius: 50px;
    font-size: 0.72rem;
    color: #a5b4fc;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.hero h1 {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #fff 0%, #c4b5fd 40%, #67e8f9 80%, #fff 100%);
    background-size: 300% 300%;
    animation: shimmer 4s ease-in-out infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0.4rem 0;
    line-height: 1.15;
    letter-spacing: -0.03em;
}
.hero .subtitle {
    color: #525280;
    font-size: 0.95rem;
    font-weight: 400;
    max-width: 520px;
    margin: 0.6rem auto 0;
    line-height: 1.7;
}

/* ── Glass Card Base ── */
.glass {
    background: rgba(255,255,255,0.025);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 1.4rem;
    margin: 0.8rem 0;
    position: relative;
    overflow: hidden;
}
.glass::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 16px;
    padding: 1px;
    background: linear-gradient(135deg, rgba(255,255,255,0.08), transparent 50%, rgba(255,255,255,0.04));
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
}

/* ── Preset Chips ── */
.preset-section { margin: 0.8rem 0; }
.preset-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 0.5rem;
}
.preset-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 0.35rem 0.65rem;
    font-size: 0.72rem;
    color: #94a3b8;
    cursor: default;
    transition: all 0.2s;
}
.preset-chip.active {
    background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(6,182,212,0.15));
    border-color: rgba(124,58,237,0.4);
    color: #c4b5fd;
    font-weight: 600;
}

/* ── Model Selector Cards ── */
.model-selector {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
    margin: 0.6rem 0;
}
.model-option {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 0.7rem;
    text-align: center;
    transition: all 0.2s;
}
.model-option.selected {
    border-color: rgba(124,58,237,0.5);
    background: rgba(124,58,237,0.08);
    box-shadow: 0 0 20px rgba(124,58,237,0.1);
}
.model-option .mo-emoji { font-size: 1.2rem; }
.model-option .mo-name {
    font-size: 0.72rem;
    font-weight: 700;
    color: #c4b5fd;
    margin-top: 0.2rem;
}
.model-option .mo-tag {
    font-size: 0.6rem;
    color: #525280;
    margin-top: 0.1rem;
}

/* ── Parameter Display ── */
.param-display {
    display: flex;
    gap: 0.5rem;
    margin: 0.5rem 0;
}
.param-pill {
    flex: 1;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
    padding: 0.45rem;
    text-align: center;
}
.param-pill .pp-val {
    font-size: 0.95rem;
    font-weight: 800;
    color: #e2e8f0;
    font-family: 'JetBrains Mono', monospace;
}
.param-pill .pp-label {
    font-size: 0.6rem;
    color: #525280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Usage Card ── */
.usage-glass {
    background: rgba(124,58,237,0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(124,58,237,0.12);
    border-radius: 16px;
    padding: 1.3rem;
    margin: 1rem 0 0.5rem;
}
.card-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
}
.card-header .icon-box {
    width: 30px; height: 30px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
}
.icon-box.purple { background: linear-gradient(135deg, #7c3aed, #6d28d9); }
.icon-box.green  { background: linear-gradient(135deg, #059669, #0d9488); }
.icon-box.blue   { background: linear-gradient(135deg, #2563eb, #0ea5e9); }

.card-header .card-title {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #a78bfa;
}

.metric-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}
.metric-box {
    background: rgba(0,0,0,0.2);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 10px;
    padding: 0.7rem;
    text-align: center;
}
.metric-box .m-value {
    font-size: 1.15rem;
    font-weight: 800;
    color: #ffffff;
    font-family: 'JetBrains Mono', monospace;
}
.metric-box .m-label {
    font-size: 0.65rem;
    color: #525280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.15rem;
}
.metric-box.full {
    grid-column: span 2;
    background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(6,182,212,0.08));
    border-color: rgba(124,58,237,0.2);
}
.metric-box.full .m-value {
    background: linear-gradient(135deg, #c4b5fd, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 1.3rem;
}

/* ── Progress Bar ── */
.token-progress {
    margin: 0.8rem 0 0.3rem;
}
.progress-labels {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.3rem;
}
.progress-labels span {
    font-size: 0.65rem;
    color: #525280;
    font-weight: 500;
}
.progress-bar-bg {
    width: 100%;
    height: 6px;
    background: rgba(255,255,255,0.05);
    border-radius: 3px;
    overflow: hidden;
}
.progress-bar-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.5s ease;
}
.progress-bar-fill.input-bar {
    background: linear-gradient(90deg, #7c3aed, #a78bfa);
}
.progress-bar-fill.output-bar {
    background: linear-gradient(90deg, #06b6d4, #67e8f9);
}

/* ── Cost Card ── */
.cost-glass {
    background: rgba(16,185,129,0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(16,185,129,0.12);
    border-radius: 16px;
    padding: 1.3rem;
    margin: 0.5rem 0 1rem;
}
.cost-glass .card-title { color: #6ee7b7; }
.cost-line {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.45rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.03);
}
.cost-line:last-child {
    border-bottom: none;
    padding-top: 0.6rem;
    margin-top: 0.2rem;
    border-top: 1px solid rgba(16,185,129,0.15);
}
.cost-line .cl-label {
    color: #525280;
    font-size: 0.82rem;
    font-weight: 500;
}
.cost-line .cl-value {
    color: #cbd5e1;
    font-size: 0.88rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}
.cost-line:last-child .cl-value {
    color: #6ee7b7;
    font-size: 1rem;
}

/* ── Model & Time Badge ── */
.badge-row {
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
    margin-bottom: 0.6rem;
}
.inline-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-size: 0.68rem;
    font-weight: 600;
}
.badge-model {
    background: rgba(124,58,237,0.12);
    border: 1px solid rgba(124,58,237,0.25);
    color: #a78bfa;
}
.badge-time {
    background: rgba(251,191,36,0.1);
    border: 1px solid rgba(251,191,36,0.2);
    color: #fbbf24;
}
.badge-tokens {
    background: rgba(6,182,212,0.1);
    border: 1px solid rgba(6,182,212,0.2);
    color: #67e8f9;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #08081a, #0a0a20) !important;
    border-right: 1px solid rgba(255,255,255,0.04);
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #e2e8f0 !important;
    font-weight: 700;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] label {
    color: #94a3b8 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.05) !important;
}

/* Sidebar Stats */
.stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.4rem;
    margin: 0.5rem 0;
}
.stat-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 0.65rem;
    text-align: center;
}
.stat-card .sc-val {
    font-size: 1.1rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
}
.stat-card .sc-label {
    font-size: 0.6rem;
    color: #525280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.1rem;
}
.sc-val.v-purple {
    background: linear-gradient(135deg, #a78bfa, #c084fc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.sc-val.v-cyan {
    background: linear-gradient(135deg, #22d3ee, #67e8f9);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.sc-val.v-gold {
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.sc-val.v-green {
    background: linear-gradient(135deg, #34d399, #6ee7b7);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}

/* Sidebar Model Card */
.sb-model-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.06), rgba(6,182,212,0.04));
    border: 1px solid rgba(124,58,237,0.15);
    border-radius: 12px;
    padding: 0.9rem;
    margin: 0.5rem 0;
}
.sb-model-card .smc-name {
    color: #c4b5fd;
    font-size: 0.88rem;
    font-weight: 700;
}
.sb-model-card .smc-desc {
    color: #525280;
    font-size: 0.75rem;
    line-height: 1.5;
    margin-top: 0.2rem;
}
.sb-model-card .smc-prices {
    display: flex;
    gap: 0.4rem;
    margin-top: 0.5rem;
}
.sb-model-card .smc-price {
    background: rgba(0,0,0,0.25);
    border-radius: 6px;
    padding: 0.2rem 0.45rem;
    font-size: 0.65rem;
    color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Chat ── */
.stChatMessage {
    background: rgba(255,255,255,0.015) !important;
    border: 1px solid rgba(255,255,255,0.035) !important;
    border-radius: 16px !important;
    margin-bottom: 0.8rem !important;
}

/* ── Chat Input ── */
.stChatInput > div {
    border: 1px solid rgba(124,58,237,0.2) !important;
    border-radius: 14px !important;
    background: rgba(255,255,255,0.025) !important;
    transition: all 0.3s ease !important;
}
.stChatInput > div:focus-within {
    border-color: rgba(124,58,237,0.5) !important;
    box-shadow: 0 0 25px rgba(124,58,237,0.12), 0 0 50px rgba(124,58,237,0.05) !important;
}
.stChatInput textarea { color: #e2e8f0 !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    padding: 0.55rem 1rem !important;
    transition: all 0.25s ease !important;
    letter-spacing: 0.02em;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(124,58,237,0.3) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
.stDownloadButton > button {
    background: linear-gradient(135deg, #059669, #0d9488) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    transition: all 0.25s ease !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(5,150,105,0.3) !important;
}

/* ── TextArea / Slider / Radio ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.025) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 0.83rem !important;
}
.stTextArea textarea:focus {
    border-color: rgba(124,58,237,0.35) !important;
    box-shadow: 0 0 15px rgba(124,58,237,0.08) !important;
}

/* ── Empty State ── */
.empty-state {
    text-align: center;
    padding: 3.5rem 1rem;
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}
.empty-state .empty-icon {
    font-size: 3.5rem;
    display: inline-block;
    animation: float 3s ease-in-out infinite;
    margin-bottom: 1rem;
}
.empty-state .empty-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #64648a;
    margin-bottom: 0.5rem;
}
.empty-state .empty-desc {
    font-size: 0.88rem;
    color: #3a3a5a;
    max-width: 400px;
    margin: 0 auto;
    line-height: 1.7;
}
.empty-state .shortcut-hint {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
    padding: 0.35rem 0.8rem;
    margin-top: 1rem;
    font-size: 0.75rem;
    color: #525280;
}
.empty-state .shortcut-hint kbd {
    background: rgba(255,255,255,0.08);
    border-radius: 4px;
    padding: 0.1rem 0.4rem;
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    color: #a78bfa;
}

/* ── Footer ── */
.app-footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: #2a2a4a;
    font-size: 0.72rem;
    border-top: 1px solid rgba(255,255,255,0.03);
    margin-top: 3rem;
}
.app-footer a { color: #7c3aed; text-decoration: none; }
.app-footer a:hover { text-decoration: underline; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
}

/* ── Divider in sidebar ── */
.sidebar-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124,58,237,0.2), transparent);
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# =============================================================
# API 키
# =============================================================
def get_api_key():
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None

api_key = get_api_key()

# =============================================================
# 모델 정의
# =============================================================
MODELS = {
    "Claude 4 Opus": {
        "id": "claude-opus-4-20250514",
        "desc": "최고 성능 · 복잡한 추론 · 최상위 모델",
        "input_cost": 15.00,
        "output_cost": 75.00,
        "emoji": "👑",
        "tag": "MOST POWERFUL",
        "color": "#f59e0b",
    },
    "Claude 4 Sonnet": {
        "id": "claude-sonnet-4-20250514",
        "desc": "빠르고 똑똑한 · 가성비 최고 · 최신 모델",
        "input_cost": 3.00,
        "output_cost": 15.00,
        "emoji": "⚡",
        "tag": "RECOMMENDED",
        "color": "#a78bfa",
    },
    "Claude 3.5 Sonnet": {
        "id": "claude-3-5-sonnet-20241022",
        "desc": "안정적 · 검증된 범용 모델",
        "input_cost": 3.00,
        "output_cost": 15.00,
        "emoji": "🎯",
        "tag": "STABLE",
        "color": "#60a5fa",
    },
    "Claude 3.5 Haiku": {
        "id": "claude-3-5-haiku-20241022",
        "desc": "초고속 · 가벼운 작업에 최적 · 저렴",
        "input_cost": 0.80,
        "output_cost": 4.00,
        "emoji": "🚀",
        "tag": "FASTEST",
        "color": "#34d399",
    },
}

# =============================================================
# 프리셋
# =============================================================
PRESETS = {
    "📚 학습 도우미": {
        "prompt": "당신은 고등학생의 학습을 돕는 친절한 튜터입니다. 개념을 쉽게 설명하고, 단계별로 풀이를 안내하며, 학생이 스스로 이해할 수 있도록 도와주세요. 한국어로 답변합니다.",
        "temp": 0.5,
    },
    "💻 코딩 전문가": {
        "prompt": "당신은 프로그래밍 전문가입니다. 코드를 작성할 때는 주석을 꼼꼼히 달고, 왜 그렇게 작성했는지 설명해주세요. 에러가 있으면 원인과 해결법을 친절히 알려주세요. 한국어로 답변합니다.",
        "temp": 0.3,
    },
    "🌍 영어 선생님": {
        "prompt": "당신은 한국 고등학생을 위한 영어 선생님입니다. 문법, 어휘, 독해, 작문을 도와주세요. 영어 표현을 설명할 때는 예문과 함께 한국어로 설명합니다.",
        "temp": 0.5,
    },
    "🔢 수학 튜터": {
        "prompt": "당신은 수학 전문 튜터입니다. 문제를 단계별로 풀어주고, 각 단계의 이유를 설명해주세요. 공식을 사용할 때는 왜 그 공식을 쓰는지도 알려주세요. 한국어로 답변합니다.",
        "temp": 0.2,
    },
    "✨ 자유 모드": {
        "prompt": "당신은 도움이 되는 AI 어시스턴트입니다. 한국어로 답변합니다.",
        "temp": 0.7,
    },
}

# =============================================================
# 세션 상태
# =============================================================
defaults = {
    "messages": [],
    "total_input_tokens": 0,
    "total_output_tokens": 0,
    "total_cost": 0.0,
    "conversation_count": 0,
    "selected_preset": "📚 학습 도우미",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =============================================================
# 대화 내보내기 함수
# =============================================================
def export_markdown():
    lines = [f"# Claude AI Studio — 대화 기록\n"]
    lines.append(f"- 내보내기 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append(f"- 총 대화: {st.session_state.conversation_count}회\n")
    lines.append(f"- 총 토큰: {st.session_state.total_input_tokens + st.session_state.total_output_tokens:,}\n")
    lines.append(f"- 총 비용: ${st.session_state.total_cost:.6f}\n\n---\n")
    for msg in st.session_state.messages:
        role = "🧑 사용자" if msg["role"] == "user" else "🤖 Claude"
        lines.append(f"\n### {role}\n\n{msg['content']}\n")
        if msg["role"] == "assistant" and "usage" in msg:
            u = msg["usage"]
            lines.append(f"\n> 📊 입력 {u['input_tokens']:,} + 출력 {u['output_tokens']:,} = {u['input_tokens']+u['output_tokens']:,} 토큰 · ${u['total_cost']:.6f}\n")
    return "\n".join(lines)

def export_json():
    data = {
        "exported_at": datetime.now().isoformat(),
        "stats": {
            "conversations": st.session_state.conversation_count,
            "total_input_tokens": st.session_state.total_input_tokens,
            "total_output_tokens": st.session_state.total_output_tokens,
            "total_cost": st.session_state.total_cost,
        },
        "messages": st.session_state.messages,
    }
    return json.dumps(data, ensure_ascii=False, indent=2)

# =============================================================
# 사이드바
# =============================================================
with st.sidebar:
    st.markdown("## ✦ Studio")

    # ── 모델 선택 ──
    st.markdown("#### 🧠 Model")
    selected_model_name = st.radio(
        "모델 선택",
        options=list(MODELS.keys()),
        index=1,
        label_visibility="collapsed",
    )
    mi = MODELS[selected_model_name]

    st.markdown(f"""
    <div class="sb-model-card">
        <div class="smc-name">{mi['emoji']} {selected_model_name}
            <span style="font-size:0.6rem; background:rgba(255,255,255,0.06); padding:0.1rem 0.4rem;
                border-radius:4px; margin-left:0.3rem; color:{mi['color']}">{mi['tag']}</span>
        </div>
        <div class="smc-desc">{mi['desc']}</div>
        <div class="smc-prices">
            <span class="smc-price">IN ${mi['input_cost']:.2f}/1M</span>
            <span class="smc-price">OUT ${mi['output_cost']:.2f}/1M</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 프리셋 ──
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown("#### 📌 Preset")
    preset_choice = st.radio(
        "프리셋 선택",
        options=list(PRESETS.keys()),
        index=list(PRESETS.keys()).index(st.session_state.selected_preset),
        label_visibility="collapsed",
    )
    st.session_state.selected_preset = preset_choice
    preset = PRESETS[preset_choice]

    # ── 파라미터 ──
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown("#### 🎛️ Parameters")

    system_prompt = st.text_area(
        "System Prompt",
        value=preset["prompt"],
        height=100,
    )

    temperature = st.slider(
        "🌡️ Temperature",
        min_value=0.0,
        max_value=1.0,
        value=preset["temp"],
        step=0.05,
        help="낮을수록 정확하고, 높을수록 창의적",
    )

    top_p = st.slider(
        "🎲 Top-P",
        min_value=0.0,
        max_value=1.0,
        value=0.95,
        step=0.05,
    )

    max_tokens = st.slider(
        "📏 Max Tokens",
        min_value=256,
        max_value=8192,
        value=2048,
        step=256,
    )

    st.markdown(f"""
    <div class="param-display">
        <div class="param-pill">
            <div class="pp-val">{temperature}</div>
            <div class="pp-label">Temp</div>
        </div>
        <div class="param-pill">
            <div class="pp-val">{top_p}</div>
            <div class="pp-label">Top-P</div>
        </div>
        <div class="param-pill">
            <div class="pp-val">{max_tokens}</div>
            <div class="pp-label">Max Tok</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 통계 ──
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown("#### 📊 Session Stats")

    total_tok = st.session_state.total_input_tokens + st.session_state.total_output_tokens
    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="sc-val v-purple">{st.session_state.conversation_count}</div>
            <div class="sc-label">대화</div>
        </div>
        <div class="stat-card">
            <div class="sc-val v-cyan">{total_tok:,}</div>
            <div class="sc-label">총 토큰</div>
        </div>
        <div class="stat-card">
            <div class="sc-val v-gold">{st.session_state.total_input_tokens:,}</div>
            <div class="sc-label">입력 토큰</div>
        </div>
        <div class="stat-card">
            <div class="sc-val v-green">{st.session_state.total_output_tokens:,}</div>
            <div class="sc-label">출력 토큰</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 비용
    st.markdown(f"""
    <div style="text-align:center; margin:0.6rem 0;">
        <div style="font-size:0.65rem; color:#525280; text-transform:uppercase; letter-spacing:0.08em;">
            총 예상 비용
        </div>
        <div style="font-size:1.4rem; font-weight:900; font-family:'JetBrains Mono',monospace;
            background:linear-gradient(135deg,#fbbf24,#f59e0b);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">
            ${st.session_state.total_cost:.4f}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 내보내기 / 초기화 ──
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown("#### 📥 Export & Reset")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.session_state.messages:
            st.download_button(
                "📄 MD",
                data=export_markdown(),
                file_name=f"claude_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                use_container_width=True,
            )
    with col_b:
        if st.session_state.messages:
            st.download_button(
                "📋 JSON",
                data=export_json(),
                file_name=f"claude_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                use_container_width=True,
            )

    st.markdown("")
    if st.button("🗑️ 전체 초기화", use_container_width=True):
        for k, v in defaults.items():
            st.session_state[k] = v
        st.rerun()

# =============================================================
# 히어로
# =============================================================
st.markdown(f"""
<div class="hero">
    <div class="hero-badge">✦ ULTIMATE EDITION · {mi['emoji']} {selected_model_name}</div>
    <h1>Claude AI Studio</h1>
    <p class="subtitle">당곡고등학교 학습 도우미 — 스트리밍 응답 · 토큰 분석 · 대화 내보내기</p>
</div>
""", unsafe_allow_html=True)

# API 키 확인
if not api_key:
    st.error("""
    ⚠️ **API 키가 설정되지 않았습니다!**

    **Streamlit Cloud:** Settings → Secrets
    ```
    ANTHROPIC_API_KEY = "sk-ant-api03-..."
    ```
    **로컬:** `.streamlit/secrets.toml`에 동일하게 추가
    """)
    st.stop()

# =============================================================
# Claude 클라이언트
# =============================================================
client = anthropic.Anthropic(api_key=api_key)

# =============================================================
# 이전 메시지
# =============================================================
if not st.session_state.messages:
    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-icon">✦</div>
        <div class="empty-title">대화를 시작해보세요</div>
        <div class="empty-desc">
            현재 <strong style="color:#c4b5fd">{selected_model_name}</strong>
            모델이 선택되어 있고,
            <strong style="color:#c4b5fd">{preset_choice}</strong> 모드로 설정되어 있습니다.
        </div>
        <div class="shortcut-hint">
            <kbd>Enter</kbd> 키로 메시지를 전송하세요
        </div>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg["role"] == "assistant" and "usage" in msg:
            u = msg["usage"]
            total_t = u['input_tokens'] + u['output_tokens']
            max_display = max(u['input_tokens'], u['output_tokens'], 1)
            inp_pct = min((u['input_tokens'] / max_display) * 100, 100)
            out_pct = min((u['output_tokens'] / max_display) * 100, 100)

            st.markdown(f"""
            <div class="badge-row">
                <span class="inline-badge badge-model">{u.get('model_emoji','')} {u.get('model_name','')}</span>
                <span class="inline-badge badge-time">⏱ {u.get('elapsed',0):.1f}s</span>
                <span class="inline-badge badge-tokens">◈ {total_t:,} tokens</span>
            </div>

            <div class="usage-glass">
                <div class="card-header">
                    <div class="icon-box purple">📊</div>
                    <div class="card-title">Token Usage</div>
                </div>
                <div class="metric-row">
                    <div class="metric-box">
                        <div class="m-value">{u['input_tokens']:,}</div>
                        <div class="m-label">📥 Input</div>
                    </div>
                    <div class="metric-box">
                        <div class="m-value">{u['output_tokens']:,}</div>
                        <div class="m-label">📤 Output</div>
                    </div>
                </div>
                <div class="metric-row">
                    <div class="metric-box full">
                        <div class="m-value">{total_t:,}</div>
                        <div class="m-label">Total Tokens</div>
                    </div>
                </div>
                <div class="token-progress">
                    <div class="progress-labels">
                        <span>Input</span>
                        <span>{u['input_tokens']:,}</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill input-bar" style="width:{inp_pct}%"></div>
                    </div>
                </div>
                <div class="token-progress">
                    <div class="progress-labels">
                        <span>Output</span>
                        <span>{u['output_tokens']:,}</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill output-bar" style="width:{out_pct}%"></div>
                    </div>
                </div>
            </div>

            <div class="cost-glass">
                <div class="card-header">
                    <div class="icon-box green">💰</div>
                    <div class="card-title" style="color:#6ee7b7">Estimated Cost</div>
                </div>
                <div class="cost-line">
                    <span class="cl-label">입력 비용</span>
                    <span class="cl-value">${u['input_cost']:.6f}</span>
                </div>
                <div class="cost-line">
                    <span class="cl-label">출력 비용</span>
                    <span class="cl-value">${u['output_cost']:.6f}</span>
                </div>
                <div class="cost-line">
                    <span class="cl-label">합계</span>
                    <span class="cl-value">${u['total_cost']:.6f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# =============================================================
# 사용자 입력 & 스트리밍 응답
# =============================================================
if prompt := st.chat_input("✦ 질문을 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            start_time = time.time()

            api_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
                if m["role"] in ("user", "assistant")
            ]

            # 스트리밍 응답
            collected_text = ""
            input_tokens = 0
            output_tokens = 0
            text_placeholder = st.empty()
            status_placeholder = st.empty()

            status_placeholder.markdown(f"*✦ {selected_model_name} 응답 생성 중...*")

            with client.messages.stream(
                model=mi["id"],
                max_tokens=max_tokens,
                system=system_prompt,
                temperature=temperature,
                top_p=top_p,
                messages=api_messages,
            ) as stream:
                for event in stream:
                    if hasattr(event, 'type'):
                        if event.type == 'content_block_delta':
                            if hasattr(event.delta, 'text'):
                                collected_text += event.delta.text
                                text_placeholder.markdown(collected_text + "▌")
                        elif event.type == 'message_start':
                            if hasattr(event.message, 'usage'):
                                input_tokens = event.message.usage.input_tokens
                        elif event.type == 'message_delta':
                            if hasattr(event.usage, 'output_tokens'):
                                output_tokens = event.usage.output_tokens

            # 스트리밍 완료
            text_placeholder.markdown(collected_text)
            status_placeholder.empty()

            elapsed = time.time() - start_time

            # 비용 계산
            ic = (input_tokens / 1_000_000) * mi["input_cost"]
            oc = (output_tokens / 1_000_000) * mi["output_cost"]
            tc = ic + oc
            total_t = input_tokens + output_tokens

            # 세션 누적
            st.session_state.total_input_tokens += input_tokens
            st.session_state.total_output_tokens += output_tokens
            st.session_state.total_cost += tc
            st.session_state.conversation_count += 1

            # 프로그레스 바 비율
            max_display = max(input_tokens, output_tokens, 1)
            inp_pct = min((input_tokens / max_display) * 100, 100)
            out_pct = min((output_tokens / max_display) * 100, 100)

            # 사용량 표시
            st.markdown(f"""
            <div class="badge-row">
                <span class="inline-badge badge-model">{mi['emoji']} {selected_model_name}</span>
                <span class="inline-badge badge-time">⏱ {elapsed:.1f}s</span>
                <span class="inline-badge badge-tokens">◈ {total_t:,} tokens</span>
            </div>

            <div class="usage-glass">
                <div class="card-header">
                    <div class="icon-box purple">📊</div>
                    <div class="card-title">Token Usage</div>
                </div>
                <div class="metric-row">
                    <div class="metric-box">
                        <div class="m-value">{input_tokens:,}</div>
                        <div class="m-label">📥 Input</div>
                    </div>
                    <div class="metric-box">
                        <div class="m-value">{output_tokens:,}</div>
                        <div class="m-label">📤 Output</div>
                    </div>
                </div>
                <div class="metric-row">
                    <div class="metric-box full">
                        <div class="m-value">{total_t:,}</div>
                        <div class="m-label">Total Tokens</div>
                    </div>
                </div>
                <div class="token-progress">
                    <div class="progress-labels">
                        <span>Input</span>
                        <span>{input_tokens:,}</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill input-bar" style="width:{inp_pct}%"></div>
                    </div>
                </div>
                <div class="token-progress">
                    <div class="progress-labels">
                        <span>Output</span>
                        <span>{output_tokens:,}</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill output-bar" style="width:{out_pct}%"></div>
                    </div>
                </div>
            </div>

            <div class="cost-glass">
                <div class="card-header">
                    <div class="icon-box green">💰</div>
                    <div class="card-title" style="color:#6ee7b7">Estimated Cost</div>
                </div>
                <div class="cost-line">
                    <span class="cl-label">입력 비용</span>
                    <span class="cl-value">${ic:.6f}</span>
                </div>
                <div class="cost-line">
                    <span class="cl-label">출력 비용</span>
                    <span class="cl-value">${oc:.6f}</span>
                </div>
                <div class="cost-line">
                    <span class="cl-label">합계</span>
                    <span class="cl-value">${tc:.6f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 메시지 저장
            st.session_state.messages.append({
                "role": "assistant",
                "content": collected_text,
                "usage": {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "input_cost": ic,
                    "output_cost": oc,
                    "total_cost": tc,
                    "elapsed": elapsed,
                    "model_name": selected_model_name,
                    "model_emoji": mi["emoji"],
                }
            })

        except anthropic.AuthenticationError:
            st.error("🔑 API 키가 유효하지 않습니다. Secrets 설정을 확인해주세요.")
        except anthropic.RateLimitError:
            st.error("⏳ 요청 한도 초과. 잠시 후 다시 시도해주세요.")
        except anthropic.APIError as e:
            st.error(f"❌ API 오류: {str(e)}")
        except Exception as e:
            st.error(f"❌ 오류: {str(e)}")

# =============================================================
# 푸터
# =============================================================
st.markdown("""
<div class="app-footer">
    ✦ Claude AI Studio · Ultimate Edition<br>
    당곡고등학교 학습 도우미<br><br>
    Built with <a href="https://streamlit.io">Streamlit</a> ·
    <a href="https://anthropic.com">Anthropic Claude API</a>
</div>
""", unsafe_allow_html=True)
