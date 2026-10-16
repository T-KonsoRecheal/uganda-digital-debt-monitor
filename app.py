import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="Uganda Digital Credit Monitor", layout="wide")

def load_data():
    data = pd.read_csv("uganda_digital_debt_data.csv")
    data['Status_Label'] = data['Default_Status'].map({0: 'Performing', 1: 'Defaulted'})
    data['Search_Key'] = data['Borrower_Name'] + " | MTN: " + data['MTN_Phone'] + " | District: " + data['District'] + " | Status: " + data['Status_Label']
    return data

df = load_data()

st.title("National Digital Debt Exposure & Loan Stacking Monitor")
st.markdown("This platform analyzes cross-network digital loan accumulation, debt stress, and default risks across Uganda.")
st.divider()

st.sidebar.header("Filter Criteria")
selected_region = st.sidebar.selectbox("Select Region", options=["All Regions"] + sorted(list(df['Region'].unique())))

if selected_region != "All Regions":
    filtered_df = df[df['Region'] == selected_region]
    available_districts = ["All Districts"] + sorted(list(filtered_df['District'].unique()))
else:
    filtered_df = df
    available_districts = ["All Districts"] + sorted(list(df['District'].unique()))

selected_district = st.sidebar.selectbox("Select District", options=available_districts)
if selected_district != "All Districts":
    filtered_df = filtered_df[filtered_df['District'] == selected_district]

col1, col2, col3, col4 = st.columns(4)
total_borrowers = len(filtered_df)
avg_loans = filtered_df['Active_Digital_Loans'].mean() if total_borrowers > 0 else 0
overall_default_rate = (filtered_df['Default_Status'].sum() / total_borrowers) * 100 if total_borrowers > 0 else 0
total_exposure = filtered_df['Total_Debt_UGX'].sum()

col1.metric("Total Sample Size", f"{total_borrowers:,}")
col2.metric("Avg Active Loans / Person", f"{avg_loans:.1f}")
col3.metric("Default Rate", f"{overall_default_rate:.1f}%")
col4.metric("Total Debt Exposure (UGX)", f"{total_exposure:,.0f}")
st.divider()

tab1, tab2, tab3 = st.tabs(["National Geospatial Risk Overview", "Borrower Debt Capacity Calculator", "👤 Individual Borrower Lookup"])

# --- TAB 1: GEOSPATIAL MAP ---
with tab1:
    st.subheader("Uganda Regional Debt Intensity Map")
    map_fig = px.density_map(
        filtered_df, lat="Latitude", lon="Longitude", z="Total_Debt_UGX",
        radius=12, center={"lat": 1.3733, "lon": 32.2903}, zoom=6.5,
        color_continuous_scale="Viridis", opacity=0.7, height=580
    )
    st.plotly_chart(map_fig, use_container_width=True)

# --- TAB 2: DEBT CAPACITY CALCULATOR (NIN INTEGRATED) ---
with tab2:
    st.subheader("Individual Cash Flow & Loan Capacity Evaluator (By NIN)")
    st.markdown("Enter or select an individual's **National ID Number (NIN)** to automatically retrieve their verified income and existing liabilities, then evaluate a new proposed credit request.")
    
    nin_options = sorted(df['National_ID_Number'].unique())
    selected_nin = st.selectbox(
        "Search or Select Borrower National ID Number (NIN)",
        options=nin_options,
        index=0,
        placeholder="Type or select NIN (e.g., CM... or CF...)..."
    )
    
    if selected_nin:
        b_record = df[df['National_ID_Number'] == selected_nin].iloc[0]
        
        st.markdown(f"### Profile Match: **{b_record['Borrower_Name']}** (`{b_record['District']} District`)")
        
        col_calc1, col_calc2 = st.columns(2)

        with col_calc1:
            fetched_income = int(b_record['Monthly_Income_UGX'])
            fetched_existing_debt = int(b_record['Total_Debt_UGX'])
            
            borrower_income = st.number_input("Verified Monthly Income (UGX)", min_value=50000, value=fetched_income, step=50000)
            existing_debt = st.number_input("Current Existing Digital Debt across Networks (UGX)", min_value=0, value=fetched_existing_debt, step=25000)
            proposed_loan = st.number_input("New Proposed Loan Amount (UGX)", min_value=10000, value=100000, step=10000)

        with col_calc2:
            new_total_debt = existing_debt + proposed_loan
            projected_dti = (new_total_debt / borrower_income) * 100 if borrower_income > 0 else 0
            safe_debt_limit = borrower_income * 0.35

            st.markdown("### **Financial Assessment Summary**")
            st.write(f"• **Projected DTI Ratio:** `{projected_dti:.1f}%`")
            st.write(f"• **Max Safe Debt Ceiling:** `UGX {safe_debt_limit:,.0f}`")
            st.write(f"• **Active Cross-Network Loans:** `{b_record['Active_Digital_Loans']}`")
            
            if new_total_debt > safe_debt_limit or projected_dti > 40:
                st.error("⚠️ **CRITICAL RISK:** Proposed debt burden exceeds safe liquidity limits. **REJECT OR RESTRUCTURE**.")
            elif projected_dti > 25:
                st.warning("⚠️ **MODERATE RISK:** Borrower is approaching maximum safe debt limits across networks.")
            else:
                st.success("✅ **LOW RISK:** Borrower maintains sufficient buffer. **APPROVE**.")

# --- TAB 3: INDIVIDUAL BORROWER LOOKUP ---
with tab3:
    st.subheader("👤 Dual-SIM KYC & Multi-Network Risk Audit")
    st.markdown("Search registry by Name, MTN number, Airtel number, or NIN to uncover cross-network loan stacking.")
    
    search_options = sorted(filtered_df['Search_Key'].unique()) if len(filtered_df) > 0 else []
    
    search_selection = st.selectbox(
        "Search Cross-Network Registry", 
        options=search_options,
        index=None,
        placeholder="Type a name or phone number (+256)..."
    )
    
    if search_selection:
        user_data = filtered_df[filtered_df['Search_Key'] == search_selection].iloc[0]
        
        st.markdown(f"## {user_data['Borrower_Name']}")
        
        mtn_display = '<span style="color:#f1c40f; font-weight:bold;">MTN</span>'
        airtel_display = '<span style="color:#e74c3c; font-weight:bold;">Airtel</span>'
        
        st.markdown(
            f"**{mtn_display}:** `{user_data['MTN_Phone']}` | "
            f"**{airtel_display}:** `{user_data['Airtel_Phone']}` | "
            f"**NIN:** `{user_data['National_ID_Number']}`", 
            unsafe_allow_html=True
        )
        
        col_prof1, col_prof2, col_prof3 = st.columns(3)
        col_prof1.metric("Demographics", f"{user_data['Gender']}, {user_data['Age']} yrs")
        col_prof2.metric("District of Residence (Loan Disbursal)", user_data['District'])
        col_prof3.metric("Current Loan Status", user_data['Status_Label'])
        
        st.divider()
        
        col_det1, col_det2 = st.columns(2)
        with col_det1:
            st.markdown("### Financial & Cross-Network Metrics")
            st.write(f"**Region:** `{user_data['Region']}`")
            st.write(f"**Primary Income Source:** `{user_data['Income_Source']}`")
            st.write(f"**Monthly Income:** `UGX {user_data['Monthly_Income_UGX']:,.0f}`")
            st.write(f"**Total Existing Debt (Across Networks):** `UGX {user_data['Total_Debt_UGX']:,.0f}`")
            st.write(f"**Active Digital Loans:** `{user_data['Active_Digital_Loans']}`")
            st.write(f"**Monthly Transactions:** `{user_data['MoMo_Monthly_Tx_Count']}`")
            
            dti_percentage = user_data['Debt_to_Income_Ratio'] * 100
            st.write(f"**Debt-to-Income (DTI) Ratio:** `{dti_percentage:.1f}%`")
            
        with col_det2:
            st.markdown("### Multi-Network Risk Assessment")
            if user_data['Default_Status'] == 1:
                st.error("⚠️ **STATUS: DEFAULTED (CROSS-NETWORK STACKING)** \n\nBorrower has accumulated concurrent credit obligations across multiple mobile money accounts. Recommend freezing further multi-SIM loan approvals.")
            elif dti_percentage > 40 and user_data['Active_Digital_Loans'] > 1:
                st.warning("⚠️ **STATUS: HIGH RISK** \n\nBorrower is utilizing multiple telecom lines to stack short-term digital loans beyond safe liquidity thresholds.")
            else:
                st.success("✅ **STATUS: PERFORMING** \n\nBorrower maintains a healthy cash flow across their primary mobile accounts.")

        st.divider()
        st.subheader("Itemized Active Loan Audit Trail & Risk-Tiered Repayment Timers")
        
        loans_json_str = user_data.get('Loans_JSON', '[]')
        loans_list = json.loads(loans_json_str) if pd.notna(loans_json_str) else []
        
        if len(loans_list) > 0:
            current_time = pd.Timestamp("2026-10-16 18:44:00")
            
            for loan in loans_list:
                due_dt = pd.to_datetime(loan['Due_Date'])
                time_diff = due_dt - current_time
                days_left = time_diff.days
                hours_left = time_diff.seconds // 3600
                
                if user_data['Default_Status'] == 1 or days_left < 0:
                    overdue_days = abs(days_left)
                    badge_color = "#e74c3c"
                    timer_text = f"DEFAULTED / OVERDUE by {overdue_days} days — CRITICAL RISK"
                elif days_left <= 5:
                    badge_color = "#e74c3c"
                    timer_text = f"{days_left} days, {hours_left} hrs remaining — CRITICAL RISK"
                elif days_left <= 14:
                    badge_color = "#e67e22"
                    timer_text = f"{days_left} days, {hours_left} hrs remaining — MODERATE RISK"
                else:
                    badge_color = "#2ecc71"
                    timer_text = f"{days_left} days remaining — LOW RISK"
                
                st.markdown(
                    f"""
                    <div style="padding: 12px; border-radius: 6px; border: 1px solid #ddd; margin-bottom: 10px; background-color: #fafafa;">
                        <b>Platform:</b> {loan['Platform']} &nbsp;|&nbsp; <b>Network:</b> {loan['Network']} &nbsp;|&nbsp; <b>Amount:</b> UGX {loan['Amount_UGX']:,.0f}<br>
                        <b>Disbursed:</b> {loan['Disbursed']} &nbsp;|&nbsp; <b>Due Date:</b> {loan['Due_Date']}<br>
                        <b>Risk Tier & Timer:</b> <span style="background-color: {badge_color}; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold;">{timer_text}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No active digital loans currently recorded for this borrower.")
