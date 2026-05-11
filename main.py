import streamlit as st
import anthropic
import time

# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title="Claude AI Studio",
    page_icon="✦",
    layout="centered",
)

# ============================================================
# 프리미엄 CSS 디자인
# ============================================================
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── 전역 리셋 ── */
* { font-family: 'Inter', sans-serif; }
code, .stCode { font-family: 'JetBrains Mono', monospace !important; }

/* ── 배경 애니메이션 ── */
.stApp {
    background: #050510;
    background-image:
        radial-gradient(ellipse 80% 60% at 20% 0%, rgba(88, 28, 255, 0.15) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 100%, rgba(0, 200, 255, 0.10) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 50% 50%, rgba(139, 92, 246, 0.05) 0%, transparent 60%);
}

/* ── 스크롤바 ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #7c3aed, #2563eb);
    border-radius: 3px;
}

/* ── 히어로 헤더 ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(37,99,235,0.2));
    border: 1px solid rgba(124,58,237,0.3);
    padding: 0.35rem 1rem;
    border-radius: 50px;
    font-size: 0.75rem;
    color: #a78bfa;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero h1 {
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0.5rem 0;
    line-height: 1.2;
    letter-spacing: -0.02em;
}
.hero .subtitle {
    color: #64648a;
    font-size: 1rem;
    font-weight: 400;
    max-width: 500px;
    margin: 0.5rem auto 0;
    line-height: 1.6;
}

/* ── 글래스 카드 ── */
.glass {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 0.8rem 0;
    position: relative;
    overflow: hidden;
}
.glass::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
}

/* ── 사용량 카드 ── */
.usage-glass {
    background: rgba(124, 58, 237, 0.06);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(124, 58, 237, 0.15);
    border-radius: 16px;
    padding: 1.4rem;
    margin: 1rem 0;
}
.usage-glass .card-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
}
.usage-glass .card-header .icon {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
}
.usage-glass .card-header .title {
    color: #c4b5fd;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
}
.metric-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 0.8rem;
    text-align: center;
}
.metric-item .value {
    font-size: 1.2rem;
    font-weight: 800;
    color: #ffffff;
    font-family: 'JetBrains Mono', monospace;
}
.metric-item .label {
    font-size: 0.7rem;
    color: #64648a;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.2rem;
}
.metric-item.highlight {
    background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(37,99,235,0.15));
    border-color: rgba(124,58,237,0.3);
}
.metric-item.highlight .value {
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── 비용 카드 ── */
.cost-glass {
    background: rgba(16, 185, 129, 0.06);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(16, 185, 129, 0.15);
    border-radius: 16px;
    padding: 1.4rem;
    margin: 0.5rem 0 1rem;
}
.cost-glass .card-header .icon {
    background: linear-gradient(135deg, #059669, #0d9488);
}
.cost-glass .card-header .title {
    color: #6ee7b7;
}
.cost-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.cost-item:last-child {
    border-bottom: none;
    padding-top: 0.7rem;
    margin-top: 0.3rem;
    border-top: 1px solid rgba(16,185,129,0.2);
}
.cost-item .cost-label {
    color: #64648a;
    font-size: 0.85rem;
    font-weight: 500;
}
.cost-item .cost-value {
    color: #e2e8f0;
    font-size: 0.9rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}
.cost-item:last-child .cost-value {
    color: #6ee7b7;
    font-size: 1rem;
}

/* ── 시간 배지 ── */
.time-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(251, 191, 36, 0.1);
    border: 1px solid rgba(251, 191, 36, 0.2);
    padding: 0.25rem 0.7rem;
    border-radius: 50px;
    font-size: 0.75rem;
    color: #fbbf24;
    font-weight: 600;
    margin-bottom: 0.8rem;
}

/* ── 사이드바 ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0a1a 0%, #0d0d24 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.05);
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #e2e8f0 !important;
    font-weight: 700;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li {
    color: #94a3b8 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.06) !important;
}

/* 사이드바 모델 카드 */
.model-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.08), rgba(37,99,235,0.08));
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.6rem 0;
}
.model-card .model-name {
    color: #c4b5fd;
    font-size: 0.9rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}
.model-card .model-desc {
    color: #64648a;
    font-size: 0.78rem;
    line-height: 1.5;
}
.model-card .model-pricing {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.6rem;
}
.model-card .price-tag {
    background: rgba(255,255,255,0.05);
    border-radius: 6px;
    padding: 0.25rem 0.5rem;
    font-size: 0.7rem;
    color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
}

/* 사이드바 스탯 */
.stat-row {
    display: flex;
    justify-content: space-between;
    gap: 0.5rem;
    margin: 0.5rem 0;
}
.stat-box {
    flex: 1;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 0.7rem;
    text-align: center;
}
.stat-box .stat-num {
    font-size: 1.2rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    color: #e2e8f0;
}
.stat-box .stat-label {
    font-size: 0.65rem;
    color: #64648a;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.15rem;
}
.stat-box.purple .stat-num {
    background: linear-gradient(135deg, #a78bfa, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-box.blue .stat-num {
    background: linear-gradient(135deg, #60a5fa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-box.gold .stat-num {
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── 채팅 메시지 ── */
.stChatMessage {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.04) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    margin-bottom: 1rem !important;
}

/* ── 입력창 ── */
.stChatInput > div {
    border: 1px solid rgba(124,58,237,0.3) !important;
    border-radius: 14px !important;
    background: rgba(255,255,255,0.03) !important;
}
.stChatInput > div:focus-within {
    border-color: rgba(124,58,237,0.6) !important;
    box-shadow: 0 0 20px rgba(124,58,237,0.15) !important;
}
.stChatInput textarea {
    color: #e2e8f0 !important;
}

/* ── 라디오 버튼 ── */
.stRadio > label {
    color: #c4b5fd !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}
.stRadio > div > label {
    color: #94a3b8 !important;
}
.stRadio > div > label[data-checked="true"] {
    color: #e2e8f0 !important;
}

/* ── 텍스트 에리어 ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 0.85rem !important;
}
.stTextArea textarea:focus {
    border-color: rgba(124,58,237,0.4) !important;
    box-shadow: 0 0 15px rgba(124,58,237,0.1) !important;
}
.stTextArea label {
    color: #94a3b8 !important;
}

/* ── 슬라이더 ── */
.stSlider label { color: #94a3b8 !important; }
.stSlider [data-testid="stThumbValue"] { color: #c4b5fd !important; }

/* ── 버튼 ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.02em;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.35) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── 에러/경고 박스 ── */
.stAlert {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important;
}

/* ── 푸터 ── */
.app-footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: #3a3a5a;
    font-size: 0.75rem;
    border-top: 1px solid rgba(255,255,255,0.04);
    margin-top: 2rem;
}
.app-footer a {
    color: #7c3aed;
    text-decoration: none;
}

/* ── 안내 카드 (사이드바) ── */
.guide-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 0.8rem;
    margin: 0.3rem 0;
}
.guide-card .step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 20px; height: 20px;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    border-radius: 50%;
    font-size: 0.65rem;
    font-weight: 800;
    color: white;
    margin-right: 0.4rem;
}
.guide-card .step-text {
    color: #94a3b8;
    font-size: 0.8rem;
}

/* ── 스피너 ── */
.stSpinner > div {
    color: #a78bfa !important;
}

/* ── 빈 채팅 상태 ── */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #3a3a5a;
}
.empty-state .empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}
.empty-state .empty-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #64648a;
    margin-bottom: 0.5rem;
}
.empty-state .empty-desc {
    font-size: 0.85rem;
    color: #4a4a6a;
    max-width: 350px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── 모델 뱃지 (채팅) ── */
.model-badge-inline {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(124,58,237,0.12);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 6px;
    padding: 0.15rem 0.5rem;
    font-size: 0.7rem;
    color: #a78bfa;
    font-weight: 600;
    margin-bottom: 0.6rem;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# API 키 로드
# ============================================================
def get_api_key():
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None

api_key = get_api_key()

# ============================================================
# 모델 정보
# ============================================================
MODELS = {
    "Claude 4 Sonnet": {
        "id": "claude-sonnet-4-20250514",
        "description": "최신 모델 · 빠르고 정확한 응답",
        "input_cost_per_1m": 3.00,
        "output_cost_per_1m": 15.00,
        "badge": "⚡ LATEST",
        "emoji": "⚡",
    },
    "Claude 3.5 Sonnet": {
        "id": "claude-3-5-sonnet-20241022",
        "description": "안정적 · 균형 잡힌 범용 모델",
        "input_cost_per_1m": 3.00,
        "output_cost_per_1m": 15.00,
        "badge": "🎯 STABLE",
        "emoji": "🎯",
    },
}

# ============================================================
# 세션 상태
# ============================================================
defaults = {
    "messages": [],
    "total_input_tokens": 0,
    "total_output_tokens": 0,
    "total_cost": 0.0,
    "conversation_count": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# 사이드바
# ============================================================
with st.sidebar:
    st.markdown("## ✦ Studio Settings")

    # 모델 선택
    selected_model_name = st.radio(
        "🧠 Model",
        options=list(MODELS.keys()),
        index=0,
    )
    mi = MODELS[selected_model_name]

    st.markdown(f"""
    <div class="model-card">
        <div class="model-name">{mi['emoji']} {selected_model_name}</div>
        <div class="model-desc">{mi['description']}</div>
        <div class="model-pricing">
            <span class="price-tag">IN ${mi['input_cost_per_1m']:.0f}/1M</span>
            <span class="price-tag">OUT ${mi['output_cost_per_1m']:.0f}/1M</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    system_prompt = st.text_area(
        "📝 System Prompt",
        value="당신은 친절하고 도움이 되는 AI 어시스턴트입니다. 한국어로 답변해주세요.",
        height=100,
    )

    max_tokens = st.slider(
        "📏 Max Tokens",
        min_value=256,
        max_value=8192,
        value=2048,
        step=256,
    )

    st.markdown("---")
    st.markdown("### 📊 Session Stats")

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-box purple">
            <div class="stat-num">{st.session_state.conversation_count}</div>
            <div class="stat-label">대화</div>
        </div>
        <div class="stat-box blue">
            <div class="stat-num">{st.session_state.total_input_tokens + st.session_state.total_output_tokens:,}</div>
            <div class="stat-label">토큰</div>
        </div>
    </div>
    <div class="stat-row">
        <div class="stat-box gold">
            <div class="stat-num">${st.session_state.total_cost:.4f}</div>
            <div class="stat-label">예상 비용</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    if st.button("🗑️ 대화 초기화", use_container_width=True):
        for k, v in defaults.items():
            st.session_state[k] = v
        st.rerun()

    st.markdown("---")
    st.markdown("### 📖 How to Use")
    st.markdown("""
    <div class="guide-card">
        <span class="step-num">1</span>
        <span class="step-text">모델을 선택합니다</span>
    </div>
    <div class="guide-card">
        <span class="step-num">2</span>
        <span class="step-text">하단 입력창에 질문을 작성합니다</span>
    </div>
    <div class="guide-card">
        <span class="step-num">3</span>
        <span class="step-text">AI 응답과 사용량을 확인합니다</span>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 메인 히어로
# ============================================================
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ Powered by Anthropic Claude API</div>
    <h1>Claude AI Studio</h1>
    <p class="subtitle">당곡고등학교 학습 도우미 — 질문을 입력하면 AI가 답변해드립니다</p>
</div>
""", unsafe_allow_html=True)

# API 키 확인
if not api_key:
    st.error("""
    ⚠️ **API 키가 설정되지 않았습니다!**

    **Streamlit Cloud:** 앱 Settings → Secrets에 아래 내용 추가
    ```
    ANTHROPIC_API_KEY = "sk-ant-api03-..."
    ```

    **로컬 테스트:** `.streamlit/secrets.toml` 파일에 동일하게 추가
    """)
    st.stop()

# ============================================================
# Claude 클라이언트
# ============================================================
client = anthropic.Anthropic(api_key=api_key)

# ============================================================
# 이전 메시지 표시
# ============================================================
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">✦</div>
        <div class="empty-title">대화를 시작해보세요</div>
        <div class="empty-desc">
            아래 입력창에 궁금한 것을 물어보세요.
            Claude AI가 친절하게 답변해드립니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg["role"] == "assistant" and "usage" in msg:
            u = msg["usage"]
            st.markdown(f"""
            <span class="model-badge-inline">{u.get('model_emoji','')} {u.get('model_name','')}</span>
            <span class="time-badge">⏱ {u.get('elapsed', 0):.1f}s</span>

            <div class="usage-glass">
                <div class="card-header">
                    <div class="icon">📊</div>
                    <div class="title">Token Usage</div>
                </div>
                <div class="metric-grid">
                    <div class="metric-item">
                        <div class="value">{u['input_tokens']:,}</div>
                        <div class="label">입력 토큰</div>
                    </div>
                    <div class="metric-item">
                        <div class="value">{u['output_tokens']:,}</div>
                        <div class="label">출력 토큰</div>
                    </div>
                    <div class="metric-item highlight" style="grid-column: span 2;">
                        <div class="value">{u['input_tokens'] + u['output_tokens']:,}</div>
                        <div class="label">총 사용 토큰</div>
                    </div>
                </div>
            </div>

            <div class="cost-glass">
                <div class="card-header">
                    <div class="icon">💰</div>
                    <div class="title">Estimated Cost</div>
                </div>
                <div class="cost-item">
                    <span class="cost-label">입력 비용</span>
                    <span class="cost-value">${u['input_cost']:.6f}</span>
                </div>
                <div class="cost-item">
                    <span class="cost-label">출력 비용</span>
                    <span class="cost-value">${u['output_cost']:.6f}</span>
                </div>
                <div class="cost-item">
                    <span class="cost-label">합계</span>
                    <span class="cost-value">${u['total_cost']:.6f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# 입력 처리
# ============================================================
if prompt := st.chat_input("✦ 질문을 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"✦ {selected_model_name} 응답 생성 중..."):
            try:
                start_time = time.time()

                api_messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                    if m["role"] in ("user", "assistant")
                ]

                response = client.messages.create(
                    model=mi["id"],
                    max_tokens=max_tokens,
                    system=system_prompt,
                    messages=api_messages,
                )

                elapsed = time.time() - start_time
                text = response.content[0].text
                inp = response.usage.input_tokens
                out = response.usage.output_tokens
                ic = (inp / 1_000_000) * mi["input_cost_per_1m"]
                oc = (out / 1_000_000) * mi["output_cost_per_1m"]
                tc = ic + oc

                st.session_state.total_input_tokens += inp
                st.session_state.total_output_tokens += out
                st.session_state.total_cost += tc
                st.session_state.conversation_count += 1

                # 응답 표시
                st.markdown(text)

                st.markdown(f"""
                <span class="model-badge-inline">{mi['emoji']} {selected_model_name}</span>
                <span class="time-badge">⏱ {elapsed:.1f}s</span>

                <div class="usage-glass">
                    <div class="card-header">
                        <div class="icon">📊</div>
                        <div class="title">Token Usage</div>
                    </div>
                    <div class="metric-grid">
                        <div class="metric-item">
                            <div class="value">{inp:,}</div>
                            <div class="label">입력 토큰</div>
                        </div>
                        <div class="metric-item">
                            <div class="value">{out:,}</div>
                            <div class="label">출력 토큰</div>
                        </div>
                        <div class="metric-item highlight" style="grid-column: span 2;">
                            <div class="value">{inp + out:,}</div>
                            <div class="label">총 사용 토큰</div>
                        </div>
                    </div>
                </div>

                <div class="cost-glass">
                    <div class="card-header">
                        <div class="icon">💰</div>
                        <div class="title">Estimated Cost</div>
                    </div>
                    <div class="cost-item">
                        <span class="cost-label">입력 비용</span>
                        <span class="cost-value">${ic:.6f}</span>
                    </div>
                    <div class="cost-item">
                        <span class="cost-label">출력 비용</span>
                        <span class="cost-value">${oc:.6f}</span>
                    </div>
                    <div class="cost-item">
                        <span class="cost-label">합계</span>
                        <span class="cost-value">${tc:.6f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": text,
                    "usage": {
                        "input_tokens": inp,
                        "output_tokens": out,
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
                st.error("⏳ API 요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요.")
            except anthropic.APIError as e:
                st.error(f"❌ API 오류: {str(e)}")
            except Exception as e:
                st.error(f"❌ 예상치 못한 오류: {str(e)}")

# ============================================================
# 푸터
# ============================================================
st.markdown("""
<div class="app-footer">
    ✦ Claude AI Studio · 당곡고등학교 학습 도우미<br>
    Built with <a href="https://streamlit.io" target="_blank">Streamlit</a> + 
    <a href="https://anthropic.com" target="_blank">Anthropic Claude API</a>
</div>
""", unsafe_allow_html=True)
