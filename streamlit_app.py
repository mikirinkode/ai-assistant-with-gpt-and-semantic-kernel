import streamlit as st
from miriko import Miriko

# setup Miriko
openai_model="gpt-3.5-turbo"
api_key=st.secrets["OPENAI_API_KEY"]
org_id=st.secrets["OPENAI_ORG_ID"]

if "miriko" not in st.session_state:
    st.session_state.miriko = Miriko(openai_model, api_key, org_id)

miriko = st.session_state.miriko if "miriko" in st.session_state else Miriko(openai_model, api_key, org_id)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#
# Web
#
st.set_page_config(layout="wide", page_title="Miriko Bot", page_icon=":robot_face:")
st.title("Miriko Bot")

# display initial message
st.write("Hello i am Miriko, your personal assistant. How can i help you?")

col1, col2 = st.columns(2)

with col1:   
    with st.container(border=True):
        # React to user input
        prompt = st.text_area(label = "What is up?", key="user_input")
        
        if prompt is not None and prompt != "":
            # add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                # create initial result placeholder
                message_placeholder = st.empty()
                full_response = ""
                
                for response in miriko.chat(prompt):
                    full_response += response.choices[0].delta.content or ""
                    message_placeholder.markdown(full_response + "")
                    message_placeholder.markdown(full_response)
                message_placeholder.markdown(full_response)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
    
    with st.expander("Show Miriko's Memory"):
        messages = miriko.get_all_miriko_memory()
        st.write(messages)
            
    st.subheader("Chat History")
    with st.container():
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])            
                
with col2:
    with st.container(border=True):
        # select skills
        skills = st.selectbox("Select Skill", ["Brainstorming"])
        
        # React to user input
        if prompt := st.text_input("Enter your Ideas", key="idea_input"):
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            # add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("Thinking..."):
                    full_response = miriko.brainstormer(prompt)
                    message_placeholder.markdown(full_response)