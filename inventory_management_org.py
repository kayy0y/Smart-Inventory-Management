import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(page_title="Hospital Inventory System", page_icon="🏥", layout="wide")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'username' not in st.session_state:
    st.session_state.username = None

# Initialize inventory data in session state
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame({
        'Item_ID': ['MED001', 'MED002', 'SUP001', 'SUP002', 'SUP003', 'MED003', 'SUP004', 'MED004'],
        'Item_Name': ['Paracetamol 500mg', 'Injection Ceftriaxone', 'Disposable Syringes', 'Surgical Gloves', 
                      'Gauze Dressings', 'Injection Adrenaline', 'IV Cannula', 'Morphine 10mg'],
        'Category': ['Medicine', 'Medicine', 'Supply', 'Supply', 'Supply', 'Emergency Medicine', 'Supply', 'Controlled Medicine'],
        'Quantity': [500, 120, 1500, 2000, 800, 50, 600, 30],
        'Min_Stock': [200, 50, 500, 800, 300, 20, 200, 10],
        'Unit': ['Tablet', 'Vial', 'Piece', 'Pair', 'Packet', 'Vial', 'Piece', 'Vial'],
        'Expiry_Date': ['2026-05-15', '2025-12-20', '2027-01-10', '2026-08-25', '2026-03-30', '2025-11-30', '2027-02-15', '2026-06-10'],
        'Location': ['Pharmacy', 'Pharmacy', 'Medical Store', 'Medical Store', 'Medical Store', 'Emergency Ward', 'Medical Store', 'Pharmacy'],
        'Last_Updated': [datetime.now().strftime('%Y-%m-%d %H:%M')] * 8
    })

if 'usage_log' not in st.session_state:
    st.session_state.usage_log = pd.DataFrame(columns=['Date_Time', 'Item_ID', 'Item_Name', 'Quantity_Used', 'Used_By', 'Department', 'Remarks'])

if 'purchase_orders' not in st.session_state:
    st.session_state.purchase_orders = pd.DataFrame(columns=['PO_ID', 'Date', 'Item_Name', 'Quantity', 'Supplier', 'Status', 'Requested_By'])

# User credentials (in real app, use secure database)
users = {
    'nurse1': {'password': 'nurse123', 'role': 'Nurse', 'name': 'Sister Priya'},
    'doctor1': {'password': 'doc123', 'role': 'Doctor', 'name': 'Dr. Sharma'},
    'admin1': {'password': 'admin123', 'role': 'Admin', 'name': 'Hospital Admin1'},
    'nurse2': {'password': 'nurse122', 'role': 'Nurse', 'name': 'Sister P.Kaur'},
    'doctor2': {'password': 'doc122', 'role': 'Doctor', 'name': 'Dr. S.K.Thakur'},
    'admin2': {'password': 'admin122', 'role': 'Admin', 'name': 'Hospital Admin2'},
    'nurse3': {'password': 'nurse121', 'role': 'Nurse', 'name': 'Sister Shefali'},
    'doctor3': {'password': 'doc121', 'role': 'Doctor', 'name': 'Dr. A.K.Gupta'},
    'admin3': {'password': 'admin121', 'role': 'Admin', 'name': 'Hospital Admin3'}
}

def login_page():
    st.title("🏥 Hospital Inventory Management System")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("🔐 Login")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        st.info("""
        **Demo Credentials:**
        - Nurse: `nurse1` / `nurse123`
        - Doctor: `doctor1` / `doc123`
        - Admin: `admin1` / `admin123`
        """)
        
        if st.button("Login", type="primary", use_container_width=True):
            if username in users and users[username]['password'] == password:
                st.session_state.logged_in = True
                st.session_state.user_role = users[username]['role']
                st.session_state.username = users[username]['name']
                st.rerun()
            else:
                st.error("❎ Invalid username or password")

def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.rerun()

def nurse_dashboard():
    st.title("👩‍⚕️ Nurse Dashboard")
    st.write(f"Welcome, **{st.session_state.username}**")
    
    tab1, tab2, tab3 = st.tabs(["📦 View Inventory", "📝 Record Usage", "⚠️ Low Stock Alerts"])
    
    with tab1:
        st.subheader("Current Inventory")
        
        # Search and filter
        col1, col2 = st.columns([2, 1])
        with col1:
            search = st.text_input("🔍 Search items", placeholder="Search by item name...")
        with col2:
            category_filter = st.selectbox("Filter by Category", ['All'] + list(st.session_state.inventory['Category'].unique()))
        
        # Filter data
        filtered_df = st.session_state.inventory.copy()
        if search:
            filtered_df = filtered_df[filtered_df['Item_Name'].str.contains(search, case=False)]
        if category_filter != 'All':
            filtered_df = filtered_df[filtered_df['Category'] == category_filter]
        
        # Display inventory with color coding
        def highlight_low_stock(row):
            if row['Quantity'] <= row['Min_Stock']:
                return ['background-color: #ffcccc'] * len(row)
            elif row['Quantity'] <= row['Min_Stock'] * 1.5:
                return ['background-color: #fff3cd'] * len(row)
            return [''] * len(row)
        
        st.dataframe(
            filtered_df.style.apply(highlight_low_stock, axis=1),
            use_container_width=True,
            height=400
        )
    
    with tab2:
        st.subheader("Record Item Usage")
        
        col1, col2 = st.columns(2)
        with col1:
            item_to_use = st.selectbox("Select Item", st.session_state.inventory['Item_Name'].tolist())
            quantity_used = st.number_input("Quantity Used", min_value=1, value=1)
            department = st.selectbox("Department", ['General Ward', 'ICU', 'Emergency', 'OT', 'OPD'])
        
        with col2:
            remarks = st.text_area("Remarks (Optional)", placeholder="Enter any notes...")
        
        if st.button("Record Usage", type="primary"):
            item_row = st.session_state.inventory[st.session_state.inventory['Item_Name'] == item_to_use]
            if not item_row.empty:
                current_qty = item_row['Quantity'].values[0]
                if current_qty >= quantity_used:
                    # Update inventory
                    st.session_state.inventory.loc[st.session_state.inventory['Item_Name'] == item_to_use, 'Quantity'] -= quantity_used
                    st.session_state.inventory.loc[st.session_state.inventory['Item_Name'] == item_to_use, 'Last_Updated'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                    
                    # Log usage
                    new_log = pd.DataFrame({
                        'Date_Time': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                        'Item_ID': [item_row['Item_ID'].values[0]],
                        'Item_Name': [item_to_use],
                        'Quantity_Used': [quantity_used],
                        'Used_By': [st.session_state.username],
                        'Department': [department],
                        'Remarks': [remarks]
                    })
                    st.session_state.usage_log = pd.concat([st.session_state.usage_log, new_log], ignore_index=True)
                    
                    st.success(f"✅ Usage recorded! Remaining quantity: {current_qty - quantity_used}")
                    st.rerun()
                else:
                    st.error(f"❌ Insufficient stock! Available: {current_qty}")
    
    with tab3:
        st.subheader("⚠️ Low Stock Alerts")
        low_stock = st.session_state.inventory[st.session_state.inventory['Quantity'] <= st.session_state.inventory['Min_Stock']]
        
        if not low_stock.empty:
            st.error(f"🚨 {len(low_stock)} items are at or below minimum stock level!")
            st.dataframe(low_stock[['Item_Name', 'Quantity', 'Min_Stock', 'Location']], use_container_width=True)
        else:
            st.success("✅ All items are adequately stocked!")

def doctor_dashboard():
    st.title("👨‍⚕️ Doctor Dashboard")
    st.write(f"Welcome, **{st.session_state.username}**")
    
    tab1, tab2, tab3 = st.tabs(["📦 View Inventory", "📝 Record Usage", "📋 Request Orders"])
    
    with tab1:
        st.subheader("Current Inventory - Priority Items")
        
        # Focus on emergency and essential items
        priority_categories = ['Emergency Medicine', 'Controlled Medicine', 'Medicine']
        priority_items = st.session_state.inventory[st.session_state.inventory['Category'].isin(priority_categories)]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Emergency Medicines", len(st.session_state.inventory[st.session_state.inventory['Category'] == 'Emergency Medicine']))
        with col2:
            st.metric("Controlled Medicines", len(st.session_state.inventory[st.session_state.inventory['Category'] == 'Controlled Medicine']))
        
        st.dataframe(priority_items, use_container_width=True, height=350)
    
    with tab2:
        st.subheader("Record Usage")
        
        col1, col2 = st.columns(2)
        with col1:
            item_to_use = st.selectbox("Select Item", st.session_state.inventory['Item_Name'].tolist())
            quantity_used = st.number_input("Quantity", min_value=1, value=1)
        
        with col2:
            department = st.selectbox("Department", ['ICU', 'Emergency', 'OT', 'General Ward', 'OPD'])
            remarks = st.text_input("Patient ID / Remarks", placeholder="Enter patient details...")
        
        if st.button("Record Usage", type="primary"):
            item_row = st.session_state.inventory[st.session_state.inventory['Item_Name'] == item_to_use]
            if not item_row.empty:
                current_qty = item_row['Quantity'].values[0]
                if current_qty >= quantity_used:
                    st.session_state.inventory.loc[st.session_state.inventory['Item_Name'] == item_to_use, 'Quantity'] -= quantity_used
                    st.session_state.inventory.loc[st.session_state.inventory['Item_Name'] == item_to_use, 'Last_Updated'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                    
                    new_log = pd.DataFrame({
                        'Date_Time': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                        'Item_ID': [item_row['Item_ID'].values[0]],
                        'Item_Name': [item_to_use],
                        'Quantity_Used': [quantity_used],
                        'Used_By': [st.session_state.username],
                        'Department': [department],
                        'Remarks': [remarks]
                    })
                    st.session_state.usage_log = pd.concat([st.session_state.usage_log, new_log], ignore_index=True)
                    
                    st.success(f"✅ Usage recorded! Remaining: {current_qty - quantity_used}")
                    st.rerun()
                else:
                    st.error(f"❌ Insufficient stock! Available: {current_qty}")
    
    with tab3:
        st.subheader("Request Purchase Order")
        
        col1, col2 = st.columns(2)
        with col1:
            item_name = st.text_input("Item Name", placeholder="Enter item name")
            quantity = st.number_input("Quantity Needed", min_value=1, value=10)
        
        with col2:
            urgency = st.selectbox("Urgency", ['Normal', 'Urgent', 'Emergency'])
            reason = st.text_area("Reason for Request", placeholder="Why is this needed?")
        
        if st.button("Submit Request", type="primary"):
            po_id = f"PO{len(st.session_state.purchase_orders) + 1001}"
            new_po = pd.DataFrame({
                'PO_ID': [po_id],
                'Date': [datetime.now().strftime('%Y-%m-%d')],
                'Item_Name': [item_name],
                'Quantity': [quantity],
                'Supplier': ['Pending'],
                'Status': [f'{urgency} - Pending Approval'],
                'Requested_By': [st.session_state.username]
            })
            st.session_state.purchase_orders = pd.concat([st.session_state.purchase_orders, new_po], ignore_index=True)
            st.success(f"✅ Purchase request {po_id} submitted successfully!")

def admin_dashboard():
    st.title("🏥 Admin Dashboard - Inventory Management")
    st.write(f"Welcome, **{st.session_state.username}**")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "➕ Add Items", "📦 Manage Stock", "🛒 Purchase Orders", "📈 Reports"])
    
    with tab1:
        st.subheader("Inventory Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Items", len(st.session_state.inventory))
        with col2:
            low_stock_count = len(st.session_state.inventory[st.session_state.inventory['Quantity'] <= st.session_state.inventory['Min_Stock']])
            st.metric("Low Stock Items", low_stock_count, delta=f"-{low_stock_count}", delta_color="inverse")
        with col3:
            st.metric("Total Usage Logs", len(st.session_state.usage_log))
        with col4:
            st.metric("Pending Orders", len(st.session_state.purchase_orders[st.session_state.purchase_orders['Status'].str.contains('Pending', na=False)]))
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("⚠️ Critical Low Stock")
            critical = st.session_state.inventory[st.session_state.inventory['Quantity'] <= st.session_state.inventory['Min_Stock']]
            if not critical.empty:
                st.dataframe(critical[['Item_Name', 'Quantity', 'Min_Stock']], use_container_width=True)
            else:
                st.success("No critical items!")
        
        with col2:
            st.subheader("🔜 Expiring Soon (30 days)")
            st.session_state.inventory['Expiry_Date'] = pd.to_datetime(st.session_state.inventory['Expiry_Date'])
            expiring = st.session_state.inventory[
                st.session_state.inventory['Expiry_Date'] <= datetime.now() + timedelta(days=30)
            ]
            if not expiring.empty:
                st.dataframe(expiring[['Item_Name', 'Quantity', 'Expiry_Date']], use_container_width=True)
            else:
                st.success("No items expiring soon!")
    
    with tab2:
        st.subheader("Add New Item to Inventory")
        
        col1, col2 = st.columns(2)
        with col1:
            new_item_id = st.text_input("Item ID", placeholder="e.g., MED005")
            new_item_name = st.text_input("Item Name", placeholder="e.g., Injection Insulin")
            new_category = st.selectbox("Category", ['Medicine', 'Supply', 'Emergency Medicine', 'Controlled Medicine', 'Equipment'])
            new_quantity = st.number_input("Initial Quantity", min_value=0, value=100)
        
        with col2:
            new_min_stock = st.number_input("Minimum Stock Level", min_value=0, value=20)
            new_unit = st.text_input("Unit", placeholder="e.g., Vial, Piece, Tablet")
            new_expiry = st.date_input("Expiry Date")
            new_location = st.text_input("Storage Location", placeholder="e.g., Pharmacy, Medical Store")
        
        if st.button("Add Item", type="primary"):
            new_item = pd.DataFrame({
                'Item_ID': [new_item_id],
                'Item_Name': [new_item_name],
                'Category': [new_category],
                'Quantity': [new_quantity],
                'Min_Stock': [new_min_stock],
                'Unit': [new_unit],
                'Expiry_Date': [new_expiry.strftime('%Y-%m-%d')],
                'Location': [new_location],
                'Last_Updated': [datetime.now().strftime('%Y-%m-%d %H:%M')]
            })
            st.session_state.inventory = pd.concat([st.session_state.inventory, new_item], ignore_index=True)
            st.success(f"✅ Item '{new_item_name}' added successfully!")
    
    with tab3:
        st.subheader("Manage Current Stock")
        
        # Select item to update
        item_to_update = st.selectbox("Select Item to Update", st.session_state.inventory['Item_Name'].tolist())
        
        if item_to_update:
            item_data = st.session_state.inventory[st.session_state.inventory['Item_Name'] == item_to_update].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"Current Quantity: **{item_data['Quantity']}** {item_data['Unit']}")
                new_qty = st.number_input("Update Quantity", min_value=0, value=int(item_data['Quantity']))
            
            with col2:
                st.info(f"Min Stock: **{item_data['Min_Stock']}**")
                new_min = st.number_input("Update Min Stock", min_value=0, value=int(item_data['Min_Stock']))
            
            with col3:
                st.info(f"Location: **{item_data['Location']}**")
                new_loc = st.text_input("Update Location", value=item_data['Location'])
            
            if st.button("Update Stock", type="primary"):
                st.session_state.inventory.loc[st.session_state.inventory['Item_Name'] == item_to_update, 'Quantity'] = new_qty
                st.session_state.inventory.loc[st.session_state.inventory['Item_Name'] == item_to_update, 'Min_Stock'] = new_min
                st.session_state.inventory.loc[st.session_state.inventory['Item_Name'] == item_to_update, 'Location'] = new_loc
                st.session_state.inventory.loc[st.session_state.inventory['Item_Name'] == item_to_update, 'Last_Updated'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                st.success("✅ Stock updated successfully!")
                st.rerun()
    
    with tab4:
        st.subheader("Purchase Orders Management")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("**Create New Purchase Order**")
            po_item = st.text_input("Item Name", key="po_item")
            po_qty = st.number_input("Quantity", min_value=1, value=100, key="po_qty")
        with col2:
            po_supplier = st.text_input("Supplier Name", key="po_supplier")
            if st.button("Create PO", type="primary"):
                po_id = f"PO{len(st.session_state.purchase_orders) + 1001}"
                new_po = pd.DataFrame({
                    'PO_ID': [po_id],
                    'Date': [datetime.now().strftime('%Y-%m-%d')],
                    'Item_Name': [po_item],
                    'Quantity': [po_qty],
                    'Supplier': [po_supplier],
                    'Status': ['Approved'],
                    'Requested_By': [st.session_state.username]
                })
                st.session_state.purchase_orders = pd.concat([st.session_state.purchase_orders, new_po], ignore_index=True)
                st.success(f"✅ Purchase Order {po_id} created!")
        
        st.markdown("---")
        st.write("**All Purchase Orders**")
        if not st.session_state.purchase_orders.empty:
            st.dataframe(st.session_state.purchase_orders, use_container_width=True)
        else:
            st.info("No purchase orders yet")
    
    with tab5:
        st.subheader("Usage Reports & Analytics")
        
        if not st.session_state.usage_log.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Usage by Department**")
                dept_usage = st.session_state.usage_log.groupby('Department')['Quantity_Used'].sum().reset_index()
                st.dataframe(dept_usage, use_container_width=True)
            
            with col2:
                st.write("**Top 5 Most Used Items**")
                top_items = st.session_state.usage_log.groupby('Item_Name')['Quantity_Used'].sum().nlargest(5).reset_index()
                st.dataframe(top_items, use_container_width=True)
            
            st.markdown("---")
            st.write("**Recent Usage Log**")
            st.dataframe(st.session_state.usage_log.tail(10), use_container_width=True)
            
            # Download reports
            if st.button("📥 Download Full Usage Report"):
                csv = st.session_state.usage_log.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"usage_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("No usage data available yet")

# Main app logic
if not st.session_state.logged_in:
    login_page()
else:
    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3063/3063155.png", width=100)
        st.title("Navigation")
        st.write(f"**Role:** {st.session_state.user_role}")
        st.write(f"**User:** {st.session_state.username}")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
        
    
    # Route to appropriate dashboard
    if st.session_state.user_role == 'Nurse':
        nurse_dashboard()
    elif st.session_state.user_role == 'Doctor':
        doctor_dashboard()
    elif st.session_state.user_role == 'Admin':

        admin_dashboard()
