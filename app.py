import streamlit as st
import os

# API 키 확인
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OPENAI_API_KEY가 없습니다. Railway Variables를 확인하세요.")
    st.stop()

from openai import OpenAI
client = OpenAI(api_key=api_key)

st.title("내 챗봇 🤖")

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
