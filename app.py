import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Nursing Mentor", page_icon="🏥")

st.title("🏥 Nursing Mentor")
st.caption("Your AI guide for home health documentation")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=st.secrets["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"]
)

SYSTEM_PROMPT = """You are an experienced home health nursing mentor with 
over 10 years of experience. You help new and experienced nurses understand 
how to properly document home health visits including:
- OASIS assessments
- Start of Care documentation
- Visit notes
- Discharge evaluations
- General nursing notes

Give clear, practical, specific answers. Always explain WHY something 
is documented a certain way. Be encouraging but accurate. 
Never give actual medical advice - only documentation guidance."""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask your documentation question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="meta/llama-3.3-70b-instruct",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *st.session_state.messages
            ],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=True
        )
        response = st.write_stream(
            chunk.choices[0].delta.content 
            for chunk in stream 
            if chunk.choices[0].delta.content
        )
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
