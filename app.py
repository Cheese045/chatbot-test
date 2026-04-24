import streamlit as st
import os
from openai import OpenAI

st.set_page_config(page_title="내 챗봇", page_icon="🤖")

st.title("내 챗봇 🤖")

# --- 가장 중요하게 바뀐 부분! ---
# 앱이 시작될 때 미리 가져오지 않고, OpenAI한테 값을 줄 때 바로 꺼내옵니다.
# 이렇게 하면 Railway가 변수를 늦게 줘도 무조건 안전합니다.
my_key = os.environ.get("MY_API_KEY", "")

if not my_key:
    st.error("🚨 Railway에 API 키가 설정되지 않았습니다!")
    st.stop()

# 위에서 통과했다면 이제 안전하게 연결
client = OpenAI(api_key=my_key)
# -----------------------------

uploaded_file = st.file_uploader("학습할 파일 업로드", type=["txt", "pdf"])

if "messages" not in st.session_state:
    st.session_state.messages = []

if uploaded_file:
    content = uploaded_file.read().decode("utf-8", errors="ignore")
    st.session_state["doc_content"] = content
    st.success("✅ 파일 업로드 완료!")

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("질문을 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    system_msg = "친절한 AI 어시스턴트입니다."
    if "doc_content" in st.session_state:
        system_msg += f"\n\n참고 문서:\n{st.session_state['doc_content'][:3000]}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_msg}] + st.session_state.messages
    )
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
