from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile
from pydantic import BaseModel

import time
import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
# from selection import classify,test

#selection.py
import time
import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
def test():
    print("hello")

def classify(input):
    load_dotenv()
    api_key = os.environ['OPENAI_API_KEY']

    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)


    assistantDeveloper = client.beta.assistants.create(
        name="",
        instructions='''You are a problem classifier and your task is to read from the instruction of users and then after understanding it classifiy it into its best posssible category.You should also make sure that if any indirect questions are asked your task is to classify it to the best possible category.
                            for example, if user is asking to send mails, send 1, 
                            if user is asking to get mails, send 2,
                            if user is asking to create database, send 3,
                            if user is asking to create a project and deploy it, send 4,
                            if user is asking to create a notepad with those details, send 5,
                            ''',
        model="gpt-4-0125-preview",
        )

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=input,
    )

    # Create the Run, passing in the thread and the assistant
    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistantDeveloper.id
    )

    # Periodically retrieve the Run to check status and see if it has completed
    # Should print "in_progress" several times before completing
    while run.status != "completed":
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"Run status: {keep_retrieving_run.status}")

        if keep_retrieving_run.status == "completed":
            print("\n")
            break

    # Retrieve messages added by the Assistant to the thread
    all_messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    # Print the messages from the user and the assistant
    print("###################################################### \n")
    print(f"USER: {message.content[0].text.value}")
    print(f"ASSISTANT: {all_messages.data[0].content[0].text.value}")
    return all_messages.data[0].content[0].text.value
#selection.py ends here

#mail reader

import imaplib
import email
from email.header import decode_header

# Function to decode email headers
def decode_subject(subject):
    decoded = decode_header(subject)[0][0]
    if isinstance(decoded, bytes):
        return decoded.decode('utf-8')
    else:
        return decoded

# IMAP server configuration
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993
EMAIL_ADDRESS = 'shraddha.mahapatra198@gmail.com'
PASSWORD = 'oyei zprw fzxu ffaj'
SEARCH_TEXT = 'price'  # Text to search for in subject or sender

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

# Login to the server
mail.login(EMAIL_ADDRESS, PASSWORD)

# Select the inbox
mail.select('inbox')

# Fetch all unseen emails
status, email_ids = mail.search(None, 'UNSEEN')

if status == 'OK':
    email_ids = email_ids[0].split()
    print("Number of Unseen Emails:", len(email_ids))  # Debugging statement

    # Ensure we have at least 10 emails
    if len(email_ids) >= 5:
        # Process only the latest 10 emails
        email_ids = email_ids[-5:]
    else:
        # Process all emails if there are fewer than 10
        email_ids = email_ids[::-1]

    for email_id in email_ids:
        # Fetch the email
        status, email_data = mail.fetch(email_id, '(RFC822)')
        print("Fetch Status:", status)  # Debugging statement
        
        if status == 'OK':
            raw_email = email_data[0][1]

            # Ensure raw_email is bytes
            if isinstance(raw_email, bytes):
                # Parse the raw email
                msg = email.message_from_bytes(raw_email)
            else:
                # Parse the raw email by encoding it to bytes
                msg = email.message_from_bytes(raw_email.encode('utf-8'))

            # Extract email headers
            subject = decode_subject(msg['subject'])
            sender = decode_header(msg['from'])[0][0]
            date = msg['date']
            
            # Print email details
            print(f"Subject: {subject}")
            print(f"From: {sender}")
            print(f"Date: {date}")
            print()

# Logout from the server
mail.logout()

#mail reader ends here


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class MessageIn(BaseModel):
    message: str

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}

@app.post("/upload_audio/")
async def upload_audio(audio_file: UploadFile = File(...)):
    return {"res":0}

@app.post("/transcript")
async def transcript(message_in: MessageIn):
    print("hello")
    print(message_in.message) 
    res = classify(message_in.message)
    print("hello print")
    print("Result = ",res)
    return {"req": res}

@app.get("/abort")
async def abort():
    print("process aborted")
    return {"message":"process aborted"}