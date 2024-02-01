import streamlit as st
from streamlit_chat import message
from langchain.llms import OpenAI
from langchain.memory import ConversationTokenBufferMemory,ConversationBufferMemory,ConversationBufferWindowMemory,ConversationSummaryMemory
from langchain.chains import ConversationChain
from dotenv import load_dotenv

#session data by default for memory
if 'conversation' not in st.session_state:
  st.session_state['conversation']=None

#for convesational view need to show past mesage
if 'messages' not in st.session_state:
  st.session_state['messages']=[]

#user api key to run the model 
if 'api_key' not in st.session_state:
  st.session_state['api_key']=''

#loading my keys
# load_dotenv()

#setting the streamlit page
st.set_page_config(page_title='Chat GPT clone')
st.markdown('<h1 style="text-align:center">How Can I Assist You!</h1>',unsafe_allow_html=True)

# sidebar details
st.sidebar.title('😊')
##get the key
key=st.sidebar.text_input('What is your api key?',type='password')
summary_button=st.sidebar.button('Start the chat')
if summary_button:
  st.session_state['api_key']=key
  # st.sidebar.write('Summarizing the conversation \n nice chat 😘. \n'+st.session_state['conversation'].memory.buffer)


#main_logic 
def get_response(user_input,api_key):
  if st.session_state['conversation'] is None:
    llm=OpenAI(model='gpt-3.5-turbo-instruct',openai_api_key=api_key)

    ## convo object
    st.session_state['conversation']=ConversationChain(
      llm=llm,
      verbose=True,
      memory=ConversationBufferMemory()
    )

  #response 
  # to get memory 
  # print(st.session_state['conversation'].memory.buffer)
  response=st.session_state['conversation'].predict(input=user_input)
  return response 

#response text cone here
response_container=st.container()
#user text come here
container=st.container()

#user container to input and submit
with container:
  with st.form(key='my_form',clear_on_submit=True):
    user_input=st.text_area('Write your query here...',key='input')
    submit_button=st.form_submit_button(label='send')
    if submit_button:
      #append the messages in the session state for conversationl view in the response container 
      st.session_state['messages'].append(user_input)
      answer=get_response(user_input,st.session_state['api_key'])
      st.session_state['messages'].append(answer)
      #triggering response container as it define above on the user so comes up first 
      with response_container:
        #user qury is always even 
        for i in range(len(st.session_state['messages'])):
          if i%2==0:
            message(st.session_state['messages'][i],is_user=True,key=str(i)+'_user')
          else:
            message(st.session_state['messages'][i],key=str(i)+'_ai')




