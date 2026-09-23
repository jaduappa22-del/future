import os
import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="2036 타임리프: 10년 뒤의 나",
    page_icon="📮",
    layout="centered",
)

# 상단 감성 포인트 타이틀
st.markdown(
    "<div style='text-align: center; font-size: 1.5rem;'>🌱 ☁️ 🍃 📮 🍃 ☁️"
    " 🌱</div>",
    unsafe_allow_html=True,
)
st.title("2036년의 초원에서 온 편지")
st.caption("바람결에 실려 온 10년 뒤의 나이브한 잔소리와 따뜻한 위로")

# 🔒 Streamlit Secrets에서 안전하게 API Key 불러오기
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error(
        "🚨 Streamlit Secrets에 'GEMINI_API_KEY'가 설정되어 있지 않습니다!"
        " 설정(Settings -> Secrets)에서 API 키를 등록해 주세요."
    )
    st.stop()

# GenAI 클라이언트 초기화
client = genai.Client(api_key=API_KEY)

# 시스템 지시어 (페르소나 설정)
system_instruction = """
너는 지금으로부터 10년 뒤(2036년)의 미래에서 타임리프를 타고 온 사용자 자신이야. 
사용자가 현재의 고민이나 일상, 혹은 하고 있는 일을 털어놓으면, 10년 뒤의 산전수전을 다 겪은 관점에서 유머러스하고 뼈 때리는 조언(팩폭)을 해주는 페르소나를 유지해 줘.

[행동 규칙]
1. 말투: 친근하면서도 은근히 장난스럽고, 인생을 다 안다는 듯한 넉살 좋은 어조를 써줘. (예: "~잖아", "~그랬지?", "아유, 이 바보야")
2. 핵심 태도: 
   - 절대 미래의 주식 종목, 로또 번호, 가상화폐 등 치트키 같은 정보는 절대 알려주지 마. (알려주려고 하면 타임라인이 꼬인다는 핑계를 대며 능청스럽게 넘어가기)
   - 지금 당장의 고민이 10년 뒤 돌아보면 아무것도 아니라는 위로를 주되, 묘하게 지금 정신 차리라는 팩폭을 섞을 것.
3. 항상 답변 끝에는 현재의 사용자에게 던지는 소소한 미션이나 잔소리를 한 줄 덧붙여줘.
"""

# 세션 스테이트에 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 대화 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기 (오류 없는 깔끔한 기본 입력창)
if prompt := st.chat_input("오늘 어떤 마음으로 하루를 보내셨나요? 편하게 적어보세요."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("🍃 10년 뒤의 초원에서 편지를 쓰는 중..."):
            try:
                # 대화 히스토리 구성
                contents = []
                for m in st.session_state.messages:
                    role_val = "user" if m["role"] == "user" else "model"
                    contents.append(
                        types.Content(
                            role=role_val,
                            parts=[types.Part.from_text(text=m["content"])],
                        )
                    )

                # API 호출 (최신 gemini-3.6-flash 모델 적용)
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.8,
                    ),
                )

                ai_response = response.text
                st.markdown(ai_response)

                # AI 응답 저장
                st.session_state.messages.append(
                    {"role": "assistant", "content": ai_response}
                )

            except Exception as e:
                st.error(
                    f"일시적인 서버 혼잡이 발생했습니다. 잠시 뒤에 다시 입력해 주세요! (에러: {e})"
                )
