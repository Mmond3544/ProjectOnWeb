import firebase_admin
import streamlit as st
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter
from st_pages import Page, show_pages, add_page_title
from datetime import datetime,time

import credent

try:
    cred = credentials.Certificate("cert.json")
    firebase_admin.initialize_app(cred)
except ValueError as e:
    app = firebase_admin.get_app()

db = firestore.client()
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Kanit&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)
subject = (
        db.collection("test")
        .where(filter=FieldFilter("adviser", "==", st.session_state['email']))
        .stream()
    )
getTestName = []
stdname = []
for s in subject:
    newsubject = s.to_dict()["subject"]
    getTestName.append(newsubject)
    for std in s.to_dict():
        student = db.collection("student").document(std).get()
        if s.to_dict()[std] == True:
            # subject = db.collection("subject").document(doc.id).get()
            x = f"{student.to_dict()['name']} {student.to_dict()['surname']}"
            if x not in stdname:
                stdname.append(x)
        elif s.to_dict()[std] == False:
            x = f"{student.to_dict()['name']} {student.to_dict()['surname']}"
            if x not in stdname:
                stdname.append(x)
subjectSelect = st.sidebar.selectbox("Subject",getTestName,index=None,placeholder="Select Subject...")
studentSelect = st.sidebar.selectbox("Student",stdname,index=None,placeholder="Select Student...")
if subjectSelect:
    docs = (
        db.collection("test")
        .where(filter=FieldFilter("adviser", "==", st.session_state['email']))
        .where(filter=FieldFilter("subject", "==", subjectSelect))
        .stream()
    )
else:
    docs = (
        db.collection("test")
        .where(filter=FieldFilter("adviser", "==", st.session_state['email']))
        .stream()
    )
room = []
student = []
for doc in docs:
    dataID = db.collection("test").document(doc.id)
    subject = db.collection("subject").document(doc.id).get()
    newsubject = subject.to_dict()['name']
    newsubject = newsubject.split("_")
    sj = newsubject[0]
    st.markdown(f"""<h1 style="font-family: 'Kanit', sans-serif; color:#6896d4;">{sj}</h1>""",
                    unsafe_allow_html=True)
    # st.subheader(doc.id)
    if studentSelect:
        stdsplit = studentSelect.split(" ")
        getStdID = (db.collection("student")
             .where(filter=FieldFilter("name", "==", stdsplit[0]))
             .where(filter=FieldFilter("surname", "==", stdsplit[1]))
             .stream())
        for get in getStdID:
            a = [get.id]
    else:
        a = doc.to_dict()
    for std in a:
            student = db.collection("student").document(std).get()
            if doc.to_dict()[std] == True:
                timediff = doc.to_dict()[f"{std}_time"] - doc.to_dict()['start_test']
                stdtime = doc.to_dict()[f"{std}_time"]
                time1 = datetime.strptime(str(stdtime), '%Y-%m-%d %H:%M:%S.%f%z').time()
                time1 = time1.strftime('%H:%M:%S')
                date = datetime.strptime(str(stdtime), '%Y-%m-%d %H:%M:%S.%f%z').date()
                date = date.strftime('%d/%m/%Y')
                new_timediff = datetime.strptime(str(timediff), '%H:%M:%S.%f').time()
                latetime = time(0, 15, 0, 0)
                if new_timediff > latetime:
                    txt = f"{student.to_dict()['name']} {student.to_dict()['surname']} เข้าสอบวิชา {sj} วันที่ {date} เวลา {time1}"
                    st.markdown(
                        f"""<p style="font-family: 'Kanit', sans-serif; color:#c4a841;font-size:18px;">{txt}</p>""",
                        unsafe_allow_html=True)
                else:
                    txt = f"{student.to_dict()['name']} {student.to_dict()['surname']} เข้าสอบวิชา {sj} วันที่ {date} เวลา {time1}"
                    st.markdown(f"""<p style="font-family: 'Kanit', sans-serif; color:#68d474;font-size:18px;">{txt}</p>""",
                            unsafe_allow_html=True)
                # st.write(f"{student.to_dict()['name']} {student.to_dict()['surname']} เข้าสอบวิชา {doc.id} วันที่ {date} เวลา {time1}")
            elif doc.to_dict()[std] == False:
                txt = f"{student.to_dict()['name']} {student.to_dict()['surname']} ไม่ได้เข้าสอบวิชา {sj}"
                st.markdown(f"""<p style="font-family: 'Kanit', sans-serif; color:#d46868;font-size:18px;">{txt}</p>""",
                            unsafe_allow_html=True)
                # st.write(f"{student.to_dict()['name']} {student.to_dict()['surname']} ไม่ได้เข้าสอบวิชา {doc.id}")