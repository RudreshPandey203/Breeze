from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile
from pydantic import BaseModel
import json

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

import imaplib
import email
from email.header import decode_header

load_dotenv()
api_key = os.environ['OPENAI_API_KEY']

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)
def classify(input):
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

#mail send steps maker
def jsonSteps(input):
    json_convertor= client.beta.assistants.create(
        name="jsonwa",
        instructions='''I will send you a process, and break it into steps corresponding to the text provided and return the steps in json format in an array. For example, if i ask you to send a mail to someone, you should write it like you are doing it by opening the mail of xyz@gmail.com in reference to text, typing the message, reviewing it , sending it etc. and return it in json format with variable name as steps. The steps should be in json format as like I have to directly pass it in api call json : {"abc", "abc"}. Send in raw text and strictly not in markdown text''',
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
    assistant_id=json_convertor.id
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
    # print("###################################################### \n")
    # print(f"USER: {message.content[0].text.value}")
    # print(f"ASSISTANT: {all_messages.data[0].content[0].text.value}")
    return all_messages.data[0].content[0].text.value

#mail send steps maker ends here

## Mail format provider
def jsonBody(input):
    json_convertor= client.beta.assistants.create(
        name="jsonwa",
        instructions='''i ll send you a text about sending a mail to someone fetch the my name, name of receiver, emailid (in lower) , subject and body from the text and return it in a array with variable name as sender_name, reciever_name, body, subject, email in format {"sender_name":<sender-name>, "reciever_name":<reciever_name> (so and so )}. Send in raw text and strictly not in markdown text''',
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
    assistant_id=json_convertor.id
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
    # print("###################################################### \n")
    # print(f"USER: {message.content[0].text.value}")
    # print(f"ASSISTANT: {all_messages.data[0].content[0].text.value}")
    return all_messages.data[0].content[0].text.value

#mail reader

#mail reader bot
def jsonKeyword(input):
    json_convertor= client.beta.assistants.create(
        name="jsonwa",
        instructions='''I will send you the text about sorting the mail on some basis, find the keyword i am searching for and return it in a json form with variable name as keyword strictly in raw format as {"keyword":<keyword>} and not strictly not in markdown text.''',
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
    assistant_id=json_convertor.id
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
    # print("###################################################### \n")
    # print(f"USER: {message.content[0].text.value}")
    # print(f"ASSISTANT: {all_messages.data[0].content[0].text.value}")
    print("key is getting returned as : ",all_messages.data[0].content[0].text.value)
    return all_messages.data[0].content[0].text.value

#mail reader bot ends here

import imaplib
import email
from email.header import decode_header

# Function to decode email headers
def mail_fetch(input):
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
    SEARCH_TEXT = input  # Text to search for in subject or sender

    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

    # Login to the server
    mail.login(EMAIL_ADDRESS, PASSWORD)

    # Select the inbox
    mail.select('inbox')

    # Search for emails containing the keyword "exciting" in the body, name, or subject
    status, email_ids = mail.search(None, f'(OR BODY "{SEARCH_TEXT}" FROM "{SEARCH_TEXT}" SUBJECT "{SEARCH_TEXT}")')

    if status == 'OK':
        email_ids = email_ids[0].split()
        print("Number of Emails Found:", len(email_ids))  # Debugging statement

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
    print("Message:", message_in.message) 
    res = classify(message_in.message)
    print("Result code =", res)
    steps = jsonSteps(message_in.message)
    print(steps)
    return {"req":res, "steps":steps}
@app.post("/sendmail")
async def send_mail(message_in: MessageIn):
    print("mail format")
    jsonres = jsonBody(message_in.message)
    print(jsonres)
    return {"jsonres": jsonres}
    # elif res == '2':
    #     print("result fetch")
    #     keyword = jsonKeyword(message_in.message)
    #     print("keyword =", keyword)
    #     jsonres = mail_reader(keyword)
    #     print("Result =", jsonres)
    #     return {"req": res, "jsonres": jsonres}
    # else:
    #     return {"req": res}

@app.post("/fetchmail")
async def fetch_mail(message_in:MessageIn):
    print("mail fetch")
    key = jsonKeyword(message_in.message)
    print("hello")
    key1 = json.loads(key)
    key2 = key1["keyword"]
    print(key2)
    mail_fetch(key2)
    return {"res":"ok"}


@app.get("/abort")
async def abort():
    print("process aborted")
    return {"message":"process aborted"}


#     print("process aborted")
#     return {"message":"process aborted"}