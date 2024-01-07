import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter
import streamlit as st
import pandas as pd
from datetime import datetime , time
try:
    cred = credentials.Certificate("cert.json")
    firebase_admin.initialize_app(cred)
except ValueError as e:
    app = firebase_admin.get_app()
stdname = []
stdtime = []
data = pd.DataFrame(columns = ['True','Late','False'])
TakeTheExam = []
NotTakeTheExam = []
late = []
count = 0
testname = []
db = firestore.client()
docs = (
    db.collection("test")
    .where(filter=FieldFilter("Teacher", "==", st.session_state['email']))
    .stream()
)
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Kanit&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)
for doc in docs:
    TakeTheExam1 = 0
    NotTakeTheExam1 = 0
    late1 = 0
    dataID = db.collection("test").document(doc.id)

    if doc.exists:
        for std in doc.to_dict():
            student = db.collection("student").document(std).get()
            if doc.to_dict()[std] == True:
                #subject = db.collection("subject").document(doc.id).get()
                timediff = doc.to_dict()[f"{std}_time"] - doc.to_dict()['start_test']
                stdtime = doc.to_dict()[f"{std}_time"]
                time1 = datetime.strptime(str(stdtime), '%Y-%m-%d %H:%M:%S.%f%z').time()
                time1 = time1.strftime('%H:%M:%S')
                date = datetime.strptime(str(stdtime), '%Y-%m-%d %H:%M:%S.%f%z').date()
                date = date.strftime('%d/%m/%Y')
                new_timediff = datetime.strptime(str(timediff), '%H:%M:%S.%f').time()
                latetime = time(0,15,0,0)
                x = f"{student.to_dict()['name']} {student.to_dict()['surname']}"
                if x not in stdname:
                    stdname.append(x)
                if new_timediff > latetime:
                    late1 += 1
                else:
                    TakeTheExam1 += 1
            elif doc.to_dict()[std] == False:
                x = f"{student.to_dict()['name']} {student.to_dict()['surname']}"
                if x not in stdname:
                    stdname.append(x)
                NotTakeTheExam1 += 1
        TakeTheExam.append(TakeTheExam1)
        late.append(late1)
        NotTakeTheExam.append(NotTakeTheExam1)
        count += 1
        getID = str(doc.id)
        getID = getID.split("_")
        testname.append(getID[0])
        data2 = pd.DataFrame({"True": [TakeTheExam1],"Late":[late1],"False": [NotTakeTheExam1]})
        sjName = db.collection("subject").document(getID[0]).get()
        data2.index = [sjName.to_dict()["name"]]
        data = pd.concat([data, data2])
    else:
        st.write('No such document!')

getTestName = []
chart_data = pd.DataFrame(data)
st.bar_chart(chart_data, color=["#c44141","#c4a841","#32a852"])

for s in testname:
    subject = db.collection("subject").document(s).get()
    newsubject = subject.to_dict()['name']
    getTestName.append(newsubject)
subjectSelect = st.sidebar.selectbox("Subject",getTestName,index=None,placeholder="Select Subject...")
studentSelect = st.sidebar.selectbox("Student",stdname,index=None,placeholder="Select Student...")
if subjectSelect:
    docs = (
        db.collection("test")
        .where(filter=FieldFilter("Teacher", "==", st.session_state['email']))
        .where(filter=FieldFilter("subject", "==", subjectSelect))
        .stream()
    )
else:
    docs = (
        db.collection("test")
        .where(filter=FieldFilter("Teacher", "==", st.session_state['email']))
        .stream()
    )
for doc in docs:
    dataID = db.collection("test").document(doc.id)
    s = doc.id
    s = s.split("_")
    subject = db.collection("subject").document(s[0]).get()
    newsubject = subject.to_dict()['name']
    sj = newsubject
    st.markdown(f"""<h1 style="font-family: 'Kanit', sans-serif; color:#6896d4;">{sj} - {doc.to_dict()['room']}</h1>""",
                    unsafe_allow_html=True)
    # st.subheader(doc.id)
    startTime = doc.to_dict()[f"start_test"]
    startTime1 = datetime.strptime(str(startTime), '%Y-%m-%d %H:%M:%S.%f%z').time()
    startTime1 = startTime1.strftime('%H:%M:%S')
    date = datetime.strptime(str(startTime), '%Y-%m-%d %H:%M:%S.%f%z').date()
    date = date.strftime('%d/%m/%Y')
    container = st.container(border=True)
    container.markdown(f"""<h5 style="font-family: 'Kanit', sans-serif; color:#6896d4;">วันที่สอบ : {date}</h5>""",
                unsafe_allow_html=True)
    container.markdown(f"""<h5 style="font-family: 'Kanit', sans-serif; color:#6896d4;">เวลาเริ่มสอบ : {startTime1}</h5>""",
                       unsafe_allow_html=True)
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
            try:
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
                        st.markdown(f"""<p style="font-family: 'Kanit', sans-serif; color:#c4a841;font-size:18px;">{txt}</p>""",unsafe_allow_html=True)
                    else:
                        txt = f"{student.to_dict()['name']} {student.to_dict()['surname']} เข้าสอบวิชา {sj} วันที่ {date} เวลา {time1}"
                        st.markdown(f"""<p style="font-family: 'Kanit', sans-serif; color:#68d474;font-size:18px;">{txt}</p>""",unsafe_allow_html=True)
                        # st.write(f"{student.to_dict()['name']} {student.to_dict()['surname']} เข้าสอบวิชา {doc.id} วันที่ {date} เวลา {time1}")
                elif doc.to_dict()[std] == False:
                    txt = f"{student.to_dict()['name']} {student.to_dict()['surname']} ไม่ได้เข้าสอบวิชา {sj}"
                    st.markdown(f"""<p style="font-family: 'Kanit', sans-serif; color:#d46868;font-size:18px;">{txt}</p>""",unsafe_allow_html=True)
                    # st.write(f"{student.to_dict()['name']} {student.to_dict()['surname']} ไม่ได้เข้าสอบวิชา {doc.id}")
            except:
                st.warning('No such document!', icon="⚠️")
