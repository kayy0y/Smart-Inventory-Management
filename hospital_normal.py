import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- PAGE SETUP ---
st.set_page_config(
    page_title="MediCare+ Dashboard",
    page_icon="🏥",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    body {background-color: #f5f6fa;}
    .metric-box {
        background-color: #fff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .patient-card {
        background: #fff;
        padding: 10px 14px;
        border-radius: 10px;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #000; /* Make text black */
    }
    .patient-info {
        text-align: left;
        font-weight: 500;
    }
    .status {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 600;
        text-align: center;
        min-width: 80px;
    }
    .admitted {background-color: #dbeafe; color: #1e3a8a;}
    .outpatient {background-color: #d1fae5; color: #065f46;}
    .surgery {background-color: #ede9fe; color: #5b21b6;}
    .discharged {background-color: #f3f4f6; color: #374151;}
    .critical {background-color: #fee2e2; color: #991b1b;}
</style>
""", unsafe_allow_html=True)

# --- INITIAL DATA ---
def init_data():
    """Initialize the default session data only once."""
    if "patients" not in st.session_state:
        st.session_state.patients = pd.DataFrame([
            {"ID": "P001", "Name": "Rahul Sharma", "Age": 45, "Department": "Cardiology", "Status": "Admitted", "Updated": "2h ago"},
            {"ID": "P002", "Name": "Akshit Sinha", "Age": 32, "Department": "Neurology", "Status": "Outpatient", "Updated": "3h ago"},
            {"ID": "P003", "Name": "Palash Sinha", "Age": 58, "Department": "Orthopedics", "Status": "Surgery", "Updated": "4h ago"},
            {"ID": "P004", "Name": "Kamakshi Vishwakarma", "Age": 28, "Department": "Pediatrics", "Status": "Discharged", "Updated": "5h ago"},
            {"ID": "P005", "Name": "Vedika Jha", "Age": 51, "Department": "Emergency", "Status": "Critical", "Updated": "1h ago"}
        ])
    if "appointments" not in st.session_state:
        st.session_state.appointments = pd.DataFrame([
            {"Patient": "Rahul Sharma", "Doctor": "Dr. A.K. Thakur", "Time": "10:00 AM", "Department": "Cardiology"},
            {"Patient": "Akshit Sinha", "Doctor": "Dr. Sarah Sinha", "Time": "11:30 AM", "Department": "Neurology"},
            {"Patient": "Palash Sinha", "Doctor": "Dr. Bhumi Yadav", "Time": "2:00 PM", "Department": "Orthopedics"}
        ])
    if "beds" not in st.session_state:
        st.session_state.beds = pd.DataFrame([
            {"Bed ID": "B101", "Ward": "ICU", "Status": "Occupied", "Patient": "Rahul Sharma"},
            {"Bed ID": "B102", "Ward": "ICU", "Status": "Available", "Patient": ""},
            {"Bed ID": "B201", "Ward": "General", "Status": "Occupied", "Patient": "Akshit Sinha"}
        ])
    if "staff" not in st.session_state:
        st.session_state.staff = pd.DataFrame([
            {"ID": "S001", "Name": "Dr. A.K. Thakur", "Role": "Cardiologist", "Shift": "Morning", "Status": "On Duty"},
            {"ID": "S002", "Name": "Dr. Bhumi Yadav", "Role": "Orthopedic Surgeon", "Shift": "Evening", "Status": "On Duty"},
            {"ID": "S003", "Name": "Dr. Anita Vishwakarma", "Role": "Pediatrician", "Shift": "Night", "Status": "Off Duty"}
        ])

init_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏥 MediCare+")
page = st.sidebar.radio(
    "Navigate",
    ["📊 Overview", "👥 Patients", "📅 Appointments", "🛏️ Beds", "👨‍⚕️ Staff"]
)

# --- PAGE: OVERVIEW ---
if page == "📊 Overview":
    st.title("📊 Hospital Overview")
    st.caption(f"📅 {datetime.now().strftime('%A, %B %d, %Y')}")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Patients", len(st.session_state.patients))
    col2.metric("Available Beds", len(st.session_state.beds.query('Status == "Available"')))
    col3.metric("Appointments", len(st.session_state.appointments))
    col4.metric("Staff On Duty", len(st.session_state.staff.query('Status == "On Duty"')))

    # Charts
    left, right = st.columns([2, 1])
    with left:
        st.subheader("Weekly Trends")
        data = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Patients": [40, 45, 52, 48, 60, 55, 38],
            "Appointments": [30, 35, 38, 32, 40, 28, 25]
        })
        fig = px.line(data, x="Day", y=["Patients", "Appointments"], markers=True, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Department Breakdown")
        dept_counts = st.session_state.patients["Department"].value_counts()
        fig = px.pie(values=dept_counts.values, names=dept_counts.index, hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    # Recent Patients
    st.subheader("🧾 Recent Patients")
    for _, row in st.session_state.patients.head().iterrows():
        st.markdown(
            f"""
            <div class='patient-card'>
                <div class='patient-info'>
                    <b>{row['Name']}</b> ({row['Age']} yrs) - {row['Department']}
                </div>
                <div>
                    <span class='status {row['Status'].lower()}'>{row['Status']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- PAGE: PATIENTS ---
elif page == "👥 Patients":
    st.title("👥 Patient Management")

    tabs = st.tabs(["📋 All Patients", "➕ Add Patient"])
    with tabs[0]:
        st.dataframe(st.session_state.patients, use_container_width=True)
    with tabs[1]:
        with st.form("new_patient"):
            name = st.text_input("Name")
            age = st.number_input("Age", 0, 120)
            dept = st.selectbox("Department", ["Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Emergency"])
            status = st.selectbox("Status", ["Admitted", "Outpatient", "Surgery", "Discharged", "Critical"])
            submitted = st.form_submit_button("Add Patient")
            if submitted and name:
                new_row = pd.DataFrame([{
                    "ID": f"P{len(st.session_state.patients)+1:03}",
                    "Name": name, "Age": age, "Department": dept,
                    "Status": status, "Updated": "Just now"
                }])
                st.session_state.patients = pd.concat([st.session_state.patients, new_row], ignore_index=True)
                st.success(f"✅ Added patient: {name}")

# --- PAGE: APPOINTMENTS ---
elif page == "📅 Appointments":
    st.title("📅 Appointment Management")
    st.dataframe(st.session_state.appointments, use_container_width=True)

# --- PAGE: BEDS ---
elif page == "🛏️ Beds":
    st.title("🛏️ Bed Management")
    st.dataframe(st.session_state.beds, use_container_width=True)

# --- PAGE: STAFF ---
elif page == "👨‍⚕️ Staff":
    st.title("👨‍⚕️ Staff Management")
    st.dataframe(st.session_state.staff, use_container_width=True)
