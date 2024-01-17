import os
import time
import speech_recognition as sr
import pyttsx3 
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from htmlTemplates import css, bot_Template, user_Template

load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=OPEN_AI_API_KEY)

with open('AI_prompt.txt', 'r') as file:
    prompt = file.read()

def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()
     

def upload_files(paths):
    file_ids = []
    for path in paths:
        file = client.files.create(file=open(path, "rb"), purpose="assistants")
        file_ids.append(file.id)

    return file_ids


def create_assistant(file_ids=None):  # Make file_ids optional with a default value of None
    assistant = client.beta.assistants.create(
        name="Jarvis",
        instructions=prompt,
        tools=[{"type": "retrieval"}],
        model="gpt-3.5-turbo-1106",
        file_ids=file_ids,  # Pass the file_ids if provided, otherwise it will be None
    )
    # st.session_state.asstID = assistant.id
    return assistant


def generate_response(message_body):
    #preparing message to be sent to the assistant. Message is not yet sent.
    message = client.beta.threads.messages.create(
       thread_id = st.session_state.threadID,
       role = "user",
       content = message_body,
    )
    return message.id


def run_assistant(context_id):
    # assistant = client.beta.assistants.retrieve(st.session_state.asstID)
    # thread = client.beta.threads.retrieve(st.session_state.threadID)

    run = client.beta.threads.runs.create(
        thread_id=st.session_state.threadID,
        assistant_id=st.session_state.asstID,
    )

    while run.status != "completed":
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=st.session_state.threadID, run_id=run.id)

    messages = client.beta.threads.messages.list(thread_id=st.session_state.threadID, order="asc", after=context_id)
    new_message = messages.data[0].content[0].text.value

    return new_message


def handle_userInput(user_question):
    #Limit to 8 for API constraints
    max_messages = 6

    # Ensure the "conversation" list doesn't exceed the maximum limit
    st.session_state.conversation = st.session_state.conversation[-max_messages:]

    # Concatenate the content of the "conversation" list into a string named "past_messages"
    for entry in st.session_state.conversation:
        user_msg = entry.get("user", "")
        rula_msg = entry.get("Rula", "")
        st.session_state.past_messages += f"User: {user_msg}\nRula: {rula_msg}\n\n"

    # context = generate_response(user_question)  # Generate thread and store thread ID
    context_string = st.session_state.past_messages + "\n" + user_question

    context_id = generate_response(context_string)
    response = run_assistant(context_id)

    if st.session_state.conversation==[]:
        st.write(user_Template.replace("{{MSG}}", user_question), unsafe_allow_html=True)
        st.write(bot_Template.replace("{{MSG}}", response), unsafe_allow_html=True)

    else:
        for entry in st.session_state.conversation:
            user_question_prev = entry.get("user", "")
            response_prev = entry.get("Rula", "")

            st.write(user_Template.replace("{{MSG}}", user_question_prev), unsafe_allow_html=True)
            st.write(bot_Template.replace("{{MSG}}", response_prev), unsafe_allow_html=True)

        st.write(user_Template.replace("{{MSG}}", user_question), unsafe_allow_html=True)
        st.write(bot_Template.replace("{{MSG}}", response), unsafe_allow_html=True)

    st.session_state.conversation.append({"user": user_question, "Rula": response})
    
    if st.session_state.voice_checkbox:
        SpeakText(response)


def main():
    load_dotenv()
    st.set_page_config(page_title="Rula")

    st.write(css, unsafe_allow_html=True)

    # Bot image in circle
    st.markdown('<div class="circle-image"><img src="https://i.ibb.co/x36DfwK/bot-avatar.jpg" alt="Profile Image"> </div>', unsafe_allow_html=True)

    st.markdown("# Hi I am Jarvis!")
    st.caption("### Jarvis at your service!")
    # st.caption("### Park with Parker!")

    st.markdown(
        """
        <div class="beginning-background" style="margin-top: 70px;">
            <div class="circle-image img">
                <img  style="height: 100px; width: 100px;" src="https://i.ibb.co/x36DfwK/bot-avatar.jpg" alt="Logo" class="logo">
            </div>
            <h2 style="margin: 100px 0 0 50px;">How can I help you today?</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.session_state.file_ids = []

    # Initialize the recognizer 
    r = sr.Recognizer() 

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if "past_messages" not in st.session_state:
        st.session_state.past_messages = ""

    user_question = st.chat_input("Ask your question here") #user question
    
    if "asstID" not in st.session_state:  # Check if assistant exists in session state
        assistant = create_assistant(file_ids=st.session_state.file_ids)  # Create if needed
        st.session_state.asstID = assistant.id  # Store for reuse

    if "threadID" not in st.session_state:  # Check if assistant exists in session state
        thread = client.beta.threads.create()    
        st.session_state.threadID = thread.id

    if user_question:
        handle_userInput(user_question)

    st.sidebar.checkbox("Enable Voice", key="voice_checkbox") 

    while st.session_state.voice_checkbox:

        # exceptions at the runtime
        try:
            
            # use the microphone as source for input.
            with sr.Microphone() as source2:
                
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level 
                r.adjust_for_ambient_noise(source2, duration=0.2)
                
                #listens for the user's input 
                audio2 = r.listen(source2)
                
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                print("Did you say ",MyText)

                if MyText == "end the conversation":
                    st.session_state.voice_checkbox = not st.session_state.voice_checkbox
                    break

                handle_userInput(MyText)
                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            print("unknown error occurred")
        
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on ***Process***.", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing.."):
                file_paths = []
                for uploaded_file in pdf_docs:
                    file_path = os.path.join("temp", uploaded_file.name)

                    # Ensure parent directory exists
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create parent directory if missing

                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    file_paths.append(file_path)
                    
                st.session_state.file_ids = upload_files(file_paths)
                assistant = client.beta.assistants.retrieve(st.session_state.asstID)
                client.beta.assistants.update(assistant_id=st.session_state.asstID, file_ids=st.session_state.file_ids)


if __name__== '__main__' :
    main()

