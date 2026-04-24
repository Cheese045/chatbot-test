import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일이나 시스템에서 강제로 환경변수 끌어오기
load_dotenv()

st.set_page_config(page_title="내 챗봇", page_icon="🤖")

st.title("내 챗봇 🤖")

# 이제 무조건 값이 들어옵니다
my_key = os.environ.get("MY_API_KEY") or os.environ.get("OPENAI_API_KEY") or ""

if not my_key:
    st.error("🚨 Railway에 API 키가 설정되지 않았습니다!")
    st.stop()

# 위에서 통과했다면 안전하게 연결
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
