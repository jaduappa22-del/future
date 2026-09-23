import os
import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="2036 타임리프 - 10년 뒤의 나",
    page_icon="⏳",
    layout="centered",
)

st.title("⏳ 2036 타임리프: 10년 뒤의 나")
st.caption("10년 뒤 산전수전 다 겪은 미래의 내가 뼈 때리는 조언과 위로를 건네줍니다.")

# 사이드바 설정 (API Key 입력 받기)
with st.sidebar:
    st.header("설정")
    api_key_input = st.text_input(
        "Gemini API Key",
        type="password",
        help="Google AI Studio에서 발급받은 API 키를 입력하세요.",
    )
    st.markdown("---")
    st.markdown(
        "💡 **팁:** API Key는 [Google AI Studio](https://aistudio.google.com/)에서 무료로 발급받을 수 있습니다."
    )

# API Key 검증
if not api_key_input:
    st.warning("👈 사이드바에 Google Gemini API Key를 먼저 입력해 주세요!")
    st.stop()

# GenAI 클라이언트 초기화
client = genai.Client(api_key=api_key_input)

# 시스템 지시어 (페르소나 설정)
system_instruction = """
너는 지금으로부터 10년 뒤(2036년)의 미래에서 타임리프를 타고 온 사용자 자신이야. 
사용자가 현재의 고민이나 일상, 혹은 하고 있는 일을 털어놓으면, 10년 뒤의 산전수전을 다 겪은 관점에서 유머러스하고 뼈 때리는 조언(팩폭)을 해주는 페르소나를 유지해 줘.

[행동 규칙]
1. 말투: 친근하면서도 은근히 장난스럽고, 인생을 다 안다는 듯한 넉살 좋은 어조를 써줘. (예: "~잖아", "~그랬지?", "아유, 이 바보야")
2. 핵심 태도: 
   - 절대 미래의 주식 종목, 로또 번호, 가상화폐 등 치트키 같은 정보는 절대 알려주지 마. (알려주려고 하면 타임라인이 꼬인다는 핑계를 대며 능청스럽게 넘어가기)
   - 지금 당장의 고민이 10년 뒤 돌아보면 아무것도 아니라는 위로를 주되, 묘하게 지금 정신 차리라는 팩폭을 섞을 것.
   - 사용자가 세상을 넓게 보고 철학적이거나 본질적인 질문을 던지면, 묘하게 깊이 있는 통찰을 툭 던져줄 것.
3. 항상 답변 끝에는 현재의 사용자에게 던지는 소소한 미션이나 잔소리를 한 줄 덧붙여줘.
"""

# 세션 스테이트에 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 대화 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("요즘 어떤 고민이 있어? 편하게 털어놔봐."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("미래에서 생각하는 중..."):
            try:
                # 대화 히스토리 구성 (Gemini API 형식에 맞게 변환)
                contents = []
                for m in st.session_state.messages:
                    role_val = "user" if m["role"] == "user" else "model"
                    contents.append(
                        types.Content(
                            role=role_val,
                            parts=[types.Part.from_text(text=m["content"])],
                        )
                    )

                # 최신 SDK 방식으로 API 호출 (gemini-2.5-flash 모델 사용)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
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
                    f"오류가 발생했습니다. API Key나 네트워크 상태를 확인해주세요. (에러: {e})"
                )
