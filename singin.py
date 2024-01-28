import streamlit as st
from firebase_admin import firestore,credentials
import firebase_admin
import pyrebase
import pandas as pd
from google.cloud.firestore_v1 import FieldFilter
from st_pages import Page, Section, add_page_title, show_pages, show_pages_from_config
from streamlit.elements import alert
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
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Kanit&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)
st.markdown("""
        <style>
        .css-c11ae4ac {display: none}
        </style>
        """, unsafe_allow_html=True)
db = firestore.client()
def login():
    try:
        auth.sign_in_with_email_and_password(email,password)
        st.balloons()
        return True
    except:
        pass
def alert_close_button_clicked():
    st.write("### Alert close callback results:")
    st.write("#### Alert was closed!")
    alert.close()

def welcome():
    st.markdown("""<style>[data-testid="stSidebar"]{visibility: visible;}</style>""", unsafe_allow_html=True)
    show_pages([
        Page("singin.py", "Home"),
        Page("ShowTest.py", "Test"),
        Page("adviser.py", "Adviser"),
        Page("chief.py", "All Test")
    ])
    with st.sidebar:
        if st.sidebar.button("Reset Password"):
            st.toast(f"URL for reset your password has send to Email : {st.session_state['email']}", icon="✅")
            auth.send_password_reset_email(st.session_state['email'])

        if st.sidebar.button("Sing Out"):
            sino()
            hideside()
def home():
    container = st.container(border=True)
    container.markdown(f"""<h2 style="font-family: 'Kanit', sans-serif; color:#7990ad;">รายวิชาและรายชื่อนักศึกษา</h2>""",unsafe_allow_html=True)
    db = firestore.client()
    docs = (
        db.collection("subject")
        .where(filter=FieldFilter(db.field_path(st.session_state['email']), "==", True))
        .stream()
    )
    for doc in docs:
        col1, col2, col3 = st.columns([2,6,2])
        with col2:
            st.markdown(f"""<h2 style="font-family: 'Kanit', sans-serif; color:#6896d4;">{doc.to_dict()["name"]}</h2>""",
                        unsafe_allow_html=True)
        std = (
            db.collection("student")
            .where(filter=FieldFilter(db.field_path(doc.to_dict()["ID"]), "==", True))
            .stream()
        )
        for s in std:
            col1, col2, col3 = st.columns(3)
            with col1 :
                st.markdown(
                    f"""<h5 style="font-family: 'Kanit', sans-serif; color:#a8c6f0;">{s.id}</h5>""",
                    unsafe_allow_html=True)
            with col2 :
                st.markdown(
                    f"""<h5 style="font-family: 'Kanit', sans-serif; color:#a8c6f0;">{s.to_dict()["name"]} {s.to_dict()["surname"]}</h5>""",
                    unsafe_allow_html=True)
            with col3 :
                st.markdown(
                    f"""<h5 style="font-family: 'Kanit', sans-serif; color:#a8c6f0;">{s.to_dict()["room"]}</h5>""",
                    unsafe_allow_html=True)
            # st.write(f"{s.to_dict()["name"]} {s.to_dict()["surname"]}")
    st.markdown("""<style>.st-emotion-cache-k7vsyb a {display: none;}</style>""", unsafe_allow_html=True)
def sino():
    streamlit_js_eval(js_expressions="parent.window.location.reload()")

def hideside():
    st.markdown("""<style>[data-testid="stSidebar"]{visibility: hidden;}</style>""", unsafe_allow_html=True)
if 'email' not in st.session_state:
    # Create an empty container
    placeholder = st.empty()
    resetBtn = st.empty()
    hideside()
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
    if submit:
        if login():
            st.session_state['email'] = email
            placeholder.empty()
            resetBtn.empty()
            home()
            getRole = db.collection("teacher").document(email).get()
            try:
                checkRole = getRole.to_dict()['chief']
            except:
                checkRole = False
            if checkRole:
                welcome()
            else:
                st.markdown("""<style>[data-testid="stSidebar"]{visibility: visible;}</style>""",
                            unsafe_allow_html=True)
                show_pages([
                    Page("singin.py", "Home"),
                    Page("ShowTest.py", "Test"),
                    Page("adviser.py", "Adviser")
                ])
                with st.sidebar:
                    if st.sidebar.button("Reset Password"):
                        st.toast(f"URL for reset your password has send to Email : {st.session_state['email']}",
                                 icon="✅")
                        auth.send_password_reset_email(st.session_state['email'])

                    if st.sidebar.button("Sing Out"):
                        sino()
                        hideside()
            #streamlit_js_eval(js_expressions="parent.window.location.reload()")
        else:
            st.error("Your Email/Password incorrect")
else:
    home()
    getRole = db.collection("teacher").document(st.session_state['email']).get()
    try:
        checkRole = getRole.to_dict()['chief']
    except:
        checkRole = False
    if checkRole:
        welcome()
    else:
        st.markdown("""<style>[data-testid="stSidebar"]{visibility: visible;}</style>""",
                    unsafe_allow_html=True)
        show_pages([
            Page("singin.py", "Home"),
            Page("ShowTest.py", "Test"),
            Page("adviser.py", "Adviser")
        ])
        with st.sidebar:
            if st.sidebar.button("Reset Password"):
                st.toast(f"URL for reset your password has send to Email : {st.session_state['email']}",
                         icon="✅")
                auth.send_password_reset_email(st.session_state['email'])

            if st.sidebar.button("Sing Out"):
                sino()
                hideside()
st.markdown("""
        <style>
        .css-c11ae4ac {display: none}
        </style>
        """, unsafe_allow_html=True)
