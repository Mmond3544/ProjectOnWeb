import streamlit as st
from firebase_admin import firestore,credentials
import firebase_admin
import pyrebase
import pandas as pd
from google.cloud.firestore_v1 import FieldFilter
from st_pages import Page, Section, add_page_title, show_pages, show_pages_from_config
from streamlit_js_eval import streamlit_js_eval
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime,time
firebaseConfig = {
    "apiKey": "AIzaSyD1nH6ruhgUTBOBaCMcDNlJdVAUZ90NvBs",
    "authDomain": "project-e41b4.firebaseapp.com",
    "databaseURL": "https://project-e41b4-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "project-e41b4",
    "storageBucket": "project-e41b4.appspot.com",
    "messagingSenderId": "73384152866",
    "appId": "1:73384152866:web:c568a753e6aa59cb75df7b",
    "measurementId": "G-V8D58C3GLV"
}
try:
    firebases = pyrebase.initialize_app(firebaseConfig)
    auth = firebases.auth()
except ValueError as e:
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

try:
    app = firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate("cert.json")
    firebase_admin.initialize_app(cred)

def login():
    try:
        auth.sign_in_with_email_and_password(email,password)
        st.balloons()
        return True
    except:
        pass

def welcome():
    st.markdown("""<style>[data-testid="stSidebar"]{visibility: visible;}</style>""", unsafe_allow_html=True)
    show_pages([
        Page("singin.py", "Home"),
        Page("ShowTest.py", "Test"),
        Page("adviser.py", "Adviser")
    ])
    with st.sidebar:
        if st.sidebar.button("Sing Out"):
            sino()
            hideside()
def home():
    db = firestore.client()
    docs = (
        db.collection("subject")
        .where(filter=FieldFilter(db.field_path(st.session_state['email']), "==", True))
        .stream()
    )
    for doc in docs:
        st.markdown(f"""<h1 style="font-family: 'Kanit', sans-serif; color:#6896d4;">{doc.to_dict()["name"]}</h1>""",
                    unsafe_allow_html=True)
        std = (
            db.collection("student")
            .where(filter=FieldFilter(db.field_path(doc.to_dict()["ID"]), "==", True))
            .stream()
        )
        for s in std:
            st.markdown(
                f"""<h5 style="font-family: 'Kanit', sans-serif; color:#a8c6f0;">{s.to_dict()["name"]} {s.to_dict()["surname"]}</h5>""",
                unsafe_allow_html=True)
            # st.write(f"{s.to_dict()["name"]} {s.to_dict()["surname"]}")
def sino():
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

def hideside():
    st.markdown("""<style>[data-testid="stSidebar"]{visibility: hidden;}</style>""", unsafe_allow_html=True)

if 'email' not in st.session_state:
    # Create an empty container
    placeholder = st.empty()
    hideside()
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
    if login():
        st.session_state['email'] = email
        placeholder.empty()
        home()
        welcome()
        #streamlit_js_eval(js_expressions="parent.window.location.reload()")
else:
    home()
    welcome()

