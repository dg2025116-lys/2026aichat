import streamlit as st
import anthropic
import time

# ============================================================
# 페이지 기본 설정
# ============================================================
st.set_page_config(
    page_title="🤖 Claude AI 질문 앱",
    page_icon="🤖",
    layout="centered",
)

# ============================================================
# 커스텀 CSS - 깔끔한 UI
# ============================================================
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }

    /* 메인 헤더 */
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
    }
    .main-header h1 {
        color: #ffffff;
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }
    .main-header p {
        color: #a0a0c0;
        font-size: 1.05rem;
    }

    /* 사이드바 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a3e, #16163a);
    }
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #c0c0ff;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li {
        color: #b0b0d0;
        font-size: 0.9rem;
    }

    /* 사용량 카드 */
    .usage-card {
        background: linear-gradient(135deg, #1e1e50, #2a2a60);
        border: 1px solid #4a4a8a;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
    }
    .usage-card h4 {
        color: #8888ff;
        margin: 0 0 0.8rem 0;
        font-size: 1rem;
    }
    .usage-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.4rem 0;
        border-bottom: 1px solid #3a3a6a;
    }
    .usage-row:last-child {
        border-bottom: none;
        padding-top: 0.6rem;
        margin-top: 0.2rem;
        border-top: 2px solid #5555aa;
    }
    .usage-label {
        color: #9999cc;
        font-size: 0.9rem;
    }
    .usage-value {
        color: #ffffff;
        font-weight: 700;
        font-size: 0.95rem;
    }
    .usage-value.total {
        color: #ffcc00;
        font-size: 1.05rem;
    }

    /* 비용 카드 */
    .cost-card {
        background: linear-gradient(135deg, #1a3a1a, #2a4a2a);
        border: 1px solid #4a8a4a;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.5rem 0 1rem 0;
    }
    .cost-card h4 {
        color: #88ff88;
        margin: 0 0 0.8rem 0;
        font-size: 1rem;
    }

    /* 채팅 메시지 */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 0.8rem;
    }

    /* 모델 선택 라디오 버튼 */
    .stRadio > label {
        color: #c0c0ff !important;
        font-weight: 600;
    }

    /* 경고/정보 박스 */
    .model-info {
        background: linear-gradient(135deg, #1a1a4a, #252560);
        border-left: 4px solid #6666ff;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin: 0.8rem 0;
        color: #b0b0e0;
        font-size: 0.88rem;
    }

    /* 누적 사용량 배지 */
    .session-badge {
        background: linear-gradient(135deg, #3a1a5a, #4a2a6a);
        border: 1px solid #7a4aaa;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        margin: 0.5rem 0;
        text-align: center;
    }
    .session-badge .number {
        color: #cc88ff;
        font-size: 1.3rem;
        font-weight: 800;
    }
    .session-badge .label {
        color: #9977bb;
        font-size: 0.8rem;
    }

    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #4a4a8a, #5a5aaa);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a5aaa, #6a6acc);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# API 키 로드 (Streamlit Secrets)
# ============================================================
def get_api_key():
    """Streamlit Secrets에서 API 키를 안전하게 불러옵니다."""
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None

api_key = get_api_key()

# ============================================================
# 모델 정보 정의
# ============================================================
MODELS = {
    "Claude 4 Sonnet (최신)": {
        "id": "claude-sonnet-4-20250514",
        "description": "빠르고 효율적인 최신 모델. 일상 질문에 추천!",
        "input_cost_per_1m": 3.00,     # $3 per 1M input tokens
        "output_cost_per_1m": 15.00,   # $15 per 1M output tokens
        "emoji": "⚡",
    },
    "Claude 3.5 Sonnet": {
        "id": "claude-3-5-sonnet-20241022",
        "description": "안정적이고 균형 잡힌 모델. 범용 추천!",
        "input_cost_per_1m": 3.00,
        "output_cost_per_1m": 15.00,
        "emoji": "🎯",
    },
}

# ============================================================
# 세션 상태 초기화
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_input_tokens" not in st.session_state:
    st.session_state.total_input_tokens = 0

if "total_output_tokens" not in st.session_state:
    st.session_state.total_output_tokens = 0

if "total_cost" not in st.session_state:
    st.session_state.total_cost = 0.0

if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0

# ============================================================
# 사이드바
# ============================================================
with st.sidebar:
    st.markdown("## ⚙️ 설정")

    # 모델 선택
    selected_model_name = st.radio(
        "🧠 AI 모델 선택",
        options=list(MODELS.keys()),
        index=0,
    )
    model_info = MODELS[selected_model_name]

    st.markdown(f"""
    <div class="model-info">
        {model_info['emoji']} <strong>{selected_model_name}</strong><br>
        {model_info['description']}<br><br>
        💰 입력: ${model_info['input_cost_per_1m']:.2f} / 1M 토큰<br>
        💰 출력: ${model_info['output_cost_per_1m']:.2f} / 1M 토큰
    </div>
    """, unsafe_allow_html=True)

    # 시스템 프롬프트 설정
    system_prompt = st.text_area(
        "📝 시스템 프롬프트 (선택사항)",
        value="당신은 친절하고 도움이 되는 AI 어시스턴트입니다. 한국어로 답변해주세요.",
        height=100,
    )

    # 최대 토큰 설정
    max_tokens = st.slider(
        "📏 최대 응답 길이 (토큰)",
        min_value=256,
        max_value=8192,
        value=2048,
        step=256,
    )

    st.markdown("---")

    # 누적 사용량 표시
    st.markdown("### 📊 세션 누적 사용량")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="session-badge">
            <div class="number">{st.session_state.conversation_count}</div>
            <div class="label">대화 횟수</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="session-badge">
            <div class="number">{st.session_state.total_input_tokens + st.session_state.total_output_tokens:,}</div>
            <div class="label">총 토큰</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="session-badge">
        <div class="number" style="color: #ffcc00;">${st.session_state.total_cost:.6f}</div>
        <div class="label">총 예상 비용</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 대화 초기화 버튼
    if st.button("🗑️ 대화 기록 초기화", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_input_tokens = 0
        st.session_state.total_output_tokens = 0
        st.session_state.total_cost = 0.0
        st.session_state.conversation_count = 0
        st.rerun()

    st.markdown("---")
    st.markdown("""
    ### 📖 사용법
    1. 모델을 선택하세요
    2. 아래 입력창에 질문을 입력하세요
    3. AI가 답변을 생성합니다
    4. 토큰 사용량과 비용을 확인하세요

    ### 🔑 API 키 설정
    Streamlit Cloud의 **Secrets**에
    `ANTHROPIC_API_KEY`를 등록하세요.
    """)

# ============================================================
# 메인 영역 - 헤더
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>🤖 Claude AI 질문 앱</h1>
    <p>당곡고등학교 학습 도우미 — Claude API로 구동됩니다</p>
</div>
""", unsafe_allow_html=True)

# API 키 확인
if not api_key:
    st.error("""
    ⚠️ **API 키가 설정되지 않았습니다!**

    **Streamlit Cloud 배포 시:**
    1. 앱 대시보드 → Settings → Secrets
    2. 아래 내용을 입력하세요:
    ```
    ANTHROPIC_API_KEY = "sk-ant-api03-여기에_키_입력"
    ```

    **로컬 테스트 시:**
    `.streamlit/secrets.toml` 파일에 같은 내용을 추가하세요.
    """)
    st.stop()

# ============================================================
# Claude API 클라이언트 생성
# ============================================================
client = anthropic.Anthropic(api_key=api_key)

# ============================================================
# 이전 대화 메시지 표시
# ============================================================
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]

    with st.chat_message(role):
        st.markdown(content)

        # 해당 메시지에 사용량 정보가 있으면 표시
        if role == "assistant" and "usage" in msg:
            usage = msg["usage"]
            st.markdown(f"""
            <div class="usage-card">
                <h4>📊 이 응답의 토큰 사용량</h4>
                <div class="usage-row">
                    <span class="usage-label">📥 입력 토큰</span>
                    <span class="usage-value">{usage['input_tokens']:,}</span>
                </div>
                <div class="usage-row">
                    <span class="usage-label">📤 출력 토큰</span>
                    <span class="usage-value">{usage['output_tokens']:,}</span>
                </div>
                <div class="usage-row">
                    <span class="usage-label">📦 합계</span>
                    <span class="usage-value total">{usage['input_tokens'] + usage['output_tokens']:,}</span>
                </div>
            </div>
            <div class="cost-card">
                <h4>💰 이 응답의 예상 비용</h4>
                <div class="usage-row">
                    <span class="usage-label">입력 비용</span>
                    <span class="usage-value">${usage['input_cost']:.6f}</span>
                </div>
                <div class="usage-row">
                    <span class="usage-label">출력 비용</span>
                    <span class="usage-value">${usage['output_cost']:.6f}</span>
                </div>
                <div class="usage-row">
                    <span class="usage-label">합계</span>
                    <span class="usage-value total">${usage['total_cost']:.6f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# 사용자 입력 처리
# ============================================================
if prompt := st.chat_input("💬 질문을 입력하세요..."):
    # 사용자 메시지 추가 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        with st.spinner(f"🤔 {selected_model_name}이(가) 생각하는 중..."):
            try:
                start_time = time.time()

                # API에 보낼 메시지 구성 (role이 user/assistant만)
                api_messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                    if m["role"] in ("user", "assistant")
                ]

                # Claude API 호출
                response = client.messages.create(
                    model=model_info["id"],
                    max_tokens=max_tokens,
                    system=system_prompt,
                    messages=api_messages,
                )

                end_time = time.time()
                elapsed = end_time - start_time

                # 응답 텍스트 추출
                assistant_text = response.content[0].text

                # 사용량 계산
                input_tokens = response.usage.input_tokens
                output_tokens = response.usage.output_tokens

                input_cost = (input_tokens / 1_000_000) * model_info["input_cost_per_1m"]
                output_cost = (output_tokens / 1_000_000) * model_info["output_cost_per_1m"]
                total_cost = input_cost + output_cost

                # 세션 누적 업데이트
                st.session_state.total_input_tokens += input_tokens
                st.session_state.total_output_tokens += output_tokens
                st.session_state.total_cost += total_cost
                st.session_state.conversation_count += 1

                # 응답 표시
                st.markdown(assistant_text)

                # 사용량 표시
                st.markdown(f"""
                <div class="usage-card">
                    <h4>📊 이 응답의 토큰 사용량 — ⏱️ {elapsed:.1f}초 소요</h4>
                    <div class="usage-row">
                        <span class="usage-label">📥 입력 토큰</span>
                        <span class="usage-value">{input_tokens:,}</span>
                    </div>
                    <div class="usage-row">
                        <span class="usage-label">📤 출력 토큰</span>
                        <span class="usage-value">{output_tokens:,}</span>
                    </div>
                    <div class="usage-row">
                        <span class="usage-label">📦 합계</span>
                        <span class="usage-value total">{input_tokens + output_tokens:,}</span>
                    </div>
                </div>
                <div class="cost-card">
                    <h4>💰 이 응답의 예상 비용</h4>
                    <div class="usage-row">
                        <span class="usage-label">입력 비용</span>
                        <span class="usage-value">${input_cost:.6f}</span>
                    </div>
                    <div class="usage-row">
                        <span class="usage-label">출력 비용</span>
                        <span class="usage-value">${output_cost:.6f}</span>
                    </div>
                    <div class="usage-row">
                        <span class="usage-label">합계</span>
                        <span class="usage-value total">${total_cost:.6f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # 메시지 저장 (사용량 정보 포함)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_text,
                    "usage": {
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "input_cost": input_cost,
                        "output_cost": output_cost,
                        "total_cost": total_cost,
                    }
                })

            except anthropic.AuthenticationError:
                st.error("🔑 API 키가 유효하지 않습니다. Secrets 설정을 확인해주세요.")
            except anthropic.RateLimitError:
                st.error("⏳ API 요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요.")
            except anthropic.APIError as e:
                st.error(f"❌ API 오류가 발생했습니다: {str(e)}")
            except Exception as e:
                st.error(f"❌ 예상치 못한 오류: {str(e)}")
