import requests
import streamlit as st


API_URL = "http://backend:8000/api/chat"


st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
)

st.title("🤖 How can We help you today.")
st.write("Your AI Customer Assistant.")


if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


question = st.chat_input("Ask your question...")


if question:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Call backend
    with st.chat_message("assistant"):

        with st.spinner("Searching the knowledge base..."):

            try:
                response = requests.post(
                    API_URL,
                    json={
                        "question": question,
                        "top_k": 3,
                    },
                    timeout=60,
                )

                response.raise_for_status()

                data = response.json()
                answer = data["answer"]

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except requests.exceptions.RequestException as e:

                error_message = (
                    "Unable to connect to the backend. "
                    "Please make sure the FastAPI server is running."
                )

                st.error(error_message)
                print(e)