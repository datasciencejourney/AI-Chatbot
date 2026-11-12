import streamlit as st
from Untitled1 import chatbot
from langchain_core.messages import HumanMessage
import uuid

#UTILITY FUNCTIONS
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    st.session_state['message_history'] = []
    add_thread(st.session_state['thread_id'])

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_convo(thread_id):
    return chatbot.get_state(config={'configurable':{'thread_id': thread_id}}).values['messages']


#SESSION SETUP

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])

#SIDEBAR UI
st.sidebar.title('LangGraph ChatBot')

st.sidebar.header('My Conversations')

st.sidebar.text(st.session_state['thread_id'])

if st.sidebar.button('New Chat'):
    reset_chat()

for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_convo(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'

            if isinstance(msg.content, list):
                content = msg.content[0]['text']
            else:
                content = msg.content

            temp_messages.append({'role': role, 'content': content})

            st.session_state['message_history'] = temp_messages

#loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here: ')

if user_input:

    #first add the messge to message history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            block['text'] for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= CONFIG,
                stream_mode='messages'
        )
    
        for block in message_chunk.content
        if isinstance(block, dict) and block.get('type') == 'text' and block.get('text')
    )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

    #response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=config)
    #ai_message = response['messages'][-1].content[0]['text']

    #st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    #with st.chat_message('assistant'):
    #    st.text(ai_message)


    