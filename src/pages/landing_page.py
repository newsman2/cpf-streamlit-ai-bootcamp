# Set up and run this Streamlit App
import streamlit as st

from helpers import llm, state, utility

state.ensure_session_states()

# region <--------- Streamlit App Configuration --------->
st.set_page_config(layout="centered", page_title="Collections")

# Do not continue if check_password is not True.
if not utility.check_password():
    st.stop()
# endregion <--------- Streamlit App Configuration --------->

st.title("CPF Assistant")

prompt = st.chat_input("What do you want to know about CPF?")

for message in st.session_state.cpf_assistant_chat_history:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

        system_message = """
        You are a helpful assistant.
        Your task is to perform the following steps:

        Step 1 - To answer questions about Singapore Central Provident Fund (CPF).
        Step 2 - To provide a summary and translate the answer into Chinese.

        If you don't know the answer, just say that you don't know.

        If the question is not about CPF, politely inform them that you are tuned to only answer questions about CPF.
        The response MUST be in the following format:
        Answer:#### <step 1 output>
        回答(概括):#### <step 2 output>
        """
        st.session_state.cpf_assistant_chat_history.append(
            {"role": "system", "content": system_message}
        )
        st.session_state.cpf_assistant_chat_history.append(
            {"role": "user", "content": prompt}
        )

    with st.chat_message("assistant"):
        messages = st.session_state.cpf_assistant_chat_history
        response = st.write_stream(llm.generate_response(messages))
        st.session_state.cpf_assistant_chat_history.append(
            {"role": "assistant", "content": response}
        )
