import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Hospital Management Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Session State ----------------
if 'notifications' not in st.session_state:
    st.session_state.notifications = 5

# ---------------- Data Functions ----------------
def get_patient_trend_data():
    return pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'Patients': [45, 52, 48, 61, 55, 38, 35],
        'Appointments': [32, 38, 35, 42, 40, 28, 25],
        'Emergency': [8, 12, 10, 15, 11, 9, 7]
    })

def get_department_data():
    return pd.DataFrame({
        'Department': ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Emergency'],
        'Patients': [145, 120, 98, 75, 52],
        'Percentage': [30, 25, 20, 15, 10]
    })

def get_recent_patients():
    return pd.DataFrame([
        {'ID': 'P001', 'Name': 'John Smith', 'Age': 45, 'Department': 'Cardiology', 'Status': 'Admitted', 'Time': '2 hours ago'},
        {'ID': 'P002', 'Name': 'Sarah Johnson', 'Age': 32, 'Department': 'Neurology', 'Status': 'Outpatient', 'Time': '3 hours ago'},
        {'ID': 'P003', 'Name': 'Michael Brown', 'Age': 58, 'Department': 'Orthopedics', 'Status': 'Surgery', 'Time': '4 hours ago'},
        {'ID': 'P004', 'Name': 'Emily Davis', 'Age': 28, 'Department': 'Pediatrics', 'Status': 'Discharged', 'Time': '5 hours ago'},
        {'ID': 'P005', 'Name': 'David Wilson', 'Age': 51, 'Department': 'Emergency', 'Status': 'Critical', 'Time': '1 hour ago'},
    ])

def get_appointments():
    return pd.DataFrame([
        {'Patient': 'Alice Cooper', 'Doctor': 'Dr. James Wilson', 'Time': '10:00 AM', 'Department': 'Cardiology'},
        {'Patient': 'Bob Martin', 'Doctor': 'Dr. Sarah Chen', 'Time': '11:30 AM', 'Department': 'Neurology'},
        {'Patient': 'Carol White', 'Doctor': 'Dr. Michael Ross', 'Time': '02:00 PM', 'Department': 'Orthopedics'},
        {'Patient': 'Daniel Lee', 'Doctor': 'Dr. Emily Stone', 'Time': '03:30 PM', 'Department': 'Pediatrics'},
    ])

status_colors = {
    'Admitted': ('#dbeafe', '#1e40af'),
    'Outpatient': ('#d1fae5', '#065f46'),
    'Surgery': ('#e9d5ff', '#6b21a8'),
    'Discharged': ('#f3f4f6', '#374151'),
    'Critical': ('#fee2e2', '#991b1b')
}

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("## 🏥 MediCare+")
    st.markdown("---")
    
    selected_tab = st.radio(
        "Navigation",
        ['Overview', 'Patients', 'Bed Management', 'Appointments', 'Staff']
    )
    
    st.markdown("---")
    
    time_range = st.selectbox("📅 Time Range", ['Today', 'This Week', 'This Month', 'This Year'])
    search_query = st.text_input("🔍 Search", placeholder="Search patients, doctors...")
    
    st.markdown("---")
    
    st.markdown(f"### 🔔 Notifications")
    st.info(f"You have {st.session_state.notifications} new notifications")
    
    st.markdown("---")
    
    st.markdown("### 👤 Admin")
    st.markdown("**John Doe**")
    st.markdown("Administrator")

# ---------------- Main Content ----------------
st.title("🏥 Hospital Management Dashboard")
st.markdown(f"**{datetime.now().strftime('%A, %B %d, %Y')}** | {time_range}")

# ---------------- Stats Cards ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Total Patients", "1,247", "8.2%")
col2.metric("🛏️ Available Beds", "42", "-3.5%")
col3.metric("📅 Appointments", "156", "12.4%")
col4.metric("👨‍⚕️ Staff on Duty", "87", "5.1%")

st.markdown("---")

# ---------------- Charts ----------------
chart_col1, chart_col2 = st.columns([2,1])

# Patient trends
with chart_col1:
    st.subheader("📈 Patient Trends")
    trend_tab = st.radio("Select View:", ["Patients Activity", "Revenue"], horizontal=True, key="trend_tabs")
    
    patient_data = get_patient_trend_data()
    
    if trend_tab == "Patients Activity":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=patient_data['Day'], y=patient_data['Patients'], mode='lines', name='Patients',
                                 fill='tozeroy', line=dict(color='#3b82f6', width=3), fillcolor='rgba(59, 130, 246, 0.3)'))
        fig.add_trace(go.Scatter(x=patient_data['Day'], y=patient_data['Appointments'], mode='lines', name='Appointments',
                                 fill='tozeroy', line=dict(color='#8b5cf6', width=3), fillcolor='rgba(139, 92, 246, 0.3)'))
    else:
        revenue_data = pd.DataFrame({'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 
                                     'Revenue': [45000, 52000, 48000, 61000, 55000, 38000, 35000]})
        fig = px.bar(revenue_data, x='Day', y='Revenue', color_discrete_sequence=['#3b82f6'])
    
    fig.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

# Department distribution
with chart_col2:
    st.subheader("🏥 Department Distribution")
    dept_data = get_department_data()
    fig = px.pie(dept_data, values='Percentage', names='Department', hole=0.3,
                 color_discrete_sequence=['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981'])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=350, showlegend=False, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ---------------- Tables ----------------
table_col1, table_col2 = st.columns(2)

# Recent Patients
with table_col1:
    st.subheader("🆕 Recent Patients")
    patients_df = get_recent_patients()
    
    for _, row in patients_df.iterrows():
        bg_color, text_color = status_colors.get(row['Status'], ('#f3f4f6', '#374151'))
        st.markdown(f"""
            <div style="background-color:{bg_color}; padding:10px; border-radius:8px; margin-bottom:8px;">
                <strong style="color:{text_color}">{row['Name']}</strong> | {row['Department']} | Age {row['Age']} | {row['Status']}
                <span style="float:right; color:#6b7280;">{row['Time']}</span>
            </div>
        """, unsafe_allow_html=True)

# Upcoming Appointments
with table_col2:
    st.subheader("📅 Upcoming Appointments")
    appointments_df = get_appointments()
    
    for _, row in appointments_df.iterrows():
        initials = ''.join([w[0] for w in row['Patient'].split()])
        st.markdown(f"""
            <div style="background:linear-gradient(135deg,#eff6ff,#f3e8ff); padding:10px; border-radius:8px; margin-bottom:8px;">
                <strong>{row['Patient']}</strong> | {row['Doctor']} | {row['Department']}
                <span style="float:right; color:#3b82f6;">{row['Time']}</span>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ---------------- Quick Actions ----------------
st.subheader("⚡ Quick Actions")
action_col1, action_col2, action_col3, action_col4 = st.columns(4)

if action_col1.button("👥 Admit Patient"):
    st.toast("Opening patient admission form...")
if action_col2.button("📅 Schedule"):
    st.toast("Opening appointment scheduler...")
if action_col3.button("🛏️ Bed Status"):
    st.toast("Loading bed availability...")
if action_col4.button("🚨 Emergency"):
    st.toast("Emergency protocol activated!", icon="🚨")

